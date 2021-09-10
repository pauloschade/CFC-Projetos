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
        # print(txBuffer)

        txSize = com1.tx.getStatus()

        size = len(txBuffer)

        full_packages = math.floor(size/114)
        remaining_bytes = size%114
        bytes_per_package = 114

        payload_size = []
        payload_list=[]
        for i in range (1, full_packages + 1):
            payload_list.append(txBuffer[(i-1)*bytes_per_package:i*bytes_per_package])
            payload_size.append((114).to_bytes(5, byteorder='big'))
        
        payload_list.append(txBuffer[size-remaining_bytes: size])
        payload_size.append((remaining_bytes).to_bytes(5, byteorder='big'))

        #HANDSHAKE
        handshake = True
        print("sending handshake...")
        while handshake:
            handshake_head = (1).to_bytes(10, byteorder='big')
            handshake_payload = (len(payload_list)).to_bytes(1, byteorder='big')
            handshake_eop = b'\xcc\xcc\xcc\xcc'
            handshake_package = handshake_head + handshake_payload + handshake_eop
            com1.sendData(handshake_package)
            rxBuffer, nRx = com1.getData(2)
            if rxBuffer != True:
                handshake = False
        print("handshake done")
        ##################################


        print("sending packages")
        print(len(payload_list))
        for i in range (len(payload_list)):

            package_number = (i).to_bytes(5, byteorder='big')

            package = package_number + payload_size[i] + payload_list[i] + b'\xcc\xcc\xcc\xcc'

            com1.sendData(package)

            response_head, a = com1.getData(10)
            reponse_payload_size= int.from_bytes(response_head, byteorder='big')
            response_payload, a = com1.getData(reponse_payload_size)
            response_eoc, a = com1.getData(4)

            if response_payload != b'\xBB': 
                break
            
        print("Data sent...")
        com1.sendData(np.asarray(txBuffer))

        total_size = 0
        for i in payload_list:
            total_size += len(i)

        print(size)
        print(total_size)





            
    
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
