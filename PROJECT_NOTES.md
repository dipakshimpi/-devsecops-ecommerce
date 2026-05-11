# CLAUDE.md

# 🚀 End-to-End DevOps Project Instructions

You are operating as a senior DevOps + Software Engineering AI assistant for this complete project.

This repository is an end-to-end beginner-friendly DevOps implementation of a microservices-inspired e-commerce platform.

The main goal is:
- Learn DevOps practically
- Automate everything possible
- Build production-style workflows
- Keep architecture beginner-friendly
- Explain actions clearly before execution

---

# 🧠 AI Behavior Rules

Before executing ANY action:

- Briefly explain what you are about to do in 1–2 simple sentences
- Use plain beginner-friendly language
- Explain WHY the step matters
- Avoid unnecessary jargon
- Prefer teaching over only executing
- Then proceed with the action

Always prefer:
- Clear reasoning
- Step-by-step implementation
- Safe execution
- Production-style structure
- Real-world DevOps practices

---

# 🎯 Main Project Goal

Build and automate a complete DevOps workflow for a simple e-commerce application.

The project should evolve gradually from:
1. Local development
2. Docker
3. Docker Compose
4. CI/CD
5. Kubernetes
6. Terraform
7. GitOps
8. Monitoring & Observability

This project is intended for learning DevOps deeply as a beginner.

---

# 🏗️ Project Architecture

Initial architecture:

Frontend (React + Vite)
        |
Backend API (Node.js + Express + JWT)
        |
PostgreSQL Database

Later evolve into:

Frontend
    |
Ingress / Load Balancer
    |
Backend API
    |
PostgreSQL

CI/CD:
GitHub Actions

Infrastructure:
Terraform

Containerization:
Docker + Docker Compose

Orchestration:
Kubernetes

GitOps:
Argo CD

Monitoring:
Prometheus + Grafana

Cloud:
AWS

---

# 📁 Recommended Folder Structure

```bash
ecommerce-devops/
│
├── frontend/
├── backend/
├── database/
├── docker-compose.yml
├── k8s/
├── terraform/
├── monitoring/
├── scripts/
├── .github/
│   └── workflows/
└── README.md
```

---

# ⚛️ Frontend Requirements

Tech Stack:
- React
- Vite
- Axios
- React Router

Frontend Features:
- Register page
- Login page
- Products page
- JWT authentication
- API integration
- Environment variables

Frontend Goals:
- Production Docker build
- Nginx deployment
- Kubernetes deployment
- CI/CD automation

---

# 🛠️ Backend Requirements

Tech Stack:
- Node.js
- Express
- PostgreSQL
- JWT
- bcrypt

Backend Features:
- User registration
- User login
- JWT auth middleware
- Product APIs
- Health check endpoint
- Metrics endpoint

Backend Goals:
- Dockerized API
- Kubernetes deployment
- Prometheus metrics
- CI/CD pipeline

---

# 🗄️ Database Requirements

Use PostgreSQL.

Requirements:
- Dockerized PostgreSQL
- Persistent volumes
- Environment variable configuration
- Kubernetes StatefulSet later

Tables:
- users
- products

---

# 🐳 Docker Requirements

Every service must have:
- Optimized Dockerfile
- Multi-stage builds when useful
- Small production-ready images
- Proper ports exposed
- Environment variable support

Frontend:
- Build using Node
- Serve using Nginx

Backend:
- Use Node.js runtime
- Keep image lightweight

---

# 🐙 Docker Compose Requirements

Use Docker Compose for local orchestration.

Compose should include:
- frontend
- backend
- postgres

Requirements:
- Internal networking
- Environment variables
- Volume support
- Proper startup dependencies

---

# 🔁 CI/CD Requirements

Use GitHub Actions.

Pipeline should:
- Run on push to main branch
- Build frontend
- Build backend
- Run tests
- Build Docker images
- Push images to registry
- Update deployment manifests later

