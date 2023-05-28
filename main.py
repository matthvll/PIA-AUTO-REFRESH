from piapy import PiaVpn
import time
import requests
from rocketry import Rocketry
from rocketry.conds import every
app = Rocketry()

#Instanciando
vpn = PiaVpn()

#clr

#Criando regra de execução agendada
@app.task('every 10 mins', execution='main')
def Iniciar():
    refresh()


def obter_endereco_ip_publico():
    resposta = requests.get('https://api.ipify.org?format=json')
    dados = resposta.json()
    endereco_ip = dados['ip']
    return endereco_ip





#Função principal que é chamada a cada 10 minutos para obter um novo IP
def refresh():
    horario_atual = time.strftime("%H:%M:%S")
    print(f'{horario_atual} - Reiniciando o IP...')
    vpn.disconnect()
    time.sleep(10)
    vpn.connect()
    time.sleep(5)
    endereco_ip_publico = obter_endereco_ip_publico()
    horario_atual = time.strftime("%H:%M:%S")
    print(f'{horario_atual} - Seu IP atual é: {endereco_ip_publico}')



app.run()