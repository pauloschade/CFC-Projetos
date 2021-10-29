#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import time
import numpy as np
import sounddevice as sd
from scipy.fftpack import fft, fftshift
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import soundfile   as sf

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    new_signal = signalMeu()
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs=44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duration = 4


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera

    time.sleep(1)

   
   #faca um print informando que a gravacao foi inicializada



    numAmostras = duration * fs
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    for i in range(3):
        print("Recording in {}...".format(3-i))
        time.sleep(1)

    print("Recording...")

    recording = sd.rec(int(numAmostras), fs, 1, blocking='True')
    sd.wait()

    print("Audio recorded")

    wav.write("./audio.wav", fs, recording)

    audio, samplerate = sf.read('audio.wav')
    yAudio = audio
    samplesAudio = len(yAudio)
    sd.play(audio)
    sd.wait()
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t=np.linspace(-duration/2, duration/2, duration*fs)

    # plot do gravico  áudio vs tempo!
    plt.plot(t, yAudio)
    plt.grid()
    plt.title('Audio x tempo')
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    X,Y = new_signal.plotFFT(yAudio, samplerate)
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    import peakutils
    index = peakutils.indexes(np.abs(Y), thres=0.31, min_dist=20)
    print("index de picos {}" .format(index))
    for freq in X[index]:
        print("freq de pico sao {}" .format(freq))
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()
    

if __name__ == "__main__":
    main()
