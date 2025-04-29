Challenge with Matrix-Based CI/CD:
The matrix-based setup automatically deploys to all environments (development, staging, production) in parallel as part of a single pipeline. This approach is efficient but may not fully align with the way we currently manage our deployments.


Our Current Process/deployment:

- Development**: Frequent deployments with regular testing and fixes. It's an ongoing cycle, not a one-time pipeline.
- Staging:
  - Monday: First drop for initial testing.
  - wedsday: Second drop with regression testing.
  - Fridy: Final drop for confirmation before production.
  - All three drops happen as part of a fixed process, even if earlier ones are successful.
- Production: Deployed only after the full staging cycle is completed.

---

Given this structure, implementing a matrix-based CI/CD flow might not be feasible without changing how our current release process works. Our existing manual setup gives us the flexibility we need for scheduled drops, validations, and issue handling between each phase.
