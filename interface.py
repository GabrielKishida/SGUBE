import PySimpleGUI as sg

class TelaPython:
    def __init__(self):
        layout = [
            [sg.Text('SGUBE o seu amigo da Poli', font='Arial 24', text_color='white')],
            [sg.Button('Livros', size=(10,2)), sg.Button('Equipamentos', size=(10,2))]
        ]

        self.janela = sg.Window('Dados da Consulta').layout(layout)

    def Iniciar(self):
        while True:
            self.button, self.values = self.janela.Read()
            if(self.button == 'Livros'):
                layoutLivro = [
                [sg.Text('Consulte a disponibilidade de livros: ', font='Arial 16', text_color='white')],
                [sg.Input(size=(30,8), key='selectL'), sg.Button('Buscar', size=(10,2))],
                [sg.Output(size=(30,20))], 
                [sg.Button('Voltar', size=(10,2))]
                ]
                self.janelaLivro = sg.Window('Dados da Consulta').layout(layoutLivro)
                while True:
                    event, self.buttonL, self.valuesL = self.janelaLivro.Read()
                    selectL = self.valuesL['selectL']
                    if (self.buttonL == 'Voltar' or event == sg.WINDOW_CLOSED):
                        break
                    elif (self.buttonL == 'Buscar'):
                        print(selectL)

            if(self.button == 'Equipamentos'):
                layoutEquip = [
                [sg.Text('Consulte a disponibilidade de equipamentos: ', font='Arial 16', text_color='white')],
                [sg.Input(size=(30,8), key='selectE'), sg.Button('Buscar', size=(10,2))],
                [sg.Output(size=(30,20))], 
                [sg.Button('Voltar', size=(10,2))]
                ]
                self.janelaEquip = sg.Window('Dados da Consulta').layout(layoutEquip)
                while True:
                    event, self.buttonE, self.valuesE = self.janelaEquip.Read()
                    selectE = self.valuesE['selectE']
                    if (self.buttonE == 'Voltar' or event == sg.WINDOW_CLOSED):
                        break
                    elif (self.buttonL == 'Buscar'):
                        print(selectE)



tela = TelaPython()
tela.Iniciar()