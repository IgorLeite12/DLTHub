import psycopg2.extensions
from typing import Optional, Iterable
from dlt.common.typing import TDataItem

# conn: a conexão com o banco de dados
# table: o nome da tabela
# last_state: a data de modificação do último registro
# replication_key: a coluna usada para identificar exclusivamente cada registro na tabela (por exemplo, um ID único)
# batch_size: o tamanho do lote de registros a serem buscados por vez, Não muda o total de linhas da consulta; só controla o “tamanho dos pacotes” trazidos da base para a aplicação.
# limit: o número máximo de registros a serem buscados, Limita o total de linhas retornadas pelo banco.

#Batch vs Limit
#O limit impõe um teto no total de linhas.
#O batch_size só controla o tamanho de cada “lote” lido por iteração.
#Exemplo: limit=2500 e batch_size=1000 → virão 3 lotes: 1000 + 1000 + 500, e depois o loop encerra.  

def get_records(
    conn: psycopg2.extensions.connection,
    table: str,
    last_state: Optional[str] = None,
    replication_key: Optional[str] = None,
    batch_size: int = 1000,
    limit: Optional[int] = None,
) -> Iterable[TDataItem]:
   
    # Monta a query SQL
    query = f"SELECT * FROM {table}"
    if limit is not None:
        query = f"{query} LIMIT {limit}"
    
    # Executa a query
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Obtém os nomes das colunas
    column_names = [desc[0] for desc in cursor.description]
    
    # Busca e retorna os dados como dicionários
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield dict(zip(column_names, row))
    
    cursor.close()
