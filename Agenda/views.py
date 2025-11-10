from models.cliente import Cliente, ClienteDAO
from models.profissional import Profissional, ProfissionalDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from datetime import datetime, timedelta

class View:

    # ----------- Auxiliares -----------

    @staticmethod
    def _validar_email_unico(email, id_excluido=None):
        email_lower = email.lower().strip()

        # Bloqueia qualquer e-mail que contenha "admin"
        if "admin" in email_lower:
            raise ValueError("E-mails contendo 'admin' são reservados e não podem ser usados.")

        # Verifica duplicidade em clientes
        for c in ClienteDAO.listar():
            if c.get_id() != id_excluido and c.get_email().lower() == email_lower:
                raise ValueError("Já existe um cliente com este e-mail.")

        # Verifica duplicidade em profissionais
        for p in ProfissionalDAO.listar():
            if p.get_id() != id_excluido and p.get_email().lower() == email_lower:
                raise ValueError("Este e-mail já está em uso por outro profissional.")

    @staticmethod
    def _verificar_horarios(id_obj, tipo):
        for h in HorarioDAO.listar():
            if (tipo == "cliente" and h.get_id_cliente() == id_obj) or \
               (tipo == "profissional" and h.get_id_profissional() == id_obj):
                raise ValueError(f"Não é possível excluir {tipo} com horários vinculados.")

    # ----------- Cliente -----------

    @staticmethod
    def cliente_inserir(nome, email, fone, senha):
        View._validar_email_unico(email)
        ClienteDAO.inserir(Cliente(0, nome, email, fone, senha))

    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        View._validar_email_unico(email, id_excluido=id)
        ClienteDAO.atualizar(Cliente(id, nome, email, fone, senha))

    @staticmethod
    def cliente_listar(): return ClienteDAO.listar()
    @staticmethod
    def cliente_listar_id(id): return ClienteDAO.listar_id(id)

    @staticmethod
    def cliente_excluir(id):
        View._verificar_horarios(id, "cliente")
        cliente = ClienteDAO.listar_id(id)
        if cliente:
            ClienteDAO.excluir(cliente)

    @staticmethod
    def cliente_autenticar(email, senha):
        return ClienteDAO.autenticar(email, senha)

    # ----------- Profissional -----------

    @staticmethod
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        View._validar_email_unico(email)
        ProfissionalDAO.inserir(Profissional(0, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_listar(): return ProfissionalDAO.listar()
    @staticmethod
    def profissional_listar_id(id): return ProfissionalDAO.listar_id(id)

    @staticmethod
    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        View._validar_email_unico(email, id_excluido=id)
        ProfissionalDAO.atualizar(Profissional(id, nome, especialidade, conselho, email, senha))

    @staticmethod
    def profissional_excluir(id):
        View._verificar_horarios(id, "profissional")
        profissional = ProfissionalDAO.listar_id(id)
        if profissional:
            ProfissionalDAO.excluir(profissional)

    @staticmethod
    def profissional_autenticar(email, senha):
        return ProfissionalDAO.autenticar(email, senha)

    # ----------- Serviço -----------

    @staticmethod
    def servico_inserir(nome, preco): ServicoDAO().inserir(Servico(0, nome, preco))
    @staticmethod
    def servico_listar(): return ServicoDAO().listar()
    @staticmethod
    def servico_listar_id(id): return ServicoDAO().listar_id(id)
    @staticmethod
    def servico_atualizar(id, nome, preco): ServicoDAO().atualizar(Servico(id, nome, preco))
    @staticmethod
    def servico_excluir(id): ServicoDAO().excluir(Servico(id, "", 0.0))

    # ----------- Horário -----------

    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        for h in HorarioDAO.listar():
            if (
            h.get_data() == data
            and h.get_id_profissional() == id_profissional
            and h.get_id_cliente() is not None
        ):
                raise ValueError("Este horário já foi agendado por outro cliente.")
        HorarioDAO.inserir(Horario(0, data, confirmado, id_cliente, id_servico, id_profissional))

    @staticmethod
    def horario_listar(): return HorarioDAO.listar()

    @staticmethod
    def horario_listar_por_profissional(id_profissional):
        horarios = [h for h in HorarioDAO.listar() if h.get_id_profissional() == id_profissional]
        return horarios
    
    @staticmethod
    def horario_listar_id(id): return HorarioDAO.listar_id(id)
    @staticmethod
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        HorarioDAO.atualizar(Horario(id, data, confirmado, id_cliente, id_servico, id_profissional))
    @staticmethod
    def horario_excluir(id): HorarioDAO.excluir(Horario(id, None, False, None, None, None))

    # ----------- Abrir Agenda -----------

    @staticmethod
    def abrir_agenda(id_profissional, data, hora_inicio, hora_fim, intervalo):
        hora_atual = datetime.combine(data, hora_inicio)
        hora_limite = datetime.combine(data, hora_fim)
        while hora_atual < hora_limite:
            HorarioDAO.inserir(Horario(0, hora_atual, False, None, None, id_profissional))
            hora_atual += timedelta(minutes=intervalo)
