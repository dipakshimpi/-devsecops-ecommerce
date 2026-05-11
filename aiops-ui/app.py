import streamlit as st
import boto3
import json
import pandas as pd
import time
import requests
import os

# --- Page Config ---
st.set_page_config(
    page_title="AIOps Troubleshooter | EKS Mumbai",
    page_icon="🧠",
    layout="wide"
)

# --- AWS Clients ---
lambda_client = boto3.client('lambda', region_name='ap-south-1')
bedrock_client = boto3.client('bedrock-runtime', region_name='ap-south-1')

# --- Smart Fallback Analysis ---
def rule_based_analysis(query, data):
    """Analyze real live data with rule-based logic when Bedrock quota is exhausted."""
    query_lower = query.lower()
    analysis = []
    analysis.append("> ⚠️ *Bedrock quota exceeded — using AIOps Rule Engine on **live** data*\n")

    # Safety: ensure data is a dict
    if not data or not isinstance(data, dict):
        analysis.append("⚠️ Lambda returned no usable data yet.")
        analysis.append("👉 Click **'Check Cluster Health'** or **'Fetch Recent Logs'** in the sidebar first, then ask your question.")
        return "\n".join(analysis)

    # --- Health Analysis (real data) ---
    if "health" in query_lower or "node" in query_lower or "cluster" in query_lower:
        analysis.append("## 🖥️ Live Cluster Health Analysis")
        nodes = data.get("nodes", [])
        if nodes:
            ready_nodes = [n for n in nodes if n.get("status") == "Ready"]
            not_ready = [n for n in nodes if n.get("status") != "Ready"]
            analysis.append(f"**Total Nodes:** {len(nodes)}")
            analysis.append(f"**Ready:** ✅ {len(ready_nodes)} | **Not Ready:** {'⚠️ ' + str(len(not_ready)) if not_ready else '✅ 0'}")
            if not_ready:
                analysis.append(f"\n**⚠️ Problem Nodes:** {[n.get('name') for n in not_ready]}")
                analysis.append("**Recommendation:** Run `kubectl describe node <name>` to check for resource pressure or taints.")
            else:
                analysis.append("\n**Recommendation:** All nodes healthy. Consider enabling Cluster Autoscaler for cost optimization.")
        else:
            analysis.append("⚠️ No node data returned. Lambda may lack `eks:ListNodegroups` permission.")

    # --- Log Analysis (real data) ---
    elif "log" in query_lower or "error" in query_lower:
        analysis.append("## 📋 Live CloudWatch Log Analysis")
        error_logs = data.get("error_logs", [])
        total = data.get("total_events", 0)
        analysis.append(f"**Total log events scanned:** {total}")
        if error_logs:
            analysis.append(f"**❌ Errors found:** {len(error_logs)}")
            for i, log in enumerate(error_logs[:3], 1):
                analysis.append(f"\n**Error {i}:** `{str(log)[:200]}`")
            analysis.append("\n**Recommendation:** Investigate the above errors — they are live from your CloudWatch log group.")
        else:
            analysis.append("**✅ No errors found** in recent logs — your cluster is clean!")
            analysis.append("**Recommendation:** Set up a CloudWatch Alarm to be alerted automatically when errors appear.")

    else:
        analysis.append("## 🤖 AIOps Rule Engine")
        analysis.append(f"**Live data received:** `{list(data.keys())}`")
        analysis.append("\nTry asking about **'health'**, **'nodes'**, **'errors'** or **'logs'** for detailed analysis.")

    return "\n".join(analysis)

