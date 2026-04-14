from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class PredictionSchema(BaseModel):
    player_name: str
    team: str
    predicted_points: float
    last_points: int
    game_date: date
    position: Optional[str] = None

class SearchResponse(BaseModel):
    status: str
    count: int
    results: List[PredictionSchema]

class GameSchema(BaseModel):
    game_id: str
    home_team: str
    away_team: str
    game_date: date
    status: str # 'Final', 'Scheduled', etc.

class CalendarResponse(BaseModel):
    date: date
    games_count: int
    games: List[GameSchema]