import requests
import json

# Suas chaves do JsonBin (as mesmas do app)
JSONBIN_BIN_ID = "6ac9e66eac6210605a24aca3"
JSONBIN_API_KEY = "$2a$10$JDZzWPNr4Ih2SxcZmtLkIOJjdLf068P7pNndXwwyTV9ooHEvd6PgK"

def atualizar_lote():
    url_get = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
    headers = {
        "X-Master-Key": JSONBIN_API_KEY
    }
    
    # Busca os dados atuais da nuvem
    response = requests.get(url_get, headers=headers)
    if response.status_code == 200:
        record = response.json().get("record", {})
        numeros_status = record.get("numeros_status", {})
        compradores = record.get("compradores", {})
        
        # Marca de 4540 até 4739 como "Reservado"
        for num in range(4540, 4740):
            numeros_status[str(num)] = "Reservado"
            compradores[str(num)] = "Reserva em Lote (Admin)"
            
        # Salva de volta na nuvem
        url_put = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
        headers_put = {
            "Content-Type": "application/json",
            "X-Master-Key": JSONBIN_API_KEY
        }
        payload = {
            "numeros_status": numeros_status,
            "compradores": compradores
        }
        
        resp_put = requests.put(url_put, headers=headers_put, json=payload)
        if resp_put.status_code == 200:
            print("Sucesso! Os números de 4540 a 4739 foram marcados como reservados na nuvem.")
        else:
            print(f"Erro ao salvar: {resp_put.text}")
    else:
        print(f"Erro ao carregar dados: {response.text}")

if __name__ == "__main__":
    atualizar_lote()