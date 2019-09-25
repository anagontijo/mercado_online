import json
import classes
from PIL import Image

class Catalogo():
    def __init__(self):
        with open("BD/catalogo.JSON","r") as read_file:
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
        imagem = Image.open("BD/imagens/"+str(codigo)+".jpg")
        imagem.show()

    def salvar_mudancas(self):
        catalogo = {"codigos":[],"nomes":[],"precos":[],"estoque":[]}
        for produto in self.produtos:
            catalogo["codigos"].append(produto.codigo)
            catalogo["nomes"].append(produto.nome)
            catalogo["precos"].append(produto.preco)
            catalogo["estoque"].append(produto.estoque)

        with open('BD/catalogo.JSON', 'w') as write_file:
            json.dump(catalogo, write_file)