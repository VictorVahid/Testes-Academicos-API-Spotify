from pytest_bdd import scenarios, given, when, then, parsers
import requests
import json
import pytest

scenarios('TCS-VictorVahid.feature')

test_context = {}

# -------------------- GIVENs --------------------

@given(parsers.parse('o ID da Faixa é "{track_id}"'))
def given_track_id(track_id):
    test_context['track_id'] = track_id

@given(parsers.parse('o ID do Artista é "{artist_id}"'))
def given_artist_id(artist_id):
    test_context['artist_id'] = artist_id

@given(parsers.parse('o tipo de retorno desejado é "{album_type}"'))
def given_album_type(album_type):
    test_context['album_type'] = album_type

@given(parsers.parse('a query de busca é "{query}"'))
def given_query(query):
    test_context['query'] = query

@given(parsers.parse('o tipo de busca é "{search_type}"'))
def given_search_type(search_type):
    test_context['search_type'] = search_type

@given(parsers.parse('o mercado de busca é "{market}"'))
def given_market(market):
    test_context['market'] = market

@given(parsers.parse('o ID do Show é "{show_id}"'))
def show_id_setup(show_id):
    test_context['show_id'] = show_id


# -------------------- WHENs --------------------

@when("eu busco a faixa")
def when_get_track(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/tracks/{test_context['track_id']}"
    test_context['response'] = requests.get(url, headers=headers)

@when("eu busço os álbuns do artista")
def when_get_artist_albums(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"include_groups": test_context.get("album_type", "album")}
    url = f"{api_base_url}/artists/{test_context['artist_id']}/albums"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("eu faço uma busca")
def when_search(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": test_context["query"], "type": test_context["search_type"]}
    url = f"{api_base_url}/search"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("eu busco os novos lançamentos")
def when_new_releases(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"country": test_context.get("market", "US")}
    url = f"{api_base_url}/browse/new-releases"
    test_context['response'] = requests.get(url, headers=headers, params=params)

@when("eu busco o artista")
def when_get_artist(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/artists/{test_context['artist_id']}"
    test_context['response'] = requests.get(url, headers=headers)

@when('eu busco o show')
def when_get_show(api_base_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{api_base_url}/shows/{test_context['show_id']}"
    test_context['response'] = requests.get(url, headers=headers)

# -------------------- THENs --------------------

@then(parsers.parse("o status code da resposta deve ser {status_code:d}"))
def then_status_code(status_code):
    assert test_context['response'].status_code == status_code

@then(parsers.parse("o campo '{field}' no corpo da resposta deve ser '{expected_value}'"))
def then_field_value(field, expected_value):
    data = test_context['response'].json()
    assert data.get(field) == expected_value

@then(parsers.parse("o campo '{field}' deve ser '{expected_value}'"))
def then_simple_field(field, expected_value):
    data = test_context['response'].json()
    assert data.get(field) == expected_value

@then(parsers.parse("a resposta deve conter uma lista de '{list_name}'"))
def then_list_exists(list_name):
    data = test_context['response'].json()
    assert list_name in data
    assert isinstance(data[list_name], list) or isinstance(data[list_name], dict)

@then(parsers.parse("a resposta deve conter um objeto '{obj_name}'"))
def then_object_exists(obj_name):
    data = test_context['response'].json()
    assert obj_name in data
    assert isinstance(data[obj_name], dict)

@then(parsers.parse("o campo '{field}' deve ser maior que {min_value:d}"))
def then_greater_than(field, min_value):
    data = test_context['response'].json()
    value = data.get(field)
    assert value is not None
    assert value > min_value

@then(parsers.parse("a lista '{list_path}' não deve ser vazia"))
def then_list_not_empty(list_path):
    parts = list_path.split(".")
    data = test_context['response'].json()
    for p in parts:
        data = data.get(p)
    assert isinstance(data, list)
    assert len(data) > 0

@then(parsers.parse("a lista '{list_path}' deve ter pelo menos {min_items:d} item"))
def then_list_min_items(list_path, min_items):
    parts = list_path.split(".")
    data = test_context['response'].json()
    for p in parts:
        data = data.get(p)
    assert len(data) >= min_items

@then(parsers.parse("o corpo da resposta deve conter a mensagem de erro '{error_message}'"))
def then_error_message(error_message):
    data = test_context['response'].json()
    assert data.get("error", {}).get("message") == error_message
