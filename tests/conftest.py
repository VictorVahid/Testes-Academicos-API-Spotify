import base64
import requests
import pytest
import os
from dotenv import load_dotenv

load_dotenv() 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1" 

@pytest.fixture(scope="session")
def access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        pytest.fail("CLIENT_ID ou CLIENT_SECRET não encontrados. Verifique o arquivo .env e o .gitignore.")

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status() 
        token = response.json()['access_token']
        return token
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Falha CRÍTICA ao obter Access Token. Erro: {e}")

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL