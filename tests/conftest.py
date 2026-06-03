import sys

from pathlib import Path


ROOT=Path(

    __file__

).resolve().parent.parent


sys.path.append(

    str(ROOT)

)
import pytest

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from app.database.database import Base



TEST_DB="sqlite:///:memory:"


engine=create_engine(

    TEST_DB

)


TestingSession=sessionmaker(

    bind=engine

)



@pytest.fixture()

def db_session():

    Base.metadata.create_all(

        engine

    )

    session=TestingSession()


    yield session


    session.close()


    Base.metadata.drop_all(

        engine

    )