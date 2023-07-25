from piapy import PiaVpn
import random
import time
import logging
import requests
logging.basicConfig(filename='logs', filemode='a', format='%(levelname)s - %(message)s')
logger=logging.getLogger() #Criando um objeto que salva todosos tipos de log
logger.setLevel(logging.DEBUG) 
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%H:%M:%S")
logger.info("Esta  é uma informação de logging")



def obter_endereco_ip_publico():
    resposta = requests.get('https://api.ipify.org?format=json')
    dados = resposta.json()
    endereco_ip = dados['ip']
    return endereco_ip



vpn =  PiaVpn() #Instanciando a VPN
status = vpn.status() #Checar status atual da PIAVPN
print("1 - Modo normal \n2 - Modo dinâmico")
chosen_mode = input("Escolha o modo de troca de IP: ")
input_minutos = int(input("Digite quantos minutos o programa deve fazer as alterações: "))
waiting_time = input_minutos * 60 #Variável usada para armazenar o valor em segundos que será passado posteriormente como parâmetro da biblioteca time
regions = ['us-vermont', 'us-maine', 'us-florida', 'us-atlanta', 'us-kentucky', 'us-baltimore', 'us-massachusetts','us-new-hampshire', 'us-south-carolina','us-east','us-tennessee','us-connecticut','us-wilmington', 'us-pennsylvania', 'us-alabama','us-virginia']
if status == 'Connected':
    vpn.disconnect()
    time.sleep(5)

while chosen_mode == "2":
    horario_atual = time.strftime("%H:%M:%S")
    print(f"{horario_atual} - Mudando localização...")
    time.sleep(1)
    chosen_region = random.choice(regions)
    horario_atual = time.strftime("%H:%M:%S")
    print(f'{horario_atual} - A região escolhida foi: ' + chosen_region)
    logging.info('A VPN FOI CONECTADA EM: ' + chosen_region)
    vpn.set_region(chosen_region)
    vpn.connect()
    status = vpn.status()
    if status == "Connected":
        horario_atual = time.strftime("%H:%M:%S")
        print(f"{horario_atual} - VPN CONECTADA")
        endereco_ip_publico = obter_endereco_ip_publico()
        horario_atual = time.strftime("%H:%M:%S")
        print(f"{horario_atual} - O IP atual é: {endereco_ip_publico}")
    time.sleep(waiting_time)
    horario_atual = time.strftime("%H:%M:%S")
    print(f"{horario_atual} - Aguardando {input_minutos} minutos até a próxima troca")
    vpn.disconnect()
    time.sleep(10)
    status = vpn.status()
    if status == "Disconnected":
        logging.info("A VPN FOI DESCONECTADA")
while chosen_mode == "1":
    horario_atual = time.strftime("%H:%M:%S")
    print(f"{horario_atual} - Mudando o IP...")
    vpn.disconnect()
    time.sleep(3)
    vpn.connect(timeout=20)
    status = vpn.status()
    if status == "Connected":
        horario_atual = time.strftime("%H:%M:%S")
        print(f"{horario_atual} - VPN CONECTADA")
        endereco_ip_publico = obter_endereco_ip_publico()
        print(f"{horario_atual} - O IP atual é: {endereco_ip_publico}")
        time.sleep(waiting_time)
    elif status == "Connecting":
        vpn.disconnect()
        time.sleep(5)
        vpn.connect(20)
        time.sleep(waiting_time)
    else:
        vpn.connect(timeout=30)
        horario_atual = time.strftime("%H:%M:%S")
        print(f"{horario_atual} - VPN CONECTADA")
        endereco_ip_publico = obter_endereco_ip_publico()
        print(f"{horario_atual} - O IP atual é: {endereco_ip_publico}")
        time.sleep(waiting_time)


