from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Query
from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import Session

from the_wicker_man.database import get_session
from the_wicker_man.models import Doente
from the_wicker_man.schemas import (
    DoentePublic,
    DoenteSchema,
    DoentesList,
    MessageSchema,
)

app = FastAPI()


@app.get('/', response_model=MessageSchema, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/doentes', status_code=HTTPStatus.CREATED,
          response_model=DoentePublic)
def create_doente(doente: DoenteSchema,
                  session: Session = Depends(get_session)):
    doente_db = session.scalar(
        select(Doente).where(
            (Doente.numero_processo == doente.numero_processo)
            )
    )

    if doente_db:
        if doente_db.numero_processo == doente.numero_processo:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Doente with this numero_processo already exists',
            )

    doente_db = Doente(
        numero_processo=doente.numero_processo,
        nome=doente.nome,
        data_nascimento=doente.data_nascimento,
        sexo=doente.sexo,
        morada=doente.morada,
    )
    session.add(doente_db)
    session.commit()
    session.refresh(doente_db)

    return doente_db


@app.get('/doentes', response_model=DoentesList, status_code=HTTPStatus.OK)
def read_doentes(
    offset: int = Query(0, ge=0),
    limit: int | None = Query(None, ge=1),  # default: no limit
    session: Session = Depends(get_session),
):
    query = select(Doente).order_by(Doente.id).offset(offset)
    if limit is not None:
        query = query.limit(limit)
    rows = session.scalars(query).all()
    doentes_public = [
        DoentePublic(
            id=row.id,
            numero_processo=row.numero_processo,
            nome=row.nome,
        )
        for row in rows
    ]
    return DoentesList(doentes=doentes_public)


@app.get('/doentes/{doente_id}',
         status_code=HTTPStatus.OK)
def read_doente(doente_id: int, session: Session = Depends(get_session)):
    doente = session.get(Doente, doente_id)
    if not doente:
        return {"error": "Doente not found"}
    return DoentePublic(
        id=doente.id,
        numero_processo=doente.numero_processo,
        nome=doente.nome,
    )


@app.put('/doentes/{doente_id}',
         status_code=HTTPStatus.OK)
def update_doente(
    doente_id: int,
    doente: DoenteSchema,
    session: Session = Depends(get_session),
):
    existing = session.get(Doente, doente_id)
    if not existing:
        return {"error": "Doente not found"}

    existing.numero_processo = doente.numero_processo
    existing.nome = doente.nome
    existing.data_nascimento = doente.data_nascimento
    existing.sexo = doente.sexo
    existing.morada = doente.morada
    session.commit()
    session.refresh(existing)

    ic(f"Doente updated: id={existing.id}")
    return DoentePublic(
        id=existing.id,
        numero_processo=existing.numero_processo,
        nome=existing.nome,
    )


@app.delete('/doentes/{doente_id}', response_model=MessageSchema)
def delete_doente(doente_id: int, session: Session = Depends(get_session)):
    doente = session.get(Doente, doente_id)
    if not doente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Doente not found'
        )

    ic(f"Deleting doente with ID: {doente_id}")
    session.delete(doente)
    session.commit()

    return {'message': 'Doente deleted'}
