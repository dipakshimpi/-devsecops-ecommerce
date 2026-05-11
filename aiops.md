# AIOps Integration Guide

## Overview
This document outlines a step‑by‑step plan to add an AI‑ops troubleshooting assistant on top of the existing DevSecOps project (Terraform, EKS, Helm, Argo CD). The approach stays within the AWS Free‑Tier (or uses a local LLM) and covers:

1. **Observability & Log Export** – Fluent Bit → CloudWatch, expose Prometheus.
2. **Lambda Action Groups** – tiny Lambdas for logs, metrics, health.
3. **AI Reasoning Layer** – local LLM (Docker) or optional Bedrock.
4. **Streamlit UI** – web interface that talks to the LLM and Lambda.
5. **GitOps Integration** – Argo CD deployment of the UI.

The guide is written for beginners; each step includes the exact commands to run on Windows PowerShell.

---
### Phase 1 – Observability & Log Export (Free‑Tier)

```powershell
# Attach CloudWatch policy to the EKS node role
aws iam attach-role-policy --role-name <EKS_NODE_ROLE> \
    --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

# Deploy Fluent Bit via Helm (collects container stdout/stderr)
helm repo add fluent https://fluent.github.io/helm-charts
helm repo update
helm install fluent-bit fluent/fluent-bit -n logging --create-namespace \
    --set backend.type=cloudwatch \
    --set backend.cloudwatch.log_group_name=/aws/eks/devsecops

# Expose Prometheus with a LoadBalancer so the AI can query it
kubectl -n monitoring patch svc prometheus-server -p '{"spec":{"type":"LoadBalancer"}}'

# Set CloudWatch log‑group retention to 1 day (keeps costs $0)
aws logs put-retention-policy --log-group-name /aws/eks/devsecops \
    --retention-in-days 1
```

---
### Phase 2 – Lambda Action Groups (Free‑Tier)

#### 2.1 Create IAM role for Lambdas
```json
# trust-policy.json (save locally)
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```
```powershell
aws iam create-role --role-name AIOpsLambdaRole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name AIOpsLambdaRole --policy-arn arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess
aws iam attach-role-policy --role-name AIOpsLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSReadOnlyAccess
```
#### 2.2 Lambda code (Python, <30 KB each)
**fetch_logs.py**
```python
import os, boto3

def handler(event, context):
    cw = boto3.client('logs')
    grp = os.getenv('LOG_GROUP')
    resp = cw.filter_log_events(logGroupName=grp, filterPattern='ERROR', limit=20)
    msgs = [e['message'] for e in resp.get('events', [])]
    return {'messages': msgs}
```
**fetch_metrics.py**
```python
import os, requests

def handler(event, context):
    query = event.get('query', 'up')
    url = os.getenv('PROM_URL') + f"/api/v1/query?query={query}"
    resp = requests.get(url)
    return resp.json()
```
**fetch_health.py**
```python
import os, boto3

def handler(event, context):
    eks = boto3.client('eks')
    resp = eks.describe_nodegroup(
        clusterName=os.getenv('CLUSTER'),
        nodegroupName=os.getenv('NODEGROUP'))
    return resp['nodegroup']
```
#### 2.3 Deploy Lambdas (example for fetch_logs)
```powershell
zip fetch_logs.zip fetch_logs.py
aws lambda create-function --function-name fetch_logs \
    --runtime python3.9 \
    --role arn:aws:iam::<ACCOUNT_ID>:role/AIOpsLambdaRole \
    --handler fetch_logs.handler \
    --zip-file fileb://fetch_logs.zip \
    --environment Variables={LOG_GROUP=/aws/eks/devsecops}
```
Repeat for the other two functions (add `PROM_URL`, `CLUSTER`, `NODEGROUP` env vars).

---
### Phase 3 – AI Reasoning Layer

**Option A – Local LLM (zero cost)**
```powershell
docker run -d --name local-llm -p 8000:80 ghcr.io/huggingface/text-generation-inference:latest \
    --model-id gpt2
```
The LLM will be reachable at `http://localhost:8000/generate`.

**Option B – Amazon Bedrock (paid, pay‑per‑token)**
```powershell
aws bedrock create-agent --agent-name devsecops-assistant \
    --foundation-model-name anthropic.claude-v2
```
Switch to this option only when you have spare credits.

---
### Phase 4 – Streamlit Front‑End
Create a folder `aiops-ui/` with these files:

**requirements.txt**
```
streamlit
boto3
requests
```
**app.py** (simplified version)
```python
import streamlit as st, boto3, requests, os, json

LLM_URL = os.getenv('LLM_URL', 'http://localhost:8000/generate')
lambda_client = boto3.client('lambda')

def ask_llm(prompt):
    r = requests.post(LLM_URL, json={'inputs': prompt})
    r.raise_for_status()
    data = r.json()
    return data.get('generated_text') or data.get('completion')

def call_lambda(name, payload):
    r = lambda_client.invoke(FunctionName=name, Payload=json.dumps(payload).encode())
    return json.loads(r['Payload'].read())

st.title('🧠 AIOps Troubleshooting Assistant')
question = st.text_input('Ask a question about the cluster')
if st.button('Run'):
    with st.spinner('Thinking...'):
        plan = ask_llm(question)
        st.subheader('AI‑Generated Plan')
        st.code(plan)
        if 'log' in plan.lower():
            out = call_lambda('fetch_logs', {})
            st.subheader('Recent error logs')
            for m in out.get('messages', []):
                st.code(m)
        elif 'metric' in plan.lower() or 'cpu' in plan.lower():
            q = 'sum(rate(container_cpu_usage_seconds_total[5m]))'
            out = call_lambda('fetch_metrics', {'query': q})
            st.subheader('Metrics')
            st.json(out)
        elif 'health' in plan.lower():
            out = call_lambda('fetch_health', {})
            st.subheader('Cluster health')
            st.json(out)
```
Run locally:
```powershell
cd aiops-ui
python -m pip install -r requirements.txt
streamlit run app.py
```
Visit `http://localhost:8501`.

---
### Phase 5 – GitOps Deployment with Argo CD
Add an Argo CD `Application` manifest (e.g., `argo-apps/aiops-ui.yaml`) that points to the `aiops-ui/` folder. After committing, Argo CD will automatically sync the UI into the cluster.

---
### Phase 6 – End‑to‑End Test (Free‑Tier)
1. Scale a workload down to provoke a failure: `kubectl -n ecommerce-app scale deployment frontend --replicas=0`.
2. In the Streamlit UI ask: *“Why is the frontend down?”*.
3. The LLM should suggest calling the health or log Lambda; the UI will display the Lambda output showing zero pods or recent errors.
4. Fix the issue (`kubectl scale ... --replicas=1`) and verify the UI now reports healthy.

---
## Summary
- No rename of `CLAUDE.md` – we keep it untouched.
- A new **`aiops.md`** file contains the full, beginner‑friendly roadmap.
- All commands are PowerShell‑compatible and designed to stay within the AWS Free Tier (or use a local LLM for zero cost).
- Once the steps are followed, you will have a production‑style AIOps assistant that can be showcased on GitHub, LinkedIn, or during interviews.

---
*Feel free to copy this markdown into a new file named `aiops.md` in the repository root.*
