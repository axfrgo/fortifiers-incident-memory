"""AWS Lambda adapter for the existing FastAPI application."""

from mangum import Mangum

from incident_memory.api import app


handler = Mangum(app, lifespan="off")
