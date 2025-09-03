from http import HTTPStatus


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_doente(client):
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


def test_read_doentes(client):
    response = client.get('/doentes')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert "doentes" in response_data
    assert isinstance(response_data["doentes"], list)
