import os
from dotenv import load_dotenv

# Tenta carregar o arquivo .env
carregou = load_dotenv()

print(f"--- DIAGNÓSTICO ---")
print(f"O arquivo .env foi encontrado? {'SIM' if carregou else 'NÃO'}")
print(f"Caminho atual onde o Python está rodando: {os.getcwd()}")
print(f"CLIENT_ID lido: {os.getenv('CLIENT_ID')}")
print(f"-------------------")