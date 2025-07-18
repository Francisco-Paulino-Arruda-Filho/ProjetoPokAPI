import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

database = client["team_builder"]

pokemons_collection = database["pokemons"]