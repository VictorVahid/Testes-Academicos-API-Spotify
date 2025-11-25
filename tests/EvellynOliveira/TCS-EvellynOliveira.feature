Feature: Testes de Novos Endpoints Pública - Evellyn Oliveira
    Como um sistema consumidor da API Spotify
    Eu quero validar endpoints ainda não explorados nas outras suítes
    Para garantir a integridade dos dados de playlists, artistas, episódios, categorias e audiobook.

    # -----------------------------------------------------------
    # 1. GET /users/{user_id}/playlists (Playlists de um Usuário)
    # -----------------------------------------------------------
    Scenario: 1. Listar playlists do usuário oficial Spotify
        Given o ID do Usuario para playlists é "kmd6hxe6t0u7cpr9bwydco63h"
        When busco as playlists do usuario
        Then o status code deve ser 200
        And a lista 'items' não deve estar vazia
        And o primeiro item da lista deve ter o campo 'owner' preenchido

    # -----------------------------------------------------------
    # 2. GET /search?type=track (Busca de Faixas)
    # -----------------------------------------------------------
    Scenario: 2. Buscar por faixas específicas
        Given que busco pelo termo "Imagine"
        And defino o tipo de busca como "track"
        When executo a busca
        Then o status code deve ser 200
        And a resposta deve conter uma lista de 'tracks.items'
        And o primeiro item da lista deve ter o campo 'name' preenchido

    # -----------------------------------------------------------
    # 3. GET /episodes/{id} (Detalhes do Episódio)
    # -----------------------------------------------------------
    Scenario: 3. Validar detalhes de um episódio específico
        Given o ID do Episodio é "7bdLNlAk7PeHO7Dt1nXTW3"
        When busco o episodio
        Then o status code deve ser 200
        And o campo 'type' deve ser igual a 'episode'
        And o campo 'duration_ms' deve ser maior que 0

    # -----------------------------------------------------------
    # 4. GET /browse/categories (Listar Todas as Categorias)
    # -----------------------------------------------------------
    Scenario: 4. Listar categorias disponíveis no mercado US
        Given defino o país como "US"
        When busco a lista de categorias
        Then o status code deve ser 200
        And a lista 'categories.items' não deve estar vazia
        And cada item da lista deve possuir o campo 'name'

    # -----------------------------------------------------------
    # 5. GET /audiobooks/{id}/chapters (Capítulos de Audiobook)
    # -----------------------------------------------------------
    Scenario: 5. Listar capítulos de um audiobook
        Given o ID do Audiobook para capitulos é "7iHfbu1YPACw6oZPAFJtqe"
        When busco os capitulos do audiobook
        Then o status code deve ser 200
        And a lista 'items' não deve estar vazia
        And o primeiro item da lista deve ter o campo 'chapter_number' preenchido

    # -----------------------------------------------------------
    # 6. GET /search?type=show (Busca Detalhada de Show)
    # -----------------------------------------------------------
    Scenario: 6. Buscar o Flow Podcast com filtros avançados
        Given que busco pelo termo "flow"
        And defino o tipo de busca como "show"
        And defino include_external como "audio"
        When executo a busca detalhada
        Then o status code deve ser 200
        And a resposta deve conter uma lista de 'shows.items'
        And a lista 'shows.items' não deve estar vazia