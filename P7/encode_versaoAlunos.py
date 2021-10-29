import matplotlib.pyplot as plt
import time
import numpy as np
import sounddevice as sd
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
from suaBibSignal import signalMeu



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

lista_v = [697,770,852,941]
lista_h = [1209, 1336, 1477, 1633]

dict_decode = {
    1209 : {697:"1", 770:"4", 852:"7", 941:'X'},
    1336 : {697:"2", 770:"5", 852:"8", 941:"0"},
    1477 : {697:"3", 770:"6", 852:"9", 941:'#'}
}

dict_encode = {
    "1" : [1209,697],
    "2" : [1336, 697],
    "3" : [1477, 697],
    "4" : [1209, 770],
    "5" : [1336, 770],
    "6" : [1477, 770],
    "7" : [1209, 852],
    "8" : [1336, 852],
    "9" : [1477,852],
    "0" : [1209,941],
    "X" : [1336,941],
    "#" : [1477,941]
}

senoide=[]


def main():
    print("Inicializando encoder")

    new_signal = signalMeu()
    
    f=44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    duration = 4

    t=np.linspace(-duration/2, duration/2, duration*f)
    sd.default.samplerate = f
    sd.default.channels = 1
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    sin_dict = {}
    for k,v in dict_encode.items():
        t, y0 = new_signal.generateSin(v[0], gainX, duration, f)
        t, y1 = new_signal.generateSin(v[1], gainX, duration, f)
        tb = t
        sin_dict[k] = y0+y1
    
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #tb =
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    NUM = int(input("Digite um número de 0 a 9  "))
    while NUM > 9 or NUM<0:
        print("Number not valid")
        NUM = int(input("Digite um número de 0 a 9"))
    NUM = str(NUM)
    print("Gerando Tom referente ao símbolo : {}".format(NUM))

    plt.plot(tb, sin_dict[NUM])
    plt.xlim(-0, 0.01)

    new_signal.plotFFT(sin_dict[NUM], f)
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides

    
    #printe o grafico no tempo do sinal a ser reproduzido
    #reproduz o som
    sd.play(sin_dict[NUM], f)
    # # Exibe gráficos
    plt.show()
    # # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
