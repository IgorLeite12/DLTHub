#!/usr/bin/env python3
"""Pipeline para carregar dados do PostgreSQL usando dlt."""
import dlt
from salesforce.sources import postgres_source


def load() -> None:
    """Executa o pipeline de extração do PostgreSQL."""

    pipeline = dlt.pipeline(
        pipeline_name="postgres_etl", 
        destination='filesystem', 
        dataset_name="postgres_data"
    )
    
    # Executa o pipeline
    load_info = pipeline.run(postgres_source())

    # Exibe informações sobre a carga
    print(load_info)


if __name__ == "__main__":
    load()
