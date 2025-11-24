Feature: Testes de Endpoints do API_Spotify  - Marcelo Carvalho
    Como um sistema consumidor da API Spotify
    Eu tenho que validar a funcionalidade e o contrato de 5 endpoints públicos
    Para garantir a integridade dos dados de 
    Álbuns, Playlists e Faixas.

    # -----------------------------------------------------------
    # 1. GET /v1/albums/{id} (Buscar Álbum Completo)
    # Álbum: "GOLDEN" - Jungkook
    # -----------------------------------------------------------
    Scenario: 1. Validar dados do álbum GOLDEN
        Given o ID do Album como "5pSk3c3wVwnb2arb6ohCPU"
        When busco o album
        Then o status code deve ser 200
        And o campo 'name' deve ser igual a 'GOLDEN'
        And o campo 'release_date' deve ser igual a '2023-11-03'

    # -----------------------------------------------------------
    # 2. GET /v1/playlists/{id} (Buscar Playlist)
    # Playlist: "Spotify Web API Testing playlist" (Criada para testes de dev)
    # ID: 3cEYpjA9oz9GiPac4AsH4n
    # -----------------------------------------------------------
    Scenario: 2. Verificar se a playlist de Teste está ativa
        Given o ID da Playlist como "3cEYpjA9oz9GiPac4AsH4n"
        When busco a playlist
        Then o status code deve ser 200
        And a resposta deve ter o campo 'description'
        And o valor booleano de 'public' deve ser True

    # -----------------------------------------------------------
    # 3. GET /v1/tracks/{id}
    # Música: "Shape of You" - Ed Sheeran (ID fixo)
    # -----------------------------------------------------------
    Scenario: 3. Validar detalhes da faixa Shape of You
        Given o ID da Faixa como "7qiZfU4dY1lWllzX7mPBI3"
        When busco a faixa
        Then o status code deve ser 200
        And o campo 'name' deve ser igual a 'Shape of You'
        And o campo 'popularity' deve ser maior que 50.0

    # -----------------------------------------------------------
    # 4. GET /v1/artists/{id}/top-tracks (Top Músicas do Artista)
    # Artista: Ed Sheeran
    # -----------------------------------------------------------
    Scenario: 4. Buscar as músicas mais tocadas do Ed Sheeran
        Given o ID do Artista como "6eUKZXaKkcviH0Ku9w2n3V"
        And define o mercado como "US"
        When busco as top tracks
        Then o status code deve ser 200
        And a lista 'tracks' não deve estar vazia
        And a lista 'tracks' deve ter 3 itens

    # -----------------------------------------------------------
    # 5. GET /v1/playlists/{id} (Cenário Negativo)
    # -----------------------------------------------------------
    Scenario: 5. Tentar buscar uma playlist inexistente
        Given o ID da Playlist como "1111111111111111111111"
        When busco a playlist
        Then o status code deve ser 404