import json


class Usuarios:
    def __init__(self):
        with open("BD/usuarios.JSON","r") as read_file:
            usuarios_json = json.load(read_file)
        self.gerentes = {}
        self.clientes = {}
        self.logins = []
        for idx, login in enumerate(usuarios_json["gerentes"]["logins"]):
            self.gerentes[login] = usuarios_json["gerentes"]["senhas"][idx]
            self.logins.append(login)
        for idx, login in enumerate(usuarios_json["clientes"]["logins"]):
            self.clientes[login] = usuarios_json["clientes"]["senhas"][idx]
            self.logins.append(login)

    def adicionar_usuario(self, login, senha, tipo):
        if login not in self.logins:
            if tipo == "G":
                self.gerentes[login] = senha
            elif tipo == "C":
                self.clientes[login] = senha

    def tipo_do_usuario(self, login):
        if login in self.logins:
            if login in self.gerentes.keys():
                return 0
            else:
                return 1
        return -1

    def remover_usuario(self, login):
        tipo = self.tipo_do_usuario(login=login)
        if tipo == 0:
            del self.gerentes[login]
        elif tipo == 1:
            del self.clientes[login]

    def salvar_mudancas(self):
        usuarios = {"clientes":{"logins":[], "senhas":[]},"gerentes":{"logins":[], "senhas":[]}}
        for gerente in self.gerentes.items():
            usuarios["gerentes"]["logins"] = gerente[0]
            usuarios["gerentes"]["senhas"] = gerente[1]
        for cliente in self.clientes.items():
            usuarios["clientes"]["logins"] = cliente[0]
            usuarios["clientes"]["senhas"] = cliente[1]

        with open('BD/usuarios.JSON', 'w') as write_file:
            json.dump(usuarios, write_file)