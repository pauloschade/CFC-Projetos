#!/usr/bin/env python3

# sudo pip install PeakUtils

import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal
from funcoes_LPF import LPF

def generateSin(freq, amplitude, time, fs):
    n = time*fs
    x = np.linspace(0.0, time, int(n))
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


    #####################
    # Normaliza audio
    #####################
    audioMax = np.max(np.abs(yAudio))
    yAudioNormalizado = yAudio/audioMax
    plt.figure("tempo")
    plt.plot(yAudioNormalizado)
    plt.grid()
    plt.title('Tricolor Normalizado')

    #####################
    # Filtra audio
    #####################
    yfiltrado = LPF(yAudioNormalizado,4000,fs)

    X, Y = calcFFT(yfiltrado, samplerate)

    plt.figure("Fourier Audio")
    plt.plot(X, np.abs(Y))
    plt.grid()
    plt.title('Tricolor Frequncia')
    #audio filtrado
    sd.play(yfiltrado)
    sd.wait()

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

    #audio + portadora
    sd.play(yAM)
    sd.wait()

    # Fourier mensagem
    XAM, YAM = calcFFT(yAM, samplerate)
    plt.figure("Fourier mensagem")
    plt.plot(XAM, np.abs(YAM))
    plt.grid()
    plt.title('msg Frequencia')


    #####################
    # Demodula sinal AM
    #####################

    yDemod = yAM * yPortadora
    yDemodFiltrado = LPF(yDemod,4000,fs)

    #audio demodulado
    sd.play(yDemodFiltrado)
    sd.wait()

    # Fourier demodulado
    XAMDemod, YAMDemod = calcFFT(yDemod, samplerate)
    XAMDemodFiltrado, YAMDemodFiltrado = calcFFT(yDemodFiltrado, samplerate)
    plt.figure("Fourier mensagem demodulada")
    plt.plot(XAMDemod, np.abs(YAMDemod), label="demodulado")
    plt.plot(XAMDemodFiltrado, np.abs(YAMDemodFiltrado),label="demodulado filtrado")
    plt.grid()
    plt.title('msg Frequencia')
    plt.legend()


    plt.show()

if __name__ == "__main__":
    main()
