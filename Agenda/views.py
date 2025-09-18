from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO

class View:
    @staticmethod
    def cliente_inserir(nome, email, fone):
        cliente = Cliente(0, nome, email, fone)
        ClienteDAO.inserir(cliente)

    @staticmethod
    def cliente_listar():
        return ClienteDAO.listar()

    @staticmethod
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone):
        cliente = Cliente(id, nome, email, fone)
        ClienteDAO.atualizar(cliente)

    @staticmethod
    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "")
        ClienteDAO.excluir(cliente)

from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO

class View:
    # ----- Cliente -----
    @staticmethod
    def cliente_inserir(nome, email, fone):
        cliente = Cliente(0, nome, email, fone)
        ClienteDAO.inserir(cliente)

    @staticmethod
    def cliente_listar():
        return ClienteDAO.listar()

    @staticmethod
    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone):
        cliente = Cliente(id, nome, email, fone)
        ClienteDAO.atualizar(cliente)

    @staticmethod
    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "")
        ClienteDAO.excluir(cliente)

    # ----- Serviço -----
    @staticmethod
    def servico_inserir(nome, preco):
        servico = Servico(0, nome, preco)  # id 0 → será sobrescrito no DAO
        dao = ServicoDAO()
        dao.inserir(servico)

    @staticmethod
    def servico_listar():
        dao = ServicoDAO()
        return dao.listar()

    @staticmethod
    def servico_listar_id(id):
        dao = ServicoDAO()
        return dao.listar_id(id)

    @staticmethod
    def servico_atualizar(id, nome, preco):
        servico = Servico(id, nome, preco)
        dao = ServicoDAO()
        dao.atualizar(servico)

    @staticmethod
    def servico_excluir(id):
        servico = Servico(id, "", 0.0)
        dao = ServicoDAO()
        dao.excluir(servico)

