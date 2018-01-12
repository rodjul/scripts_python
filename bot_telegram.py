#!/usr/bin/env python3

import time
import requests
import os

print("Usando bot do telegram")

TOKEN = ""
URL   = "https://api.telegram.org/bot"


def getUpdate():
	print("Obtendo ultimas interacoes")
	return requests.get(URL+TOKEN+"/getUpdates").json()
	
def getWhoChatWithMe(response):
	length = len(response['result'])
	id_user = response['result'][length-1]['message']['chat']['id']
	first_name = response['result'][length-1]['message']['chat']['first_name']
	text = response['result'][length-1]['message']['text']
	update_id = response['result'][length-1]['update_id']
	return (id_user, first_name, text, update_id)


def sendMessage(chat_id, text):
	print("Enviando mensagem")
	requests.post(URL+TOKEN+"/sendMessage?chat_id="+str(chat_id)+"&text="+text)

def sendCommand(id_user,command):
	print("%d - Comando usado: %s" %(id_user,command))
	os.system(command)


def main():
	CONTROLE_CHAT = 0
	while True:

		getUpd = getUpdate()

		(id_user, first_name, text, update_id) = getWhoChatWithMe(getUpd)

		#condicao pra que quando o servidor for iniciado, nao obtenha o ultimo id obtido e envie a iteracao pro usuario
		if CONTROLE_CHAT == 0: CONTROLE_CHAT = update_id

		if not CONTROLE_CHAT == update_id:
			CONTROLE_CHAT = update_id
			
			if text == "/example":
				sendMessage(id_user,"Ola "+first_name+"! Essa é uma funcao teste")
			if text == "/help":
				sendMessage(id_user,"/example - funcao que retorna uma string teste\n")
			if text == "/loop":
				while True:
					getUpd = getUpdate()
					(id_user, first_name, text, update_id) = getWhoChatWithMe(getUpd)
					if text == "STOP":
						break
					sendMessage(id_user,"¯\_(ツ)_/¯ "+first_name + " ¯\_(ツ)_/¯")

			if text.startswith("/command"):
				command = text.split(" ")[1:]
				command = " ".join(command) #colocando espacos entre as palavras obs:strip() tira os espacos do inicio e fim
				sendCommand(id_user,command)
	
	#length = len(getUpd['result'])
	#print(getUpd['result'][length-1]['message']['chat']['id'])

	#time.sleep(3)


main()

