class FluxoUsuario:
    def __init__(self):
        self.usuarios = {}

    def set_estado(self, chat_id, estado):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]["estado"] = estado

    def get_estado(self, chat_id):
        return self.usuarios.get(chat_id, {}).get("estado")

    def resetar(self, chat_id):
        self.usuarios.pop(chat_id, None)

    def set_nome(self, chat_id, nome):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]["nome"] = nome

    def get_nome(self, chat_id):
        return self.usuarios.get(chat_id, {}).get("nome", "Não informado")

    def set_telefone(self, chat_id, telefone):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]["telefone"] = telefone

    def get_telefone(self, chat_id):
        return self.usuarios.get(chat_id, {}).get("telefone", "Não informado")

    def set_servico(self, chat_id, servico):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]["servico"] = servico

    def get_servico(self, chat_id):
        return self.usuarios.get(chat_id, {}).get("servico", "Não informado")

    def todos_chat_ids(self):
        return [chat_id for chat_id in self.usuarios if isinstance(chat_id, int)]

fluxo = FluxoUsuario()
