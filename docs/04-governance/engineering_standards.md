# Aurora Lakehouse Engineering Standards

Establishes standardized naming conventions across the Aurora Healthcare Lakehouse Platform, metadata definitions, governance principles, and best engineering practices adopted.

The objective is to ensure consistency, governance, maintainability and scalability across all platform assets while following modern Lakehouse engineering practices.

**Principles:**

- **Optimise for clarity, not for brevity**: Explicit naming over short obscure codes.
- **Pragmatism over perfection**: Solve for production stability and business value first.
- **Build for the next engineer**: Self-documenting pipelines, standardized code, clear lineage.
- **Quality over elegance**: Robust data validation beats complex one-liners.

&nbsp;
## Table of Contents

1. [Naming Conventions](#1-naming-conventions)
2. [Table & Column Conventions](#2-table--column-conventions)
3. [Medallion Architecture](#3-medallion-architecture)
4. [Metadata Model](#4-metadata-model)
5. [Business Data Domains](#5-business-data-domains)
6. [Security, Governance & Compliance Framework](#6-security-governance--compliance-framework)
7. [Best Practices](#7-best-practices)
8. [References](#references)

&nbsp;
## 1. Naming Conventions
#### 1.1 Catalogs
Catalog represents isolated deployment environments. One catalog per environment.

| Environment | Catalog           |
| ----------- | ----------------- |
| Development | `healthcare_dev`  |
| Test / UAT  | `healthcare_uat`  |
| Production  | `healthcare_prod` |

#### 1.2 Schemas
Represents the logical layers following the Medallion Architecture.

| Layer   | Schema       |
| ------- | ------------ |
| Landing | `00_landing` |
| Bronze  | `01_bronze`  |
| Silver  | `02_silver`  |
| Gold    | `03_gold`    |


#### 1.3 Volumes & Storage Paths
Volumes and storage locations must reflect environment isolation and business responsibility.

Examples:
- `/Volumes/healthcare_<env>/00_landing/raw_landing_volume/`
- `gs://healthcare-landing-<env>/checkpoints_volume/`
- `s3://healthcare-reference-data-<env>/reference_data_volume/`

&nbsp;
## 2. Table & Column Conventions

#### 2.1 Basic Conventions:

- **Lowercase & `snake_case`**: Single underscores only.
- **Plural Entity Naming**: Tables must represent sets of entities (e.g., `dim_allergies` instead of `dim_allergy`).
- **Self-Descriptive**: Concise, clear, and unambiguous.

#### 2.2 Prefixes

| Prefix | Purpose                                 | Example                       |
|--------|-----------------------------------------|-------------------------------|
| raw_   | Unprocessed stream/file landing         | `raw_patient_events`          |
| stg_   | Ephemeral staging for transformations   | `stg_claims_cleansed`         |
| int_   | Intermediate business entity transforms | `int_encounter_billing`       |
| snap_  | Point-in-time snapshot tables           | `snap_monthly_patient_status` |
| dim_   | Conformed Dimensions                    | `dim_patients`                |
| fct_   | Fact Tables                             | `fct_claims`                  |
| mart_  | Aggregated Data Mart / Product Tables   | `mart_clinical_readmissions`  |


#### 2.3 Slowly Changing Dimensions (SCD)
For historical tracking changes in Silver and Gold dimensions:
- **SCD Type 1 (Overwrite)**: Default for correcting erroneous source records where history is irrelevant.
- **SCD Type 2 (Historical Tracking)**: Mandatory standard for critical master data (`dim_patients`, `dim_providers`). Must include technical columns:
     - **Physical Table (`*_history`):** Delta table managed via `create_auto_cdc_flow` (`stored_as_scd_type = "2"`).
     - `__START_AT` (Timestamp): Record version effective start time (mapped from `sequence_by`).
     - `__END_AT` (Timestamp): Record version end time (`NULL` for active records).
     - `is_current` (Boolean): Derived column (`__END_AT IS NULL`) indicating active state.

#### 2.4 Columns

Must be descriptive and follow consistent naming standards.

- Use `snake_case`.
- Consistent identifiers across layers (e.g., `patient_id` must keep the same name from Bronze to Gold).
- **Forbidden Reserved Words**: Never name a column date, time, user, group, or select. Use explicit terms like `calendar_date`, `service_timestamp`, `created_by_user`.

#### 2.5 Data Type Standards

| Business Attribute | Preferred Type |
|--------------------|----------------|
| Identifiers | STRING |
| Monetary values | DECIMAL(18,2) |
| Dates | DATE |
| Event timestamps | TIMESTAMP |
| Flags | BOOLEAN |
| Codes | STRING |

&nbsp;
## 3. Medallion Architecture

#### 3.1 Landing Layer
- Raw file landing zone (Cloud Storage / Storage Volumes).
- Immutable storage; original files are preserved.
- Multi-format support (JSON, CSV, Parquet, HL7/FHIR, XML).

#### 3.2 Bronze
Store source data with minimal transformation while preserving source fidelity for auditability.

**Naming convention:**
`bronze_<entity>` (e.g., `bronze_patients`)

**Allowed operations:**
- Metadata enrichment (`_ingestion_timestamp`, `_source_file_name`, `_rescued_data`).
- Schema evolution and parsing via Auto Loader.
- Data type alignment for technical compatibility.

**Forbidden:**
- Business filtering or rules.
- Joins and aggregations.
- Deduplication (duplicates must be preserved exactly as ingested).

#### 3.3 Silver
Provides cleansed, standardized, and conformed business entities across the enterprise.

**Naming convention:**
`silver_<domain>_<entity>` (e.g., `silver_clinical_patients`)

**Mandatory standards:**
- **Deduplication**: Window functions over primary key with business timestamp ordering.
- **Type Casting**: Strict contract enforcement (converting string dates to TIMESTAMP/DATE).
- **Null Handling**: Business defaults applied via standardized mapping dictionaries (fillna).
- **String Sanitization**: Lowercase/trim text fields and convert empty strings "" to NULL.

#### 3.4 Gold
Exposes business-ready, analytical data products built for BI tools, ML models, and executive reporting.

##### Dimensional Modelling (Kimball): 

- **Dimensions:** `dim_patients`
- **Facts:** `fct_encounters`


#### 3.5 Data Mart
Domain-specific, aggregate views or tables optimized for end-user reporting.

**Naming convetion:**
`mart_<business_domain>_<use_case>` (e.g., `mart_financial_monthly_revenue`, `mart_clinical_readmission_rates`)

&nbsp;
## 4. Metadata Model

| Attribute | Required | Type / Enum | Example | Description |
| :--- | :---: | :--- | :--- | :--- |
| **`entity_name`** | Yes | String | `patients` | Logical entity identifier in `snake_case`. |
| **`domain`** | Yes | String | `Clinical` | Top-level business data domain owning the asset. |
| **`business_unit`** | Yes | String | `Population Health` | Internal business organizational unit financing or consuming the asset. |
| **`source_system`** | Yes | String | `Synthea_EHR` | Upstream origin system feeding the pipeline. |
| **`source_path`** | Yes | String | `/Volumes/healthcare_dev/00_landing/raw_landing_volume/patients/` | Cloud storage location, volume path, or topic name. |
| **`target_layer`** | Yes | Enum | `Silver` | Medallion layer (`Landing`, `Bronze`, `Silver`, `Gold`). |
| **`target_table_name`** | Yes | String | `silver_clinical_patients` | Fully qualified production table name. |
| **`primary_key`** | Optional | String / List | `patient_id` | Business primary key identifier or composite key. |
| **`incremental_strategy`** | Yes | Enum | `Merge` | Execution pattern (`Append`, `Merge`, `SCD1`, `SCD2`, `Overwrite`). |
| **`scd_type`** | Optional | Enum | `SCD2` | Explicit historical tracking strategy (`None`, `SCD1`, `SCD2`). |
| **`materialization_type`** | Yes | Enum | `Table` | Physical object type (`Table`, `View`, `Materialized View`, `Streaming Table`). |
| **`cluster_by_keys`** | Optional | List | `["facility_id", "patient_id"]` | Columns used for Liquid Clustering or Partitioning/Clustering optimization. |
| **`lineage_upstream_tables`** | Optional | List | `["01_bronze.bronze_patients"]` | Parent tables used as inputs to track direct data lineage. |
| **`quality_rules_suite`** | Optional | String | `gx_clinical_patients_v1` | Data quality test suite identifier (Great Expectations, Soda, DLT). |
| **`data_owner`** | Yes | String | `Clinical Operations Domain Lead` | Business entity accountable for data authorization. |
| **`data_steward`** | Yes | String | `Aurora Data Team` | Technical group responsible for pipeline maintenance. |
| **`contains_pii`** | Yes | Boolean | `true` | Flag indicating presence of sensitive personal data. |
| **`sensitivity_level`** | Yes | Enum | `Confidential` | Classification tier (`Public`, `Internal`, `Confidential`, `Restricted`). |
| **`pii_type`** | Optional | Enum | `HIPAA_PHI` | Specific compliance category (`HIPAA_PHI`, `PCI_DSS`, `GDPR_PII`, `None`). |
| **`masking_policy`** | Optional | String | `mask_sha256_salted` | Dynamic data masking function or policy tag applied. |
| **`retention_days`** | Yes | Integer | `2555` | Data retention SLA in days (e.g., 2555 days / 7 years for HIPAA). |
| **`tags`** | Optional | Map / List | `{"environment": "prod", "compliance": "hipaa"}` | Key-value tags for Unity Catalog / Dataplex taxonomy. |

#### 4.1 Data Classification
| Classification | Purpose | Mental Rule | Typical Examples | Encryption Recommended |
|----------------|---------|-------------|------------------|------------------------|
| **Public** | Safe for public disclosure. | Anyone can know this information without causing harm. | Hospital name, department, procedure catalogue, country, ICD reference tables | No |
| **Internal** | Internal operational information. | Company information that does not identify a patient and causes little or no damage if disclosed. | City, State, County, Latitude, Longitude, System Name, Table Name | Optional |
| **Restricted** | Personally Identifiable Information (PII). | Identifies a patient but does not directly enable fraud. | Patient Name, Birth Date, Gender, Race, Ethnicity, Address, ZIP Code, Phone Number | Recommended |
| **Confidential** | Highly Sensitive Information. | Enables identity theft, financial fraud, or severe privacy violations if exposed. | SSN, Passport Number, Driver's License Number, Insurance Number, Financial Coverage, Credit Card Information | **Required** |


&nbsp;
## 5. Business Data Domains

| Domain | Description | Canonical Scope & Entities |
| :--- | :--- | :--- |
| **`Party & Directory`** | Master entities representing people, practitioner roles, and legal organizations. | Patients, Providers, Organizations, Practitioners, Locations, Devices |
| **`Clinical & Encounters`** | Diagnostic, observational, procedural, and therapeutic care events. | Encounters, Conditions, Procedures, Observations, Medications, Immunizations |
| **`Financial & Coverage`** | Administrative billing lifecycle, coverage details, and financial transactions. | Claims, Payers, Coverage, ClaimResponses, ExplanationOfBenefit |

&nbsp;
## 6. Security, Governance & Compliance Framework
#### 6.1 Cryptography 
- **Workspace Compliance**: Enable Compliance Security Profile (CSP), select the HIPAA standard, and enforce Enhanced Security Monitoring across production workspaces.
- **In-Transit**: TLS 1.2+ required across all network hops via native cloud private networking constructs (PrivateLink / VPC Peering / Private Service Connect). Public internet exposure of PHI endpoints is strictly forbidden. 
- **At-Rest**: AES-256 Customer-Managed Keys (CMEK) mandatory for all managed delta storage, control plane assets, Lakehouse roots and external cloud storage buckets.

#### 6.2 PII / PHI Governance & Anonymization
- **Catalog Tags:** All PHI datasets at the catalog layer must be tagged with `contains_pii = true` and `pii_type = HIPAA_PHI`.
- **Tokenization (Silver):** Direct identifiers (`patient_id`, `ssn`, `cpf`) at ingestion using SHA-256 with a salt managed in secure secret store.
- **Dynamic Access (Gold):** Redact PHI fields (`patient_name`) dynamically apply Column Masks and Row-Level Security (RLS) policies based on entitlement roles. 


&nbsp;
## 7. Best Practices
#### Ingestion & Orchestration 
- **Auto Loader / Cloud Storage Transfer:** Use native cloud ingestion tools (`cloudFiles` in Spark) for auto-detecting file arrival. 
- **Idempotency**: pipelines must be re-runnable for any historical date without creating duplicate data (`MERGE` statements or deterministic partition overwrites).
- **Checkpoints**: Maintain explicit checkpoint paths for streaming and incremental workloads.

#### Data Modeling & Storage Performance
- **One-to-One Traceability**: Maintain single-source lineage by mapping each raw landing file to exactly one Bronze table.
- **Liquid Clustering**: optimization technique (`CLUSTER BY (col1, col2)`) that replaces conventional table partitioning and `Z-ORDER` for datasets larger than 10GB.

#### Quality & Governance
- **Data Lineage**: End-to-end lineage capture from Landing to Gold.
- **Least Privilege**: Default access set to `NO ACCESS`. Permissions are managed via fine-grained access control.
- **CI/CD Deployment**: Deploy platform architecture and code via **IaC (Terraform)** and **Declarative Automation Bundles (DABs)**, manual executions via notebooks is strictly prohibited.

#### Observability
- **Job Monitoring & Pipeline SLAs**: Production workflows must enforce automated SLA failure alerts, track compute disk spill, and emit execution metrics to unified telemetry tables (e.g., `system.lakeflow.jobs`).

&nbsp;
## References
- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

- [Databricks well-architecture framework. Phase 2: Design workspace strategy](https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/workspace-strategy)

- [Databricks well-architecture framework. Phase 3: Unity Catalog](https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/unity-catalog#catalog-design-patterns)

- [Databricks - Data Guides: Tags](https://docs.databricks.com/aws/en/database-objects/tags)

- [Data Dictionary and Unity Catalog: Best Practices in a Medallion Architecture](https://community.databricks.com/t5/data-governance/data-dictionary-and-unity-catalog-best-practices-in-a-medallion/td-p/160616)

- [Databricks data governance - Best practices for ABAC policies](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/best-practices?utm_source=chatgpt.com)

- [Databricks Unity Catalog Tags: Governance Best Practices & Patterns](https://community.databricks.com/t5/technical-blog/databricks-unity-catalog-tags-governance-best-practices-amp/ba-p/146575?utm_source=chatgpt.com)

- [Databricks Best practices for performance efficiency](https://docs.databricks.com/aws/en/lakehouse-architecture/performance-efficiency/best-practices)

- [Databricks Security & Compliance](https://docs.databricks.com/aws/en/security/privacy/hipaa)

- [BigQuery Admin reference guide: Data governance](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-admin-reference-guide-data-governance)