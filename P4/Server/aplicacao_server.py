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
import os
import io
import PIL.Image as Image
from array import array
import math
from Server import Server

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "/dev/cu.usbmodem141201"                  # Windows(variacao de)

def bytes_to_img(bytes):
    image = Image.open(io.BytesIO(bytes))
    image.save('bytes.jpeg')

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        newServer = Server(com1)
        newServer.read_package()
        print("Message received")
        time.sleep(1.5)
        print("ready to receive")

        
        while not newServer.done:
            print(f"receiving {newServer.index} out of {newServer.rx_size}")
            newServer.read_package()
        bytes_to_img(newServer.rx_buffer)


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
