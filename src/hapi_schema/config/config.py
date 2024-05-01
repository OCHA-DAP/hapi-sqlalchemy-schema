import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def create_pg_uri_from_env_without_protocol():
    hapi_db_name = os.getenv("HAPI_DB_NAME", "hapi")
    hapi_db_user = os.getenv("HAPI_DB_USER", "hapi")
    hapi_db_pass = os.getenv("HAPI_DB_PASS", "hapi")
    hapi_db_host = os.getenv("HAPI_DB_HOST", "localhost")
    hapi_db_port = int(os.getenv("HAPI_DB_PORT", 45432))

    sql_alchemy_asyncypg_db_uri = f"{hapi_db_user}:{hapi_db_pass}@{hapi_db_host}:{hapi_db_port}/{hapi_db_name}"
    return sql_alchemy_asyncypg_db_uri


@dataclass
class Config:
    # HAPI Database configuration
    SQL_ALCHEMY_ASYNCPG_DB_URI: str
    SQL_ALCHEMY_PSYCOPG2_DB_URI: str


CONFIG = None


def get_config() -> Config:
    global CONFIG
    if not CONFIG:
        db_uri_without_protocol = create_pg_uri_from_env_without_protocol()

        sql_alchemy_asyncypg_db_uri = (
            f"postgresql+asyncpg://{db_uri_without_protocol}"
        )
        sql_alchemy_psycopg2_db_uri = (
            f"postgresql+psycopg2://{db_uri_without_protocol}"
        )
        CONFIG = Config(
            SQL_ALCHEMY_ASYNCPG_DB_URI=sql_alchemy_asyncypg_db_uri,
            SQL_ALCHEMY_PSYCOPG2_DB_URI=sql_alchemy_psycopg2_db_uri,
        )

    return CONFIG
