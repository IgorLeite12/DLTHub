import dlt
from salesforce.sources import postgres_source

def load() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="postgres_etl", 
        destination='filesystem', 
        dataset_name="postgres_data"
    )

    source = postgres_source()
    
    print("Extraindo dados do PostgreSQL com psycopg2 e carregando para MinIO como CSV...")

    # Executa o pipeline
    load_info = pipeline.run(source, write_disposition="append", loader_file_format='csv')

    # Exibe informações sobre a carga
    print(load_info)
    print("--- Pipeline com psycopg2 concluído com sucesso! ---")


if __name__ == "__main__":
    load()
