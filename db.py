import mysql.connector  # Importa a biblioteca para conectar ao MySQL #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
import mysql.connector.errors  # Importa as classes de erro do MySQL

# Exceção personalizada para erros de conexão com o banco de dados
class DatabaseConnectionError(Exception):
    pass

class DB:
    def __init__(self):
        self.connection = None  # Inicializa a variável de conexão #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

    def create_connection(self):
        # Tenta criar uma conexão com o banco de dados
        try:
            connection = mysql.connector.connect(
                host = "localhost",  # Host do banco de dados
                port = "3306",  # Porta do banco de dados
                user = "root",  # Usuário do banco de dados
                password ="",  # Senha do banco de dados
                database = "fabrica"  # Nome do banco de dados
            )
            return connection  # Retorna a conexão
        except mysql.connector.errors.InterfaceError as error:
            # Levanta uma exceção personalizada em caso de erro de conexão
            raise DatabaseConnectionError("Unable to connect to the database") from error

    def login_user(self, username, password):
        # Tenta autenticar um usuário no banco de dados
        connection = self.create_connection()  # Cria uma conexão #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()  # Cria um cursor para executar consultas
            # Executa uma consulta para verificar o usuário e a senha #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
            cursor.execute(f"Select * From usuarios where idUsuarios = {username} and senha = '{password}';")
            result = cursor.fetchall()  # Obtém todos os resultados da consulta

            user = {}  # Dicionário para armazenar informações do usuário

            if len(result) > 0:
                # Se o usuário for encontrado, armazena suas informações
                user['id'] = result[0][0]
                user['nome'] = result[0][1]
                user['funcao'] = result[0][2]
                user['senha'] = result[0][3]
            else:
                # Se o usuário não for encontrado, define um erro
                user["error"] = True

            cursor.close()  # Fecha o cursor
            connection.close()  # Fecha a conexão #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

            return user  # Retorna as informações do usuário

    def get_user_name(self, username):
        # Obtém o nome de um usuário pelo id
        connection = self.create_connection()  # Cria uma conexão

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()  # Cria um cursor
            # Executa uma consulta para obter o nome do usuário
            cursor.execute(f"Select nomeUsuario From usuarios where idUsuarios = {username};")
            result = cursor.fetchall()  # Obtém todos os resultados
            return result  # Retorna os resultados #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

    def get_products_by_area(self, area):
        # Obtém produtos de uma área específica
        connection = self.create_connection()  # Cria uma conexão

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()  # Cria um cursor
            # Executa uma consulta para obter produtos da área
            cursor.execute(f"Select * From produtos where area = {area};")
            result = cursor.fetchall()  # Obtém todos os resultados

            products = {}  # Dicionário para armazenar produtos
            for i in range(len(result)):
                # Armazena informações de cada produto #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
                products[result[i][0]] = {
                    "id": result[i][0],
                    "nome": result[i][1],
                    "quantidade": result[i][2],
                    "lote": result[i][3],
                    "data": result[i][4],
                }

            cursor.close()  # Fecha o cursor
            connection.close()  # Fecha a conexão

            return products  # Retorna os produtos

    def get_all_products(self):
        # Obtém todos os produtos
        connection = self.create_connection()  # Cria uma conexão

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()  # Cria um cursor
            cursor.execute(f"SELECT * FROM produtos")  # Executa uma consulta para obter todos os produtos
            result = cursor.fetchall()  # Obtém todos os resultados #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

            products = {}  # Dicionário para armazenar produtos
            for i in range(len(result)):
                # Armazena informações de cada produto
                products[result[i][0]] = {
                    "id": result[i][0],
                    "nome": result[i][1],
                    "quantidade": result[i][2],
                    "lote": result[i][3],
                    "data": result[i][4],
                }

            cursor.close()  # Fecha o cursor
            connection.close()  # Fecha a conexão

            return products  # Retorna os produtos

    def get_product_name(self, id):
        # Obtém informações de um produto pelo id
        connection = self.create_connection()  # Cria uma conexão #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()  # Cria um cursor
            # Executa uma consulta para obter o nome, quantidade e ID do produto
            cursor.execute(f"Select nomeProduto, quantidade, idProdutos From produtos where idProdutos = {id};")
            res = cursor.fetchall()  # Obtém todos os resultados
            result = {}  # Dicionário para armazenar informações do produto

            if len(res) > 0:
                # Se o produto for encontrado, armazena suas informações #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
                result['nome'] = res[0][0]
                result['quantidade'] = res[0][1]
                result['id'] = res[0][2]
            else:
                # Se o produto não for encontrado, define um erro
                result["error"] = True

            cursor.close()  # Fecha o cursor
            connection.close()  # Fecha a conexão

            return result  # Retorna as informações do produto

    def make_sale(self, quantity, destination, id):
        # Registra uma venda no banco de dados
        connection = self.create_connection()
          # Cria uma conexão

        if connection is None:
            return False  # Retorna falso se a conexão falhar
        else:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT quantidade FROM produtos WHERE idProdutos = {id};""")# Verifique a quantidade disponível antes de atualizar
            res = cursor.fetchone()
            
            if res:
                quantidade_atual = res[0]
                if int(quantity) <= int(quantidade_atual):
                    cursor.execute(f"""UPDATE produtos
                                    SET quantidade = quantidade - {quantity} 
                                    WHERE idProdutos = {id};""")
                    
                    print("Venda realizada com sucesso!")

                    connection.commit()  # Confirma as alterações no banco de dados
                else:
                    print("Quantidade escolhida é maior que a disponível. Venda não realizada.")
            else:
                print("Produto não encontrado.")

            cursor.close()  # Fecha o cursor
            connection.close()  # Fecha a conexão

    def get_sales(self):
        # Obtém todas as vendas registradas
        connection = self.create_connection()  # Cria uma conexão

        if connection is None:
            return False  # Retorna falso se a conexão falhar #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)
        else:
            cursor = connection.cursor()  # Cria um cursor
            # Executa uma consulta para obter informações sobre as vendas
            cursor.execute(f"""SELECT vendas.idvendas, vendas.dataHora, vendas.quantidadeVenda, vendas.destino, produtos.nomeProduto
                            FROM vendas
                            INNER JOIN produtos ON vendas.idprodutos = produtos.idprodutos;
                            """)
            result = cursor.fetchall()  # Obtém todos os resultados

            sales = {}  # Dicionário para armazenar vendas

            for i in range(len(result)):
                # Armazena informações de cada venda
                sales[result[i][0]] = {
                    'id': result[i][0],
                    'data': result[i][1],
                    'quantidade': result[i][2],
                    'destino': result[i][3],
                    'nomeproduto': result[i][4]
                }

            cursor.close()  # Fecha o cursor 
            connection.close()  # Fecha a conexão #FEITO PELA EQUIPE DO BRENO(EVITANDO CÓPIAS)

            return sales  # Retorna as vendas
