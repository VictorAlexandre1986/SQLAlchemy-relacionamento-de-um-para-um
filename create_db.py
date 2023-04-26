from config_db import Base, engine

Base.metadata.create_all(engine)