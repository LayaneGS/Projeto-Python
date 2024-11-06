# a linha abaixo imports o flask para o meu projeto
from flask import Flask, render_template, request, redirect

# A linha abaixo importa a biblioteca que faz a ação direta no banco
from flask_sqlalchemy import SQLAlchemy

# a linha abaixo é uma variavel da aplicação 
app = Flask(__name__)

app.secret_key = 'Layane'

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+mysqlconnector://Layyy:Layy240620@localhost:3306/db_loja'
 
    # '{SGBD}://{usuario}:{senha}@{servidor}:{porta}/{database}'.format(
    #     SGBD = 'mysql+mysqlconnector',
    #      usuario = 'root',
    #    senha = 'Layy240620@',
    #      servidor = 'localhost',
    #     porta = '3306',
    #      database = 'db_loja'
    #  )

# a linha abaixo instancia o banco de dados
db = SQLAlchemy(app)

# agora vamos criar a classe modelo da entidade
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome_produto = db.Column(db.String(50), nullable=False)
    marca_produto = db.Column(db.String(30), nullable=True)
    preco_produto = db.Column(db.Float, nullable=False)


# Essa func serve para representar a classe com o parametro, no caso do self seria para lista apenas o necessário e não todas as colunas
    def __repr__(self):
        return '<Name %r>' % self.name

# a linha abaixo é criada a primeira rota
@app.route('/ola')
def mostra():
    return "<h1>iniciando o projeto Flask</h1>"

@app.route('/lista')
def lista_produtos():

    lista_tabela = Produto.query.order_by(Produto.id)

    return render_template("lista.html",
                            descricao = "Aqui temos diversas marcas",
                            produtos_listado = lista_tabela)


@app.route('/cadastrar')
def cadastrar_produto():
    return render_template("cadastro.html")

@app.route('/inserir', methods=['post']) #essa rota não da para ser acessada diretamente pela URL por conta do methodo post
def adiciona_registro():

#AS LINHAS ABAIXO SÃO AS VARIAVEIS QUE VÃO
# RECEBER O QUE OS USUÁRIOS DIGITAM NOS CAMPOS
    nome = request.form['txtNome']
    marca = request.form['txtMarca']
    preco = float(request.form['txtPreco'])

    #A LINHA ABAIXO INSTANCIA UM NOVO PRODUTO
    # COM AS INFORMAÇÕES QUE DIGITOU
    novo_prod = Produto(nome_produto = nome, marca_produto = marca, preco_produto = preco)

    # a linha abaixo adiciona na tabela os dados
    db.session.add(novo_prod)


# a linha abaixo grava as alterações no banco de dados
    db.session.commit()

   

   # return lista_produtos()

    return redirect('/lista')

@app.route('/teste')
def teste():
    return render_template('teste.html')

# essa parte é para editar o produto
@app.route('/editar/<int:id>') #quando vier editar vai precisar do ID e já converte para int
def editar_produto(id): 
    # a linha abaixo busca exatamente o produto com o id passado
    produto = Produto.query.filter_by(id = id).first() # serve para não duplicar o id

    # a linha abaixo manda o produto encontrado para a página
    return render_template('editar.html', produto_listado = produto)

# A rota abaixo salva
@app.route('/atualizar', methods=['POST',])
def atualiza_produto():

    print("ta aqui --- ", request.form['txtId'])

    atualizar = Produto.query.filter_by(id =  request.form['txtId']).first()

    # As linhas abaixo passa os novos valores para os determinados campos
    atualizar.nome_produto = request.form['txtNome']
    atualizar.marca_produto = request.form['txtMarca']
    atualizar.preco_produto = request.form['txtPreco']

    db.session.add(atualizar)

    db.session.commit()

    return redirect('/lista')

@app.route('/excluir/<int:id>')
def excluir_produto(id):
    Produto.query.filter_by(id = id).delete()

    db.session.commit()

    return redirect('lista')

@app.route('/login')
def login():
    return render_template('login.html')

app.run(debug=True)
