Create a professional Azure Data Factory CI/CD architecture diagram based on Microsoft's latest ADF CI/CD approach using ADF Utilities and GitHub Actions.

Requirements:

Environment:

* Azure Data Factory Dev
* Azure Data Factory Prod
* GitHub Repository

Git Structure:

* Feature Branches
* Main Branch

Workflow:

1. Developers create or modify ADF pipelines, datasets, linked services, triggers, and dataflows in ADF Dev.
2. Changes are committed to Feature Branches.
3. Pull Request is raised and merged into Main Branch.
4. GitHub Actions pipeline is triggered automatically on merge to Main.
5. GitHub Actions uses ADF Utilities (npm package) to:

   * Validate ADF artifacts
   * Export ARM Templates
   * Generate deployment artifacts
6. ARM Templates are published as build artifacts.
7. GitHub Actions deploys the ARM Templates to ADF Prod.
8. Environment-specific parameters are applied during deployment.
9. Triggers in Prod are stopped before deployment and restarted after successful deployment.
10. Deployment approval gate is required before Prod deployment.

Diagram Layout:

Left Section:

* Developers
* Feature Branches
* Pull Request
* Main Branch

Center Section:

* GitHub Actions CI Pipeline
* ADF Utilities
* Validation Stage
* ARM Template Generation Stage
* Artifact Publishing Stage

Right Section:

* Azure Data Factory Dev
* Azure Data Factory Prod

Flow Arrows:
Developer → Feature Branch → Pull Request → Main Branch → GitHub Actions → ADF Utilities → ARM Template Artifact → Approval Gate → Deploy to ADF Prod

Include Azure icons and GitHub icons.

Use a modern enterprise architecture style similar to Microsoft Azure reference architecture diagrams.

Show CI and CD stages separately.

Add labels:

* Continuous Integration
* ARM Template Generation
* Continuous Deployment
* Environment Promotion (Dev → Prod)

Output as a clean architecture diagram suitable for technical design documentation and management presentations.
