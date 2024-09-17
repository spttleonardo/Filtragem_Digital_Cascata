import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import math
from scipy.signal import lfilter, convolve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv

class UpdateableMatplotlibPlot:
    def __init__(self, canvas):
        self.fig_agg = None
        self.figure = None
        self.canvas = canvas

    def plot(self, figure):
        self.figure = figure
        self.figure_drawer()

    def figure_drawer(self):
        if self.fig_agg is not None:
            self.fig_agg.get_tk_widget().forget()
        self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas)
        self.fig_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.fig_agg.draw()

    def plot1(self, data):
        self.data = data
        self.figure_controller()
        self.figure_drawer()

    def figure_controller(self):
        if self.figure is None:
            self.figure = plt.figure(figsize=(10, 8))
            self.axes = self.figure.add_subplot(111)
            self.line, = self.axes.plot(self.data)
            self.axes.set_title("Example of a Matplotlib plot updating in Tkinter")
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

def IIR_manual(dados, tempo, beta=0.1):
    y = np.zeros(len(dados))
    for i in range(2, len(dados)):
        y[i] = beta * dados[i] + (1 - beta) * y[i-1]
    plt.plot(tempo, y)
    mplcursors.cursor(hover=True)
    plt.title('Sinal filtrado com IIR manual')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def IIR_auto(dados, beta):
    num = [beta]
    den = [1, -(1 - beta)]
    filtrado = lfilter(num, den, dados)
    return filtrado

def main(path, opt1, opt2, opt3):
    df = pd.read_csv(path, sep=';')
    contador = 0
    if opt1 != 'Selecione a Opção':
        contador += 1
    if opt2 != 'Selecione a Opção':
        contador += 1
    if opt3 != 'Selecione a Opção':
        contador += 1
    amostras = df['Sample']
    dados = df['Dados,PesoAtual[%DB1003,DBD2]'].str.replace(',', '.').astype(float)
    tempo = np.arange(len(dados)) * 1e-3
    fig, ax = plt.subplots(contador + 1, 1, figsize=(10, 8))

    ax[0].plot(tempo, dados)
    mplcursors.cursor(hover=True)
    ax[0].set_title('Sinal Atual ao longo do tempo')
    ax[0].set_ylabel('Peso Atual')
    ax[0].grid(True)

    if opt1 != 'Selecione a Opção':
        if opt1 == 'Filtro FIR':
            h = filtro_fir()
            dados_filtrado = convolve(dados, h)
            tempo_filtrado = np.arange(len(dados_filtrado)) * 1e-3
            ax[1].plot(tempo_filtrado, dados_filtrado)
            ax[1].set_title('Sinal Filtrado com FIR automático')
            ax[1].set_ylabel('Amplitude')
            ax[1].grid(True)

    ax[contador-1].set_xlabel('Tempo(s)')
    return fig, dados_filtrado

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def confirm_action():
    arquivo_selecionado = entry_file.get()
    opcao_selecionada = combo_opt1.get()
    opcao_selecionada1 = combo_opt2.get()
    opcao_selecionada2 = combo_opt3.get()

    if arquivo_selecionado and (opcao_selecionada != 'Selecione a Opção' or opcao_selecionada1 != 'Selecione a Opção' or opcao_selecionada2 != 'Selecione a Opção'):
        fig, dados = main(arquivo_selecionado, opcao_selecionada, opcao_selecionada1, opcao_selecionada2)
        janela.plot(fig)
        with open('filtrado.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(dados)
    else:
        messagebox.showerror("Erro", "Nenhum arquivo e/ou opção de filtro foi selecionado!")

def changeOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))
    
# # Criação da janela principal
# root = tk.Tk()
# root.title("Seleção de Arquivo")
# root.geometry("1500x1000")

# frame_left = tk.Frame(root)
# frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=50, pady=50)

# frame_right = tk.Frame(root)
# frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# label_file = tk.Label(frame_left, text="Selecione um arquivo:")
# label_file.pack(pady=5)
# entry_file = tk.Entry(frame_left, width=50)
# entry_file.pack(pady=5)
# btn_browse = tk.Button(frame_left, text="Procurar", command=browse_file)
# btn_browse.pack(pady=5)

# options = ["Filtro FIR", "Filtro IIR", "Média Móvel"]

