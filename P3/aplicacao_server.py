#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random 

commands=[b'\x00'b'\xFF',b'\x00',b'\x0F',b'\xF0',b'\xFF'b'\x00',b'\xFF']

def random_command_list():
    commands_len = random.randint(10,30)
    commands_list = []
    for i in range(commands_len):
        command_number = random.randint(0,5)
        if command_number == (0 or 4):
            commands_list.append(b'\xAA')
        commands_list.append(commands[command_number])
    commands_list.append(b'\xBB')
    len_commands = len(commands_list)
    list_to_bytesArray = b''.join(commands_list)
    return list_to_bytesArray

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "/dev/cu.usbmodem14201"                  # Windows(variacao de)


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        com1.rx.clearBuffer()

        print("reception about to start...")
        rxBuffer, nRx = com1.getData(2)
        print("received sacrifice")
        com1.rx.clearBuffer()
        print("sending confirmation...")
        com1.sendData(b'\xcc\xcc')
        com1.rx.clearBuffer()

        print("receiving data...")

        receive = True
        received_bytes_list = []

        while receive:
            rxBuffer, nRx = com1.getData(1)
            print(rxBuffer)
            if rxBuffer ==  b'\xBB':
                receive = False
            elif rxBuffer == b'\xAA':
                rxBuffer, nRx = com1.getData(2)
                received_bytes_list.append(rxBuffer)
            else:
                received_bytes_list.append(rxBuffer)
        print(received_bytes_list)
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
