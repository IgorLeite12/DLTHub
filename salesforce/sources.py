"""Source para PostgreSQL usando dlt.

Este source extrai dados de tabelas PostgreSQL e carrega no destino configurado.
"""

from dlt.sources import DltResource
from typing import Iterable, List

import dlt
from dlt.common.typing import TDataItem

from .records import get_records
from .client import PostgresCredentials, make_postgres_client


@dlt.source(name="postgres")
def postgres_source(
        credentials: PostgresCredentials = dlt.secrets.value,
        tables: List[str] = None,
) -> Iterable[DltResource]:
    """
    Source dlt para extrair dados do PostgreSQL.

    Args:
        credentials: Credenciais do PostgreSQL (obtidas automaticamente de .dlt/secrets.toml)

    Returns:
        Iterable de recursos dlt
    """
    client = make_postgres_client(credentials)

    # Define recursos (tabelas) para extrair
    @dlt.resource(write_disposition="replace")
    def employee() -> Iterable[TDataItem]:
        """Extrai dados da tabela employee"""
        yield from get_records(client, "employee")

    return (
        employee,
    )