def ask_llm(prompt, context_data="", raw_data=None):
    """Use Groq (free) to analyze real infrastructure data with Llama 3."""
    groq_api_key = st.session_state.get('groq_key', '')
    
    if not groq_api_key:
        # No key yet — fall back to rule engine
        return rule_based_analysis(prompt, raw_data), "🧠 AIOps Rule Engine (enter Groq key in sidebar)"

    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        system_msg = (
            "You are an expert DevSecOps and AIOps engineer. "
            "You are analyzing a live EKS cluster named 'ecommerce-cloud' in AWS Mumbai (ap-south-1). "
            "Be concise, specific, and actionable. Use bullet points."
        )
        user_msg = f"User asked: '{prompt}'.\n\nLive data from AWS:\n{context_data if context_data else 'No data fetched yet.'}"

        body = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 600,
            "temperature": 0.3
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'], "🦙 Llama 3.3 70B via Groq (Free)"

    except requests.exceptions.HTTPError as e:
        return rule_based_analysis(prompt, raw_data), f"🧠 Rule Engine (Groq error: {e.response.status_code})"
    except Exception as e:
        return rule_based_analysis(prompt, raw_data), f"🧠 Rule Engine (Error: {str(e)[:60]})"

def call_lambda(function_name, payload={}):
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return json.loads(response['Payload'].read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

# --- UI Header ---
st.title("🧠 AIOps Troubleshooting Assistant")
st.caption("EKS Cluster: `ecommerce-cloud` | Region: `ap-south-1` (Mumbai) | AI: Amazon Bedrock + Claude")
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg", width=80)
    st.header("🎛️ Controls")
    st.markdown("**Cluster:** `ecommerce-cloud`")
    st.markdown("**Region:** `ap-south-1`")
    st.divider()

    # Groq API Key input
    groq_key = st.text_input("🔑 Groq API Key (free)", type="password",
                              placeholder="gsk_...", help="Get free key at console.groq.com")
    if groq_key:
        st.session_state['groq_key'] = groq_key
        st.success("✅ Llama 3.3 70B ready!")
    else:
        st.warning("Enter Groq key to enable real AI")
    st.divider()

    if st.button("🔍 Check Cluster Health", use_container_width=True):
        with st.spinner("Fetching health data from Lambda..."):
            health = call_lambda('fetch_health')
            st.session_state['health'] = health
            st.success("Done!")

    if st.button("📋 Fetch Recent Logs", use_container_width=True):
        with st.spinner("Fetching CloudWatch logs..."):
            logs = call_lambda('fetch_logs')
            st.session_state['logs'] = logs
            st.success("Done!")

    st.divider()
    st.caption("Powered by: EKS + Fluent Bit + Lambda + Bedrock")

# --- Main Query Area ---
query = st.text_input(
    "💬 Ask the AI about your infrastructure",
    placeholder="e.g., 'Are there any errors?', 'Check cluster health', 'Security scan'"
)

if query:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.info(f"**Analyzing:** {query}")

    context_data = ""
    fetched_data = None

    with st.spinner("🔄 Collecting live data from AWS..."):
        if any(word in query.lower() for word in ["log", "error", "fatal"]):
            result = call_lambda('fetch_logs')
            if 'body' in result:
                fetched_data = json.loads(result['body'])
                context_data = f"Log data: {fetched_data}"
        elif any(word in query.lower() for word in ["health", "node", "pod", "cluster"]):
            result = call_lambda('fetch_health')
            if 'body' in result:
                fetched_data = json.loads(result['body'])
                context_data = f"Health data: {fetched_data}"

    with st.spinner("🤖 AI is analyzing..."):
        ai_response, source = ask_llm(query, context_data, raw_data=fetched_data)

    st.subheader("🤖 AI Analysis & Recommendation")
    st.caption(f"Source: {source}")
    st.markdown(ai_response)

    if fetched_data:
        with st.expander("📄 Raw Data from Lambda"):
            st.json(fetched_data)

st.divider()

# --- Dashboard ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖥️ Nodes Status")
    if 'health' in st.session_state:
        health_data = st.session_state['health']
        if 'body' in health_data:
            parsed = json.loads(health_data['body'])
            st.json(parsed)
        else:
            st.json(health_data)
    else:
        st.info("Click **'Check Cluster Health'** in the sidebar to load live data.")

with col2:
    st.subheader("📋 Recent Logs")
    if 'logs' in st.session_state:
        log_data = st.session_state['logs']
        if 'body' in log_data:
            parsed = json.loads(log_data['body'])
            st.json(parsed)
        else:
            st.json(log_data)
    else:
        st.info("Click **'Fetch Recent Logs'** in the sidebar to load CloudWatch data.")
