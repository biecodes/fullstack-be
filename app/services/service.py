from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os, sys
import time
from typing import Optional
import traceback

from loguru import logger
import srsly

path_this = os.path.dirname(os.path.abspath(__file__))
path_project = os.path.dirname(os.path.join(path_this, '..'))
path_root = os.path.dirname(os.path.join(path_this, '../..'))
sys.path.append(path_root)
sys.path.append(path_project)
sys.path.append(path_this)

from press_redis_processor import RedisProcessor

app = FastAPI(
    title="Press Release Generation",
    description="Generate Press Release Document",
    version="0.0.1",
    timeout=500
)

redis = RedisProcessor()

class PromptStatementText(BaseModel):
    log_id: str = Field(default="log id")
    log_index: str = Field(default='log index')
    client_name: str = Field(example="Polda Metro Jaya")
    persona: str = Field(example="The regional police force responsible for maintaining law and order in the Jakarta metropolitan area, including Jakarta, Depok, Tangerang, and Bekasi. As part of law enforcement, Polda Metro Jaya plays a crucial role in crime prevention, public security, traffic regulation, and counterterrorism efforts.")
    text: Optional[str] = Field(example="Satresnarkoba Polres Metro Depok Berikan Himbauan Pencegahan Penyalahgunaan Narkoba di Pondok Pinus Permai")
    additional_context: bool = Field(default=False)

class PromptStatementStatus(BaseModel):
    id: str = Field()
    client_name: str = Field()

@app.post("/request")
def request(request: PromptStatementText):
    logger.debug(f"Received payload: {request.model_dump(mode='json')}") 
    
    try:
        data = request.dict()
        data["id"] = None
        
        result = redis.request(data)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error in request endpoint: {str(traceback.format_exc())}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while requesting Press Release Document."
        ) from e
