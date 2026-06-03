from app.database.database import engine
from app.database.database import Base

from app.database.reading import WeatherReading
from app.database.event import WeatherEvent

# Take all ORM models registered in Base and Using the engine to create tables
Base.metadata.create_all(bind=engine)

print("tables created")