# Architecture Decisions (WIP)

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

### ADR-003: Naming Conventions & Governance
- The platform requires standardized naming conventions to ensure
consistency, discoverability, governance, and maintainability across
all Lakehouse layers.
- Adopts standardized naming conventions for catalogs, schemas,
volumes and tables following Medallion Architecture principles.
- The detailed standards are maintained in dedicated governance
documentation.

### ADR-007: IaC via DABs
- Reproducible deployments for Databricks workflows and resources across environments.
- Use Declarative Automation Bundles (DABs) to manage pipeline jobs, target catalogs, and environment configurations.
- Enables version-controlled, automated CI/CD deployment.


Notes: 
- organize our workloads with one job per catalog, and then use one or more pipelines to load tables into the appropriate schemas.