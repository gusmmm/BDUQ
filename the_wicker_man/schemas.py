from datetime import date

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class DoenteSchema(BaseModel):
    numero_processo: int
    nome: str
    data_nascimento: date  # was str; Pydantic will parse "YYYY-MM-DD"
    sexo: str
    morada: str


class DoentePublic(BaseModel):
    id: int
    numero_processo: int
    nome: str


class DoenteDB(DoenteSchema):
    id: int


class DoentesList(BaseModel):
    doentes: list[DoentePublic]
