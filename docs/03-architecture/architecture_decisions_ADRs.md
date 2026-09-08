# Architecture Decisions Records (ADRs)
These **Architecture Decision Records (ADRs)** capture the key architectural decisions adopted throughout the design and evolution of the Aurora Healthcare Data Platform. Each ADR documents the rationale behind major engineering choices to ensure consistency, traceability, maintainability, and future platform evolution.

- [ ] [ADR-001: Lakehouse Architecture](#adr-001-lakehouse-architecture)
- [ ] [ADR-002: Source-Oriented Landing Strategy](#adr-002-source-oriented-landing-strategy)
- [ ] [ADR-003: Engineering Standards & Naming Conventions](#adr-003-engineering-standards--naming-conventions)
- [ ] [ADR-004: Contract-as-Code](#adr-004-contract-as-code)
- [ ] [ADR-005: Infrastructure as Code](#adr-005-infrastructure-as-code)
- [ ] [ADR-006: Metadata-Driven Engineering](#adr-006-metadata-driven-engineering)
- [ ] [ADR-007: Reusable Framework Capabilities](#adr-007-reusable-framework-capabilities)
- [ ] [ADR-008: Canonical Data Modelling](#adr-008-canonical-data-modelling)
- [ ] [ADR-009: Data Quality by Design](#adr-009-data-quality-by-design)
- [ ] [ADR-010: Data Products](#adr-010-data-products)
- [ ] [ADR-011: Domain-Oriented Platform](#adr-011-domain-oriented-platform)
- [ ] [ADR-012: Observability by Default](#adr-012-observability-by-default)
- [ ] [ADR-013: Platform-as-a-Product](#adr-013-platform-as-a-product)

&nbsp;
### ADR-001: Lakehouse Architecture
- Adopt the Medallion Architecture to separate raw, standardized, and business-ready datasets into Bronze, Silver, and Gold layers.
- Organize enterprise assets through Unity Catalog to provide centralized governance, lineage, and discoverability.
- Preserve data progressively across layers, allowing quality and business rules to evolve incrementally.
- Promote scalable analytical workloads while reducing coupling between ingestion and consumption.

&nbsp;
### ADR-002: Source-Oriented Landing Strategy
- Organize landing data by source entity to preserve raw system fidelity.
- Store immutable source files before any transformation occurs.
- Maintain ingestion traceability through timestamped landing structures.
- Enable reproducible reprocessing and historical replay when required.

&nbsp;
### ADR-003: Engineering Standards & Naming Conventions
- Standardize naming conventions across datasets, notebooks, jobs, pipelines, repositories, and metadata assets.
- Establish common engineering patterns to improve maintainability and onboarding.
- Promote consistency across all business domains regardless of implementation team.
- Separate governance standards from implementation logic through dedicated documentation.

&nbsp;
### ADR-004: Contract-as-Code
- Adopt the Open Data Contract Standard (ODCS) as the canonical specification for dataset governance.
- Describe schema, ownership, metadata, quality expectations, and security policies as executable contracts.
- Validate datasets before promotion through automated contract verification.
- Extend ODCS through the Aurora Contract Engine to support healthcare-specific governance requirements.

&nbsp;
### ADR-005: Infrastructure as Code
- Manage platform resources declaratively through Infrastructure-as-Code principles using Terraform and Databricks Asset Bundles (DABs).
- Package engineering assets and pipeline workflows into version-controlled deployment bundles.
- Enable repeatable deployments across development, testing, and production environments.
- Support automated CI/CD and version-controlled platform evolution.

&nbsp;
### ADR-006: Metadata-Driven Engineering
- Drive platform behavior through metadata rather than hardcoded implementations.
- Configure ingestion, modelling, validation, and governance using declarative specifications.
- Reduce engineering duplication by promoting reusable metadata patterns.
- Enable platform extensibility without modifying framework code.

&nbsp;
### ADR-007: Reusable Core Engineering Frameworks 
- Build reusable engineering frameworks before implementing business pipelines.
- Treat ingestion, logging, validation, metadata, and quality as shared platform capabilities.
- Encourage standardization across every healthcare domain.
- Reduce development effort through reusable engineering services.

&nbsp;
### ADR-008: Canonical Data Modelling
- Transform heterogeneous healthcare datasets into enterprise canonical models.
- Decouple downstream consumers from source-specific schemas.
- Promote semantic consistency across all business domains.
- Simplify analytical and AI workloads through standardized representations.

&nbsp;
### ADR-009: Data Quality by Design
- Treat Data Quality as an integral component of every pipeline.
- Validate datasets before promotion across Medallion layers.
- Define quality expectations declaratively through Data Contracts.
- Prevent unreliable data from propagating downstream.

&nbsp;
### ADR-010: Data Products
- Expose curated datasets as governed Data Products instead of isolated analytical tables.
- Assign clear ownership and lifecycle management to every published dataset.
- Promote self-service consumption across analytical workloads.
- Increase business trust through certified and documented data assets.

&nbsp;
### ADR-011: Domain-Oriented Platform
- Organize datasets according to business capabilities rather than operational systems.
- Encourage ownership at the business-domain level.
- Support independent evolution of healthcare domains.
- Align platform organization with Domain-Driven Design principles.

&nbsp;
### ADR-012: Observability by Default
- Embed monitoring, logging, auditing, and operational metrics into every engineering component.
- Monitor platform health independently from business pipelines.
- Detect failures proactively through centralized observability.
- Improve platform reliability and operational transparency.

&nbsp;
### ADR-013: Platform-as-a-Product
- Design Aurora as a reusable enterprise platform instead of a collection of ETL pipelines.
- Prioritize reusable capabilities before business implementations.
- Separate platform engineering from domain engineering.
- Continuously evolve the platform through automation, governance, and engineering standards.