# label_opt1 = tk.Label(frame_left, text="Filtro 1:")
# label_opt1.pack(side=tk.LEFT, pady=5)
# combo_opt1 = ttk.Combobox(frame_left, values=options, state="readonly")
# combo_opt1.set("Selecione a Opção")
# combo_opt1.pack(side=tk.LEFT, fill = tk.X, expand=True)


# label_1 = tk.Label(frame_left, text="")
# label_1.pack(pady=30)

# label_opt2 = tk.Label(frame_left, text="Selecione a Opção 2:")
# label_opt2.pack(side=tk.LEFT, pady=5)
# combo_opt2 = ttk.Combobox(frame_left, values=options, state="readonly")
# combo_opt2.set("Selecione a Opção")
# combo_opt2.pack(side=tk.LEFT, fill = tk.X, expand=True)


# label_opt3 = tk.Label(frame_left, text="Selecione a Opção 3:")
# label_opt3.pack(side=tk.LEFT, pady=5)
# combo_opt3 = ttk.Combobox(frame_left, values=options, state="readonly")
# combo_opt3.set("Selecione a Opção")
# combo_opt3.pack(side=tk.LEFT, fill = tk.X, expand=True)

# btn_confirm = tk.Button(frame_left, text="Confirmar", command=confirm_action)
# #changeOnHover(btn_confirm, "red", "yellow")
# btn_confirm.pack(pady=10)

# canvas = tk.Canvas(frame_right, bg="lightblue")
# canvas.pack(fill=tk.BOTH, expand=True)

# janela = UpdateableMatplotlibPlot(canvas)
# janela.plot1(np.zeros(1024))
# Criação da janela principal
root = tk.Tk()
root.title("Seleção de Arquivo")
root.geometry("1500x1000")

# Frame esquerdo
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=50, pady=50)

# Frame direito
frame_right = tk.Frame(root)
frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Label e Entry para seleção de arquivo
label_file = tk.Label(frame_left, text="Selecione um arquivo:")
label_file.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_file = tk.Entry(frame_left, width=50)
entry_file.grid(row=0, column=1, padx=5, pady=5, sticky="w")
btn_browse = tk.Button(frame_left, text="Procurar", command=browse_file)
btn_browse.grid(row=0, column=2, padx=5, pady=5)

# Opções para combobox
options = ["Filtro FIR", "Filtro IIR", "Média Móvel"]

style = ttk.Style()
style.configure('Custom.TCombobox',font=('Arial', 50), padding=15)

# Label e Combobox para Filtro 1
label_opt1 = tk.Label(frame_left, text="Filtro 1:", font=('Ubuntu Medium', 15))
label_opt1.grid(row=1, column=0, padx=5, pady=50, sticky="w")
combo_opt1 = ttk.Combobox(frame_left, values=options, state="readonly", style='Custom.TCombobox')
combo_opt1.set("Selecione a Opção")
combo_opt1.configure(font=('Arial', 12))
combo_opt1.grid(row=1, column=1, padx=0, pady=50, sticky="ew")

# Label e Combobox para Filtro 2
label_opt2 = tk.Label(frame_left, text="Filtro 2:")
label_opt2.grid(row=2, column=0, padx=5, pady=50, sticky="w")
combo_opt2 = ttk.Combobox(frame_left, values=options, state="readonly")
combo_opt2.set("Selecione a Opção")
combo_opt2.grid(row=2, column=1, padx=5, pady=50, sticky="ew")

# Label e Combobox para Filtro 3
label_opt3 = tk.Label(frame_left, text="Filtro 3:")
label_opt3.grid(row=3, column=0, padx=5, pady=50, sticky="w")
combo_opt3 = ttk.Combobox(frame_left, values=options, state="readonly")
combo_opt3.set("Selecione a Opção")
combo_opt3.grid(row=3, column=1, padx=5, pady=50, sticky="ew")

# Label adicional
# label_1 = tk.Label(frame_left, text="")
# label_1.grid(row=4, column=0, columnspan=3, pady=30)

# Botão de confirmação
btn_confirm = tk.Button(frame_left, text="Confirmar", command=confirm_action)
btn_confirm.grid(row=5, column=0, columnspan=3, pady=50)

# Canvas no frame direito
canvas = tk.Canvas(frame_right, bg="lightblue")
canvas.pack(fill=tk.BOTH, expand=True)

janela = UpdateableMatplotlibPlot(canvas)
janela.plot1(np.zeros(1024))

root.mainloop()
