import psycopg2


class AppBd:

    def __init__(self):
        self.connection = None
        print("Método Construtor")

    def open_connection(self):

        try:
            self.connection = psycopg2.connect(database="loja_armazenamento",
                                                   user="postgres",
                                                   password="root",
                                                   host="localhost",
                                                   port="5432")

        except(Exception, psycopg2.Error) as error:
            if self.connection:
                print("Erro ao se conectar com o banco de dados", error)

    def select_data(self):
        registros = []
        cursor = None
        try:
            self.open_connection()
            cursor = self.connection.cursor()

            print('Selecionando todos os produtos')
            sql_select_query = """SELECT * FROM public."PRODUTO";"""

            cursor.execute(sql_select_query)
            registros = cursor.fetchall()
            print(registros)

        except (Exception, psycopg2.Error) as error:
            print("Erro na operação de seleção de dados", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print('A conexão foi fechada.')
        return registros

    def insert_product(self, codigo, nome, preco):
        cursor = None
        try:
            self.open_connection()
            cursor = self.connection.cursor()
            sql_insert_query = """INSERT INTO public."PRODUTO"("CODIGO", "NOME", "PRECO")
                                    VALUES(%s, %s, %s);"""
            data_to_insert = (codigo, nome, preco)
            cursor.execute(sql_insert_query, data_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "inserção de dado(s) realizado(s) com sucesso!")

        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print('Falha ao inserir registo na Tabela Produtos.', error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o Banco de Dados foi encerrada.")

    def update_data(self, codigo, nome, preco):
        cursor = None
        try:
            self.open_connection()
            cursor = self.connection.cursor()

            #registro antes da atualização
            print('Registros de produtos antes da atualização: ')
            sql_select_query = """SELECT * FROM public."PRODUTO" WHERE "CODIGO"=%s;"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)

            #atualizando dados na tabela
            sql_update_query = """UPDATE public."PRODUTO" SET "NOME" =%s, "PRECO" = %s WHERE "CODIGO"=%s;"""
            cursor.execute(sql_update_query, (nome, preco, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registo atualizado com sucesso!")

            #tabela depois da atualizaçao
            print('Registro depois da atualização: ')
            sql_select_query = """SELECT * FROM public."PRODUTO" WHERE "CODIGO"=%s;"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone
            print(record)

        except (Exception, psycopg2.Error) as error:
            print("Erro na atualização.", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o Banco de Dados foi encerrada")

    def delete_data(self, codigo):
        cursor = None

        try:
            self.open_connection()
            cursor = self.connection.cursor()

            #apagando dados
            sql_delete_query = """DELETE FROM public."PRODUTO"
                                    WHERE "CODIGO"= %s;"""
            cursor.execute(sql_delete_query, (codigo,))
            self.connection.commit()

            count = cursor.rowcount
            print(count, "Registro(s) excluído com sucesso")

        except (Exception, psycopg2.Error) as error:
            print("Erro na exclusão", error)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o Banco de Dados foi fechada com sucesso.")
