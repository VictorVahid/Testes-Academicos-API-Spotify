from pytest_bdd import scenarios, given, when, then, parsers
import requests
import pytest
import json

scenarios('TCS-CarlosEduardo.feature')

test_context = {}

# -------------------- GIVENs --------------------

@given(parsers.parse('o ID do Album é "{album_id}"'))
def given_album_id(album_id):
    test_context['album_id'] = album_id
    
@given(parsers.parse('o ID da Playlist é "{playlist_id}"'))
def given_playlist_id(playlist_id):
    test_context['playlist_id'] = playlist_id

@given(parsers.parse('o ID do Show é "{show_id}"'))
def given_show_id(show_id):
    test_context['show_id'] = show_id
    if 'params' not in test_context:
        test_context['params'] = {}

@given(parsers.parse("defino o parâmetro de query '{param_name}' como {param_value:d}"))
def given_query_param_int(param_name, param_value):
    if 'params' not in test_context:
        test_context['params'] = {}
    test_context['params'][param_name] = param_value

# -------------------- WHENs --------------------

@when("eu busco as faixas do álbum")
def when_get_album_tracks(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/albums/{test_context['album_id']}/tracks"
    test_context['response'] = requests.get(url, headers=headers)
    
@when("eu busco as faixas da playlist")
def when_get_playlist_tracks(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/playlists/{test_context['playlist_id']}/tracks"
    test_context['response'] = requests.get(url, headers=headers)
    
@when("eu busco os episódios do show")
def when_get_show_episodes(api_base_url, access_token):
    # Endpoint documentado: /v1/shows/{id}/episodes
    url = f"{api_base_url}/shows/{test_context['show_id']}/episodes"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    test_context['response'] = requests.get(
        url, 
        headers=headers, 
        params=test_context.get('params', {})
    )
    
# -------------------- THENs --------------------

@then(parsers.parse("o status code da resposta deve ser {status_code:d}"))
def then_status_code(status_code):
    assert test_context['response'].status_code == status_code
    
@then(parsers.parse("a resposta deve conter uma lista de '{list_name}'"))
def then_check_list_exists(list_name):
    data = test_context['response'].json()
    assert list_name in data
    assert isinstance(data[list_name], list)
    
@then("todas as faixas devem ter o campo 'type' igual a 'track'")
def then_check_track_type():
    data = test_context['response'].json()
    items = data.get('items', [])
    for item in items:
        assert item['type'] == 'track'
        
@then("cada item da lista deve possuir o campo 'track_number' com um valor numérico")
def then_check_track_number():
    data = test_context['response'].json()
    items = data.get('items', [])
    for item in items:
        assert isinstance(item.get('track_number'), int)

@then(parsers.parse("cada item da lista deve possuir o campo '{field}' preenchido"))
def then_check_field_in_list(field):
    data = test_context['response'].json()
    items = data.get('items', [])
    
    assert len(items) > 0, "A lista de itens veio vazia!"
    
    for item in items:
        assert item.get(field) is not None, f"O campo '{field}' está faltando em um dos itens"

@then(parsers.parse("o primeiro item da lista deve ter o campo '{field}' preenchido"))
def then_check_first_item_field(field):
    data = test_context['response'].json()
    items = data.get('items', [])
    
    assert len(items) > 0, "A lista de itens veio vazia!"
    assert items[0].get(field) is not None, f"O primeiro item não tem o campo '{field}'"

@then(parsers.parse('o status code da resposta deve ser {status_code:d}'))
def then_status_code(status_code):
    assert test_context['response'].status_code == status_code, \
        f"Erro na requisição: {test_context['response'].text}"

@then(parsers.parse("a resposta deve conter uma lista de '{list_name}'"))
def then_check_list_exists(list_name):
    data = test_context['response'].json()
    assert list_name in data, f"Campo '{list_name}' não encontrado no JSON."
    assert isinstance(data[list_name], list), f"Campo '{list_name}' não é uma lista."

@then(parsers.parse("todos os itens da lista devem ter o campo '{field}' igual a '{expected_value}'"))
def then_check_all_items_value(field, expected_value):
    data = test_context['response'].json()
    items = data.get('items', [])
    
    assert len(items) > 0, "A lista de episódios está vazia."
    
    for item in items:
        assert item.get(field) == expected_value, \
            f"Item com ID {item.get('id')} tem '{field}' diferente de '{expected_value}'"

@then(parsers.parse("cada item da lista deve possuir o campo '{field}'"))
def then_check_field_presence(field):
    data = test_context['response'].json()
    items = data.get('items', [])
    
    for item in items:
        # Verifica se a chave existe (mesmo que seja null, a chave deve existir)
        assert field in item, f"O campo '{field}' não existe no episódio {item.get('id')}"

@then(parsers.parse("o primeiro item da lista deve ter o campo '{field}' preenchido"))
def then_check_first_item_field(field):
    data = test_context['response'].json()
    items = data.get('items', [])
    
    if len(items) > 0:
        val = items[0].get(field)
        assert val is not None and val != "", f"O campo '{field}' está vazio no primeiro item."