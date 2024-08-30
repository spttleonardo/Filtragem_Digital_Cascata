import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import math
from scipy.signal import lfilter, convolve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import PySimpleGUI as sg

class updateable_matplotlib_plot():
    def __init__(self, canvas) -> None:
        self.fig_agg = None 
        self.figure = None
        self.canvas = canvas

    def plot(self, figure):  # Agora a função aceita uma figura já criada
        self.figure = figure
        self.figure_drawer()

    # Desenha a figura no canvas
    def figure_drawer(self):
        if self.fig_agg is not None: 
            self.fig_agg.get_tk_widget().forget()
        self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas.TKCanvas)
        self.fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.fig_agg.draw()

    def plot1(self, data):
        self.data = data
        self.figure_controller()
        self.figure_drawer()

    #put all of your normal matplotlib stuff in here
    def figure_controller(self):
        #first run....
        if self.figure is None:
            self.figure = plt.figure()
            self.axes = self.figure.add_subplot(111)
            self.line, = self.axes.plot(self.data)
            self.axes.set_title("Example of a Matplotlib plot updating in PySimpleGUI")
        #all other runs
        else:            
            self.line.set_ydata(self.data)#update data            
            self.axes.relim() #scale the y scale
            self.axes.autoscale_view() #scale the y scale

    #finally draw the figure on a canvas
    # def figure_drawer(self):
    #     if self.fig_agg is not None: self.fig_agg.get_tk_widget().forget()
    #     self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas.TKCanvas)
    #     self.fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    #     self.fig_agg.draw()
def filtro_fir():
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

    return h
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
def IIR_auto(dados, beta):

    # Definindo os parâmetros
    beta = 0.1

    # Coeficientes do filtro
    num = [beta]
    den = [1, -(1 - beta)]

    # Aplicando o filtro
    filtrado = lfilter(num, den, dados)

    
    
    
    return filtrado
