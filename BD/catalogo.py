import json
import sys
import os
sys.path.insert(1, os.path.abspath('')[:-2])
import classes
from PIL import Image
import pandas as pd

class Catalogo():
    def __init__(self):
        with open("catalogo.JSON","r") as read_file:
            produtos_json = json.load(read_file)
        self.produtos = []
        self.codigos = produtos_json["codigos"]
        for idx, codigo in enumerate(produtos_json["codigos"]):
            self.produtos.append(classes.Produto(codigo, produtos_json["nomes"][idx],
                                         produtos_json["precos"][idx], produtos_json["estoque"][idx]))

    def adicionar_produto(self, novo, qtd, codigo, preco=None,nome=None):
        if novo:
            self.produtos.append(classes.Produto(codigo, nome, preco, qtd))
            self.codigos.append(codigo)
        else:
            self.produtos[self.codigos.index(codigo)].adicionar_estoque(qtd)

    def remover_produto(self, codigo, qtd=None):
        if codigo in self.codigos:
            if qtd == None:
                del self.produtos[self.codigos.index(codigo)]
            else:
                self.produtos[self.codigos.index(codigo)].remover_estoque(qtd)

    def verifica_estoque(self, codigo):
        if codigo in self.codigos:
            return self.produtos[self.codigos.index(codigo)].estoque
        else:
            return 0

    def verifica_preco(self, codigo):
        if codigo in self.codigos:
            return self.produtos[self.codigos.index(codigo)].preco
        else:
            return 0

    def modificar_preco(self, codigo, preco):
        if codigo in self.codigos:
            self.produtos[self.codigos.index(codigo)].mudar_preco(preco)

    def visualizar_imagem(self, codigo):
        imagem = Image.open("imagens/"+str(codigo)+".jpg")
        imagem.show()

    def inserir_produtos_de_csv(self, csv_path):
        """
            O csv deve ter as colunas com os nomes Cod | Nome | Preco | Qtd
        """
        new_products = pd.read_csv(csv_path)
        print(new_products)
        for _, product in new_products.iterrows():
            if not product["Cod"] in self.codigos:
                self.adicionar_produto(novo=True, qtd=product["Qtd"], codigo=product["Cod"], preco=product["Preco"],nome=product["Nome"])
        self.salvar_mudancas()

    def salvar_mudancas(self):
        catalogo = {"codigos":[],"nomes":[],"precos":[],"estoque":[]}
        for produto in self.produtos:
            catalogo["codigos"].append(produto.codigo)
            catalogo["nomes"].append(produto.nome)
            catalogo["precos"].append(produto.preco)
            catalogo["estoque"].append(produto.estoque)

        with open('catalogo.JSON', 'w') as write_file:
            json.dump(catalogo, write_file)

cat = Catalogo()
cat.inserir_produtos_de_csv(csv_path="catalogo.csv")
