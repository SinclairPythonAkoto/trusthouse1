from trusthouse.db import Base, engine
from trusthouse.models import Base

Base.metadata.create_all(bind=engine)
