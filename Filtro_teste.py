import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import math
from scipy.signal import lfilter, convolve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

import PySimpleGUI as sg

def draw_plot(canvas, fig):
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

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
    df = pd.read_csv(path, sep=';')

    # Atribuindo dados das colunas sample e peso atual a variveis criadas
    amostras = df['Sample']
    dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)

    # Criando vetor de tempo
    tempo = np.arange(len(dados)) * 1e-3

    fig, ax = plt.subplots(3, 1, figsize=(10, 8))  # Criando a figura e os eixos

    ax[0].plot(tempo, dados)
    ax[0].set_title('Sinal Atual ao longo do tempo')
    ax[0].set_xlabel('Tempo(s)')
    ax[0].set_ylabel('Peso Atual')
    ax[0].grid(True)

    # Filtro FIR
    fsamp = 1000
    fp = 35
    fs = 50
    wpd = 2 * np.pi * fp
    wsd = 2 * np.pi * fs
    wp = wpd / fsamp
    ws = wsd / fsamp
    wt = ws - wp
    M = np.ceil((6.6 * np.pi / wt)) + 1
    hd = lowpass(ws, M)
    w_hamm = np.hamming(M)
    h = hd * w_hamm
    dados_filtrado = convolve(dados, h)
    tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

    ax[1].plot(tempo_filtrado, dados_filtrado)
    ax[1].set_title('Sinal Filtrado com FIR automatico')
    ax[1].set_xlabel('Tempo(s)')
    ax[1].set_ylabel('Amplitude')
    ax[1].grid(True)

    # Filtro IIR e Média Móvel
    beta = 0.1
    filtrado = IIR_auto(dados_filtrado, tempo_filtrado, beta)
    window_size = 55
    window = np.ones(window_size) / window_size
    sinal_final = convolve(filtrado, window)
    tempo_final = np.arange(len(sinal_final)) * 1e3

    ax[2].plot(tempo_final, sinal_final)
    ax[2].set_title('Dados Filtrados e Média Móvel')
    ax[2].set_xlabel('Tempo (s)')
    ax[2].set_ylabel('Amplitude')
    ax[2].grid(True)

    plt.tight_layout()
    return fig  # Retornando o objeto Figure


# Opções de filtro
options = ["Filtro FIR", "Filtro IIR - primeira ordem", "Média Móvel"]

# Layout da janela
layout = [
    [sg.Text('Selecione um arquivo')],
    [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse('Procurar')],
    [sg.Text('Selecione uma opção:')],
    [sg.Combo(options, key='-COMBO-', default_value='Selecione a Opção')],
    [sg.Combo(options, key='-COMBO1-', default_value='Selecione a Opção')],
    [sg.Combo(options, key='-COMBO2-', default_value='Selecione a Opção')],
    [sg.Button('Confirmar'), sg.Button('Cancelar')],
    [sg.Text('Peso [g]: ')],
    [sg.Text(key='-CAMPO-', enable_events=True)],
    [sg.Canvas(key='-CANVAS-')]
]

# Criação da janela
window = sg.Window('Seleção de Arquivo', layout, size=(1200, 700))
peso = 0
# Inicialização do Canvas
fig_canvas_agg = None

# Loop de eventos
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break

    if event == 'Confirmar':
        opcao_selecionada = values['-COMBO-']
        opcao_selecionada1 = values['-COMBO1-']
        opcao_selecionada2 = values['-COMBO2-']
        arquivo_selecionado = values['-FILE-']
        if arquivo_selecionado and opcao_selecionada != 'Selecione a Opção':
            #sg.popup(f'Você selecionou o arquivo: {arquivo_selecionado}')
            fig = main(arquivo_selecionado)
            # Se já houver um gráfico no canvas, removê-lo
            if fig_canvas_agg:
                fig_canvas_agg.get_tk_widget().forget()
            
            # Desenhar o novo gráfico no Canvas
            fig_canvas_agg = draw_plot(window['-CANVAS-'].TKCanvas, fig)

            peso = 280
            window['-CAMPO-'].update(peso)
        else:
            sg.popup('Nenhum arquivo e/ou opção de filtro foi selecionado!')

# Fechando a janela
window.close()
