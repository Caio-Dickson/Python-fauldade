# Questão 3 — POO: Usuários com Encapsulamento

class Usuario:
    def __init__(self, id_, nome, email):
        self.__id    = id_
        self.__nome  = nome
        self.set_email(email)

    # Getters
    def get_id(self):    return self.__id
    def get_nome(self):  return self.__nome
    def get_email(self): return self.__email

    # Setters
    def set_nome(self, nome):   self.__nome = nome
    def set_email(self, email):
        if "@" in email:
            self.__email = email
        else:
            print("E-mail inválido")
            self.__email = None

    def __repr__(self):
        return f"Usuario(id={self.__id}, nome='{self.__nome}', email='{self.__email}')"


class GerenciadorUsuarios:
    def __init__(self):
        self.usuarios = []

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def remover_usuario_por_id(self, id_):
        self.usuarios = [u for u in self.usuarios if u.get_id() != id_]

    def listar_usuarios(self):
        for u in self.usuarios:
            print(u)