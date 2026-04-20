from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.main import app
from app.oauth2 import create_access_token
from app.database import get_db, Base
from app import models


DATABASE_URL = f"postgresql+psycopg://postgres:1234@localhost:5432/mprosody_db_test"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture
def client(session):

    def override_get_db():
        # db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)