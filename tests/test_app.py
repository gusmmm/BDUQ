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


def test_read_doente_not_found(client):
    response = client.get('/doentes/9999')  # Assuming 9999 does not exist
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"error": "Doente not found"}


def test_read_doente(client):
    # First, create a doente to ensure there is one to read
    doente_data = {
        "numero_processo": 12346,
        "nome": "Maria Silva",
        "data_nascimento": "1990-02-02",
        "sexo": "F",
        "morada": "Avenida Exemplo, 456"
    }
    create_response = client.post('/doentes', json=doente_data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_doente = create_response.json()
    doente_id = created_doente["id"]

    # Now, read the created doente
    read_response = client.get(f'/doentes/{doente_id}')
    assert read_response.status_code == HTTPStatus.OK
    read_doente = read_response.json()
    assert read_doente["numero_processo"] == doente_data["numero_processo"]
    assert read_doente["nome"] == doente_data["nome"]
