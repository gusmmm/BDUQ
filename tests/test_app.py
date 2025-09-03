from http import HTTPStatus

from fastapi.testclient import TestClient

from the_wicker_man.app import app

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_doente():
    doente_data = {
        "numero_processo": 12345,
        "nome": "João Silva",
        "data_nascimento": "1980-01-01",
        "sexo": "M",
        "morada": "Rua Exemplo, 123"
    }
    response = client.post('/doentes', json=doente_data)
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert response_data["numero_processo"] == doente_data["numero_processo"]
    assert response_data["nome"] == doente_data["nome"]
