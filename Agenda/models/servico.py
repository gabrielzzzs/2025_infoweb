import json

class Servico:
    def __init__(self, codigo, nome, preco):
        self.codigo, self.nome, self.preco = codigo, nome, preco

    # Getters e Setters (compatibilidade com outras telas)
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


class ServicoDAO:
    _arquivo = "servicos.json"

    @classmethod
    def _abrir(cls):
        try:
            with open(cls._arquivo, "r", encoding="utf-8") as f:
                return [Servico.from_json(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def _salvar(cls, servicos):
        with open(cls._arquivo, "w", encoding="utf-8") as f:
            json.dump([s.to_json() for s in servicos], f, ensure_ascii=False, indent=4)

    # CRUD
    @classmethod
    def inserir(cls, servico):
        servicos = cls._abrir()
        servico.set_codigo(max((s.get_codigo() for s in servicos), default=0) + 1)
        servicos.append(servico)
        cls._salvar(servicos)

    @classmethod
    def listar(cls):
        return cls._abrir()

    @classmethod
    def listar_id(cls, id):
        return next((s for s in cls._abrir() if s.get_codigo() == id), None)

    @classmethod
    def atualizar(cls, servico):
        servicos = cls._abrir()
        for i, s in enumerate(servicos):
            if s.get_codigo() == servico.get_codigo():
                servicos[i] = servico
                break
        cls._salvar(servicos)

    @classmethod
    def excluir(cls, servico):
        servicos = [s for s in cls._abrir() if s.get_codigo() != servico.get_codigo()]
        cls._salvar(servicos)
