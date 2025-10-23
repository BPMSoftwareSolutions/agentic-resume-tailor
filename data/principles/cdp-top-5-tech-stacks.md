# Include Top 5 tech stacks
Me: I want to add a node to a best practice: - top 5 tech stacks used Let's see what that would look like for the "Develop" activity

Excellent — that’s a smart next step 👏🏾

You’re essentially moving from a *knowledge representation* model (descriptive SAFe structure) toward a **practical engineering extension**, where each *Best Practice* can now include real-world **implementation context** — like “Top Tech Stacks Used”.

Here’s how that addition would look structurally under the `"Develop"` activity in your tree JSON:

---

### 🧱 Example: `Develop` activity with `"top_tech_stacks"` node

```json
{
  "name": "Develop",
  "index": 6,
  "best_practices": [
    {
      "name": "Continuous Integration",
      "label": "CDP-Continuous-Integration",
      "description": "The ability to integrate and build the solution automatically, including validating the changes in a shared environment.",
      "top_tech_stacks": [
        {
          "stack": "Python + FastAPI + GitHub Actions",
          "context": "Used for backend microservices and API pipelines with automated testing and deployment."
        },
        {
          "stack": "Java + Spring Boot + Jenkins",
          "context": "Common enterprise CI setup for monolithic and microservice Java systems."
        },
        {
          "stack": "Node.js + Docker + AWS CodePipeline",
          "context": "Used in full-stack JavaScript applications and cloud-native pipelines."
        },
        {
          "stack": ".NET Core + Azure DevOps + Terraform",
          "context": "Typical Microsoft ecosystem CI/CD workflow with Infrastructure-as-Code."
        },
        {
          "stack": "Go + Kubernetes + ArgoCD",
          "context": "Modern lightweight build/deploy pipeline for distributed services."
        }
      ]
    },
    {
      "name": "Test Automation",
      "label": "CDP-Test-Automation",
      "description": "Automated testing ensures rapid feedback and prevents regression.",
      "top_tech_stacks": [
        {
          "stack": "Python + PyTest + Selenium",
          "context": "Used for functional and browser automation tests."
        },
        {
          "stack": "JavaScript + Cypress + GitHub Actions",
          "context": "Modern UI testing framework for CI pipelines."
        },
        {
          "stack": "Java + JUnit + Jenkins",
          "context": "Classic test automation combination in enterprise Java systems."
        },
        {
          "stack": "C# + NUnit + Azure Pipelines",
          "context": "Used in Microsoft-based QA automation setups."
        },
        {
          "stack": "Playwright + Docker + GitLab CI",
          "context": "Cross-browser testing with containerized runners."
        }
      ]
    }
  ]
}
```

---

### 💡 Structural Notes

* The new field `"top_tech_stacks"` is a **list of objects** — so you can include both a human-friendly stack name *and* the context or example usage.
* This pattern generalizes beautifully: you could later add nodes like `"recommended_tools"`, `"observability_metrics"`, or `"security_controls"` for the same hierarchical level.



Here’s your **Stage** (key activity) node with a `top_tech_stacks` list added to **each best practice** (5 stacks apiece), keeping your original text intact:

```json
{
  "name": "Stage",
  "index": 8,
  "best_practices": [
    {
      "name": "Maintain a staging environment",
      "label": "CDP-Maintain-a-staging-environment",
      "description": "A staging environment, which matches production provides the place for such validation.\n\n© Scaled Agile, Inc.\nInclude this copyright notice with the copied content.\n\nRead the FAQs on how to use SAFe content and trademarks here:\nhttps://www.scaledagile.com/about/about-us/permissions-faq/\nExplore Training at:\nhttps://www.scaledagile.com/training/calendar/",
      "top_tech_stacks": [
        { "stack": "Kubernetes + Helm + Argo CD", "context": "Staging namespace with app-of-apps pattern and environment parity." },
        { "stack": "AWS ECS + CodePipeline + Parameter Store", "context": "Containerized staging services with config isolation per stage." },
        { "stack": "Azure App Service Slots + Azure Pipelines", "context": "Staging slots for web/API with slot swap validation." },
        { "stack": "Docker Compose + GitHub Actions", "context": "Lightweight staging for smaller teams with PR-triggered builds." },
        { "stack": "Terraform + Terragrunt + Atlantis", "context": "Infra parity for staging via GitOps-driven IaC workflows." }
      ]
    },
    {
      "name": "Blue/Green deployment",
      "label": "CDP-Blue/Green-deployment",
      "description": "The blue/green pattern involves two environments–live (production) and idle (staging). Changes flow continuously to the idle environment where they are staged until ready to deploy to production. At that point, a switch is flipped (a load balancer is updated for example), and the idle environment becomes the live environment, while the previous live environment becomes the new idle environment. This enables continuous delivery, zero-downtime deployment, and fast recovery from failures.\n\n© Scaled Agile, Inc.\nInclude this copyright notice with the copied content.\n\nRead the FAQs on how to use SAFe content and trademarks here:\nhttps://www.scaledagile.com/about/about-us/permissions-faq/\nExplore Training at:\nhttps://www.scaledagile.com/training/calendar/",
      "top_tech_stacks": [
        { "stack": "Kubernetes + Argo Rollouts + NGINX/ALB", "context": "Blue/green via Service/Ingress switch or target group shift." },
        { "stack": "AWS ALB Target Groups + Auto Scaling", "context": "Route cutover between blue/green ASGs with health checks." },
        { "stack": "Spinnaker + GCP/GKE", "context": "Managed blue/green strategies with automated rollbacks." },
        { "stack": "Azure App Service Slots + Traffic %", "context": "Stage swaps with pre-swap validation and traffic redirection." },
        { "stack": "Nomad + Fabio/LB + Consul", "context": "HashiCorp stack for service discovery and LB-based switch." }
      ]
    },
    {
      "name": "System demo",
      "label": "CDP-System-demo",
      "description": "This is the event where stakeholders evaluate a solution’s readiness to be deployed to production.\n\n© Scaled Agile, Inc.\nInclude this copyright notice with the copied content.\n\nRead the FAQs on how to use SAFe content and trademarks here:\nhttps://www.scaledagile.com/about/about-us/permissions-faq/\nExplore Training at:\nhttps://www.scaledagile.com/training/calendar/",
      "top_tech_stacks": [
        { "stack": "Kubernetes + Ephemeral Namespaces + Helmfile", "context": "On-demand demo envs spun up per PI/feature branch." },
        { "stack": "GitHub Actions + Vercel/Netlify", "context": "Auto preview deployments for web frontends reviewed in demos." },
        { "stack": "Heroku Review Apps + Postgres", "context": "One-click demo apps per PR with seeded data." },
        { "stack": "Azure Static Web Apps + Functions", "context": "Frontend+API demo slots with auth and staging domains." },
        { "stack": "Render/Cloud Run + PR Deploys", "context": "Ephemeral demo services with automatic teardown." }
      ]
    }
  ]
}
```
