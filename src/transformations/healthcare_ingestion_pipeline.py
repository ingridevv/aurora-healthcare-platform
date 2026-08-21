from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Define paths
main_catalog = "healthcare_dev"
landing_schema = "00_landing"
bronze_schema = "01_bronze"
raw_volume = "raw_landing_volume"
checkpoint_volume = "checkpoints_volume"

base_path = f"/Volumes/{main_catalog}/{landing_schema}/{raw_volume}/synthea/"
checkpoint_path = f"/Volumes/{main_catalog}/{bronze_schema}/{checkpoint_volume}/"

# Discover entities
def discover_entities(base_path):
    """
    Scan landing zone and discover all entities.
    Args:
        base_path: Path to synthea directory
    Returns:
        List of entity names (e.g., ["allergies", "patients"])
    """
    # 1. List all items in base_path
    try:
        files = dbutils.fs.ls(base_path)
    except Exception as e: 
        raise ValueError(f"Cannot access landing zone: {e}")

    # 2. Filter to only directories and build list
    entity_names = []  # ← Create list to collect entities
    for file in files:
        # Loop through subdirectories only
        if not file.isDir():
            continue
        # Extract entity names
        entity_name = file.name.rstrip("/")
        entity_names.append(entity_name)  # ← Add to list

    # 3. Return the list
    return entity_names

# Store entities dynamically
entities = discover_entities(base_path)

for entity in entities:
    @dp.table(
        name=f"bronze_{entity}",
        comment=f"Bronze ingestion for {entity}",
        table_properties={"quality": "bronze"}
    )
    def ingest_to_bronze(e=entity):
        return (
            spark.readStream.format("cloudFiles") \
            .option("cloudFiles.format", "csv") \
            .option("header", "true") \
            .option("rescuedDataColumn", "_rescued_data") \
            .option("cloudFiles.schemaLocation", f"{checkpoint_path}{e}/_schema") \
            .load(f"{base_path}/{e}/{e}.csv") \
            .withColumn("_ingested_at", current_timestamp()) \
            .withColumn("_source_file", col("_metadata.file_path"))
            )












