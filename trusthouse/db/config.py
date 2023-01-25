from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./trusthoue.db"
engine = create_engine(DATABASE_URL)
