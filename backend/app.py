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
# Creació de la instància FastAPI amb infomració bàsica de l'API
app = FastAPI(
    title="Gestor de Pel·lícules API",
    summary="API REST amb FastAPI i MongoDB per gestionar informació de pel·lícules",
)

# --- CONFIGURACIÓ CORS AFEGIDA AQUÍ ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet que qualsevol web es connecti (ideal per desenvolupament)
    allow_credentials=True,
    allow_methods=["*"],  # Permet tots els mètodes com POST, GET, PUT, DELETE
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
# Obtenim la URL de la variable d'entorn per seguretat.
# Si no troba la variable, farà servir localhost per defecte.

# mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
# client = AsyncMongoClient(mongodb_url)

client = AsyncMongoClient(os.environ["MONGODB_URL"])

# Selecció de la base de dades i de la col·lecció adaptada al teu domini
db = client.gestor_pelicules
pelicules_collection = db.get_collection("pelicules")

# PyObjectId per a la compatibilitat entre MongoDB i JSON/Pydantic
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
class PeliculaModel(BaseModel):
    """
    Model que representa una pel·lícula.
    Conté tots els camps requerits a l'enunciat de l'Sprint 4.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    # Camps obligatoris del gestor de pel·lícules
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: Literal["pendent de veure", "vista"] = Field(...)
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)
    usuari: str = Field(...)

    # Configuració addicional del model Pydantic per a Swagger UI
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
    """
    Insereix una nova pel·lícula a la base de dades.
    """
    # Convertim el model a diccionari i excloem l'ID perquè el generi MongoDB
    pelicula_dict = pelicula.model_dump(by_alias=True, exclude=["id"])

    # Inserim a la col·lecció
    nova_pelicula = await pelicules_collection.insert_one(pelicula_dict)

    # Recuperem el document inserit per retornar-lo
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
    """
    Llista totes les dades de pel·lícules a la base de dades.
    La resposta no està paginada i es limita a 1000 resultats.
    """
    return await pelicules_collection.find().to_list(1000)

@app.delete(
    "/pelicules/{id}", 
    response_description="Esborra una pel·lícula"
)
async def delete_pelicula(id: str):
    """
    Elimina una pel·lícula de la base de dades utilitzant el seu ID.
    Si l'operació té èxit, retorna un codi 204 (No Content).
    """
    delete_result = await pelicules_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Pel·lícula amb id {id} no trobada")
