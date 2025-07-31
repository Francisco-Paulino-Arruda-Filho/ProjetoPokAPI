import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


database = client["team_builder"]

pokemons_collection = database["pokemons"]
users_collection = database["users"]