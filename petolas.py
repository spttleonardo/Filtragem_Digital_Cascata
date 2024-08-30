# # # import PySimpleGUI as sg
# # # import matplotlib.pyplot as plt
# # # import numpy as np

# # # # Função para desenhar o gráfico no Canvas
# # # def draw_plot(canvas, fig):
# # #     figure_canvas_agg = sg.Canvas(fig.canvas)
# # #     figure_canvas_agg.draw()
# # #     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
# # #     return figure_canvas_agg

# # # # Função que cria o gráfico
# # # def create_plot():
# # #     # Exemplo de dados
# # #     x = np.linspace(0, 10, 100)
# # #     y = np.sin(x)
    
# # #     # Criando o gráfico com Matplotlib
# # #     fig, ax = plt.subplots()
# # #     ax.plot(x, y)
# # #     ax.set_title("Seno de X")
# # #     ax.set_xlabel("X")
# # #     ax.set_ylabel("Seno(X)")
    
# # #     return fig

# # # # Layout da janela
# # # layout = [
# # #     [sg.Text('Gráfico de Exemplo')],
# # #     [sg.Canvas(key='-CANVAS-')],
# # #     [sg.Button('Plotar Gráfico'), sg.Button('Sair')]
# # # ]

# # # # Criação da janela
# # # window = sg.Window('Plotando Gráfico no PySimpleGUI', layout, finalize=True)

# # # # Inicialização do Canvas
# # # fig_canvas_agg = None

# # # # Loop de eventos
# # # while True:
# # #     event, values = window.read()

# # #     if event == sg.WINDOW_CLOSED or event == 'Sair':
# # #         break
    
# # #     if event == 'Plotar Gráfico':
# # #         # Criar o gráfico
# # #         fig = create_plot()
        
# # #         # Se já houver um gráfico no canvas, removê-lo
# # #         if fig_canvas_agg:
# # #             fig_canvas_agg.get_tk_widget().forget()
        
# # #         # Desenhar o novo gráfico no Canvas
# # #         fig_canvas_agg = draw_plot(window['-CANVAS-'].TKCanvas, fig)

# # # # Fechando a janela
# # # window.close()
# # #!/usr/bin/env python
# # import PySimpleGUI as sg

# # import matplotlib
# # matplotlib.use('TkAgg')

# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # """
# # Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

# # Basic steps are:
# #  * Create a Canvas Element
# #  * Layout form
# #  * Display form (NON BLOCKING)
# #  * Draw plots onto convas
# #  * Display form (BLOCKING)
 
# #  Based on information from: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
# #  (Thank you Em-Bo & dirck)
# # """


# # #------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

# # import numpy as np
# # import matplotlib.pyplot as plt

# # from matplotlib.ticker import NullFormatter  # useful for `logit` scale

# # # Fixing random state for reproducibility
# # np.random.seed(19680801)

# # # make up some data in the interval ]0, 1[
# # y = np.random.normal(loc=0.5, scale=0.4, size=1000)
# # y = y[(y > 0) & (y < 1)]
# # y.sort()
# # x = np.arange(len(y))

# # # plot with various axes scales
# # plt.figure(1)

# # # linear
# # plt.subplot(221)
# # plt.plot(x, y)
# # plt.yscale('linear')
# # plt.title('linear')
# # plt.grid(True)


# # # log
# # plt.subplot(222)
# # plt.plot(x, y)
# # plt.yscale('log')
# # plt.title('log')
# # plt.grid(True)


# # # symmetric log
# # plt.subplot(223)
# # plt.plot(x, y - y.mean())
# # plt.yscale('symlog')
# # plt.title('symlog')
# # plt.grid(True)

# # # logit
# # plt.subplot(224)
# # plt.plot(x, y)
# # plt.yscale('logit')
# # plt.title('logit')
# # plt.grid(True)
# # plt.gca().yaxis.set_minor_formatter(NullFormatter())
# # plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
# #                     wspace=0.35)
# # fig = plt.gcf()      # if using Pyplot then get the figure from the plot
# # figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# # #------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# # #------------------------------- Beginning of Matplotlib helper code -----------------------


# # def draw_figure(canvas, figure, loc=(0, 0)):
# #     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
# #     figure_canvas_agg.draw()
# #     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
# #     return figure_canvas_agg

# # def delete_figure_agg(figure_agg):
# #     figure_agg.get_tk_widget().forget()
# #     plt.close('all')

# # #------------------------------- Beginning of GUI CODE -------------------------------

# # # define the window layout
# # layout = [[sg.Text('Plot test', font='Any 18')],
# #           [sg.Canvas(size=(figure_w, figure_h), key='canvas')],
# #           [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

# # # create the form and show it without the plot
# # window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True)

# # # add the plot to the window
# # fig_canvas_agg = draw_figure(window['canvas'].TKCanvas, fig)

