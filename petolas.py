import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

# Função para desenhar o gráfico no Canvas
def draw_plot(canvas, fig):
    figure_canvas_agg = sg.Canvas(fig.canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Função que cria o gráfico
def create_plot():
    # Exemplo de dados
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Criando o gráfico com Matplotlib
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Seno de X")
    ax.set_xlabel("X")
    ax.set_ylabel("Seno(X)")
    
    return fig

# Layout da janela
layout = [
    [sg.Text('Gráfico de Exemplo')],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Button('Plotar Gráfico'), sg.Button('Sair')]
]

# Criação da janela
window = sg.Window('Plotando Gráfico no PySimpleGUI', layout, finalize=True)

# Inicialização do Canvas
fig_canvas_agg = None

# Loop de eventos
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    
    if event == 'Plotar Gráfico':
        # Criar o gráfico
        fig = create_plot()
        
        # Se já houver um gráfico no canvas, removê-lo
        if fig_canvas_agg:
            fig_canvas_agg.get_tk_widget().forget()
        
        # Desenhar o novo gráfico no Canvas
        fig_canvas_agg = draw_plot(window['-CANVAS-'].TKCanvas, fig)

# Fechando a janela
window.close()