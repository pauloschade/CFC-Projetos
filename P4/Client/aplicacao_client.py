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
from Client import Client
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports;
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem141101" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

def img_to_bytes(img):

    with open(img, "rb") as image:
        f = image.read()
        b = bytearray(f)
        return b

def bytes_to_img(bytes):
    image = Image.open(io.BytesIO(bytes))
    image.save('bytes.jpeg')



def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        # #SACRIFICE
        # ####################################
        # print("sending sacrifice...")
        # com1.sendData(b'\xcc\xcc')
        # print("Sacrifice bytes sent...")
        # ####################################

        print("Calculating")

        txBuffer = img_to_bytes("img.jpeg")

        newClient = Client(txBuffer, com1)
        print("Client Created")

        newClient.setup_packages()
        print("packages setup")

        while newClient.handshake:
            newClient.send_start_package()
            print("Start Package sent")
            newClient.receive_package()
            print("starting transmission...")

        while not newClient.done:
            print(f"sending {newClient.index + 1}")
            newClient.send_packages()
            time.sleep(0.1)
            newClient.receive_package()

        
        # print(txBuffer)





            
    
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
