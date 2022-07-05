import os
from sqla_wrapper import SQLAlchemy

db_url = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
print(db_url)

db = SQLAlchemy(db_url)

# db = SQLAlchemy(
#     dialect="postgresql",
#     user=os.getenv("DATABASE_URL"),
#     password=os.getenv("DATABASE_URL"),
#     host=os.getenv("DATABASE_URL"),
#     name=os.getenv("DATABASE_URL"),
# )
