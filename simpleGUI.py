import PySimpleGUI as sg

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
            sg.popup(f'Você selecionou o arquivo: {arquivo_selecionado}')
            
        else:
            sg.popup('Nenhum arquivo foi selecionado!')

# Fechando a janela
window.close()
