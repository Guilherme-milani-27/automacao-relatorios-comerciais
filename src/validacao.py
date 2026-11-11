
# src/validacao.py

class ErroValidacao(Exception):
    """
    Representa um erro estrutural nos arquivos de entrada.
    """

    def __init__(self, mensagem, detalhes):
        super().__init__(mensagem)
        self.detalhes = detalhes
