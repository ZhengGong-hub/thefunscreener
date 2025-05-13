from app.database.db_task_manager import TaskManagerRepository
from app.database.postgres_database import PostgresDatabase
from app.config.config import Config

config = Config().load_configuration()

postgresdb = PostgresDatabase(**config.database.db_config)
task_manager = TaskManagerRepository(postgresdb)

res = task_manager.query_global_market_cap(asofdate="2025-05-03", mktcap_thres=10e3, country="US", allow_fuzzy=True)
print(res)

# mega cap 200b
# large cap 10b
# mid cap 2b
