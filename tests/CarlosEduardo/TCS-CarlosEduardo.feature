Feature: Testes de Endpoints de Busca Pública - Carlos Eduardo
    Como um sistema consumidor da API Spotify
    Eu quero validar a funcionalidade e o contrato de 5 endpoints públicos
    Para garantir a integridade dos dados de faixas, artistas e lançamentos.

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
    # 2. GET /playlists/{playlist_id}/tracks (Itens da Playlist) - Imagem 3
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
