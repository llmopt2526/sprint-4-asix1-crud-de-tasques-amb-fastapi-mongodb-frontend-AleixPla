import os

#Carreguem la url del MongoDB Atlas des del fitxer .env
from dotenv import load_dotenv
load_dotenv()

from typing import Optional, List, Literal

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
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
                "titol": "Creep",
                "descripcio": "Un càmera accepta una feina per filmar la vida quotidiana...",
                "estat": "vista",
                "puntuacio": 4,
                "genere": "Terror",
                "usuari": "Aleix"
            }
        },
    )

class EstatUpdateModel(BaseModel):
    estat: Literal["pendent de veure", "vista"] = Field(...)

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

# Nou endpoint per a obtindre una pel·lícula per la seva id
@app.get(
    "/pelicules/{id}",
    response_description="Obté una única pel·lícula per ID",
    response_model=PeliculaModel,
    response_model_by_alias=False,
)
async def show_pelicula(id: str):
    """
    Busca una pel·lícula específica a la base de dades utilitzant el seu ID.
    """
    if (pelicula := await pelicules_collection.find_one({"_id": ObjectId(id)})) is not None:
        return pelicula

    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")

# Per a esborrar pel·lícules
@app.delete(
    "/pelicules/{id}", 
    response_description="Esborra una pel·lícula"
)
async def delete_pelicula(id: str):
    delete_result = await pelicules_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")

# Per a actualitzar NOMÉS l'estat de la pel·lícula desde POSTMAN
@app.put(
    "/pelicules/{id}",
    response_description="Actualitza només l'estat d'una pel·lícula existent",
    response_model=PeliculaModel,
    response_model_by_alias=False,
)
async def update_pelicula(id: str, dades_actualitzacio: EstatUpdateModel = Body(...)):
    peli_actualitzada = await pelicules_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"estat": dades_actualitzacio.estat}},
        return_document=ReturnDocument.AFTER
    )

# Si troba la película i l'actualitza, la mostra al frontend
    if peli_actualitzada is not None:
        return peli_actualitzada

# Si no la troba, mostra un error
    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")
