import json

from models.dao import DAO  # ← nova herança

class Servico:
    def __init__(self, codigo, nome, preco):
        self.codigo, self.nome, self.preco = codigo, nome, preco

    # Getters e Setters
    def get_codigo(self): return self.codigo
    def get_nome(self): return self.nome
    def get_preco(self): return self.preco
    def set_codigo(self, codigo): self.codigo = codigo
    def set_nome(self, nome): self.nome = nome
    def set_preco(self, preco): self.preco = preco

    # Serialização
    def to_json(self): return vars(self)
    @staticmethod
    def from_json(d): return Servico(d["codigo"], d["nome"], d["preco"])

    def __str__(self):
        return f"{self.codigo} - {self.nome} - R$ {self.preco:.2f}"


# ---------- DAO com herança ----------
class ServicoDAO(DAO):
    def __init__(self):
        super().__init__("servicos.json")

    def from_json(self, dic):
        return Servico(dic["codigo"], dic["nome"], dic["preco"])

    # CRUD herdando comportamento do DAO
    def inserir(self, servico):
        self._objetos = self.abrir()
        servico.set_codigo(max((s.get_codigo() for s in self._objetos), default=0) + 1)
        self._objetos.append(servico)
        self.salvar()

    def listar(self):
        return self.abrir()

    def listar_id(self, id):
        return next((s for s in self.abrir() if s.get_codigo() == id), None)

    def atualizar(self, servico):
        self._objetos = self.abrir()
        for i, s in enumerate(self._objetos):
            if s.get_codigo() == servico.get_codigo():
                self._objetos[i] = servico
                break
        self.salvar()

    def excluir(self, servico):
        self._objetos = [s for s in self.abrir() if s.get_codigo() != servico.get_codigo()]
        self.salvar()
