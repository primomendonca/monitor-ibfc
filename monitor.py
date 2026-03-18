import requests
from bs4 import BeautifulSoup
import os

# O GitHub puxa esses dados dos "Secrets" que você acabou de criar
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://concursos.ibfc.org.br/informacoes/476/"

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto})

def verificar():
    print("Iniciando verificação na nuvem...")
    try:
        # 1. Acessa o site
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Pega o conteúdo da página
        conteudo_atual = soup.get_text()

        # 3. Lê o último estado salvo no GitHub
        arquivo_nome = "ultimo_estado.txt"
        if os.path.exists(arquivo_nome):
            with open(arquivo_nome, "r", encoding="utf-8") as f:
                conteudo_antigo = f.read()
        else:
            conteudo_antigo = ""

        # 4. Compara
        if conteudo_atual != conteudo_antigo:
            print("Mudança detectada!")
            enviar_msg(f"🚀 ATUALIZAÇÃO IBFC!\nO site do concurso mudou.\nConfira: {URL}")
            # Salva o novo estado para a próxima vez
            with open(arquivo_nome, "w", encoding="utf-8") as f:
                f.write(conteudo_atual)
        else:
            print("Sem alterações.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verificar()
