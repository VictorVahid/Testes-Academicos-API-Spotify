from pytest_bdd import scenarios, given, when, then, parsers
import requests
import pytest

# Conecta com o arquivo de feature
scenarios('TCS-Marcelo.feature')

test_context = {}

# -------------------- GIVENs --------------------

@given(parsers.parse('o ID do Album como "{album_id}"'))
def setup_album_id(album_id):
    test_context['album_id'] = album_id

@given(parsers.parse('o ID da Playlist como "{playlist_id}"'))
def setup_playlist_id(playlist_id):
    test_context['playlist_id'] = playlist_id

@given(parsers.parse('defino os IDs das Faixas como "{tracks_ids}"'))
def setup_multiple_tracks(tracks_ids):
    test_context['tracks_ids'] = tracks_ids

@given(parsers.parse('o ID do Artista como "{artist_id}"'))
def setup_artist_id(artist_id):
    test_context['artist_id'] = artist_id

@given(parsers.parse('define o mercado como "{market}"'))
def setup_market(market):
    test_context['market'] = market

@given(parsers.parse('defino o ID da Categoria como "{category_id}"'))
def setup_category_id(category_id):
    test_context['category_id'] = category_id

# -------------------- WHENs --------------------

@when("busco o album")
def get_album(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/albums/{test_context['album_id']}"
    test_context['response'] = requests.get(url, headers=headers)

@when("busco a playlist")
def get_playlist(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"market": "US"} 
    url = f"{api_base_url}/playlists/{test_context['playlist_id']}"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco varias faixas")
def get_several_tracks(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/tracks"
    params = {"ids": test_context['tracks_ids']}
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco as top tracks")
def get_top_tracks(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"market": test_context.get('market', 'US')} 
    url = f"{api_base_url}/artists/{test_context['artist_id']}/top-tracks"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("busco a categoria especifica")
def get_single_category(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/browse/categories/{test_context['category_id']}"
    params = {"country": "US"}
    test_context['response'] = requests.get(url, headers=headers, params=params)

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

@then(parsers.parse("o campo '{field}' deve ser maior que {min_value:f}"))
def check_float_value(field, min_value):
    data = test_context['response'].json()
    value = data.get(field)
    assert value is not None
    assert float(value) > min_value

@then(parsers.parse("a resposta deve ter o campo '{field}'"))
def check_field_exists(field):
    data = test_context['response'].json()
    assert field in data

@then(parsers.parse("o valor booleano de '{field}' deve ser {boolean_val}"))
def check_boolean(field, boolean_val):
    data = test_context['response'].json()
    expected = True if boolean_val == 'True' else False
    assert data.get(field) == expected

@then(parsers.parse("a lista '{list_name}' não deve estar vazia"))
def check_list_not_empty(list_name):
    data = test_context['response'].json()
    lista = data.get(list_name)
    assert isinstance(lista, list)
    assert len(lista) > 0

@then(parsers.parse("a lista '{list_name}' deve ter {qtd:d} itens"))
def check_list_min_len(list_name, qtd):
    data = test_context['response'].json()
    lista = data.get(list_name)
    assert len(lista) >= qtd

@then(parsers.parse("o campo '{field}' deve ser igual a '{expected_value}'"))
def check_field_value(field, expected_value):
    data = test_context['response'].json()
    assert data.get(field) == expected_value