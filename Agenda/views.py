from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.profissional import Profissional, ProfissionalDAO
from models.horario import Horario, HorarioDAO
from datetime import datetime, timedelta

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

    @staticmethod
    def cliente_inserir(nome, email, fone, senha):
        cliente = Cliente(0, nome, email, fone, senha)
        ClienteDAO.inserir(cliente)

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        cliente = Cliente(id, nome, email, fone, senha)
        ClienteDAO.atualizar(cliente)

    @staticmethod
    def cliente_autenticar(email, senha):
        return ClienteDAO.autenticar(email, senha)


    # ----- Serviço -----
    @staticmethod
    def servico_inserir(nome, preco):
        servico = Servico(0, nome, preco)  # id 0 → será atualizado pelo DAO
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

    # ----- Profissional -----
    @staticmethod
    def profissional_inserir(nome, especialidade, email, fone):
        profissional = Profissional(0, nome, especialidade, email, fone)
        ProfissionalDAO.inserir(profissional)

    @staticmethod
    def profissional_listar():
        return ProfissionalDAO.listar()

    @staticmethod
    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, email, fone):
        profissional = Profissional(id, nome, especialidade, email, fone)
        ProfissionalDAO.atualizar(profissional)

    @staticmethod
    def profissional_excluir(id):
        profissional = Profissional(id, "", "", "", "")
        ProfissionalDAO.excluir(profissional)


    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        # Impede agendamento duplicado (mesma data, mesmo profissional)
        horarios = HorarioDAO.listar()
        for h in horarios:
            if (
                h.get_data() == data
                and h.get_id_profissional() == id_profissional
                and h.get_id_cliente() is not None
            ):
                raise ValueError("Este horário já foi agendado por outro cliente.")

        obj = Horario(0, data, confirmado, id_cliente, id_servico, id_profissional)
        HorarioDAO.inserir(obj)

    @staticmethod
    def horario_listar():
        return HorarioDAO.listar()

    @staticmethod
    def horario_listar_id(id):
        return HorarioDAO.listar_id(id)

    @staticmethod
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        obj = Horario(id, data, confirmado, id_cliente, id_servico, id_profissional)
        HorarioDAO.atualizar(obj)

    @staticmethod
    def horario_excluir(id):
        obj = Horario(id, None, False, None, None, None)
        HorarioDAO.excluir(obj)

    # ----- Profissional -----
    @staticmethod
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        ProfissionalDAO.inserir(Profissional(0, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_listar():
        return ProfissionalDAO.listar()

    @staticmethod
    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        ProfissionalDAO.atualizar(Profissional(id, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_excluir(id):
        ProfissionalDAO.excluir(Profissional(id, "", "", "", "", ""))

    @staticmethod
    def profissional_autenticar(email, senha):
        return ProfissionalDAO.autenticar(email, senha)

    @staticmethod
    def abrir_agenda(id_profissional, data, hora_inicio, hora_fim, intervalo):
        hora_atual = datetime.combine(data, hora_inicio)
        hora_limite = datetime.combine(data, hora_fim)
        qtd = 0

        while hora_atual < hora_limite:
            horario = Horario(
                id=0,
                data=hora_atual,
                confirmado=False,
                id_cliente=None,
                id_servico=None,
                id_profissional=id_profissional
            )
            HorarioDAO.inserir(horario)
            hora_atual += timedelta(minutes=intervalo)
            qtd += 1

        return qtd