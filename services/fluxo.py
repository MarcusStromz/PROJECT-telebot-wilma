class FluxoUsuario:
    def __init__(self):
        self.usuarios = {}

    def set_estado(self, chat_id, estado):
        self.usuarios[chat_id] = estado

    def get_estado(self, chat_id):
        return self.usuarios.get(chat_id)

    def resetar(self, chat_id):
        self.usuarios.pop(chat_id, None)

fluxo = FluxoUsuario()
