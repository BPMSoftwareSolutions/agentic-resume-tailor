
---

## 🏢 **Edward Jones**

**Role:** Principal Consultant / Platform Team Delivery Lead
**Focus:** Modernizing the Digital Client Experience (DCX) platform to support microservices, real-time telemetry, and AI-powered features across 13 Agile teams

### 🔄 Continuous Exploration (CE)

* **Modernized the Online Access Platform:** Decomposed Edward Jones' legacy monolith into **domain-aligned microservices**, forming the technical foundation of a modern Online Access experience for 8M+ clients.
* **Enabled AI-Augmented Experiences:** Designed **RESTful APIs** and event-driven contracts to support emerging AI capabilities like **scenario planning, goal tracking, and recommendation engines**—all aligning with Edward Jones' vision of "advisor intelligence" and **next-best action prompts**.
* **Client-Advised Product Alignment:** Collaborated with product and advisor teams to evolve the platform in sync with client-facing tools like the **goal progress module**, **secure messaging**, and **outside account aggregation**, which were actively rolling out to web and mobile apps.

### 🧪 Continuous Integration (CI)

* **Built-in Quality at Scale:** Implemented **CI/CD pipelines using Azure DevOps, Jenkins, and Terraform**—enabling consistent integration across 13+ Agile delivery teams.
* **Enterprise DevSecOps:** Hardened platform pipelines with **IaC validation, secret rotation (via KeeperSecurity), static scans, and role-based access**, ensuring sensitive data compliance aligned with the firm’s $1.5B tech transformation.
* **AI & API Observability:** Embedded **Dynatrace and Splunk** to monitor latency, availability, and AI trigger points for features like **advisor prompts** and **automated portfolio suggestions**—vital for gauging trust in AI-assisted workflows.

### 🚀 Continuous Deployment (CD)

* **Multi-Team Delivery Enablement:** Built trunk-based release infrastructure supporting **parallel team delivery**, with integrated **feature flags and environment-specific gates** to control risk in production across legacy and cloud systems.
* **Cloud-Native Readiness:** Positioned services for containerization and hybrid deployment across **on-prem, AWS, and Oracle Cloud**, reflecting Edward Jones’ move away from legacy systems to scalable, service-oriented platforms like Salesforce and Oracle HCM.

### 📈 Release on Demand

* **Flexible & Incremental Rollouts:** Enabled **selective rollout of new AI-linked features** (e.g., scenario planning and goal visualization tools) without disrupting the advisor-client experience.
* **Full-Stack Observability & Governance:** Monitored **system-level and model-specific KPIs**, ensuring alignment with Edward Jones' compliance standards and delivering traceability across client interactions and AI logic.

---

---

## 🏢 **BPM Software Solutions**

**Role:** Senior Software Architect / Engineering Lead
**Focus:** Building AI orchestration platforms and deploying intelligent services in safety-critical and compliance-heavy industries like transportation, law enforcement, and public education

### 🔄 Continuous Exploration (CE)

* **AI for Smart Fleet Safety:** Led architecture and engineering for **Safe Fleet’s AI transformation**, delivering real-time analytics and computer vision pipelines across school buses, patrol vehicles, and transit systems.
* **Pluggable AI Orchestration with RenderX:** Designed and deployed **RenderX**, a flexible orchestration engine for LLM and vision workflows—supporting **license plate recognition (LPR)**, **driver behavior detection**, and **automated evidence packaging** from camera streams.
* **Customer Co-Design:** Partnered directly with fleet operations leaders, school district compliance teams, and public safety SMEs to align AI outputs with operational workflows and legal chain-of-custody requirements.
* **Feedback Loops & Governance:** Enabled **human-in-the-loop labeling**, automated **prompt audit logging**, and escalation workflows to refine LLM output—essential for building **court-admissible stop-arm violation packets** and **real-time officer alerts**.

### 🧪 Continuous Integration (CI)

* **Secure-by-Design Infrastructure:** Applied **AES-256 encryption**, **KeeperSecurity**, and **KMS** to protect sensitive data—including vehicle telemetry, school bus video feeds, and ALPR results—meeting **CJIS, SOC 2**, and **FERPA-aligned** standards.
* **AI Observability at Scale:** Instrumented RenderX pipelines to track **inference latency, model confidence, and drift**, enabling **risk flagging** for violations or false positives in AI vision models—especially relevant in **SAVES** and **FOCUS H2** platforms.

### 🚀 Continuous Deployment (CD)

* **Fleet-Wide Cloud Deployment:** Provisioned Safe Fleet’s cloud backend infrastructure using **Terraform** and **Kubernetes**, ensuring consistent orchestration across 10,000+ edge-connected vehicles (school buses, trucks, patrol cars).
* **Automated CI/CD Pipelines:** Delivered **GitHub Actions-based automation** to deploy full-stack AI services—including RAG-based LLM chains and video-processing models—across **GovCloud-compliant** environments.
* **Multi-Model Routing & AI Extension:** Enabled configurable switching between **OpenAI, Anthropic, Rekor**, and custom vision models—supporting both **on-vehicle GPU inference (e.g., NVIDIA Jetson)** and **cloud-based orchestration**, depending on fleet type and latency needs.

### 📈 Release on Demand

* **Contextual AI Workflows:** RenderX enabled **role-based orchestration**—e.g., school safety officers could launch review workflows from violation events; transit supervisors received auto-flagged bus lane violations; officers got real-time ALPR alerts from in-car cameras.
* **Safe, Auditable Rollouts:** All AI workflows supported **version-controlled prompt templates**, **automated rollback**, and **immutable audit trails**—crucial for public sector trust, evidence handling, and legal defensibility in violation enforcement.

---
