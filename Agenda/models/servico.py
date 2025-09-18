class Servico:
    def __init__(self, codigo, nome, preco):
        self._codigo = codigo
        self._nome = nome
        self._preco = preco

    # getters
    def get_codigo(self):
        return self._codigo

    def get_nome(self):
        return self._nome

    def get_preco(self):
        return self._preco

    # setters
    def set_codigo(self, codigo):
        self._codigo = codigo

    def set_nome(self, nome):
        self._nome = nome

    def set_preco(self, preco):
        self._preco = preco

    def to_json(self):
        return {
            "Código": self._codigo,
            "Nome": self._nome,
            "Preço": self._preco
        }

    def __str__(self):
        return f"{self._codigo} - {self._nome} - R$ {self._preco:.2f}"

from models.servico import Servico

class ServicoDAO:
    _servicos = []
    _id_counter = 1

    def inserir(self, servico):
        servico.set_codigo(ServicoDAO._id_counter)
        ServicoDAO._id_counter += 1
        ServicoDAO._servicos.append(servico)

    def listar(self):
        return ServicoDAO._servicos

    def listar_id(self, id):
        for s in ServicoDAO._servicos:
            if s.get_codigo() == id:
                return s
        return None

    def atualizar(self, servico):
        for i, s in enumerate(ServicoDAO._servicos):
            if s.get_codigo() == servico.get_codigo():
                ServicoDAO._servicos[i] = servico
                return True
        return False

    def excluir(self, servico):
        ServicoDAO._servicos = [
            s for s in ServicoDAO._servicos if s.get_codigo() != servico.get_codigo()
        ]
