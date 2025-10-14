"""PostgreSQL source helpers"""

import psycopg2.extensions
from typing import Optional, Iterable
from dlt.common.typing import TDataItem

from .settings import IS_PRODUCTION


def get_records(
    conn: psycopg2.extensions.connection,
    table: str,
    last_state: Optional[str] = None,
    replication_key: Optional[str] = None,
) -> Iterable[TDataItem]:
    """
    Extrai registros de uma tabela PostgreSQL.

    Args:
        conn: Conexão psycopg2 com o banco PostgreSQL
        table: Nome da tabela para extrair dados
        last_state: Estado anterior para carga incremental (não implementado ainda)
        replication_key: Chave de replicação para carga incremental (não implementado ainda)

    Yields:
        Dict: Dicionário representando um registro da tabela
    """
    # Monta a query SQL
    if IS_PRODUCTION:
        query = f"SELECT * FROM {table}"
    else:
        # Em modo de teste, limita a 100 registros
        query = f"SELECT * FROM {table} LIMIT 100"
    
    # Executa a query
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Obtém os nomes das colunas
    column_names = [desc[0] for desc in cursor.description]
    
    # Busca e retorna os dados como dicionários
    rows = cursor.fetchall()
    for row in rows:
        yield dict(zip(column_names, row))
    
    cursor.close()
