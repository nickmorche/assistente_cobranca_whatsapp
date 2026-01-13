from assistente_cobranca_whatsapp.csv_repo import (
    carregar_contatos,
    salvar_contatos,
)
from assistente_cobranca_whatsapp.mensagens import MENSAGEM_COBRANCA
from assistente_cobranca_whatsapp.whatsapp import WhatsAppBot
from assistente_cobranca_whatsapp.delay import human_delay, typing_delay, heavy_delay


def main():
    contatos = carregar_contatos()
    bot = WhatsAppBot()

    for contato in contatos:
        if contato["pagou"]:
            print(f"✔ {contato['nome']} já pagou")
            continue

        print(f"🔍 Verificando {contato['nome']}")
        bot.abrir_conversa(contato["telefone"])

        if bot.encontrou_comprovante():
            print("💰 Comprovante encontrado → marcando como pago")
            contato["pagou"] = True
            salvar_contatos(contatos)
            continue

        if bot.ultima_cobranca_mais_8h():
            print("❌ Sem pagamento → enviando cobrança")
            bot.enviar_mensagem(MENSAGEM_COBRANCA)
        else:
            print("⏳ Ainda dentro do intervalo de 8h")

        heavy_delay()

    salvar_contatos(contatos)


        

if __name__ == "__main__":
    main()

# TODO: Criar um robô que verifique 24h por dia e adaptar python para fazer isto