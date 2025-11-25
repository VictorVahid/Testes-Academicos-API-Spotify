Feature: Testes de Endpoints de Busca Pública - Carlos Eduardo
    Como um sistema consumidor da API Spotify
    Eu quero validar a funcionalidade e o contrato de 6 endpoints públicos
    Para garantir a integridade dos dados de álbuns, playlists e podcasts.

    # -----------------------------------------------------------
    # 1. GET /v1/albums/{id}/tracks (Listar músicas do álbum)
    # -----------------------------------------------------------
    Scenario: 1. Lista todas as faixas existente dentro do álbum
        Given o ID do Album é "78sQV6OtO1w4eri7CNLzkt"
        When eu busco as faixas do álbum
        Then o status code da resposta deve ser 200
        And a resposta deve conter uma lista de 'items'
        And todas as faixas devem ter o campo 'type' igual a 'track'
        And cada item da lista deve possuir o campo 'name' preenchido
        And cada item da lista deve possuir o campo 'track_number' com um valor numérico

    # -----------------------------------------------------------
    # 2. GET /playlists/{playlist_id}/tracks (Itens da Playlist)
    # -----------------------------------------------------------
    Scenario: 2. Lista todas as faixas de uma playlist
        Given o ID da Playlist é "4WDx8GQVfJL1sV3fEYUQwZ"
        When eu busco as faixas da playlist
        Then o status code da resposta deve ser 200
        And a resposta deve conter uma lista de 'items'
        And o primeiro item da lista deve ter o campo 'added_at' preenchido

    # -----------------------------------------------------------
    # 3. GET /shows/{id}/episodes (Listar episódios de um show)
    # -----------------------------------------------------------
    Scenario: 1. Consulta episódios de um podcast específico
        Given o ID do Show é "3V5LBozjo4vNg2oJoA4Wb2"
        And defino o parâmetro de query 'limit' como 10
        When eu busco os episódios do show
        Then o status code da resposta deve ser 200
        And a resposta deve conter uma lista de 'items'
        And todos os itens da lista devem ter o campo 'type' igual a 'episode'
        And cada item da lista deve possuir o campo 'duration_ms'
        And cada item da lista deve possuir o campo 'release_date'
        And o primeiro item da lista deve ter o campo 'description' preenchido

    # -----------------------------------------------------------
    # 4. GET /albums (Listar vários álbuns por ID)
    # -----------------------------------------------------------
    Scenario: 4. Consulta informações de vários álbuns simultaneamente
        # IDs de exemplo: Queens of the Stone Age e Beyoncé
        Given defino o parâmetro de query 'ids' como "382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo"
        When eu busco múltiplos álbuns
        Then o status code da resposta deve ser 200
        And a resposta deve conter uma lista de 'albums'
        And todos os itens da lista devem ter o campo 'type' igual a 'album'
        And cada item da lista deve possuir o campo 'total_tracks' com um valor numérico

    # -----------------------------------------------------------
    # 5. GET /albums/{id} (Cenário de Erro - Não Encontrado)
    # -----------------------------------------------------------
    Scenario: 5. Valida retorno 404 ao buscar um álbum inexistente
        # Usamos um ID com formato válido (22 caracteres) mas que não existe
        Given o ID do Album é "0000000000000000000000"
        When eu busco os detalhes do álbum
        Then o status code da resposta deve ser 404

    # -----------------------------------------------------------
    # 6. GET /playlists/{playlist_id} (Cenário de Erro - Não Encontrado)
    # -----------------------------------------------------------
    Scenario: 6. Valida retorno 404 ao buscar uma playlist inexistente
        # ID fictício com formato válido (Base62)
        Given o ID da Playlist é "0000000000000000000000"
        When eu busco os detalhes da playlist
        Then o status code da resposta deve ser 404
