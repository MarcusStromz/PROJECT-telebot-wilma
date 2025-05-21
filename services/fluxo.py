class FluxoUsuario:
    def __init__(self):
        self.usuarios = {}
        self.servicos = {}

    def set_estado(self, chat_id, estado):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]['estado'] = estado

    def get_estado(self, chat_id):
        return self.usuarios.get(chat_id, {}).get('estado')

    def set_servico(self, chat_id, servico):
        if chat_id not in self.usuarios:
            self.usuarios[chat_id] = {}
        self.usuarios[chat_id]['servico'] = servico

    def get_servico(self, chat_id):
        return self.usuarios.get(chat_id, {}).get('servico')

    def resetar(self, chat_id):
        self.usuarios.pop(chat_id, None)

fluxo = FluxoUsuario()
