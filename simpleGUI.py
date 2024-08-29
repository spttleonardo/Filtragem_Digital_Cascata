# import PySimpleGUI as sg

# # Layout da janela
# layout = [
#     [sg.Text('Selecione um arquivo')],
#     [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse('Procurar')],
#     [sg.Button('Confirmar'), sg.Button('Cancelar')]
# ]

# # Criação da janela
# window = sg.Window('Seleção de Arquivo', layout)

# # Loop de eventos
# while True:
#     event, values = window.read()

#     if event == sg.WINDOW_CLOSED or event == 'Cancelar':
#         break
    
#     if event == 'Confirmar':
#         arquivo_selecionado = values['-FILE-']
#         if arquivo_selecionado:
#             sg.popup(f'Você selecionou o arquivo: {arquivo_selecionado}')
            
#         else:
#             sg.popup('Nenhum arquivo foi selecionado!')

# # Fechando a janela
# window.close()
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class updateable_matplotlib_plot():
    def __init__(self, canvas) -> None:
        self.fig_agg = None 
        self.figure = None
        self.canvas = canvas

    def plot(self, data):
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
    def figure_drawer(self):
        if self.fig_agg is not None: self.fig_agg.get_tk_widget().forget()
        self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas.TKCanvas)
        self.fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.fig_agg.draw()

def getGUI():
    # All the stuff inside your window.
    layout = [  [sg.Canvas(size=(500,500), key='canvas')],
                [sg.Button('Update', key='update'), sg.Button('Close')] ]

    # Create the Window
    window = sg.Window('Updating a plot example....', layout)
    return window


if __name__ == '__main__':
    window = getGUI()
    #window.Maximize()
    spectraPlot = updateable_matplotlib_plot(window['canvas']) #what canvas are you plotting it on
    window.finalize() #show the window
    spectraPlot.plot(np.zeros(1024)) # plot an empty plot    
    while True:
        event, values = window.read()
        if event == "update":
             some_spectrum = np.random.random(1024) # data to be plotted
             spectraPlot.plot(some_spectrum) #plot the data           
        if event == sg.WIN_CLOSED or event == 'Close': break # if user closes window or clicks cancel

    window.close()