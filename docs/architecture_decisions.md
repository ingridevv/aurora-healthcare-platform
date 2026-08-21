# Architecture Decisions

The Healthcare Data Platform follows the modern data platform framework best practices across its multiple domains:

### ADR-001: Medallion Architecture with Unity Catalog
- Use the medallion architecture to structure the data lake (bronze, silver, gold).
- Use Unity Catalog managed tables for all lakehouse data (bronze through gold).
- Use Unity Catalog volumes for landing zones and raw unstructured data.
- Implement data quality checks at each layer (bronze, silver, gold).
- Use Unity Catalog to enable data discovery and lineage tracking.

### ADR-002: Dynamic Single-Entity Landing Strategy
- Data is organized by entity and timestamp to simulate incremental ingestion.
- Organize landing volume storage with subfolder per entity.

### ADR-007: IaC via DABs
- Reproducible deployments for Databricks workflows and resources across environments.
- Use Declarative Automation Bundles (DABs) to manage pipeline jobs, target catalogs, and environment configurations.
- Enables version-controlled, automated CI/CD deployment.