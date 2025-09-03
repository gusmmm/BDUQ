from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class DoenteSchema(BaseModel):
    numero_processo: int
    nome: str
    data_nascimento: str
    sexo: str
    morada: str


class DoentePublic(BaseModel):
    numero_processo: int
    nome: str


class DoenteDB(DoenteSchema):
    id: int
