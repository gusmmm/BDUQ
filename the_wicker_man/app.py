from http import HTTPStatus

from fastapi import FastAPI
from icecream import ic

from the_wicker_man.schemas import (
    DoenteDB,
    DoentePublic,
    DoenteSchema,
    DoentesList,
    MessageSchema,
)

app = FastAPI()

database = []


@app.get('/', response_model=MessageSchema, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/doentes', status_code=HTTPStatus.CREATED,
          response_model=DoentePublic)
def create_doente(doente: DoenteSchema):
    doente_id = len(database) + 1
    doente_db = DoenteDB(id=doente_id, **doente.model_dump())
    database.append(doente_db)
    ic(f"Doente created: {doente_db.model_dump()}")
    return doente_db

@app.get('/doentes', response_model=DoentesList, status_code=HTTPStatus.OK)
def read_doentes():
    doentes_public = [DoentePublic(**doente.model_dump()) for doente in database]
    return DoentesList(doentes=doentes_public)
