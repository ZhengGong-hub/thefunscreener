from app.database import PostgresDatabase
from app.database.db_task_manager import TaskManagerRepository
from app.api.api_server import TheFunScreenerServer
from app.api.api_service import TheFunScreenerService
from app.api.api import TheFunScreenerAPI

from app.config.config import Config

config = Config().load_configuration()


def setup():
    # Initialize dependencies
    database = PostgresDatabase(**config.database.db_config)
    task_manager = TaskManagerRepository(database)

    # Create server
    server = TheFunScreenerServer()

    # Create business services
    thefunscreener_service = TheFunScreenerService(task_manager)

    # Api endpoints
    api = TheFunScreenerAPI(thefunscreener_service)

    # Register api endpoints on the server
    server.add_routes(api.router)

    return server


# Create the app instance for Gunicorn or FastAPI to use
server = setup()
app = server.app

if __name__ == "__main__":
    # Run the server
    # the change of port and host is done in the api_server.py file
    server.run()
