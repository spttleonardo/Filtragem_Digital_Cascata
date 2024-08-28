import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import math
from scipy.signal import lfilter, convolve

import PySimpleGUI as sg


def my_fft(sinal, fs):
    
    # Comprimento do sinal
    N = len(sinal)

    # Vetor de frequencia
    aux = np.arange(len(sinal))
    T = N/fs
    frequencia = aux/T

    S = np.fft.fft(sinal)/N

    # Frequencia positivas apenas
    fc = math.ceil(N/2)
    S = S[1:fc]
    frequencia = frequencia[1:fc]

    plt.plot(frequencia, abs(S))

    mplcursors.cursor(hover=True)
    
    #plt.subplot(1, 3, 3)
    plt.title('Analise de Espectro')
    plt.xlabel('Frequencia em Hz')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()


def lowpass(fc, M):

    # Calculando o parâmetro alpha
    alpha = (M-1)/2

    n = np.arange(M)

    m = n - alpha + np.finfo(float).eps  # eps é o valor mínimo representável que evita divisão por zero
    
    # Calculando a resposta do filtro ideal

    hd = np.sin(fc * m) / (np.pi * m)
    # Tratando o caso m = 0 para evitar divisão por zero
    hd[m == 0] = fc / np.pi
    
    return hd


def IIR_manual(dados, tempo, beta = 0.1):
    y = np.zeros(len(dados))

    for i in range(2,len(dados)):
        y[i] = beta*dados[i] + (1-beta)*y[i-1]

    plt.plot(tempo, y)

    mplcursors.cursor(hover=True)

    #plt.subplot(1, 3, 2)
    plt.title('Sinal filtrado com IIR manual')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.show()


def IIR_auto(dados, tempo, beta = 0.1):

    # Definindo os parâmetros
    beta = 0.1

    # Coeficientes do filtro
    num = [beta]
    den = [1, -(1 - beta)]

    # Aplicando o filtro
    filtrado = lfilter(num, den, dados)

    
    return filtrado


def main(path):
    # Importando dados
    df = pd.read_csv("Original Data.csv", sep=';')

    # Atribuindo dados das colunas sample e peso atual a variveis criadas
    amostras = df['Sample']
    dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)

    # Criando vetor de tempo
    tempo = np.arange(len(dados)) * 1e-3

    plt.subplot(3, 1, 1)
    plt.plot(tempo, dados)  # Adiciona marcadores de pontos

    mplcursors.cursor(hover=True)

    plt.title('Sinal Atual ao longo do tempo')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Peso Atual')
    plt.grid(True)
    #plt.show()

    # FFT
    #my_fft(dados, 1000)

    ### Iniciando projeto filtro

    #frequencia de amostragem
    fsamp = 1000

    ## Definiçoes do filtro
    fp = 35 # frequencia de passagem
    fs = 50 # frequencia de corte

    # normalizando em freq digital
    wpd = 2*np.pi*fp
    wsd = 2*np.pi*fs

    wp = wpd/fsamp # frequencia de passagem digital
    ws = wsd/fsamp # frequencia de corte digital

    # frequencia de transicao
    wt = ws - wp

    # frequencia de corte intermediaria
    #wc = (ws + wp)/2

    M = np.ceil((6.6*np.pi/wt))+1 #valor de 6.6 é tabelado para janela de hamming

    hd = lowpass(ws,M) # funcao sinc para passa baixa ideal

    # Aplicando a janela de Hamming
    w_hamm = np.hamming(M)
    h = hd * w_hamm

    dados_filtrado = convolve(dados, h)

    tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

    plt.subplot(3, 1, 2)
    plt.plot(tempo_filtrado, dados_filtrado)

    mplcursors.cursor(hover=True)

    plt.title('Sinal Filtrado com FIR automatico')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    #plt.show()

    # Filtro IIR first order manual
    beta = 0.05
    #IIR_manual(dados_filtrado, tempo_filtrado, beta)


    # Filtro IIR first order auto
    beta = 0.1
    filtrado = IIR_auto(dados_filtrado, tempo_filtrado, beta)


    window_size = 55
    window = np.ones(window_size)/window_size
    sinal_final = convolve(filtrado, window)

    tempo_final = np.arange(len(sinal_final)) *1e3

    plt.subplot(3, 1, 3)
    plt.plot(tempo_final, sinal_final)

    plt.legend()
    plt.title('Dados Filtrados e Média Móvel')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    mplcursors.cursor(hover=True)
    plt.show()



# Layout da janela
layout = [
    [sg.Text('Selecione um arquivo')],
    [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse('Procurar')],
    [sg.Button('Confirmar'), sg.Button('Cancelar')]
]

# Criação da janela
window = sg.Window('Seleção de Arquivo', layout)

# Loop de eventos
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    
    if event == 'Confirmar':
        arquivo_selecionado = values['-FILE-']
        if arquivo_selecionado:
            #sg.popup(f'Você selecionou o arquivo: {arquivo_selecionado}')
            main(arquivo_selecionado)
        else:
            sg.popup('Nenhum arquivo foi selecionado!')

# Fechando a janela
window.close()
