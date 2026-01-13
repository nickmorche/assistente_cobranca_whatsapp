from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import tempfile

from assistente_cobranca_whatsapp.delay import (
    human_delay,
    heavy_delay,
    typing_delay
)

class WhatsAppBot:
    def __init__(self):
        options = webdriver.ChromeOptions()

        # profile_dir = tempfile.mkdtemp(prefix="whatsapp_profile_")
        # options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument(r"--user-data-dir=C:\Users\nickm\whatsapp_profile")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://web.whatsapp.com")

        print("Escaneie o QR Code do WhatsApp Web")
        heavy_delay()

    def abrir_conversa(self, telefone: str) -> None:
        self.driver.get(f"https://web.whatsapp.com/send?phone={telefone}")
        heavy_delay()

    def extrair_dados_mensagem(self, outer_html: str) -> dict:
        soup = BeautifulSoup(outer_html, "html.parser")

        # 1️⃣ Texto da mensagem
        texto_span = soup.select_one("span[data-testid='selectable-text']")
        texto = texto_span.get_text(strip=True) if texto_span else None

        # 2️⃣ Data / hora / remetente
        meta_div = soup.select_one("div.copyable-text[data-pre-plain-text]")
        raw_meta = meta_div["data-pre-plain-text"] if meta_div else None

        data_envio = None
        remetente = None

        if raw_meta:
            # Exemplo:
            # [11:35, 10/01/2026] Nicolas Lima Morche:
            raw_meta = raw_meta.strip()

            data_str = raw_meta.split("]")[0].replace("[", "")
            remetente = raw_meta.split("]")[1].replace(":", "").strip()

            data_envio = datetime.strptime(data_str, "%H:%M, %d/%m/%Y")

        # 3️⃣ Direção da mensagem (quem enviou)
        enviada_por_mim = "message-out" in outer_html
        direcao = "me" if enviada_por_mim else "contact"

        return {
            "texto": texto,
            "data_envio": data_envio,
            "remetente": remetente,
            "direcao": direcao,
        }

    def encontrou_comprovante(self) -> bool:
        human_delay()
        mensagens = self.driver.find_elements(By.CSS_SELECTOR, "div.message-in")

        for msg in mensagens[-10:]:
            if msg.find_elements(By.CSS_SELECTOR, "img"):
                return True
            if msg.find_elements(By.CSS_SELECTOR, "span[data-icon='document']"):
                return True
            
        return False
    
    def ultima_cobranca_mais_8h(self) -> bool:
        human_delay()
        mensagens = self.driver.find_elements(By.CSS_SELECTOR, "div.message-out")

        if not mensagens:
            return True
        
        ultima = mensagens[-2]
        outer_html = ultima.get_attribute('outerHTML')
        # print(ultima.get_attribute('outerHTML'))
        dados = self.extrair_dados_mensagem(outer_html)
        print(dados)
        # {'texto': 'Quando puder, por favor nos envie o comprovante.', 'data_envio': datetime.datetime(2026, 1, 10, 11, 35), 'remetente': 'Nicolas Lima Morche', 'direcao': 'me'}
        quit()

        # raw_data = ultima.find_element(
        #     By.CSS_SELECTOR,
        #     "span[data-pre-plain-text]"
        # )
        # #.get_attribute("data-pre-plain-text")
        # print(raw_data)

        data_str = raw_data.split("]")[0].replace("[", "")
        data_msg = datetime.strptime(data_str, "%H:%M, %d/%m/%Y")

        time.sleep(20)

        return datetime.now() - data_msg > timedelta(hours=8)
    
    def enviar_mensagem(self, texto: str) -> None:
        human_delay(0.5, 1.2)
        try:
            caixa = self.driver.find_element(
                By.XPATH,
                "//div[@contenteditable='true' and @data-tab='10']"
            )
        except:
            caixa = self.driver.find_element(
                By.XPATH,
                "//div[@contenteditable='true' and @aria-placeholder='Digite uma mensagem']"
            )

        caixa.click()
        human_delay(0.5, 1.2)

        for char in texto:
            caixa.send_keys(char)
            typing_delay(char)
        
        human_delay()
        caixa.send_keys(Keys.ENTER)
        heavy_delay()