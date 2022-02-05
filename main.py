import definicao
import datetime
from time import sleep
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import sqlite3
import io
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
app = Flask(__name__)


#GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN,
pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN,
pull_up_down = GPIO.PUD_DOWN)
 
print("Aperte o botão para iniciar o programa")
    
while True:
    if GPIO.input(16) == True:
        break
    

#CONFIGURAÇÃO ADS
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0) #MODO SILGLE-ENDED
#chan = AnalogIn(ads, ADS.P0, ADS.P1) MODO DIFERENCIAL
ads.mode = Mode.CONTINUOUS
ads.gain = 1


nova_medicao = 1
while nova_medicao == 1:
    
    #CONFIGURAÇÃO BANCO DE DADOS
    conn = sqlite3.connect('datalogger.db')
    cursor = conn.cursor()

    #FASE DE CONFIGURAÇÃO DO DATALOGGER
    print('FASE DE CONFIGURAÇÃO')
    dados = definicao.arquivo() #aqui configura o BD também
    unidade_de_medida = str(input('Digite a unidade de medida:  '))
    limites = definicao.valida(float(input("Digite o limite inferior: ")), float(input("Digite o limite superior: ")))
    print(f'O limite inferior é {limites[0]} {unidade_de_medida} e o limite superior {limites[1]} {unidade_de_medida}')
    escala_total = definicao.escala(limites[0], limites[1])
    print(f'A variação total do conversor é de {escala_total} {unidade_de_medida}')


    tipo_conversor = definicao.conversor(int(input('''Digite o número correspondente ao sensor utilizado
                [1] Tensão
                [2] Corrente (0-20mA)
                [3] Corrente (4-20mA)
                Sensor corresponde ao número:  ''')))
    print(f' {tipo_conversor[1]}')
    #print(f' {tipo_conversor[0]}') - número do tipo do conversor

    resolução = definicao.equivalente(escala_total, tipo_conversor[0])
    print(f'A resolução é de 1 para {resolução:.4f} {unidade_de_medida}')



    #aux = 0 # APENAS PARA TESTE (posteriormente colocar critérios de parada)
    

    # FAZER CONDIÇÃO DE PARADA -- BOTÃO BREAK OU ALGO ASSIM 
        
    while True:
        valor_real = definicao.conversão(limites[0], resolução, chan.value, tipo_conversor[0])
        #INSERIR DADOS DO SENSOR NO BANCO DE DADOS (SQLite)
        now = datetime.datetime.now()
        dia = now.day
        mes = now.month
        ano = now.year
        hora = now.hour
        minuto = now.minute
        segundo = now.second    
        #aux = aux + 1  
        data = (dia, mes, ano, hora, minuto, segundo, valor_real)
        cursor.execute("INSERT INTO "+dados+"(dia, mes, ano, hora, minuto,"
                        "segundo, dado) VALUES(?, ?, ?, ?, ?, ?, ?)",data)
        conn.commit()
        #print("Valor Convertido: {:.2f} --- Valor de tensão: {:.2f} V".format(dec, chan.voltage))
        #print(f'{dia}/{mes}/{ano} -- {hora}:{minuto}:{segundo} ---> {valor_real:.3f} {unidade_de_medida}')
        #print(f'Valor convertido ---> // {chan.value}  //  {valor_real:.3f} {unidade_de_medida}')
        print('Valor convertido ---> // {}  //  {:.3f} {}'.format(chan.value, valor_real, unidade_de_medida))    
        sleep(2)
        if GPIO.input(20) == True:
            break
       

    # CRIA UM BACKUP .sql DO BANCO DE DADOS ATUAL
    # ALTERAR ESSA PARTE COM A VALIDAÇÃO 'S' E 'N'  --> (se precisar)
    while True:
        backup = str(input('Deseja fazer backup dos dados? [S/N]: '))
        if backup in 'sS':   
            file_name = str(input('Digite o nome do arquivo de backup: '))
            file_name = file_name + '.sql'
            with io.open(file_name, 'w') as f:
                for linha in conn.iterdump():
                    f.write('%s\n' % linha)
            print('Backup realizado com sucesso!')
            break
        elif backup in 'nN':
            break 
        else:
            print('Resposta Inválida!')
    conn.close()
    
    
    while True:
        nova_medicao = input('Nova medição? [S/N]: ')
        if nova_medicao in 'Nn':
            nova_medicao = 0
            print('Programa Finalizado!')
            break
        elif nova_medicao in 'Ss':
            nova_medicao = 1
            break
        else:
            print('Resposta Inválida!')     

