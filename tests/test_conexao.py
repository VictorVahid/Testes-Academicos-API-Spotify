import requests

def test_token_generation_successful(access_token):
    assert isinstance(access_token, str)
    assert len(access_token) > 50 

def test_can_connect_to_api(access_token, api_base_url):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{api_base_url}/markets", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert 'markets' in response_data