# # event, values = window.read()
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import mplcursors
# import math
# from scipy.signal import lfilter, convolve
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import PySimpleGUI as sg

# def draw_plot(canvas, fig):
#     for widget in canvas.winfo_children():  # Limpa o canvas existente
#         widget.destroy()  
#     figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg

# def main(path, cv_width, cv_height):
#     # Importando dados
#     df = pd.read_csv(path, sep=';')

#     # Atribuindo dados das colunas sample e peso atual a variáveis criadas
#     amostras = df['Sample']
#     dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)

#     # Criando vetor de tempo
#     tempo = np.arange(len(dados)) * 1e-3

#     fig, ax = plt.subplots(3, 1, figsize=(cv_width/100, cv_height/100))  # Criando a figura e os eixos

#     ax[0].plot(tempo, dados)
#     ax[0].set_title('Sinal Atual ao longo do tempo')
#     ax[0].set_xlabel('Tempo(s)')
#     ax[0].set_ylabel('Peso Atual')
#     ax[0].grid(True)

#     # Filtro FIR
#     fsamp = 1000
#     fp = 35
#     fs = 50
#     wpd = 2 * np.pi * fp
#     wsd = 2 * np.pi * fs
#     wp = wpd / fsamp
#     ws = wsd / fsamp
#     wt = ws - wp
#     M = np.ceil((6.6 * np.pi / wt)) + 1
#     hd = 1#lowpass(ws, M)
#     w_hamm = np.hamming(M)
#     h = hd * w_hamm
#     dados_filtrado = convolve(dados, h)
#     tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3

#     ax[1].plot(tempo_filtrado, dados_filtrado)
#     ax[1].set_title('Sinal Filtrado com FIR automático')
#     ax[1].set_xlabel('Tempo(s)')
#     ax[1].set_ylabel('Amplitude')
#     ax[1].grid(True)

#     # Filtro IIR e Média Móvel
#     beta = 0.1
#     filtrado = 1#IIR_auto(dados_filtrado, tempo_filtrado, beta)
#     window_size = 55
#     window = np.ones(window_size) / window_size
#     sinal_final = convolve(filtrado, window)
#     tempo_final = np.arange(len(sinal_final)) * 1e-3

#     ax[2].plot(tempo_final, sinal_final)
#     ax[2].set_title('Dados Filtrados e Média Móvel')
#     ax[2].set_xlabel('Tempo (s)')
#     ax[2].set_ylabel('Amplitude')
#     ax[2].grid(True)

#     return fig  # Retornando o objeto Figure

# # Opções de filtro
# options = ["Filtro FIR", "Filtro IIR - primeira ordem", "Média Móvel"]
# cv_width = 700
# cv_height = 300
# col1 = sg.Column([
#     [sg.Text('Selecione um arquivo')],
#     [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse('Procurar')],
#     [sg.Text('Selecione uma opção:')],
#     [sg.Combo(options, key='-COMBO-', default_value='Selecione a Opção')],
#     [sg.Combo(options, key='-COMBO1-', default_value='Selecione a Opção')],
#     [sg.Combo(options, key='-COMBO2-', default_value='Selecione a Opção')],
#     [sg.Button('Confirmar'), sg.Button('Cancelar')],
#     [sg.Text('Peso [g]: ')],
#     [sg.Text(key='-CAMPO-', enable_events=True)]
# ])

# # Layout da janela
# layout = [
#     [col1, sg.Canvas(key='-CANVAS-', size=(cv_width, cv_height), pad=((500,0),(0,0)))]
# ]

# # Criação da janela
# window = sg.Window('Seleção de Arquivo', layout, finalize=True, size=(1200, 500), resizable=True)
# window.Maximize()
# canvas = window['-CANVAS-'].TKCanvas
# canvas.config(bg='lightblue')
# peso = 0

# # Loop de eventos
# while True:
#     event, values = window.read()

#     if event == sg.WINDOW_CLOSED or event == 'Cancelar':
#         break

#     if event == 'Confirmar':
#         opcao_selecionada = values['-COMBO-']
#         opcao_selecionada1 = values['-COMBO1-']
#         opcao_selecionada2 = values['-COMBO2-']
#         arquivo_selecionado = values['-FILE-']
#         if arquivo_selecionado and opcao_selecionada != 'Selecione a Opção':
#             fig = main(arquivo_selecionado, cv_width, cv_height)
#             fig_canvas_agg = draw_plot(canvas, fig)
#             peso = 280
#             window['-CAMPO-'].update(peso)
#         else:
#             sg.popup('Nenhum arquivo e/ou opção de filtro foi selecionado!')

