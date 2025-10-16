from typing import Iterator, Dict, Any
import dlt
import datetime
from .client import PostgresCredentials, make_postgres_client
from .records import get_records


@dlt.source(name="postgres")
def postgres_source(
        credentials: PostgresCredentials = dlt.secrets.value,
):
    # Cria a conexão com o banco de dados
    conn = make_postgres_client(credentials)

    @dlt.resource(name="employee", write_disposition="replace")
    def get_employee(
            last_modified_at=dlt.sources.incremental("modified_at",
                                                     initial_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    ) -> Iterator[Dict[str, Any]]:
        yield from get_records(conn, "employee", last_state=last_modified_at, limit=1000)


    @dlt.resource(name="customer", write_disposition="replace")
    def get_customer(
            last_modified_at=dlt.sources.incremental("modified_at",
                                                     initial_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    ) -> Iterator[Dict[str, Any]]:
        yield from get_records(conn, "customer", last_state=last_modified_at, limit=1000)


    @dlt.resource(name="product", write_disposition="replace")
    def get_product(
            last_modified_at=dlt.sources.incremental("modified_at",
                                                     initial_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    ) -> Iterator[Dict[str, Any]]:
        yield from get_records(conn, "product", last_state=last_modified_at, limit=1000)

    return (
        get_employee,
        get_customer,
        get_product
    )