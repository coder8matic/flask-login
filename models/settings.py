import os
from sqla_wrapper import SQLAlchemy

db_url = os.getenv("DATABASE_URL")
print(db_url)
#                 .replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

# db = SQLAlchemy(
#     dialect="postgresql",
#     user=os.getenv("DATABASE_URL"),
#     password=os.getenv("DATABASE_URL"),
#     host=os.getenv("DATABASE_URL"),
#     name=os.getenv("DATABASE_URL"),
# )
