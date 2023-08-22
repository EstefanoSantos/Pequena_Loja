import tkinter as tk
from tkinter import ttk
import crud

class PrincipalBd:

    def __init__(self, win):

        self.obj_bd = crud.AppBd()

        #componentes Label
        self.lbCodigo = tk.Label(win, text="Código do Produto:")
        self.lbNome = tk.Label(win, text="Nome do Produto:")
        self.lbPreco = tk.Label(win, text="Preço do Produto:")

        #componentes entry
        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()

        #componentes Button
        self.btnCadastrar = tk.Button(win, text="Cadastrar", command=self.f_cadastrar_produto)
        self.btnAtualizar = tk.Button(win, text="Atualizar", command=self.f_atualizar_produto)
        self.btnExcluir = tk.Button(win, text="Exluir", command=self.f_exluir_produto)
        self.btnLimpar = tk.Button(win, text="Limpar", command=self.f_limpar_tela)

        # --------------------------------------------------------------------------
        # Componentes Treeviw
        # ---------------------------------------------------------------------------

        self.dadosColunas = ("Código", "Nome", "Preço")

        self.treeProdutos = ttk.Treeview(win,
                                         columns=self.dadosColunas,
                                         selectmode='browse')

        self.verscrolbar = ttk.Scrollbar(win,
                                         command=self.treeProdutos.yview,
                                         orient="vertical")
        self.verscrolbar.pack(side='right', fill='x')

        self.treeProdutos.configure(yscrollcommand=self.verscrolbar.set)

        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preço", text="Preço")

        self.treeProdutos.column("Código", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preço", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady=10)

        self.treeProdutos.bind("<<TreeviewSelect>>",
                               self.carregar_dados_iniciais)

    # --------------------------------------------------------------------------
    #Posicionamento dos componentes na tela
    #---------------------------------------------------------------------------

        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lbNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)

        self.lbPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)

        self.treeProdutos.place(x=100, y=300)
        self.verscrolbar.place(x=605, y=300, height=225)
        self.carregar_dados_iniciais()

        #selecionando itens na treeviw

    def apresentar_itens_selecionados(self, event):
        self.f_limpar_tela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(1, nome)
            self.txtPreco.insert(2, preco)

    def carregar_dados_iniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.obj_bd.select_data()
            print('***********Dados disponíveis no BD**************')
            for item in registros:
                codigo = item[0]
                nome = item[1]
                preco = item[2]
                print("Código = ", codigo)
                print("Nome   = ", nome)
                print("Preço  = ", preco, '\n')
                print('-----------------------')

                self.treeProdutos.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo, nome, preco))

                self.iid = self.iid + 1
                self.id = self.id + 1
                print('Dados da Base')
        except:
            print('Ainda não existem dados pra carregar.')

    def f_ler_campos(self):
        codigo = None
        nome = None
        preco = None

        try:
            print('*************dados disponíveis************')
            codigo = int(self.txtCodigo.get())
            print('codigo', codigo)
            nome = self.txtNome.get()
            print('nome', nome)
            preco = float(self.txtPreco.get())
            print('preco', preco)
            print("Leitura do dados com sucesso!")
        except:
            print("Não foi possível carregar os dados")

        return codigo, nome, preco

    def f_cadastrar_produto(self):
        try:
            print('***************dados disponíveis*************')
            codigo, nome, preco = self.f_ler_campos()
            self.obj_bd.insert_product(codigo, nome, preco)
            self.treeProdutos.insert('', 'end', iid = self.iid, values=(codigo, nome, preco))

            self.iid = self.iid + 1
            self.id = self.id + 1
            self.f_limpar_tela()
            print('Produto cadastrado com sucesso!')
        except:
            print('Não foi possível efetuar o cadastro')

    def f_atualizar_produto(self):
        try:
            print('***************dados disponíveis***************')
            codigo, nome, preco = self.f_ler_campos()
            self.obj_bd.update_data(codigo, nome, preco)

            #recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregar_dados_iniciais()
            self.f_limpar_tela()
            print('Produto atualizado com sucesso!')
        except:
            print('Não foi possível fazer a atualização.')

    def f_exluir_produto(self):
        try:
            print('*****************dados disponíveis****************')
            codigo, nome, preco = self.f_ler_campos()
            self.obj_bd.delete_data(codigo,)

            #recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregar_dados_iniciais()
            self.f_limpar_tela()
            print('Produto excluído com sucesso!')
        except:
            print('Não foi possível exluir o produto.')

    def f_limpar_tela(self):
        print('******************dados disponíveis***********************')
        self.txtCodigo.delete(0, tk.END)
        self.txtNome.delete(0, tk.END)
        self.txtPreco.delete(0, tk.END)


janela = tk.Tk()
principal = PrincipalBd(janela)
janela.title('Armazém Preferido')
janela.geometry("820x600+10+10")
janela.mainloop()















