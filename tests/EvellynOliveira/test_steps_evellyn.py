from pytest_bdd import scenarios, given, when, then, parsers
import requests
import pytest

scenarios('TCS-EvellynOliveira.feature')

test_context = {}

# -------------------- GIVENs --------------------

@given(parsers.parse('defino o país como "{country_code}"'))
def setup_country(country_code):
    test_context['country'] = country_code

@given(parsers.parse('o ID do Usuario para playlists é "{user_id}"'))
def setup_user_playlists_id(user_id):
    test_context['user_id'] = user_id

@given(parsers.parse('que busco pelo termo "{query}"'))
def setup_search_query(query):
    test_context['query'] = query

@given(parsers.parse('defino o tipo de busca como "{type}"'))
def setup_search_type(type):
    test_context['search_type'] = type

@given(parsers.parse('o ID da Categoria é "{category_id}"'))
def setup_category_id(category_id):
    test_context['category_id'] = category_id

@given(parsers.parse('o ID do Episodio é "{episode_id}"'))
def setup_episode_id(episode_id):
    test_context['episode_id'] = episode_id

@given(parsers.parse('o ID do Audiobook para capitulos é "{audiobook_id}"'))
def setup_audiobook_chapters_id(audiobook_id):
    test_context['audiobook_id'] = audiobook_id

@given(parsers.parse('defino include_external como "{val}"'))
def setup_include_external(val):
    test_context['include_external'] = val

# -------------------- WHENs --------------------

@when("busco as playlists do usuario")
def get_user_playlists(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/users/{test_context['user_id']}/playlists"
    params = {"limit": 5}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("executo a busca")
def perform_simple_search(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/search"
    params = {
        "q": test_context['query'],
        "type": test_context['search_type'],
        "limit": 5
    }
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("executo a busca detalhada")
def perform_advanced_search(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/search"
    
    params = {
        "q": test_context.get('query'),
        "type": test_context.get('search_type'),
        "market": test_context.get('country', 'US'),
        "limit": test_context.get('limit', 10),
        "offset": test_context.get('offset', 0),
        "include_external": test_context.get('include_external')
    }
    params = {k: v for k, v in params.items() if v}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco as playlists da categoria")
def get_category_playlists(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/browse/categories/{test_context['category_id']}/playlists"
    params = {"country": "US", "limit": 5}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco o episodio")
def get_episode(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"market": "US"} 
    url = f"{api_base_url}/episodes/{test_context['episode_id']}"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco a lista de categorias")
def get_all_categories(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/browse/categories"
    params = {"country": test_context.get('country', 'US'), "limit": 10}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco os capitulos do audiobook")
def get_audiobook_chapters(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/audiobooks/{test_context['audiobook_id']}/chapters"
    params = {"market": "US", "limit": 5}
    test_context['response'] = requests.get(url, headers=headers, params=params)

# -------------------- THENs --------------------

@then(parsers.parse("o status code deve ser {status_code:d}"))
def check_status_code(status_code):
    if test_context['response'].status_code != status_code:
        print(f"DEBUG ERRO: {test_context['response'].text}")
    assert test_context['response'].status_code == status_code, \
        f"Status incorreto! Recebido: {test_context['response'].status_code}"

@then("a resposta deve conter a mensagem de destaque")
def check_message_exists():
    data = test_context['response'].json()
    assert 'message' in data
    assert len(data['message']) > 0

@then(parsers.parse("a lista '{list_path}' não deve estar vazia"))
def check_list_path_not_empty(list_path):
    data = test_context['response'].json()
    keys = list_path.split('.')
    val = data
    for k in keys:
        val = val.get(k, {})
    assert isinstance(val, list)
    assert len(val) > 0

@then(parsers.parse("a resposta deve conter uma lista de '{list_path}'"))
def check_list_exists_nested(list_path):
    check_list_path_not_empty(list_path)

@then(parsers.parse("a lista '{list_name}' deve ter pelo menos {qtd:d} item"))
def check_list_min_size(list_name, qtd):
    data = test_context['response'].json()
    lista = data.get(list_name)
    assert isinstance(lista, list)
    assert len(lista) >= qtd

@then(parsers.parse("o campo '{field}' deve ser igual a '{expected}'"))
def check_field_equals(field, expected):
    data = test_context['response'].json()
    assert str(data.get(field)) == expected

@then(parsers.parse("o campo '{field}' deve ser maior que {val:d}"))
def check_field_greater(field, val):
    data = test_context['response'].json()
    assert data.get(field) > val

@then(parsers.parse("o primeiro item da lista deve ter o campo '{field}' preenchido"))
def check_first_item_field(field):
    data = test_context['response'].json()
    found_list = None
    for key, value in data.items():
        if isinstance(value, list) and len(value) > 0:
            found_list = value
            break
        elif isinstance(value, dict) and 'items' in value:
            found_list = value['items']
            break
    assert found_list is not None, "Nenhuma lista encontrada na resposta"
    assert found_list[0].get(field) is not None

@then(parsers.parse("cada item da lista deve possuir o campo '{field}'"))
def check_all_items_field(field):
    data = test_context['response'].json()
    if 'categories' in data:
        items = data['categories']['items']
    else:
        items = data.get('items', [])
        
    for item in items:
        assert field in item

@then(parsers.parse("a resposta deve conter a mensagem de erro '{error_message}'"))
def check_error_message(error_message):
    data = test_context['response'].json()
    returned_message = data.get("error", {}).get("message")
    assert returned_message == error_message, \
        f"Esperava mensagem '{error_message}', mas recebeu '{returned_message}'"