def main(path,opt1,opt2,opt3):#As opts ja vêm como string
    # Importando dados
    df = pd.read_csv(path, sep=';')

    # Atribuindo dados das colunas sample e peso atual a variveis criadas
    amostras = df['Sample']
    dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)

    # Criando vetor de tempo
    tempo = np.arange(len(dados)) * 1e-3

    fig, ax = plt.subplots(4, 1)#, figsize=(7,4))  # Criando a figura e os eixos

    ax[0].plot(tempo, dados)
    ax[0].set_title('Sinal Atual ao longo do tempo')
    ax[0].set_xlabel('Tempo(s)')
    ax[0].set_ylabel('Peso Atual')
    ax[0].grid(True)
    
    if opt1 != 'Selecione a Opção':
        if opt1 == 'Filtro FIR':
            # Filtro FIR
            h = filtro_fir()
            dados_filtrado = convolve(dados, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

            ax[1].plot(tempo_filtrado, dados_filtrado)
            ax[1].set_title('Sinal Filtrado com FIR automatico')
            ax[1].set_xlabel('Tempo(s)')
            ax[1].set_ylabel('Amplitude')
            ax[1].grid(True)
            #leo gay
            
        elif opt1 == 'Filtro IIR':
            beta = 0.1
            dados_filtrado = IIR_auto(dados,beta)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            print(len(dados_filtrado))
            print(type(dados_filtrado))
            print(dados_filtrado)
            ax[1].plot(tempo_filtrado, dados_filtrado)
            ax[1].set_title('Sinal Filtrado com IIR automático')
            ax[1].set_xlabel('Tempo(s)')
            ax[1].set_ylabel('Amplitude')
            ax[1].grid(True)
        elif opt1 == 'Média Móvel':
            window_size = 55
            window = np.ones(window_size) / window_size
            dados_filtrado = convolve(dados, window)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[1].plot(tempo_filtrado, dados_filtrado)
            ax[1].set_title('Sinal Filtrado com Média Móvel')
            ax[1].set_xlabel('Tempo(s)')
            ax[1].set_ylabel('Amplitude')
            ax[1].grid(True)

    if opt2 != 'Selecione a Opção':
        if opt2 == 'Filtro FIR':
            # Filtro FIR
            h = filtro_fir()
            dados_filtrado = convolve(dados_filtrado, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

            ax[2].plot(tempo_filtrado, dados_filtrado)
            ax[2].set_title('Sinal Filtrado com FIR automatico')
            ax[2].set_xlabel('Tempo(s)')
            ax[2].set_ylabel('Amplitude')
            ax[2].grid(True)
        elif opt2 == 'Filtro IIR':
            beta = 0.1
            dados_filtrado = IIR_auto(dados_filtrado,beta)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[2].plot(tempo_filtrado, dados_filtrado)
            ax[2].set_title('Sinal Filtrado com IIR automático')
            ax[2].set_xlabel('Tempo(s)')
            ax[2].set_ylabel('Amplitude')
            ax[2].grid(True)
        elif opt2 == 'Média Móvel':
            window_size = 55
            window = np.ones(window_size) / window_size
            dados_filtrado = convolve(dados_filtrado, window)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[2].plot(tempo_filtrado, dados_filtrado)
            ax[2].set_title('Sinal Filtrado com Média Móvel')
            ax[2].set_xlabel('Tempo(s)')
            ax[2].set_ylabel('Amplitude')
            ax[2].grid(True)

    if opt3 != 'Selecione a Opção':
        if opt3 == 'Filtro FIR':
            # Filtro FIR
            h = filtro_fir()
            dados_filtrado = convolve(dados_filtrado, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

            ax[3].plot(tempo_filtrado, dados_filtrado)
            ax[3].set_title('Sinal Filtrado com FIR automatico')
            ax[3].set_xlabel('Tempo(s)')
            ax[3].set_ylabel('Amplitude')
            ax[3].grid(True)
        elif opt3 == 'Filtro IIR':
            beta = 0.1
            dados_filtrado = IIR_auto(dados_filtrado,beta)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[3].plot(tempo_filtrado, dados_filtrado)
            ax[3].set_title('Sinal Filtrado com IIR automático')
            ax[3].set_xlabel('Tempo(s)')
            ax[3].set_ylabel('Amplitude')
            ax[3].grid(True)
        elif opt3 == 'Média Móvel':
            window_size = 55
            window = np.ones(window_size) / window_size
            dados_filtrado = convolve(dados_filtrado, window)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[3].plot(tempo_filtrado, dados_filtrado)
            ax[3].set_title('Sinal Filtrado com Média Móvel')
            ax[3].set_xlabel('Tempo(s)')
            ax[3].set_ylabel('Amplitude')
            ax[3].grid(True)
    

    return fig  # Retornando o objeto Figure

if __name__ == '__main__':
    # Opções de filtro
    options = ["Filtro FIR", "Filtro IIR", "Média Móvel"]
    cv_width = 800
    cv_height = 500
    col1 = sg.Column([
        [sg.Text('Selecione um arquivo')],
        [sg.Input(key='-FILE-', enable_events=True, expand_x=True), sg.FileBrowse('Procurar')],
        [sg.Text('Selecione uma opção:')],
        [sg.Combo(options, key='-COMBO-', default_value='Selecione a Opção', expand_x=True)],
        [sg.Combo(options, key='-COMBO1-', default_value='Selecione a Opção', expand_x=True)],
        [sg.Combo(options, key='-COMBO2-', default_value='Selecione a Opção', expand_x=True)],
        [sg.Button('Confirmar', expand_x=True), sg.Button('Cancelar', expand_x=True)],
        [sg.Text('Peso [g]: ')],
        [sg.Text(key='-CAMPO-', enable_events=True, expand_x=True)]
    ], expand_y=True, expand_x=True)
    col2 = [
        [sg.Canvas(key='-CANVAS-', size=(cv_width,cv_height), pad=((0,0),(0,0)))]
    ]
    # Layout da janela
    layout = [
        [col1,sg.VerticalSeparator(),sg.Column(col2, size=(800,500))]
    ]

    # Criação da janela
    window = sg.Window('Seleção de Arquivo', layout, finalize = True, size=(1200, 500),resizable=True)
    window.Maximize()
    canvas = window['-CANVAS-'].TKCanvas
    canvas.config(bg='lightblue')
    janela = updateable_matplotlib_plot(window['-CANVAS-']) #what canvas are you plotting it on
    window.finalize() #show the window
    janela.plot1(np.zeros(1024)) # plot an empty plot

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
            if arquivo_selecionado and (opcao_selecionada != 'Selecione a Opção' or opcao_selecionada1 != 'Selecione a Opção' or opcao_selecionada != 'Selecione a Opção'):
                #sg.popup(f'Você selecionou o arquivo: {arquivo_selecionado}')
                fig = main(arquivo_selecionado,opcao_selecionada,opcao_selecionada1,opcao_selecionada2)
                janela.plot(fig)
            else:
                sg.popup('Nenhum arquivo e/ou opção de filtro foi selecionado!')

    # Fechando a janela
    window.close()