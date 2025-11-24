````markdown
# 🎵 Testes Acadêmicos - API Spotify

Projeto acadêmico para validação e testes automatizados dos endpoints da API do Spotify.

---

## 📋 Pré-requisitos

* **Python 3.10+** instalado.
* **Git** instalado.
* Credenciais do Spotify Developer (`Client ID` e `Client Secret`).

---

## 🚀 Instalação e Configuração (Windows)

### 1. Clonar o Repositório
```bash
git clone [https://github.com/VictorVahid/Testes-Academicos-API-Spotify.git](https://github.com/VictorVahid/Testes-Academicos-API-Spotify.git)
cd Testes-Academicos-API-Spotify
````

### 2\. Criar e Ativar Ambiente Virtual

```bash
python -m venv venv
.\venv\Scripts\activate
```

> Se aparecer `(venv)` no terminal, está correto.

### 3\. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4\. Configurar Credenciais (.env)

Crie um arquivo chamado `.env` na **raiz do projeto** e adicione suas chaves:

```ini
CLIENT_ID=sua_chave_client_id
CLIENT_SECRET=sua_chave_client_secret
```

-----

## 🧪 Como Rodar os Testes

### Validar Conexão (Teste de Ambiente)

Para garantir que a API está respondendo e as chaves estão corretas, execute:

```bash
pytest tests/test_conexao.py
```

✅ **Resultado Esperado:** 2 testes devem passar com sucesso.

### Rodar Todos os Testes

Para executar a bateria completa de testes já criados:

```bash
pytest
```
