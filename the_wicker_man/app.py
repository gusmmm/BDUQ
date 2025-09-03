from http import HTTPStatus

from fastapi import FastAPI

from the_wicker_man.schemas import Message

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}

@app.post('/doentes', status_code=HTTPStatus.CREATED)
def create_doente():
    return {"message": "Doente created successfully"}