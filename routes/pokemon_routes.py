from fastapi import APIRouter, HTTPException
from models.Team import Team
from models.Pokemon import Pokemon
from bson import ObjectId
from database import pokemons_collection as collection
from models.User import TeamCreateRequest

router = APIRouter()

@router.post("/team", response_model=Team)
async def create_team(payload: TeamCreateRequest):
    team = Team(user_id=payload.user_id)
    result = await collection.insert_one(team.dict(by_alias=True))
    created = await collection.find_one({"_id": result.inserted_id})
    return Team(**created)

@router.get("/all_teams", response_model=list[Team])
async def get_all_teams():
    teams = await collection.find().to_list(1000)
    return [Team(**team) for team in teams]

@router.post("/team/{team_id}/slot/{slot_index}", response_model=Team)
async def add_pokemon_to_slot(team_id: str, slot_index: int, pokemon: Pokemon):
    if slot_index < 0 or slot_index >= 6:
        raise HTTPException(status_code=400, detail="Invalid slot index")
    
    team = await collection.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team["team"][slot_index] = pokemon.dict()
    await collection.update_one({"_id": ObjectId(team_id)}, {"$set": {"team": team["team"]}})
    
    updated_team = await collection.find_one({"_id": ObjectId(team_id)})
    return Team(**updated_team)

@router.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: str):
    team = await collection.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    
    return Team(**team)  

@router.put("/team/{team_id}/slot/{slot_index}", response_model=Team)
async def update_pokemon_slot(team_id: str, slot_index: int, pokemon: Pokemon):
    if slot_index < 0 or slot_index >= 6:
        raise HTTPException(status_code=400, detail="Invalid slot index")
    
    await collection.update_one(
        {"_id": ObjectId(team_id)},
        {"$set": {f"team.{slot_index}": pokemon.dict()}}
    )
    team = await collection.find_one({"_id": ObjectId(team_id)})
    return Team(**team)

@router.delete("/team/{team_id}/slot/{slot_index}", response_model=Team)
async def remove_pokemon_from_slot(team_id: str, slot_index: int):
    if slot_index < 0 or slot_index >= 6:
        raise HTTPException(status_code=400, detail="Invalid slot index")
    
    await collection.update_one(
        {"_id": ObjectId(team_id)},
        {"$set": {f"team.{slot_index}": None}}
    )
    team = await collection.find_one({"_id": ObjectId(team_id)})
    return Team(**team)

@router.delete("/team/{team_id}", response_model=Team)
async def delete_team(team_id: str):
    team = await collection.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    await collection.delete_one({"_id": ObjectId(team_id)})
    return Team(**team)

@router.get("/team/{team_id}", response_model=Team)
async def get_team_by_id(team_id: str):
    team = await collection.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return Team(**team)

@router.get("/team/{user_id}/user", response_model=list[Team])
async def get_teams_by_user(user_id: str):
    print(f"Fetching teams for user_id: {user_id}")
    teams = await collection.find({"user_id": ObjectId(user_id)}).to_list(1000)
    return [Team(**team) for team in teams]

