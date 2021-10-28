

#importe as bibliotecas
import matplotlib.pyplot as plt
import time
import numpy as np
import sounddevice as sd
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    f=44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    def generateSin(freq, time, fs):
        n = time*fs #numero de pontos
        x = np.linspace(0.0, time, n)  # eixo do tempo
        s = np.sin(freq*x*2*np.pi)
        plt.figure()
        plt.plot(x,s)
        return (x, s)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
