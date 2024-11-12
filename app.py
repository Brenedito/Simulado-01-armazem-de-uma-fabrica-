from flask import Flask, render_template, request, redirect  # Importa as bibliotecas do Flask para criação de rotas e manipulação de templates #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
from db import DB, DatabaseConnectionError  # Importa a classe de conexão com o banco de dados e a exceção para erros de conexão
import datetime  # Importa o módulo para manipulação de datas

app = Flask(__name__)  # Cria uma instância do aplicativo Flask

user = {}  # Inicializa um dicionário para armazenar as informações do usuário que faz login #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
DB = DB()  # Instancia a classe DB, que gerencia a conexão e operações no banco de dados


@app.route("/")  # Define a rota para a página inicial
def index():
    # Renderiza a página de login com uma variável que indica se houve erro
    return render_template("login.html", error=False)


@app.route("/logout")  # Define a rota para o logout
def logout():
    # Redireciona o usuário de volta para a página inicial após o logout
    return redirect("/")


@app.route("/logar", methods={'POST'})  # Define a rota para o login com o método POST #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
def login():
    try:
        global user  # Declara a variável user como global para que seu valor possa ser acessado em outras partes do código
        username = request.form["user"]  # Obtém o nome de usuário do formulário de login
        password = request.form["senha"]  # Obtém a senha do formulário de login

        # Imprime os valores do nome de usuário e senha no console para depuração
        print(username, password)

        # Chama o método de login da classe DB, passando as credenciais do usuário
        user = DB.login_user(username, password)

        # Verifica se houve um erro no processo de login
        if "error" in user:
            # Renderiza a página de login novamente com uma variável que indica erro
            return render_template('login.html', error=True)
        else:
            # Renderiza a página da fábrica com as informações do usuário logado #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
            return render_template("fabrica.html", user=user)
    except DatabaseConnectionError:
        # Trata a exceção caso a conexão com o banco de dados falhe
        return render_template("errologar.html"), 500  # Renderiza uma página de erro e retorna status 500


@app.route("/fabrica")  # Define a rota para a página da fábrica
def factory():
    # Renderiza a página da fábrica, passando as informações do usuário logado
    return render_template("fabrica.html", user=user)


@app.route("/area/<int:area>")  # Define a rota para acessar produtos por área, recebendo o ID da área como parâmetro
def area(area):
    # Obtém os produtos da área especificada no banco de dados
    res = DB.get_products_by_area(area)

    # Renderiza a página da área, passando os produtos obtidos
    return render_template("area.html", produto=res)


@app.route("/venda/<int:id>")  # Define a rota para acessar a página de vendas de um produto específico, usando o ID do produto
def sell(id):
    # Obtém o nome do produto com base no ID fornecido #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
    res = DB.get_product_name(id)

    # Renderiza a página de vendas, passando o nome do produto
    return render_template("vendas.html", produto=res)


@app.route("/vendendo/<int:id>", methods={'POST'})  # Define a rota para processar a venda de um produto
def selling(id):
    global quantity, destination, product_id  # Declara variáveis globais para uso posterior na função

    # Obtém a quantidade e o destino da venda a partir do formulário
    quantity = request.form["quant"]
    destination = request.form["destino"]
    product_id = id  # Armazena o ID do produto que está sendo vendido #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

    # Chama o método para registrar a venda no banco de dados
    DB.make_sale(quantity, destination, product_id)

    # Redireciona o usuário de volta para a página da fábrica após registrar a venda
    return redirect("/fabrica")


@app.route("/relatoriovendas")  # Define a rota para acessar o relatório de vendas
def sales_report():
    # Obtém todas as vendas registradas no banco de dados
    sales = DB.get_sales()

    # Renderiza a página do relatório de vendas, passando os dados das vendas
    return render_template("relatorio.html", vendas=sales)


@app.route("/estoque")  # Define a rota para acessar a página de estoque
def stock():
    # Obtém todos os produtos disponíveis no estoque
    stock = DB.get_all_products()

    # Renderiza a página de estoque, passando os produtos e a data atual
    return render_template("estoque.html", estoque=stock, date=datetime.datetime.now().date())


if __name__ == '__main__':  # Verifica se o script está sendo executado diretamente
    # Inicia o servidor Flask em modo de depuração para facilitar o desenvolvimento #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
    app.run(debug=True)
