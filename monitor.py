import requests
from bs4 import BeautifulSoup
import os

# --- SEUS DADOS ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# --- LISTA DE SITES PARA MONITORAR ---
# Você pode adicionar quantos quiser aqui, seguindo o padrão abaixo
SITES = [
    {
        "nome": "IBFC - Concurso Principal",
        "url": "https://concursos.ibfc.org.br/informacoes/476/",
        "arquivo": "estado_ibfc.txt"
    },
    {
        "nome": "VUNESP - Outro Concurso",
        "url": "https://www.vunesp.com.br/",
        "arquivo": "estado_vunesp.txt"
    }
      {
        "nome": "IBADE - PC ES",
        "url": "https://portal.ibade.selecao.site/edital/ver/110",
        "arquivo": "estado_ibade.txt"
    }
 {
        "nome": "IDECAN",
        "url": "https://concurso.idecan.org.br/",
        "arquivo": "estado_idecan.txt"
    }
]

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto})

def verificar():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for site in SITES:
        print(f"Verificando {site['nome']}...")
        try:
            response = requests.get(site['url'], headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            conteudo_atual = soup.get_text()

            if os.path.exists(site['arquivo']):
                with open(site['arquivo'], "r", encoding="utf-8") as f:
                    conteudo_antigo = f.read()
            else:
                conteudo_antigo = ""

            if conteudo_atual != conteudo_antigo:
                print(f"Mudança detectada em {site['nome']}!")
                enviar_msg(f"🚀 ATUALIZAÇÃO: {site['nome']}\nConfira: {site['url']}")
                with open(site['arquivo'], "w", encoding="utf-8") as f:
                    f.write(conteudo_atual)
            else:
                print(f"Sem alterações em {site['nome']}.")

        except Exception as e:
            print(f"Erro ao verificar {site['nome']}: {e}")

if __name__ == "__main__":
    verificar()
