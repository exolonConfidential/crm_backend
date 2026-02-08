from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from dotenv import load_dotenv
import os

load_dotenv()

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.db.models.base import Base
from app.db.models.location import Location
from app.db.models.owner import Owner
from app.db.models.property import Property
from app.db.models.insurance_details import InsuranceDetails

target_metadata = Base.metadata


# ---- IMPORTANT: IGNORE POSTGIS TABLES ----
def include_object(object, name, type_, reflected, compare_to):
    POSTGIS_TABLES = {
        "spatial_ref_sys",
        "layer",
        "topology",
        "geography_columns",
        "geometry_columns",
        "raster_columns",
        "raster_overviews",
    }

    # ignore PostGIS internal tables
    if type_ == "table" and name in POSTGIS_TABLES:
        return False

    # ignore entire topology schema
    if getattr(object, "schema", None) in {"topology", "tiger", "tiger_data"}:
        return False

    return True


# ---- OFFLINE MIGRATIONS ----
def run_migrations_offline():

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,   # ✅ applied here
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---- ONLINE MIGRATIONS (ASYNC) ----
async def run_migrations_online():

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        def do_run_migrations(connection):
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_object=include_object,   # ✅ THIS WAS MISSING
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ---- ENTRYPOINT ----
def run():

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        import asyncio
        asyncio.run(run_migrations_online())


run()