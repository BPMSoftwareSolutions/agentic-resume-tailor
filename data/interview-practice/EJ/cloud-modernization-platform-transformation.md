
### 🧱 1. “What were the biggest challenges in decomposing the monolith into microservices?”

**Situation:**
Edward Jones’ *Online Access* platform was a decade-old monolith tightly coupled across UI, API, and database layers. Any small change triggered full-stack regression testing and multi-team coordination.

**Task:**
We needed to break the system into deployable, independently scalable services without disrupting daily operations or investor-facing uptime.

**Action:**

* Started with **domain discovery workshops**—mapped business capabilities (accounts, authentication, portfolio, notifications) into bounded contexts.
* Used **Strangler Fig pattern** to carve out APIs incrementally—new services handled new endpoints while the monolith continued to serve existing traffic.
* Introduced a **shared API Gateway** and centralized auth layer to decouple identity and routing early.
* Piloted the first microservice (“Account Summary”) to prove the deployment pipeline, monitoring, and rollback process.

**Result:**
Gradually decomposed 7 major modules into 20+ services with zero downtime; reduced average release cycle from **2 weeks → 2 days**.
**Reflection:**
“I learned that the hardest part wasn’t the code—it was orchestrating people and interfaces.”

---

### 🧩 2. “How did you decide on service boundaries and communication patterns?”

**Situation:**
The existing code base had shared data models and mixed business logic, so arbitrary slicing would only create distributed confusion.

**Task:**
Define service boundaries that aligned with business domains and avoided chatty inter-service calls.

**Action:**

* Applied **Domain-Driven Design** techniques—identified aggregate roots and domain events.
* Grouped services around **business capabilities** (e.g., Portfolio Analytics, Trade Execution, Client Profile).
* Used **RESTful APIs** for synchronous interactions; introduced **SNS/SQS event topics** for async notifications (e.g., trade completed, account updated).
* Enforced contract testing and versioned OpenAPI specs for all interfaces.

**Result:**
Services became loosely coupled yet cohesive; cross-service latency dropped 30 %; changes could be deployed independently.
**Reflection:**
“Boundary decisions drove the org structure—each team owned one domain, one pipeline, one backlog.”

---

### ☁️ 3. “What did your deployment topology look like — did you use ECS, EKS, or Lambda?”

**Situation:**
We needed a deployment model that supported mixed workloads—long-running services, event triggers, and batch jobs—while keeping ops overhead low.

**Task:**
Select compute runtimes optimized for cost, scalability, and DevOps maturity.

**Action:**

* Adopted **AWS ECS Fargate** for containerized microservices (no server maintenance).
* Used **AWS Lambda** for event-driven components (notifications, scheduled reconciliations).
* Deployed **API Gateway** in front for routing and throttling.
* Managed IaC with **Terraform**, parameterizing VPCs, IAM, and autoscaling rules.
* Configured blue/green deployments via GitHub Actions + CodeDeploy for safe rollouts.

**Result:**
Achieved **100 % environment parity** between staging and production; mean deploy time under **5 minutes**; zero downtime across all releases for 12 months.
**Reflection:**
“Fargate gave us container consistency; Lambda gave us agility—each fit its rhythm.”

---

### 🧮 4. “How did you manage shared data models or cross-service dependencies?”

**Situation:**
The monolith used a single relational schema shared across modules; splitting it risked data inconsistency and tight coupling through the back door.

**Task:**
Ensure each service owned its data while still supporting cross-domain queries and reports.

**Action:**

* Adopted the **Database-per-Service** pattern—each microservice had its own schema and API gateway contract.
* Created **data-replication pipelines** using SNS + SQS to broadcast domain events (e.g., Client Updated) to interested services.
* Introduced a **read-only Data Warehouse** for cross-service analytics, fed via event streams.
* Enforced schema versioning and migration scripts in CI/CD to keep DB drift visible.

**Result:**
Removed direct DB coupling; enabled independent schema evolution; improved data integrity and auditability.
**Reflection:**
“Once we treated data as an API, everything else fell into place.”

---

### ⚖️ 5. “What trade-offs did you make between speed of delivery and architectural purity?”

**Situation:**
Business wanted faster client-facing releases, while architects pushed for ideal DDD isolation.

**Task:**
Balance iterative delivery with long-term maintainability.

**Action:**

* Delivered **vertical slices** first—end-to-end features built through one microservice stack, even if some dependencies stayed in the monolith.
* Deferred full event-driven refactors until KPIs justified them.
* Instituted an **architecture runway** process—approved “good-enough” solutions now, scheduled refactoring epics for later sprints.

**Result:**
Met delivery deadlines without accruing runaway tech debt; by quarter 4, refactors caught up and aligned to enterprise standards.
**Reflection:**
“Purity never shipped a feature—but a planned imperfection always can.”

---

### 📈 6. “How did you measure success — performance, scalability, or team velocity?”

**Situation:**
Stakeholders needed proof the modernization was paying off beyond architecture diagrams.

**Task:**
Define measurable outcomes that balanced business, technical, and team metrics.

**Action:**

* Established KPIs for **deployment frequency**, **change-failure rate**, and **MTTR** (from DORA metrics).
* Tracked **API latency**, **95th-percentile response time**, and **autoscaling events** in CloudWatch.
* Surveyed developer sentiment quarterly on deployment friction and local-dev speed.

**Result:**

* Release frequency ↑ 2×
* Incident rate ↓ 35 %
* Mean restore time ↓ 60 %
* Developer satisfaction +25 pts

**Reflection:**
“When we saw velocity and stability improve together, we knew the culture—not just the code—had changed.”

