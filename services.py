import requests
import sett
import json
import time



def obtener_Mensagem_whatsapp(message):
    if 'type' not in message :
        text = 'mensagem não reconhecida'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensagem não processada'

    
    return text

print(obtener_Mensagem_whatsapp)

def enviar_Mensagem_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("Enviado ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensagem enviado', 200
        else:
            return 'erro ao enviar mensagem', response.status_code
    except Exception as e:
        return e,403
    
def text_Mensagem(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Messagem(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Messagem(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opções",
                    "sections": [
                        {
                            "title": "Seções",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Messagem(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Messagem(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Messagem(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Messagem(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Mensagem(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensagem do usuário: ",text)

    markRead = markRead_Mensagem(messageId)
    list.append(markRead)
    time.sleep(2)

    if "oi" in text:
        body = "Olá 👋, seja bem vindo a Triar Contabiilidade, qual setor gostaria de entrar em contato?"
        footer = "Equipe Triar"
        options = ["Recepção", "RH","Fiscal","Financeiro","Contábil", "Cadastro e Legalização","Sistemas e Aplicativos"]

        listReply = listReply_Messagem(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Messagem(number, messageId, "🫡")

        list.append(replyReaction)
        list.append(listReply)
    
    elif "recepção" in text:
        body = "Quer falar com quem da recepção? "
        footer = "Equipe Recepção 👇"
        options = ["Ariane", "Larissa Trindade"]

        replyButtonData = buttonReply_Messagem(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData)

    elif "rh" in text:
        body = "Quer falar com quem do RH?"
        footer = "Equipe RH 👇"
        options = ["Sarah","Camila","Heloisa"]

        replyButtonData = buttonReply_Messagem(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)

    elif "fiscal" in text:
        body = "Quer falar com quem do fiscal? "
        footer = "Equipe Fiscal 👇"
        options = ["Aline","Rysssa","Polyana" ]

        buttonReply = buttonReply_Messagem(number, options, body, footer, "sed4",messageId)
        list.append(buttonReply)

    elif "contábil" in text :
        body = "Quer falar com quem do Contábil?"
        footer = "Equipe Contabil 👇"
        options = ["Pessoa1", "Pessoa2", "Pessoa3"]

        buttonReply = buttonReply_Messagem(number, options, body, footer, "sed5",messageId)
        list.append(buttonReply)

    elif "financeiro" in text:
        body = "Quer falar com quem do Financeiro?"
        footer = "Equipe Financeiro 👇"
        options = ["Pessoa1", "Pessoa2", "Pessoa3"]

        buttonReply = buttonReply_Messagem(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    
    elif "cadastro" in text or "legalização" in text:
        textMessage = text_Mensagem(number, "Cadastro e Legalização")
        list.append(textMessage)

    elif "sistema" in text or "aplicativo" in text:
        textMessage = text_Mensagem(number, "Sistemas e Aplicativos")
        list.append(textMessage)
        
    elif "não" in text or "obrigado" in text:
        textMessage = text_Mensagem(number,"Agradecemos o contato, caso precise de algo mais entre em contato. Tenha um bom dia. 👋")
        list.append(textMessage)
    
    else :
        data = text_Mensagem(number,"Não entendi sua pergunta")
        list.append(data)

    for item in list:
        enviar_Mensagem_whatsapp(item)
