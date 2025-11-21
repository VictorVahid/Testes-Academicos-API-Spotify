Feature: Testes de Endpoints de Busca Pública - Victor Vahid
    Como um sistema consumidor da API Spotify
    Eu quero validar a funcionalidade e o contrato de 5 endpoints públicos
    Para garantir a integridade dos dados de faixas, artistas e lançamentos.

    # -----------------------------------------------------------
    # 1. GET /v1/tracks/{id} (Buscar Faixa)
    # -----------------------------------------------------------
    Scenario: 1. Busca de uma Faixa Existente com sucesso
        Given o ID da Faixa é "3z8h0TU7ReDPLIbEnYhWZb"
        When eu busco a faixa
        Then o status code da resposta deve ser 200
        And o campo 'name' no corpo da resposta deve ser 'Bohemian Rhapsody'
        And o campo 'type' deve ser 'track'

    # -----------------------------------------------------------
    # 2. GET /v1/artists/{id}/albums (Buscar Álbuns de Artista)
    # -----------------------------------------------------------
    Scenario: 2. Busca de álbuns de um artista famoso
        Given o ID do Artista é "0oSGxfWSnnOXhD2fKuz2Gy"
        And o tipo de retorno desejado é "album"
        When eu busço os álbuns do artista
        Then o status code da resposta deve ser 200
        And a resposta deve conter uma lista de 'items'
        And o campo 'total' deve ser maior que 10

    # -----------------------------------------------------------
    # 3. GET /v1/search?type=artist (Buscar Artistas)
    # -----------------------------------------------------------
    Scenario: 3. Busca de artista por termo de pesquisa
        Given a query de busca é "Lady Gaga"
        And o tipo de busca é "artist"
        When eu faço uma busca
        Then o status code da resposta deve ser 200
        And a resposta deve conter um objeto 'artists'
        And a lista 'artists.items' não deve ser vazia

    # -----------------------------------------------------------
    # 4. GET /v1/browse/new-releases (Novos Lançamentos)
    # -----------------------------------------------------------
    Scenario: 4. Obter a lista de novos lançamentos no Brasil
        Given o mercado de busca é "BR"
        When eu busco os novos lançamentos
        Then o status code da resposta deve ser 200
        And a resposta deve conter um objeto 'albums'
        And a lista 'albums.items' deve ter pelo menos 1 item

    # -----------------------------------------------------------
    # 5. GET /v1/artists/{id} (Buscar Artista)
    # -----------------------------------------------------------
    Scenario: 5. Busca de um Artista Inexistente (Caso Negativo)
        Given o ID do Artista é "4aawyAB9vmqN3uQ7FjRGXX"
        When eu busco o artista
        Then o status code da resposta deve ser 404
        And o corpo da resposta deve conter a mensagem de erro 'Resource not found'

        # -----------------------------------------------------------
    # 6. GET /v1/shows/{id} (Buscar um Show/Podcast)
    # ID: 3d50QnF91JzN1T8oQyJ4fL (Exemplo de podcast)
    # -----------------------------------------------------------
    Scenario: 6. Busca de um Show/Podcast existente
    Given o ID do Show é "1GLSDdk9CDEwziGNIlnb8a"
    When eu busco o show
    Then o status code da resposta deve ser 200
    And o campo 'name' no corpo da resposta deve ser 'Podpah'
    And o campo 'type' deve ser 'show'