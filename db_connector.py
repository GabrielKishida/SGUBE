#%% Imports
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import PySimpleGUI as sg

def geraInsert(dataFrame, entidade):
    insertions = []
    for c in range(len(dataFrame.index)):
        insertion = "INSERT INTO " + entidade + " ("
        for i, atributo in enumerate(dataFrame.columns):
            size = len(dataFrame.columns)
            if(i == size-1):
                insertion += str(atributo)
            else:
                insertion += str(atributo) + ","
        
        insertion += ") VALUES ("

        for j, atributo in enumerate(dataFrame.loc[c]):
            size = len(dataFrame.columns)
            if(j == size-1):
                insertion += "'" + str(atributo) + "'" 
            else:
                insertion += "'" + str(atributo) + "'" + ","
        
        insertion += ")"
        insertions.append(insertion)

    return insertions

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Interface:
    def __init__(self):
        self.layout = [
            [sg.Image(os.path.join(__location__, "sgube.png"), key='key1', size=(220, 190)), sg.Text('                 SGUBE' + '\n' '     O seu amigo na Poli!', font='Avenir 26', text_color='white')],
            [sg.Button('Equipamentos', size=(22,1), font='Avenir', button_color=('white', 'gray')), 
             sg.Button('Livros', size=(22,1), font='Avenir', button_color=('white', 'gray')), 
             sg.Button('Pessoas', size=(22,1), font='Avenir', button_color=('white', 'gray'))], 
            [sg.Output(size=(100,20))], 
            [sg.Button('Sair', size=(12,1), button_color=('white', 'gray'), font='Avenir 14', border_width=1)]
        ]

    def commit(self):
        self.con.commit()

    def connect(self):
        self.con = mysql.connector.connect(host='localhost',database='mydb',user='fabicom',password='mac0321')
        self.cursor = self.con.cursor()

    def insert(self, insertion):
        for insert in insertion:
            insercao_sql = insert
            self.cursor.execute(insercao_sql)

    def endConnection(self):
        if (self.con.is_connected()):
            self.con.close()
            self.cursor.close()
            print("Conexão ao MySQL encerrada")
 
    def make_win1(self):
        return sg.Window('SGUBE', self.layout, location=(800,600),size=(600, 530), finalize=True)

    def make_win(self, janela):
        if(janela == 'Equipamentos'):
            layout = [
            [sg.Text('Consulte a disponibilidade de Equipamentos: ', font='Arial 18', text_color='white')],
            [sg.Input(size=(50,20), key='selectE'), sg.Button('Buscar', size=(22,1))],
            [sg.Output(size=(100,20))], 
            [sg.Button('Sair', size=(10,2))]
            ]
            return sg.Window('Equipamento', layout, location=(800,600), finalize=True)

        elif(janela == 'Livros'):
            layout = [
            [sg.Text('Consulte a disponibilidade de Livros: ', font='Arial 18', text_color='white')],
            [sg.Input(size=(60,20), key='selectL'), sg.Button('Buscar', size=(22,1))],
            [sg.Output(size=(100,20))], 
            [sg.Button('Sair', size=(10,2))]
            ]
            return sg.Window('Livros', layout, location=(800,600), finalize=True)

        elif(janela == 'Pessoas'):
            layout = [
            [sg.Text('Consulte por um NUSP: ', font='Arial 18', text_color='white')],
            [sg.Input(size=(60,20), key='selectNusp')],
            [sg.Text('Consulte pelo Nome: ', font='Arial 18', text_color='white')],
            [sg.Input(size=(60,20), key='selectNome')],
            [sg.Button('Alunos', size=(22,1), font='Avenir', button_color=('white', 'gray')), 
             sg.Button('Professores', size=(22,1), font='Avenir', button_color=('white', 'gray')), 
             sg.Button('Funcionários', size=(22,1), font='Avenir', button_color=('white', 'gray'))], 
            [sg.Output(size=(100,20))],
            [sg.Button('Sair', size=(10,2))]
            ]
            return sg.Window('Pessoas', layout, location=(800,600), finalize=True)

    def iniciar(self):
        window1, window2 = self.make_win1(), None        
        while True:     
            window, self.button, self.values = sg.read_all_windows()
            if self.button == sg.WIN_CLOSED or self.button == 'Sair':
                window.close()
                if window == window2:       
                    window2 = None
                elif window == window1:  
                    if (self.con.is_connected()):
                        self.con.close()
                        self.cursor.close()
                    break
        
            elif self.button == 'Equipamentos' and not window2:
                window2 = self.make_win('Equipamentos')
                while True:
                    self.buttonE, self.valuesE = window2.Read()
                    if self.buttonE == 'Buscar':
                        selectE = self.valuesE['selectE']
                        try:
                            consulta_sql = "select * from tipoEquipamento, Equipamento where tipoEquipamento.idtipoEquipLab = Equipamento.tipoEquipamento_idtipoEquipLab AND " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()

                            for linha in linhas:
                                print("ID:", linha[0])
                                print("Nome:", linha[1])
                                print("Modelo:", linha[2])
                                print("Tipo:", linha[3], "\n")
                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)
                    elif self.buttonE == sg.WIN_CLOSED or self.buttonE == 'Sair':
                        break
                window2.close()
                window2 = None

            elif self.button == 'Livros' and not window2:
                window2 = self.make_win('Livros')
                while True:
                    self.buttonL, self.valuesL = window2.Read()
                    if self.buttonL == 'Buscar Aluno':
                        selectL = self.valuesL['selectL']
                        try:
                            consulta_sql = "select * from Livro where Livro.nome LIKE '%" + selectL + "%'"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()

                            for linha in linhas:
                                print("NUSP:", linha[0])
                                print("Área:", linha[1])
                                print("Ano de Ingresso:", linha[2])
                                print("Nome:", linha[3])
                                print("E-mail:", linha[4], "\n")
                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonL == 'Buscar':
                        try:
                            consulta_sql = "select * from Aluno"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()
 
                            for linha in linhas:
                                print("NUSP:", linha[0])
                                print("Área:", linha[1])
                                print("Ano de Ingresso:", linha[2])
                                print("Nome:", linha[3])
                                print("E-mail:", linha[4], "\n")
                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)
                    elif self.buttonL == sg.WIN_CLOSED or self.buttonL == 'Sair':
                        break
                window2.close()
                window2 = None
            
            elif self.button == 'Pessoas' and not window2:
                window2 = self.make_win('Pessoas')
                while True:
                    self.buttonP, self.valuesP = window2.Read()
                    if self.buttonP == 'Alunos':
                        selectNusp = self.valuesP['selectNusp']
                        selectNome = self.valuesP['selectNome']
                        try:

                            if(selectNusp != '' and selectNome == ''):
                                consulta_sql = "select * from Aluno where Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Área:", linha[1])
                                    print("Ano de Ingresso:", linha[2])
                                    print("Nome:", linha[3])
                                    print("E-mail:", linha[4], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                consulta_sql = "select * from Aluno where Aluno.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Área:", linha[1])
                                    print("Ano de Ingresso:", linha[2])
                                    print("Nome:", linha[3])
                                    print("E-mail:", linha[4], "\n")

                            elif(selectNusp != '' and selectNome != ''):
                                consulta_sql = "select * from Aluno where Aluno.nome LIKE '%" + selectNome + "%'" + "AND Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Área:", linha[1])
                                    print("Ano de Ingresso:", linha[2])
                                    print("Nome:", linha[3])
                                    print("E-mail:", linha[4], "\n")


                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonP == 'Professores':
                        selectNusp = self.valuesP['selectNusp']
                        selectNome = self.valuesP['selectNome']
                        try:

                            if(selectNusp != '' and selectNome == ''):
                                consulta_sql = "select * from Professor where Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Sala:", linha[1])
                                    print("Cargo:", linha[2])
                                    print("Departamento:", linha[3])
                                    print("Nome:", linha[4])
                                    print("E-mail:", linha[5])
                                    print("Telefone:", linha[6], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                consulta_sql = "select * from Professor where Professor.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Sala:", linha[1])
                                    print("Cargo:", linha[2])
                                    print("Departamento:", linha[3])
                                    print("Nome:", linha[4])
                                    print("E-mail:", linha[5])
                                    print("Telefone:", linha[6], "\n")

                            elif(selectNusp != '' and selectNome != ''):
                                consulta_sql = "select * from Professor where Professor.nome LIKE '%" + selectNome + "%'" + "AND Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Sala:", linha[1])
                                    print("Cargo:", linha[2])
                                    print("Departamento:", linha[3])
                                    print("Nome:", linha[4])
                                    print("E-mail:", linha[5])
                                    print("Telefone:", linha[6], "\n")

                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonP == 'Funcionários':
                        selectNusp = self.valuesP['selectNusp']
                        selectNome = self.valuesP['selectNome']
                        try:
                            if(selectNusp != '' and selectNome == ''):
                                consulta_sql = "select * from Funcionario where Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Função:", linha[1])
                                    print("Nome:", linha[2])
                                    print("E-mail:", linha[3])
                                    print("Telefone:", linha[4], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                consulta_sql = "select * from Funcionario where Funcionario.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Função:", linha[1])
                                    print("Nome:", linha[2])
                                    print("E-mail:", linha[3])
                                    print("Telefone:", linha[4], "\n")

                            elif(selectNusp != '' and selectNome != ''):
                                consulta_sql = "select * from Funcionario where Funcionario.nome LIKE '%" + selectNome + "%'" + "AND Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("NUSP:", linha[0])
                                    print("Função:", linha[1])
                                    print("Nome:", linha[2])
                                    print("E-mail:", linha[3])
                                    print("Telefone:", linha[4], "\n")
                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonP == sg.WIN_CLOSED or self.buttonP == 'Sair':
                        break
                window2.close()
                window2 = None

        window.close()
#%%
sg.theme('Black')

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

database = [pd.read_csv(os.path.join(__location__, "alunos.csv")),
            pd.read_csv(os.path.join(__location__, "Professor.csv")),
            pd.read_csv(os.path.join(__location__, "Trabalha_Em.csv")),
            pd.read_csv(os.path.join(__location__, "Responsavel_Por.csv")),
            pd.read_csv(os.path.join(__location__, "Livro.csv")),
            pd.read_csv(os.path.join(__location__, "Laboratorio.csv")),
            pd.read_csv(os.path.join(__location__, "Funcionario.csv")),
            pd.read_csv(os.path.join(__location__, "tipoEquipamento.csv")),
            pd.read_csv(os.path.join(__location__, "Equipamento.csv"))
]

entity = ["Aluno", "Professor", "Trabalha_Em", "Responsavel_Por", "Livro", "Laboratorio", "Funcionario", "tipoEquipamento", "Equipamento"]

tela = Interface()
tela.connect()
for i in range(len(entity)):
    tela.insert(geraInsert(database[i], entity[i]))
tela.iniciar()
#tela.commit()
#tela.endConnection()
