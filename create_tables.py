from library.db import engine
from library.models import Base

Base.metadata.create_all(engine)

print("Tables created successfully!")
