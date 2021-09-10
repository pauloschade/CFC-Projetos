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

        # #SACRIFICE
        # ##################################
        # print("reception about to start...")
        # rxBuffer, nRx = com1.getData(2)
        # print("received sacrifice")
        # #################################

        #HANDSHAKE
        print("receiving handshake")
        handshake_head, nRx = com1.getData(10)
        handshake_payload_size = int.from_bytes(handshake_head, byteorder='big')
        print(handshake_payload_size)
        all_packages, nRx = com1.getData(handshake_payload_size)
        print(all_packages)
        eop, nRx = com1.getData(4)
        com1.sendData(b'\xBB\xBB')
        print("handshake done")
        ##################################

        print("setting up...")
        payloads_received = []
        all_packages = int.from_bytes(all_packages, byteorder='big')

        print(all_packages)
        
        print("receiving data...")

        com1.rx.clearBuffer()

        img_received = b''

        for i in range(all_packages):

            print("receiving payload {}" .format(i+1))

            number_bytes, nRx = com1.getData(5)

            number = int.from_bytes(number_bytes, byteorder='big')

            header_data, nRx = com1.getData(5)

            payload_size = int.from_bytes(header_data, byteorder='big')
            payload_data, nRx = com1.getData(payload_size)

            payloads_received.append(payload_data)
            img_received += payload_data
            EOC_data, nRx = com1.getData(4)


            if number != i or EOC_data !=  b'\xcc\xcc\xcc\xcc':
                print("error")
                head_error = (1).to_bytes(10, byteorder='big')
                payload_error = b'\xFF'
                eoc_error =  b'\xcc\xcc\xcc\xcc'
                com1.sendData(head_error + payload_error + eoc_error)
                break
            print("confirming receiption")
            head_success = (1).to_bytes(10, byteorder='big')
            payload_success = b'\xBB'
            eoc_success =  b'\xcc\xcc\xcc\xcc'
            com1.sendData(head_success + payload_success + eoc_success)

        bytes_to_img(img_received)

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