# # Fechando a janela
# window.close()
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

    def figure_controller(self):
        if self.figure is None:
            self.figure = plt.figure()
            self.axes = self.figure.add_subplot(111)
            self.line, = self.axes.plot(self.data)
            self.axes.set_title("Example of a Matplotlib plot updating in PySimpleGUI")
        else:            
            self.line.set_ydata(self.data)
            self.axes.relim()
            self.axes.autoscale_view()

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
    N = len(sinal)
    aux = np.arange(len(sinal))
    T = N/fs
    frequencia = aux/T
    S = np.fft.fft(sinal)/N
    fc = math.ceil(N/2)
    S = S[1:fc]
    frequencia = frequencia[1:fc]
    plt.plot(frequencia, abs(S))
    mplcursors.cursor(hover=True)
    plt.title('Analise de Espectro')
    plt.xlabel('Frequencia em Hz')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def lowpass(fc, M):
    alpha = (M-1)/2
    n = np.arange(M)
    m = n - alpha + np.finfo(float).eps
    hd = np.sin(fc * m) / (np.pi * m)
    hd[m == 0] = fc / np.pi
    return hd

def IIR_manual(dados, tempo, beta = 0.1):
    y = np.zeros(len(dados))
    for i in range(2,len(dados)):
        y[i] = beta*dados[i] + (1-beta)*y[i-1]
    plt.plot(tempo, y)
    mplcursors.cursor(hover=True)
    plt.title('Sinal filtrado com IIR manual')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def IIR_auto(dados, beta):
    beta = 0.1
    num = [beta]
    den = [1, -(1 - beta)]
    filtrado = lfilter(num, den, dados)
    return filtrado

def main(path,opt1,opt2,opt3):
    df = pd.read_csv(path, sep=';')
    amostras = df['Sample']
    dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)
    tempo = np.arange(len(dados)) * 1e-3
    fig, ax = plt.subplots(4, 1, figsize=(10,8))
    ax[0].plot(tempo, dados)
    ax[0].set_title('Sinal Atual ao longo do tempo')
    ax[0].set_xlabel('Tempo(s)')
    ax[0].set_ylabel('Peso Atual')
    ax[0].grid(True)
    
    if opt1 != 'Selecione a Opção':
        if opt1 == 'Filtro FIR':
            h = filtro_fir()
            dados_filtrado = convolve(dados, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[1].plot(tempo_filtrado, dados_filtrado)
            ax[1].set_title('Sinal Filtrado com FIR automático')
            ax[1].set_xlabel('Tempo(s)')
            ax[1].set_ylabel('Amplitude')
            ax[1].grid(True)

        elif opt1 == 'Filtro IIR':
            beta = 0.1
            dados_filtrado = IIR_auto(dados,beta)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
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
            h = filtro_fir()
            dados_filtrado = convolve(dados_filtrado, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[2].plot(tempo_filtrado, dados_filtrado)
            ax[2].set_title('Sinal Filtrado com FIR automático')
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
            h = filtro_fir()
            dados_filtrado = convolve(dados_filtrado, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[3].plot(tempo_filtrado, dados_filtrado)
            ax[3].set_title('Sinal Filtrado com FIR automático')
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

    plt.tight_layout()
    return fig

layout = [
    [sg.Text('Sistema de Filtragem de Sinais', justification='center', font='Helvetica 20')],
    [sg.Text('Insira o path do arquivo:'), sg.Input(key='path', expand_x=True), sg.FileBrowse()],
    [sg.Text('Escolha o primeiro filtro:'),
     sg.Combo(['Selecione a Opção','Filtro FIR','Filtro IIR','Média Móvel'], key='opt1', default_value='Selecione a Opção', expand_x=True)],
    [sg.Text('Escolha o segundo filtro:'),
     sg.Combo(['Selecione a Opção','Filtro FIR','Filtro IIR','Média Móvel'], key='opt2', default_value='Selecione a Opção', expand_x=True)],
    [sg.Text('Escolha o terceiro filtro:'),
     sg.Combo(['Selecione a Opção','Filtro FIR','Filtro IIR','Média Móvel'], key='opt3', default_value='Selecione a Opção', expand_x=True)],
    [sg.Canvas(key='controls_cv')],
    [sg.Canvas(key='fig_cv', expand_x=True, expand_y=True)],
    [sg.Button('Confirmar', size=(10, 1), font='Helvetica 14'),
     sg.Exit(size=(10, 1), font='Helvetica 14')],
]

window = sg.Window('Sistema de Filtragem', layout, finalize=True, resizable=True)
window.Maximize()

canvas_elem = window['fig_cv']
canvas = canvas_elem.TKCanvas

updatable_plot = updateable_matplotlib_plot(canvas)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Confirmar':
        path = values['path']
        opt1 = values['opt1']
        opt2 = values['opt2']
        opt3 = values['opt3']
        fig = main(path, opt1, opt2, opt3)
        updatable_plot.plot(fig)

window.close()
