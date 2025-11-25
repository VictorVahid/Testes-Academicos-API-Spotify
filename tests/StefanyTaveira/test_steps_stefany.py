from pytest_bdd import scenarios, given, when, then, parsers
import requests
import pytest

# Conecta com o feature
scenarios('TCS-Stefany.feature')

test_context = {}

# -------------------- GIVENs --------------------

@given(parsers.parse('defino o ID da Categoria como "{category_id}"'))
def setup_category_id(category_id):
    test_context['category_id'] = category_id

@given(parsers.parse('defino os IDs dos Artistas como "{artists_ids}"'))
def setup_multiple_artists(artists_ids):
    test_context['artists_ids'] = artists_ids

@given(parsers.parse('defino o ID do Audiobook como "{audiobook_id}"'))
def setup_audiobook_id(audiobook_id):
    test_context['audiobook_id'] = audiobook_id

@given(parsers.parse('defino o ID do Usuario como "{user_id}"'))
def setup_user_id(user_id):
    test_context['user_id'] = user_id

@given(parsers.parse('defino o ID do Artista como "{artist_id}"'))
def setup_artist_id(artist_id):
    test_context['artist_id'] = artist_id

# -------------------- WHENs --------------------

@when("busco a categoria")
def get_category(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/browse/categories/{test_context['category_id']}"
    params = {"country": "US"}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco varios artistas")
def get_several_artists(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/artists"
    params = {"ids": test_context['artists_ids']}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco o audiobook")
def get_audiobook(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/audiobooks/{test_context['audiobook_id']}"
    params = {"market": "US"} 
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco o usuario")
def get_user(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/users/{test_context['user_id']}"
    test_context['response'] = requests.get(url, headers=headers)

@when("busco os mercados disponiveis")
def get_markets(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/markets"
    test_context['response'] = requests.get(url, headers=headers)

# -------------------- THENs --------------------

@then(parsers.parse("o status code deve ser {status_code:d}"))
def check_status_code(status_code):
    if test_context['response'].status_code != status_code:
        print(f"ERRO: Retornou {test_context['response'].status_code}. Msg: {test_context['response'].text}")
    assert test_context['response'].status_code == status_code

@then(parsers.parse("o campo '{field}' deve ser igual a '{expected_value}'"))
def check_field_value(field, expected_value):
    data = test_context['response'].json()
    assert data.get(field) == expected_value

@then(parsers.parse("a lista '{field_path}' não deve estar vazia"))
def check_nested_list_not_empty(field_path):
    data = test_context['response'].json()
    keys = field_path.split('.')
    val = data
    for k in keys:
        val = val.get(k)
    assert isinstance(val, list)
    assert len(val) > 0

@then(parsers.parse("a lista '{list_name}' deve ter {min_qtd:d} itens"))
def check_list_min_len(list_name, min_qtd):
    data = test_context['response'].json()
    lista = data.get(list_name)
    assert len(lista) >= min_qtd