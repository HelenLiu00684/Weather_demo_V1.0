####################################################
#
# PyTest Test Infrastructure
#
# Responsibility
#
# Configure an isolated testing environment
# for the Weather Monitoring Platform.
#
# Responsibilities
#
# • Create an in-memory SQLite database
#
# • Initialize database schema
#
# • Provide reusable database sessions
#
# • Clean up testing resources automatically
#
# Dependencies
#
# • PyTest Fixtures
#
# • SQLAlchemy
#
# • SQLite (In-Memory)
#
# Processing Pipeline
#
# Create Test Database
#          ↓
# Create Database Schema
#          ↓
# Create Database Session
#          ↓
# Execute Test Cases
#          ↓
# Close Database Session
#          ↓
# Remove Database Schema
#
####################################################
import sys

from pathlib import Path

####################################################
#
# Step 1. Configure Project Import Path
#
# Add the project root directory to the
# Python module search path.
#
# This allows test modules to import
# application packages using:
#
#     from app.xxx import ...
#
####################################################
#
# Resolve the project root directory
# relative to this test file.
#
ROOT=Path(

    __file__

).resolve().parent.parent

#
# Register the project root so Python
# can locate application modules.
#
sys.path.append(

    str(ROOT)

)

import pytest

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool

from app.database.database import Base


####################################################
#
# Step 2. Configure Testing Database
#
# Use an in-memory SQLite database for
# unit testing.
#
# Advantages
#
# • Fast execution
#
# • No external database required
#
# • Automatically discarded after tests
#
####################################################
TEST_DB="sqlite://"

####################################################
#
# Step 3. Create SQLAlchemy Engine
#
# Configure the SQLAlchemy engine used
# by all unit tests.
#
# Special Configuration
#
# check_same_thread=False
#
#     Allow multiple threads to share
#     the same SQLite connection.
#
# StaticPool
#
#     Reuse one in-memory database
#     throughout the entire test run.
#
####################################################

engine=create_engine(

    TEST_DB,
#
# SQLite connection options.
#
    connect_args={

        "check_same_thread":False

    },
#
# Keep the same in-memory database alive
# during the entire testing session.
#
    poolclass=StaticPool

)


####################################################
#
# Step 4. Create Testing Session Factory
#
# Create a SQLAlchemy session factory
# bound to the testing database engine.
#
# Each call to:
#
#     TestingSession()
#
# creates a new database session.
#
####################################################
TestingSession=sessionmaker(

    bind=engine

)


####################################################
#
# Step 5. Database Session Fixture
#
# Responsibility
#
# Provide an isolated database session
# for every test case.
#
# Fixture Lifecycle
#
# Create Tables
#        ↓
# Create Session
#        ↓
# Execute Test
#        ↓
# Close Session
#        ↓
# Drop Tables
#
####################################################
@pytest.fixture()

def db_session():
#
# Create all database tables before
# executing the current test.
#
    Base.metadata.create_all(

        engine

    )

#
# Create a new SQLAlchemy session
# connected to the testing database.
#
    session=TestingSession()

#
# Yield the session to the test case.
#
# Test execution pauses here while the
# test performs database operations.
#
    yield session

#
# Close the database session after
# the test completes.
#
    session.close()

#
# Remove all database tables to ensure
# the next test starts with a clean
# database environment.
#
    Base.metadata.drop_all(

        engine

    )