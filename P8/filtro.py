#!/usr/bin/env python3

# sudo pip install PeakUtils

import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal
from scipy import signal as sg

from funcoes_LPF import LPF

def generateSin(freq, amplitude, time, fs):
    n = time*fs
    x = np.linspace(0.0, time, n)
    s = amplitude*np.sin(freq*x*2*np.pi)
    return (x, s)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal)
    return(xf, yf[0:N//2])

def main():
    fs = 44100
    sd.default.samplerate = fs
    sd.default.channels = 1
    audio, samplerate = sf.read('camFis.wav')
    yAudio = audio[:,1]
    samplesAudio = len(yAudio)

#     sd.play(audio)
#     sd.wait()

    yfiltrado = LPF(yAudio,4000,fs)
    sd.play(yfiltrado)
    sd.wait()

    #####################
    # Normaliza audio
    #####################
    audioMax = np.max(np.abs(yAudio))
    yAudioNormalizado = yAudio/audioMax

    plt.figure("tempo")
    plt.plot(yAudioNormalizado)
    plt.grid()
    plt.title('audio')


    X, Y = calcFFT(yfiltrado, samplerate)
    plt.figure("Fourier Audio")
    plt.plot(X, np.abs(Y))
    plt.grid()
    plt.title('Oi Frequencia')

    #####################
    # Gera portadora
    #####################
    freqPortadora = 14000
    xPortadora, yPortadora = generateSin(freqPortadora, 1, samplesAudio/samplerate, samplerate)
    plt.figure("portadora")
    plt.title('Portadora')
    plt.plot(xPortadora[0:500], yPortadora[0:500])
    plt.grid()

    #####################
    # Gera sinal AM
    # AM-SC
    #####################
    yAM = yfiltrado * yPortadora
    plt.figure("AM")
    plt.title('AM')
    plt.plot(yAM[0:500])
    plt.grid()

    # Fourier mensagem
    XAM, YAM = calcFFT(yAM, samplerate)
    plt.figure("Fourier mensagem")
    plt.plot(XAM, np.abs(YAM))
    plt.grid()
    plt.title('msg Frequencia')

    #####################
    # Demodula sinal AM
    # AM-SC
    # via product detection e low pass filter
    # https://en.wikipedia.org/wiki/Product_detector
    #####################
    audioAM, audioAMFS = sf.read('oiModuladoAM.wav')
    yAMFile = audioAM[:,1]

    xPortadoraDemod, yPortadoraDemod = generateSin(freqPortadora, 1, len(yAMFile)/samplerate, samplerate)

    yDemod = yAMFile * yPortadoraDemod

    XAMDemod, YAMDemod = calcFFT(yDemod, samplerate)
    XAMDemodFiltrado, YAMDemodFiltrado = calcFFT(yDemodFiltrado, samplerate)
    plt.figure("Fourier mensagem demodulada")
    #plt.plot(XAMDemod, np.abs(YAMDemod))
    plt.plot(XAMDemodFiltrado, np.abs(YAMDemodFiltrado))
    plt.grid()
    plt.title('msg Frequencia')


    #####################
    # Reproduz audio
    #####################
    sd.play(yDemod, samplerate)

    #####################
    # Reproduz audio
    #####################
    sd.play(yDemodFiltrado, samplerate)

    ## Exibe gráficos
    plt.show()
    sd.wait()

    


if __name__ == "__main__":
    main()
