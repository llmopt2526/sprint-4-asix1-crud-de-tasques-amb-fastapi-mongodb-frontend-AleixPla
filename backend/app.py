import os

from dotenv import load_dotenv
load_dotenv()

from typing import Optional, List, Literal

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
# --- NOVA IMPORTACIÓ PER AL CORS ---
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId
import asyncio
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument

# ------------------------------------------------------------------------ #
#                         Inicialització de l'aplicació                    #
# ------------------------------------------------------------------------ #
app = FastAPI(
    title="Gestor de Pel·lícules API",
    summary="API REST amb FastAPI i MongoDB per gestionar informació de pel·lícules",
)

# --- CONFIGURACIÓ CORS AFEGIDA AQUÍ ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
# Corregit per evitar l'error KeyError: MONGODB_URL
client = AsyncMongoClient(os.environ.get("MONGODB_URL", "mongodb://localhost:27017"))

db = client.gestor_pelicules
pelicules_collection = db.get_collection("pelicules")

PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
class PeliculaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: Literal["pendent de veure", "vista"] = Field(...)
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)
    usuari: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "Dune: Part Dos",
                "descripcio": "En Paul Atreides s'uneix als Fremen.",
                "estat": "vista",
                "puntuacio": 5,
                "genere": "Ciència Ficció",
                "usuari": "Maria"
            }
        },
    )

# ------------------------------------------------------------------------ #
#                               Endpoints API                              #
# ------------------------------------------------------------------------ #

@app.post(
    "/pelicules/",
    response_description="Afegeix una nova pel·lícula",
    response_model=PeliculaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_pelicula(pelicula: PeliculaModel = Body(...)):
    pelicula_dict = pelicula.model_dump(by_alias=True, exclude=["id"])
    nova_pelicula = await pelicules_collection.insert_one(pelicula_dict)
    pelicula_creada = await pelicules_collection.find_one(
        {"_id": nova_pelicula.inserted_id}
    )
    return pelicula_creada

@app.get(
    "/pelicules/",
    response_description="Llista totes les pel·lícules",
    response_model=List[PeliculaModel],
    response_model_by_alias=False,
)
async def list_pelicules():
    return await pelicules_collection.find().to_list(1000)

@app.delete(
    "/pelicules/{id}", 
    response_description="Esborra una pel·lícula"
)
async def delete_pelicula(id: str):
    delete_result = await pelicules_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")

# --- NOU: ENDPOINT PER ACTUALITZAR ---
@app.put(
    "/pelicules/{id}",
    response_description="Actualitza una pel·lícula existent",
    response_model=PeliculaModel,
    response_model_by_alias=False,
)
async def update_pelicula(id: str, pelicula: PeliculaModel = Body(...)):
    actualitzacio = pelicula.model_dump(by_alias=True, exclude=["id"])
    
    peli_actualitzada = await pelicules_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": actualitzacio},
        return_document=ReturnDocument.AFTER
    )
    
    if peli_actualitzada is not None:
        return peli_actualitzada

    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")
