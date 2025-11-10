import json
import os

# ============================================================
# Classe Base - DAO (Data Access Object)
# ============================================================
class DAO:
    def __init__(self, arquivo):
        """
        Inicializa o DAO com o nome do arquivo JSON.
        Exemplo: DAO("clientes.json")
        """
        self._arquivo = arquivo
        self._objetos = []

    # --------------------------------------------------------
    # Métodos auxiliares genéricos
    # --------------------------------------------------------
    def abrir(self):
        """Abre o arquivo JSON e carrega os objetos."""
        self._objetos = []
        if not os.path.exists(self._arquivo):
            return []
        try:
            with open(self._arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if conteudo:
                    lista_dic = json.loads(conteudo)
                    self._objetos = [self.from_json(dic) for dic in lista_dic]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return self._objetos

    def salvar(self):
        """Salva os objetos atuais no arquivo JSON."""
        with open(self._arquivo, "w", encoding="utf-8") as f:
            json.dump([obj.to_json() for obj in self._objetos], f, ensure_ascii=False, indent=4)

    # --------------------------------------------------------
    # Métodos que as subclasses devem implementar
    # --------------------------------------------------------
    def from_json(self, dic):
        """
        Cada DAO específico deve sobrescrever este método
        para retornar o objeto correto.
        Exemplo: return Cliente.from_json(dic)
        """
        raise NotImplementedError("O método from_json() deve ser implementado na subclasse.")

    # --------------------------------------------------------
    # Métodos genéricos (comportamento padrão)
    # --------------------------------------------------------
    def listar(self):
        """Retorna todos os objetos."""
        return self.abrir()

    def listar_id(self, id):
        """Retorna um objeto pelo ID."""
        return next((obj for obj in self.abrir() if getattr(obj, "get_id")() == id), None)

    def inserir(self, obj):
        """Adiciona um novo objeto ao JSON."""
        self._objetos = self.abrir()
        novo_id = max((getattr(o, "get_id")() for o in self._objetos), default=0) + 1
        obj.set_id(novo_id)
        self._objetos.append(obj)
        self.salvar()

    def atualizar(self, obj):
        """Atualiza um objeto existente."""
        self._objetos = self.abrir()
        for i, o in enumerate(self._objetos):
            if getattr(o, "get_id")() == getattr(obj, "get_id")():
                self._objetos[i] = obj
                self.salvar()
                return
        self.salvar()

    def excluir(self, obj):
        """Remove um objeto do arquivo."""
        self._objetos = [o for o in self.abrir() if getattr(o, "get_id")() != getattr(obj, "get_id")()]
        self.salvar()
