# backend/tests/test_endpoints.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_operation_history():
    robot_id = 1  # ID do robô que estamos testando
    response = client.get(f"/api/robots/{robot_id}/history")
    
    # Verificar se o status da resposta é 200
    assert response.status_code == 200, f"Erro ao acessar o histórico do robô {robot_id}, status code: {response.status_code}"

    # Verificar se a chave 'history' está presente na resposta
    response_data = response.json()
    assert "history" in response_data, f"A chave 'history' não foi encontrada na resposta para o robô {robot_id}"

    # Verificar se a chave 'history' é uma lista
    assert isinstance(response_data["history"], list), f"A chave 'history' não contém uma lista para o robô {robot_id}"

    # Caso o histórico de operações esteja vazio, podemos verificar se ele está retornando uma lista vazia
    assert response_data["history"] == [], f"O histórico de operações para o robô {robot_id} deveria ser uma lista vazia"
