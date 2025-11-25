Feature: Testes de Endpoints Inéditos - Stefany
    Como a QA Stefany
    Quero validar endpoints de Categorias, Shows, Usuários e Artistas Relacionados
    Para garantir a cobertura de áreas não testadas anteriormente.

    # -----------------------------------------------------------
    # 1. GET /v1/browse/categories/{id} (Categorias)
    # Categoria: "Party" (Festas)
    # -----------------------------------------------------------
    Scenario: 1. Validar detalhes da categoria Party
        Given defino o ID da Categoria como "party"
        When busco a categoria
        Then o status code deve ser 200
        And o campo 'name' deve ser igual a 'Party'

   # -----------------------------------------------------------
    # 2. GET /v1/artists?ids={id1},{id2} (Buscar Vários Artistas)
    # Artistas: Coldplay e BTS
    # -----------------------------------------------------------
    Scenario: 2. Buscar dados de Coldplay e BTS ao mesmo tempo
        # Passamos os dois IDs separados por virgula
        Given defino os IDs dos Artistas como "4gzpq5DPGxESKxvKamJMIq,3Nrfpe0tUJi4Q4DXYqBpF3"
        When busco varios artistas
        Then o status code deve ser 200
        And a lista 'artists' deve ter 2 itens

    # -----------------------------------------------------------
    # 3. GET /v1/users/{user_id} (Perfil de Usuário)
    # Usuário: "spotify" (Perfil oficial do Spotify)
    # -----------------------------------------------------------
    Scenario: 3. Validar perfil oficial do Spotify
        Given defino o ID do Usuario como "spotify"
        When busco o usuario
        Then o status code deve ser 200
        And o campo 'type' deve ser igual a 'user'
        And o campo 'uri' deve ser igual a 'spotify:user:spotify'

   # -----------------------------------------------------------
    # 4. GET /v1/audiobooks/{id}
    # Audiobook: Dune
    # Mercado: US (Obrigatório para Audiobooks)
    # -----------------------------------------------------------
    Scenario: 4. Buscar Audiobook de Dune no mercado US
        Given defino o ID do Audiobook como "7iHfbu1YPACw6oZPAFJtqe"
        When busco o audiobook
        Then o status code deve ser 200
        And o campo 'name' deve ser igual a 'Dune: Book One in the Dune Chronicles'

    # -----------------------------------------------------------
    # 5. GET /v1/markets (Mercados Disponíveis)
    # Lista global de países
    # -----------------------------------------------------------
    Scenario: 5. Listar países onde o Spotify opera
        When busco os mercados disponiveis
        Then o status code deve ser 200
        And a lista 'markets' não deve estar vazia
        And a lista 'markets' deve ter 50 itens