from typing import Optional

import psycopg2
from dlt.common.typing import TSecretStrValue
from dlt.common.configuration.specs import CredentialsConfiguration, configspec
from dlt.common.configuration import with_config


@configspec
class PostgresCredentials(CredentialsConfiguration):
    
    database: str = "sale"
    username: str = "postgres"
    password: TSecretStrValue = "sale123"
    host: str = "localhost"
    port: Optional[int] = 5433

    
    def __str__(self) -> str:
        return f"PostgresCredentials(host={self.host}, database={self.database}, user={self.username})"


@with_config(spec=PostgresCredentials)
def make_postgres_client(
    credentials: PostgresCredentials = None,
) -> psycopg2.extensions.connection:

    return psycopg2.connect(
        dbname=credentials.database,
        user=credentials.username,
        password=credentials.password,
        host=credentials.host,
        port=credentials.port,
    )
