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

def deviceQuery(device, place):
    if device == "Livro":
        query = "select tipo" + device + ".nome, tipo" + device + ".autor, tipo" + device + ".edicao, tipo" + device + ".ano_lancamento, " + place + ".nome, " + place + ".endereco, Aparato.disponivel "
    elif device == "Equipamento":
        query = "select tipo" + device + ".nome, tipo" + device + ".tipo, tipo" + device + ".modelo, " + place + ".nome, " + place + ".endereco, Aparato.disponivel "
    else:
        print("Algo deu errado em deviceQuery")
        return("")
    query += "from ((((tipo" + device + " "
    query += "INNER JOIN " + device + " ON tipo" + device + ".idtipo" + device + " = " + device + ".tipo" + device + "_idtipo" + device + ") "
    query += "INNER JOIN Aparato ON Aparato.idAparato = " + device + ".Aparato_idAparato) "
    query += "INNER JOIN " + place + "_has_Aparato ON " + place + "_has_Aparato.Aparato_idAparato = Aparato.idAparato) "
    query += "INNER JOIN " + place + " ON " + place + ".id" + place + " = " + place + "_has_Aparato." + place + "_id" + place + ") "
    return query

def loanQuery(person, device):
    query = query = "select " + person + ".nome, " + person + ".nusp, Aparato.idAparato, tipo" + device + ".nome, "
    if device == "Equipamento":
        query += "tipo" + device + ".tipo, tipo" + device + ".modelo "
    elif device == "Livro":
        query += "tipo" + device + ".autor, tipo" + device + ".edicao, tipo" + device + ".ano_lancamento "
    else:
        print("Algo deu errado em deviceQuery")
        return("")
    query += "from ((((" + person + " "
    query += "INNER JOIN " + person + "_has_Aparato ON " + person + ".nusp = " + person + "_has_Aparato." + person + "_nusp) "
    query += "INNER JOIN Aparato ON Aparato.idAparato = " + person + "_has_Aparato.Aparato_idAparato) "
    query += "INNER JOIN " + device + " ON " + device + ".Aparato_idAparato = Aparato.idAparato)"
    query += "INNER JOIN tipo" + device + " ON " + device + ".tipo" + device + "_idtipoEquip = tipo" + device + ".idtipoEquip) "
    return query


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
            [sg.Text('Consulte a disponibilidade de Livros ', font='Arial 18', text_color='white')],
            [sg.Text('Consulte por um Nome: ', font='Arial 18', text_color='white')],
            [sg.Input(size=(60,20), key='selectNomeLivro')],
            [sg.Text('Consulte pelo Nome do(a) Autor(a): ', font='Arial 18', text_color='white')],
            [sg.Input(size=(60,20), key='selectAutor'), sg.Button('Buscar', size=(22,1))],
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
                            #consulta_sql = "select Biblioteca.nome, tipoEquipamento.nome, tipoEquipamento.tipo, tipoEquipamento.modelo, Aparato.disponivel from ((((tipoEquipamento INNER JOIN Equipamento ON tipoEquipamento.idtipoEquip = Equipamento.tipoEquipamento_idtipoEquip) INNER JOIN Aparato ON Aparato.idAparato = Equipamento.Aparato_idAparato) INNER JOIN Biblioteca_has_Aparato ON Biblioteca_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Biblioteca ON Biblioteca.idBiblioteca = Biblioteca_has_Aparato.Biblioteca_idBiblioteca) where " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            #consulta_sql = "select tipoEquipamento.nome, tipoEquipamento.tipo, tipoEquipamento.modelo, Laboratorio.nome, Laboratorio.endereco, Aparato.disponivel from ((((tipoEquipamento INNER JOIN Equipamento ON tipoEquipamento.idtipoEquip = Equipamento.tipoEquipamento_idtipoEquip) INNER JOIN Aparato ON Aparato.idAparato = Equipamento.Aparato_idAparato) INNER JOIN Laboratorio_has_Aparato ON Laboratorio_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Laboratorio ON Laboratorio.idLaboratorio = Laboratorio_has_Aparato.Laboratorio_idLaboratorio) where " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            consulta_sql = deviceQuery("Equipamento","Laboratorio") + "where " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()
                            for linha in linhas:
                                print("Nome equipamento: ", linha[0])
                                print("Tipo: ", linha[1])
                                print("Modelo: ", linha[2])
                                print("Laboratorio: ", linha[3])
                                print("Endereco do Lab: ", linha[4])
                                print("Disponibilidade: ", linha[5], "\n")

                            #consulta_sql = "select tipoEquipamento.nome, tipoEquipamento.tipo, tipoEquipamento.modelo, Biblioteca.nome, Biblioteca.endereco, Aparato.disponivel from ((((tipoEquipamento INNER JOIN Equipamento ON tipoEquipamento.idtipoEquip = Equipamento.tipoEquipamento_idtipoEquip) INNER JOIN Aparato ON Aparato.idAparato = Equipamento.Aparato_idAparato) INNER JOIN Biblioteca_has_Aparato ON Biblioteca_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Biblioteca ON Biblioteca.idBiblioteca = Biblioteca_has_Aparato.Biblioteca_idBiblioteca) where " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            consulta_sql = deviceQuery("Equipamento","Biblioteca") + "where " + "tipoEquipamento.nome LIKE '%" + selectE + "%'"
                            self.cursor.execute(consulta_sql)
                            linhas = self.cursor.fetchall()
                            for linha in linhas:
                                print("Nome equipamento: ", linha[0])
                                print("Tipo: ", linha[1])
                                print("Modelo: ", linha[2])
                                print("Biblioteca: ", linha[3])
                                print("Endereco do Bib: ", linha[4])
                                print("Disponibilidade: ", linha[5], "\n")

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
                    if self.buttonL == 'Buscar':
                        selectLivro = self.valuesL['selectNomeLivro']
                        selectAutor = self.valuesL['selectAutor']
                        try:
                            if(selectLivro != '' and selectAutor == ''):
                                #consulta_sql = "select * from tipoLivro, Livro where Livro.tipoLivro_idtipoLivro = tipoLivro.idtipoLivro AND tipoLivro.nome LIKE '%" + selectLivro + "%'"
                                
                                # Consulta para checar livros em bibliotecas
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Biblioteca.nome, Biblioteca.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Biblioteca_has_Aparato ON Biblioteca_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Biblioteca ON Biblioteca.idBiblioteca = Biblioteca_has_Aparato.Biblioteca_idBiblioteca) where " + "tipoLivro.nome LIKE '%" + selectLivro + "%'"
                                consulta_sql = deviceQuery("Livro","Biblioteca") + "where " + "tipoLivro.nome LIKE '%" + selectLivro + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome da biblioteca:", linha[4])
                                    print("Endereco da bib:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                                # Consulta para checar livros em Laboratorios
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Laboratorio.nome, Laboratorio.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Laboratorio_has_Aparato ON Laboratorio_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Laboratorio ON Laboratorio.idLaboratorio = Laboratorio_has_Aparato.Laboratorio_idLaboratorio) where " + "tipoLivro.nome LIKE '%" + selectLivro + "%'"
                                consulta_sql = deviceQuery("Livro","Laboratorio") + "where " + "tipoLivro.nome LIKE '%" + selectLivro + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome do Laboratorio:", linha[4])
                                    print("Endereco do lab:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                            elif(selectLivro == '' and selectAutor != ''):
                                #consulta_sql = "select * from tipoLivro, Livro where Livro.tipoLivro_idtipoLivro = tipoLivro.idtipoLivro AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                
                                # Consulta para checar livros em bibliotecas
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Biblioteca.nome, Biblioteca.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Biblioteca_has_Aparato ON Biblioteca_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Biblioteca ON Biblioteca.idBiblioteca = Biblioteca_has_Aparato.Biblioteca_idBiblioteca) where " + "tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                consulta_sql = deviceQuery("Livro","Biblioteca") + "where " + "tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome da biblioteca:", linha[4])
                                    print("Endereco da bib:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                                # Consulta para checar livros em Laboratorios
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Laboratorio.nome, Laboratorio.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Laboratorio_has_Aparato ON Laboratorio_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Laboratorio ON Laboratorio.idLaboratorio = Laboratorio_has_Aparato.Laboratorio_idLaboratorio) where " + "tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                consulta_sql = consulta_sql = deviceQuery("Livro","Laboratorio") + "where " + "tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome do Laboratorio:", linha[4])
                                    print("Endereco do lab:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                            elif(selectLivro != '' and selectAutor != ''):
                                #consulta_sql = "select * from tipoLivro, Livro where Livro.tipoLivro_idtipoLivro = tipoLivro.idtipoLivro AND tipoLivro.nome LIKE '%" + selectLivro + "%'" + " AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                
                                # Consulta para checar livros em bibliotecas
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Biblioteca.nome, Biblioteca.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Biblioteca_has_Aparato ON Biblioteca_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Biblioteca ON Biblioteca.idBiblioteca = Biblioteca_has_Aparato.Biblioteca_idBiblioteca) where tipoLivro.nome LIKE '%" + selectLivro + "%'" + " AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                consulta_sql = deviceQuery("Livro","Biblioteca") + "where tipoLivro.nome LIKE '%" + selectLivro + "%'" + " AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome da biblioteca:", linha[4])
                                    print("Endereco da bib:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                                # Consulta para checar livros em Laboratorios
                                #consulta_sql = "select tipoLivro.nome, tipoLivro.autor, tipoLivro.edicao, tipoLivro.ano_lancamento, Laboratorio.nome, Laboratorio.endereco, Aparato.disponivel from ((((tipoLivro INNER JOIN Livro ON tipoLivro.idtipoLivro = Livro.tipoLivro_idtipoLivro) INNER JOIN Aparato ON Aparato.idAparato = Livro.Aparato_idAparato) INNER JOIN Laboratorio_has_Aparato ON Laboratorio_has_Aparato.Aparato_idAparato = Aparato.idAparato) INNER JOIN Laboratorio ON Laboratorio.idLaboratorio = Laboratorio_has_Aparato.Laboratorio_idLaboratorio) where tipoLivro.nome LIKE '%" + selectLivro + "%'" + " AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                consulta_sql = deviceQuery("Livro","Laboratorio") + "where tipoLivro.nome LIKE '%" + selectLivro + "%'" + " AND tipoLivro.autor LIKE '%" + selectAutor + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome:", linha[0])
                                    print("Autor:", linha[1])
                                    print("Edição:", linha[2])
                                    print("Ano de Lançamento:", linha[3])
                                    print("Nome do Laboratorio:", linha[4])
                                    print("Endereco do lab:", linha[5])
                                    print("Disponibilidade:", linha[6], "\n")

                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonL == 'Buscar':
                        try:
                            print("Insira algum parâmetro de busca!", "\n")
                            #consulta_sql = "select * from Aluno"
                            #self.cursor.execute(consulta_sql)
                            #linhas = self.cursor.fetchall()
 
                            #for linha in linhas:
                                #print("NUSP:", linha[0])
                                #print("Área:", linha[1])
                                #print("Ano de Ingresso:", linha[2])
                                #print("Nome:", linha[3])
                                #print("E-mail:", linha[4], "\n")
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
                                #consulta_sql = "select * from Aluno where Aluno.nusp LIKE '%" + selectNusp + "%'"
                                #consulta_sql = "select Aluno.nome, Aluno.nusp, Aparato.idAparato, tipoEquipamento.nome, tipoEquipamento.tipo, tipoEquipamento.modelo from ((((Aluno INNER JOIN Aluno_has_Aparato ON Aluno.nusp = Aluno_has_Aparato.Aluno_nusp) INNER JOIN Aparato ON Aparato.idAparato = Aluno_has_Aparato.Aparato_idAparato) INNER JOIN Equipamento ON Equipamento.Aparato_idAparato = Aparato.idAparato) INNER JOIN tipoEquipamento ON Equipamento.tipoEquipamento_idtipoEquip = tipoEquipamento.idtipoEquip) where Aluno.nusp LIKE '%" + selectNusp + "%' "
                                
                                consulta_sql = loanQuery("Aluno","Equipamento") + "where Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Aluno","Livro") + "where Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                #consulta_sql = "select * from Aluno where Aluno.nome LIKE '%" + selectNome + "%'"

                                consulta_sql = loanQuery("Aluno","Equipamento") + "where Aluno.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Aluno","Livro") + "where Aluno.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                            elif(selectNusp != '' and selectNome != ''):
                                #consulta_sql = "select * from Aluno where Aluno.nome LIKE '%" + selectNome + "%'" + "AND Aluno.nusp LIKE '%" + selectNusp + "%'"
                                
                                consulta_sql = loanQuery("Aluno","Equipamento") + "where Aluno.nome LIKE '%" + selectNome + "%'" + "AND Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Aluno","Livro") + "where Aluno.nome LIKE '%" + selectNome + "%'" + "AND Aluno.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Aluno: ", linha[0])
                                    print("NUSP do Aluno: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")


                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonP == 'Professores':
                        selectNusp = self.valuesP['selectNusp']
                        selectNome = self.valuesP['selectNome']
                        try:

                            if(selectNusp != '' and selectNome == ''):
                                #consulta_sql = "select * from Professor where Professor.nusp LIKE '%" + selectNusp + "%'"
                                
                                consulta_sql = loanQuery("Professor","Equipamento") + "where Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Professor","Livro") + "where Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                #consulta_sql = "select * from Professor where Professor.nome LIKE '%" + selectNome + "%'"
                                
                                consulta_sql = loanQuery("Professor","Equipamento") + "where Professor.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Professor","Livro") + "where Professor.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                            elif(selectNusp != '' and selectNome != ''):
                                #consulta_sql = "select * from Professor where Professor.nome LIKE '%" + selectNome + "%'" + "AND Professor.nusp LIKE '%" + selectNusp + "%'"
                                
                                consulta_sql = loanQuery("Professor","Equipamento") + "where Professor.nome LIKE '%" + selectNome + "%'" + "AND Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Professor","Livro") + "where Professor.nome LIKE '%" + selectNome + "%'" + "AND Professor.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Professor: ", linha[0])
                                    print("NUSP do Professor: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                        except Error as e:
                            print("Erro ao acessar tabela MySQL", e)

                    elif self.buttonP == 'Funcionários':
                        selectNusp = self.valuesP['selectNusp']
                        selectNome = self.valuesP['selectNome']
                        try:
                            if(selectNusp != '' and selectNome == ''):
                                #consulta_sql = "select * from Funcionario where Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                
                                consulta_sql = loanQuery("Funcionario","Equipamento") + "where Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Funcionario","Livro") + "where Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")

                            elif(selectNusp == '' and selectNome != ''):
                                #consulta_sql = "select * from Funcionario where Funcionario.nome LIKE '%" + selectNome + "%'"
                                
                                consulta_sql = loanQuery("Funcionario","Equipamento") + "where Funcionario.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Funcionario","Livro") + "where Funcionario.nome LIKE '%" + selectNome + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")


                            elif(selectNusp != '' and selectNome != ''):
                                #consulta_sql = "select * from Funcionario where Funcionario.nome LIKE '%" + selectNome + "%'" + "AND Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                
                                consulta_sql = loanQuery("Funcionario","Equipamento") + "where Funcionario.nome LIKE '%" + selectNome + "%'" + "AND Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Equipamento: ", linha[3])
                                    print("Tipo Equipamento: ", linha[4])
                                    print("Modelo Equipamento: ", linha[5], "\n")
                                
                                consulta_sql = loanQuery("Funcionario","Livro") + "where Funcionario.nome LIKE '%" + selectNome + "%'" + "AND Funcionario.nusp LIKE '%" + selectNusp + "%'"
                                self.cursor.execute(consulta_sql)
                                linhas = self.cursor.fetchall()

                                for linha in linhas:
                                    print("Nome do Funcionario: ", linha[0])
                                    print("NUSP do Funcionario: ", linha[1])
                                    print("ID Aparato: ", linha[2])
                                    print("Nome Livro: ", linha[3])
                                    print("Autor: ", linha[4])
                                    print("Edição: ", linha[5])
                                    print("Ano de lançamento: ", linha[6], "\n")
                                    
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
            pd.read_csv(os.path.join(__location__, "Equipamento.csv")),
            pd.read_csv(os.path.join(__location__, "tipoLivro.csv")),
            pd.read_csv(os.path.join(__location__, "Laboratorio_has_Aparato.csv")),
            pd.read_csv(os.path.join(__location__, "Biblioteca_has_Aparato.csv")),
            pd.read_csv(os.path.join(__location__, "Biblioteca.csv")),
            pd.read_csv(os.path.join(__location__, "Aparato.csv"))
]

entity = ["Aluno", "Professor", "Trabalha_Em", "Responsavel_Por", "Livro", "Laboratorio", "Funcionario", "tipoEquipamento", "Equipamento", "tipoLivro", "Biblioteca_has_Aparato", "Biblioteca", "Aparato"]

tela = Interface()
tela.connect()
for i in range(len(entity)):
    tela.insert(geraInsert(database[i], entity[i]))
tela.iniciar()
#tela.commit()
#tela.endConnection()
