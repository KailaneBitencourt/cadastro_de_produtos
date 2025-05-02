from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas #importação para criar o pdf

numero_id = 0 #global

#Conexão do código com o banco de dados
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

#Função para editar os dados da tabela
def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall() 
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))

    produto = cursor.fetchall() #retorna os produtos

    tela_editar.show() #faz a tela aparecer

    numero_id = valor_id

    #faz aparecer o item e suas características na terceira tela
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))

#Função para salvar os dados editados
def salvar_dados_editados():
    #pega o número do id
    global numero_id
    #pega o que o usuário digitou
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    
    #atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    banco.commit()
    #atualizar as janelas
    tela_editar.close() #fecha a terceira tela
    segunda_tela.close() #fecha a segunda tela
    chama_segundatela()


#Função para excluir os dados da tabela
def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall() #os ids estarão salvos nessa variável
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    banco.commit() #para ser alterado na tabela do banco de dados

#função para gerar o pdf
def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 15)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "PREÇO")
    pdf.drawString(410,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")


def funcao_principal():
    #ler o que está nas caixas de texto 
    linha1 = interface.lineEdit.text() 
    linha2 = interface.lineEdit_2.text() 
    linha3 = interface.lineEdit_3.text() 

    categoria = ""

    #Verifica o botão de opção selecionado
    if interface.radioButton.isChecked():
        print("Categoria: informática")
        categoria = "Informática"

    elif interface.radioButton_2.isChecked():
        print("Categoria: Alimentação")
        categoria = "Alimentação"

    else:
        print("Categoria: Eletrônicos")   
        categoria = "Eletrônicos"

    #imprime o código, preço e descrição
    print("Código:  ", linha1)
    print("Descrição:  ", linha2)
    print("Preço:  ", linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit() 
    interface.lineEdit.setText("") #limpa os espaços após enviar o produto 
    interface.lineEdit_2.setText("")
    interface.lineEdit_3.setText("")

#função para chamar a tela de listar dados
def chama_segundatela():
    segunda_tela.show() #abre a segunda tela

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) #pega o número de linhas
    segunda_tela.tableWidget.setColumnCount(5) #são as colunas já definidas: id, codigo, preco,categoria e descricao

    #pecorre a matriz gerada pelos dados 
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) #str converte para string
    

app=QtWidgets.QApplication([])
interface=uic.loadUi("interface.ui") #importando a primeira tela
segunda_tela=uic.loadUi("listardados.ui") #importando a segunda tela
tela_editar=uic.loadUi("menu_editar.ui") #importando a terceira tela
interface.pushButton.clicked.connect(funcao_principal)
interface.pushButton_2.clicked.connect(chama_segundatela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)






interface.show() #abre a terceira tela
app.exec()    

#Criando a tabela para o banco de dados
""" create table produtos(
    id INT NOT NULL AUTO_INCREMENT,
    codigo INT,
    descricao VARCHAR(50),
    preco DOUBLE,
    categoria VARCHAR(20),
    PRIMARY KEY(id)
); """

#inserindo itens na tabela
#INSERT INTO produtos(codigo,descricao,preco,categoria) VALUES (123, "impressora", 500.00,"informatica");
