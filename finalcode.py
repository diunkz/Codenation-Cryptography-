import hashlib
import json
import requests
from string import ascii_lowercase as alfabeto

#cifra de césar
def cifraDeCesar(string, numeroDeCasas):
    palavra = ""
    for letra in string:
        if letra.isalpha():
            palavra = palavra + (alfabeto[(alfabeto.index(letra) - numeroDeCasas) % len(alfabeto)])
        else:
            palavra = palavra + letra
    return palavra

#request da url
token = "3f51fde9a767d0ec7c6ad2e00664d0f4bc5926bc"
url = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token="
req = requests.get(url+token)
dados = req.json()

#adicionando a cifra decifrada no dicionário
dados["decifrado"] = cifraDeCesar(dados["cifrado"], dados["numero_casas"])

#calculando sh1 e adicionando no dicionário
sh1_calculado = hashlib.sha1(dados["decifrado"].encode())
dados["resumo_criptografico"] = sh1_calculado.hexdigest()

#abrindo o arquivo para adicionar o novo json
with open('answer.json', 'w') as json_file:
    json.dump(dados,json_file)
    json_file.close()

#enviar com POST
urlpost = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token="+token
file = {"answer": open("answer.json", "rb")}
requests.post(urlpost, files=file)
print(req.status_code)
print(req.content)
