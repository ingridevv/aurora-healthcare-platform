## Project Concept: Healthcare Claims CDC Pipeline

**Core Components:**
* **Dataset**: synthetic healthcare data (Medicare claims, patient records, or hospital readmissions)
* **Ingestion Layer**: Auto Loader to continuously ingest new files.
* **CDC Processing**: Track claim status changes (submitted → approved → paid)
* **Medallion Architecture**: Bronze (raw) → Silver (cleaned) → Gold (analytics-ready)
* **DABs**: Package everything for deployment across environments

**Workflow:**
* Setting up DAB project structure with YAML configuration
* Implementing Auto Loader for incremental ingestion
* Using Delta's Change Data Feed for CDC tracking
* Building Lakeflow Spark Declarative Pipelines
* Managing resources, permissions, and deployments

**Project Flow:**
1. Generate/download sample health claims data
2. Create DAB structure (bundle configuration, notebooks, pipelines)
3. Build bronze layer with Auto Loader
4. Implement CDC tracking on claim status changes
5. Create silver/gold layers for analytics
6. Deploy with `databricks bundle deploy`