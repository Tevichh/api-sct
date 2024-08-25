from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ["MYSQL_USER"]
passw = os.environ["MYSQL_PASSWORD"]
host = os.environ["MYSQL_HOST"]
dataBase = os.environ["MYSQL_DATABASE"]

DATABASE_CONECTION_URI = f"mysql://{user}:{passw}@{host}/{dataBase}"
