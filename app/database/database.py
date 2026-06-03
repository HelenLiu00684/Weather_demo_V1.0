from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base

####################################################

#

# Database Layer

#

# Responsibilities:

#

# Create SQLite connection

#

# Provide shared ORM base

#

# Provide session factory

#

# SQLite acts as authoritative state

#

####################################################

DATABASE_URL="sqlite:///weather.db"

engine=create_engine(


DATABASE_URL,
echo=True
)

SessionLocal=sessionmaker(
bind=engine
)

Base=declarative_base()
