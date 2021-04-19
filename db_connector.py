#%% Imports
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import PySimpleGUI as sg

class Interface:
    def __init__(self):
        self.layout = [
            [sg.Text('SGUBE' + '\n' 'O seu amigo na Poli!', font='Avenir 24', text_color='white')],
            [sg.Button('Professores', size=(12,1), font='Avenir'), sg.Button('Equipamentos', size=(12,1), font='Avenir')], 
            [sg.Output(size=(30,20)), sg.Button('Consulta', size=(10,2))], 
            [sg.Button('Sair', size=(10,2))]
        ]

    def commit(self):
        self.con.commit()

    def connect(self):
        self.con = mysql.connector.connect(host='localhost',database='mydb',user='fabicom',password='mac0321')
        self.cursor = self.con.cursor()

    def insert(self):
        insert_aluno = ["INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('12345678','Computação','2019','Michael Jackson','mjj@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('12478955','Mecânica','2016','Arthur Gabriel','arthurgabriel@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('45612844','Mecânica','2017','Davi Luiz Arlindo','davi.arlindo@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('58475687','Mecânica','2019','Vitor Hugo Seichas','vitorhugoseichas@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('65878445','Computação','2020','João Pedro Henrique','joaopedrohenrique@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('92054548','Computação','2020','João Pedro Cardoso','joaopedrocardoso@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('5641547','Elétrica','2018','João Pedro Zucci','joaozucci@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('23645878','Elétrica','2018','Flávio Ciparrone','alunopreparado@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('1064587','Elétrica','2019','Luiz Otávio de Souza','luizotavio.souza@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('77845848','Produção','2019','Pedro Henrique Juissen','pedrojuissen@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('65848788','Produção','2018','João Guilherme Negueba','joaonegueba@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('68549874','Produção','2020','Ana Luiza Maracujá','ana.maracuja@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('54517084','Civil','2021','Maria Helena Nogueira Torres','marianogueira.torres@usp.br')",
        "INSERT INTO Aluno (nusp, area, ano_ingresso, nome, email) VALUES ('65874448','Civil','2018','Benedita Alvarenga de Luzia','benedita.luzia@usp.br')"]
        for insert in insert_aluno:
            insercao_sql = insert
            self.cursor.execute(insercao_sql)
        insercao_sql = "INSERT INTO Professor (nusp, sala, cargo, departamento, nome, email, telefone) VALUES ('9876543','C250', 'professor titular','PCS', 'Tobias', 'tobias@usp.br', '41989898998')"
        self.cursor.execute(insercao_sql)


    def endConnection(self):
        if (self.con.is_connected()):
            self.con.close()
            self.cursor.close()
            print("Conexão ao MySQL encerrada")
 
    def make_win1(self):
        return sg.Window('SGUBE', self.layout, location=(800,600), finalize=True)

    def make_win(self, janela):
        if(janela == 'Professores'):
            layout = [
            [sg.Text('Consulte a disponibilidade de livros: ', font='Arial 16', text_color='white')],
            [sg.Input(size=(30,8), key='selectL'), sg.Button('Buscar', size=(10,2))],
            [sg.Output(size=(30,20))], 
            [sg.Button('Sair', size=(10,2))]
            ]
            return sg.Window('Consulta', layout, location=(800,600), finalize=True)

        elif(janela == 'Equipamentos'):
            layout = [
            [sg.Text('Consulte a disponibilidade de equipamentos: ', font='Arial 16', text_color='white')],
            [sg.Input(size=(30,10), key='selectL')],
            [sg.Button('Buscar', size=(10,2)), sg.Button('Buscar Aluno', size=(10,2))],
            [sg.Output(size=(30,20))], 
            [sg.Button('Sair', size=(10,2))]
            ]
            return sg.Window('Second Window', layout, location=(800,600), finalize=True)

    def iniciar(self):
        window1, window2 = self.make_win1(), None        # start off with 1 window open
        while True:     
            window, self.button, self.values = sg.read_all_windows()
            if self.button == sg.WIN_CLOSED or self.button == 'Sair':
                window.close()
                if window == window2:       # if closing win 2, mark as closed
                    window2 = None
                elif window == window1:     # if closing win 1, exit program
                    if (self.con.is_connected()):
                        self.con.close()
                        self.cursor.close()
                        #print("Conexão ao MySQL encerrada")
                    break

            elif(self.button == 'Consulta'):
                try:
                    consulta_sql = "select * from Aluno where Aluno.nome LIKE '%Ciparrone'"
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
        
            elif self.button == 'Professores' and not window2:
                window2 = self.make_win('Professores')
                while True:
                    self.buttonL, self.valuesL = window2.Read()
                    if self.buttonL == 'Buscar':
                        try:
                            consulta_sql = "select * from Aluno"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()
                            #print(linhas)
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

            elif self.button == 'Equipamentos' and not window2:
                window2 = self.make_win('Equipamentos')
                while True:
                    self.buttonL, self.valuesL = window2.Read()
                    if self.buttonL == 'Buscar Aluno':
                        selectL = self.valuesL['selectL']
                        try:
                            consulta_sql = "select * from Aluno where Aluno.nome LIKE '%" + selectL + "%'"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()
                            #print(linhas)
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
                            #print(linhas)
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

        window.close()

    # def iniciar(self):
    #     while True:
    #         self.button, self.values = self.janela.Read()
    #         if(self.button == 'Consulta' ):
    #             try:
    #                 consulta_sql = "select * from Aluno"
    #                 self.cursor.execute(consulta_sql)
    #                 linhas = self.cursor.fetchall()
    #                 #print(linhas)
    #                 for linha in linhas:
    #                     print("NUSP:", linha[0])
    #                     print("Área:", linha[1])
    #                     print("Ano de Ingresso:", linha[2])
    #                     print("Nome:", linha[3])
    #                     print("E-mail:", linha[4], "\n")
    #             except Error as e:
    #                 print("Erro ao acessar tabela MySQL", e)
            
    #         elif(self.button == 'Sair' ):
    #             if (self.con.is_connected()):
    #                 self.con.close()
    #                 self.cursor.close()
    #                 #print("Conexão ao MySQL encerrada")
    #             break

            # if(self.button == 'Professores'):
            #     layoutLivro = [
            #     [sg.Text('Consulte a disponibilidade de livros: ', font='Arial 16', text_color='white')],
            #     [sg.Input(size=(30,8), key='selectL'), sg.Button('Buscar', size=(10,2))],
            #     [sg.Output(size=(30,20))], 
            #     [sg.Button('Voltar', size=(10,2))]
            #     ]
            #     self.janelaLivro = sg.Window('Dados da Consulta').layout(layoutLivro)
            #     while True:
            #         self.buttonL, self.valuesL = self.janelaLivro.Read()
            #         selectL = self.valuesL['selectL']
            #         if (self.buttonL == 'Voltar'):
            #             self.janelaLivro.Close()
            #             self.janela.Clear()
            #             self.janela = sg.Window('Dados da Consulta').layout(self.layout)
            #             break
            #         elif (self.buttonL == 'Buscar'):
            #             print(selectL)

            # if(self.button == 'Equipamentos'):
            #     layoutEquip = [
            #     [sg.Text('Consulte a disponibilidade de equipamentos: ', font='Arial 16', text_color='white')],
            #     [sg.Input(size=(30,8), key='selectE'), sg.Button('Buscar', size=(10,2))],
            #     [sg.Output(size=(30,20))], 
            #     [sg.Button('Voltar', size=(10,2))]
            #     ]
            #     self.janelaEquip = sg.Window('Dados da Consulta').layout(layoutEquip)
            #     while True:
            #         event, self.buttonE, self.valuesE = self.janelaEquip.Read()
            #         selectE = self.valuesE['selectE']
            #         if (self.buttonE == 'Voltar' or event == sg.WINDOW_CLOSED):
            #             break
            #         elif (self.buttonL == 'Buscar'):
            #             print(selectE)
#%%
sg.theme('Black')
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

professores = pd.read_csv(os.path.join(__location__, "sgube_professores.csv"))

from tkinter import font
import tkinter
root = tkinter.Tk()
fonts = list(font.families())
fonts.sort()
root.destroy()

print(fonts)

#%%
tela = Interface()
tela.connect()
#tela.insert()
tela.iniciar()
#tela.commit()
#tela.endConnection()