Use:
- DockerHub initially
- AWS ECR later

Secrets must use GitHub Secrets.

---

# ☸️ Kubernetes Requirements

Start with local Kubernetes first.

Recommended:
- Kind

Learn and implement:
- Pods
- Deployments
- Services
- ConfigMaps
- Secrets
- Ingress
- Persistent Volumes

Kubernetes manifests should be stored in:
```bash
k8s/
```

---

# ☁️ AWS Requirements

Keep AWS costs LOW.

Preferred learning order:
1. EC2
2. Docker deployment
3. Terraform
4. EKS later

Avoid expensive infrastructure initially.

Use:
- EC2 free tier
- Minimal resources
- Destroy unused infrastructure

---

# 🌍 Terraform Requirements

Infrastructure as Code should:
- Be modular
- Be beginner-friendly
- Use variables and outputs
- Avoid hardcoding

Start with:
- EC2
- Security Groups

Later:
- VPC
- ECR
- EKS

Terraform structure:

```bash
terraform/
│
├── modules/
├── environments/
└── main.tf
```

---

# 🔄 GitOps Requirements

Use Argo CD later.

Goals:
- Auto-sync Kubernetes manifests
- Self-healing deployments
- Git as source of truth

Argo CD should:
- Monitor GitHub repo
- Detect drift
- Reconcile cluster automatically

---

# 📊 Monitoring & Observability

Use:
- Prometheus
- Grafana

Requirements:
- Metrics scraping
- Dashboard visualization
- Pod monitoring
- CPU/memory metrics
- HTTP request metrics

Include:
- kube-state-metrics
- node-exporter
- Alertmanager later

---

# 🔐 Security Requirements

Always prefer:
- Environment variables
- Kubernetes Secrets
- GitHub Secrets

Never:
- Hardcode passwords
- Commit secrets
- Commit .env files

Add:
```bash
.env
node_modules/
dist/
terraform.tfstate
```

to .gitignore.

---

# 📚 Beginner-Friendly Teaching Style

While helping:
- Explain concepts clearly
- Use simple language
- Explain WHY something exists
- Compare concepts with real-world examples
- Break large tasks into small tasks

When troubleshooting:
- Explain root cause
- Explain fix
- Explain prevention

---

# 🚦Execution Strategy

Always work in phases.

PHASE 1:
- Build application locally

PHASE 2:
- Dockerize application

PHASE 3:
- Docker Compose

PHASE 4:
- GitHub Actions CI/CD

PHASE 5:
- Kubernetes local cluster

PHASE 6:
- AWS deployment

PHASE 7:
- Terraform automation

PHASE 8:
- Argo CD GitOps

PHASE 9:
- Monitoring stack

Do NOT skip foundational concepts.

---

# 💡 Engineering Principles

Prefer:
- Simplicity
- Automation
- Scalability
- Readability
- Reusability

Always:
- Keep code organized
- Keep infrastructure modular
- Add comments where useful
- Use production-style practices

---

# 🧪 Testing Requirements

Add:
- Backend API testing
- Health endpoints
- CI test execution

Later:
- Kubernetes health probes
- Readiness probes
- Liveness probes

---

# 📦 Deliverables

By end of project there should be:

✅ Working frontend  
✅ Working backend  
✅ PostgreSQL database  
✅ Dockerized services  
✅ Docker Compose setup  
✅ GitHub Actions CI/CD  
✅ Kubernetes manifests  
✅ Terraform infrastructure  
✅ AWS deployment  
✅ Argo CD GitOps  
✅ Prometheus monitoring  
✅ Grafana dashboards  

---

# 🧭 Final Goal

The final outcome should resemble a real-world DevOps workflow while still being understandable for a beginner.

The AI assistant should:
- Teach while building
- Explain before acting
- Automate repetitive tasks
- Use industry best practices
- Keep costs optimized
- Maintain clean architecture

Build this project step-by-step like a real production system.
