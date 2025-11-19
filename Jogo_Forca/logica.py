import random
import string

class JogoForca:  #Lógica do jogo da forca.
    def __init__(self, lista_palavras=None, max_erros=6, palavra_escolhida=None):
        self._palavras_padrao = lista_palavras or [
            "AMIZADE", "CRIANCA", "CORACAO", "ARTE", "MUSICA", "FLORES",
            "VERAO", "PRAIA", "SABEDORIA", "FAMILIA", "FUTURO", "SONHO"
        ]

        self.max_erros = max_erros
        self.palavra_escolhida = palavra_escolhida.upper() if palavra_escolhida else None
        self.reiniciar()


    def escolher_palavra(self):  #Escolher uma palavra aleatória
        self.palavra_escolhida = random.choice(self._palavras_padrao).upper()


    def reiniciar(self, palavra=None):  #Recomeçar o jogo do zero com uma nova palavra
        if palavra:
            self.palavra_escolhida = palavra.upper()
        else:
            self.escolher_palavra()  #sempre escolhe outra

        self.letras_certas = set()
        self.letras_erradas = set()
        self.erros = 0
        self.finalizado = False


    def tentar_letra(self, letra):  #Validar e processar o chute de uma letra
        if self.finalizado:
            return {'ok': False, 'mensagem': 'O jogo já terminou. Reinicie para jogar novamente.'}

        if not letra or not isinstance(letra, str):
            return {'ok': False, 'mensagem': 'Entrada inválida.'}

        letra = letra.strip().upper()

        if len(letra) != 1 or letra not in string.ascii_uppercase:
            return {'ok': False, 'mensagem': 'Digite apenas uma letra A-Z.'}

        if letra in self.letras_certas or letra in self.letras_erradas:
            return {'ok': False, 'mensagem': f'Você já usou "{letra}".'}

        if letra in self.palavra_escolhida:
            self.letras_certas.add(letra)
            if self.venceu():
                self.finalizado = True
            return {'ok': True, 'mensagem': 'Acertou!!!'}
        else:
            self.letras_erradas.add(letra)
            self.erros += 1
            if self.perdeu():
                self.finalizado = True
            return {'ok': False, 'mensagem': 'Errou! ):'}


    def palavra_formatada(self):  #Retornar a palavra com traços e letras reveladas
        return " ".join([c if c in self.letras_certas else "_" for c in self.palavra_escolhida])


    def venceu(self):  #Retornar True se todas as letras foram descobertas
        return set(self.palavra_escolhida).issubset(self.letras_certas)


    def perdeu(self):  #Retornar True se os erros atingiram o limite
        return self.erros >= self.max_erros


    def tentativas_restantes(self):
        return self.max_erros - self.erros


    def letras_erradas_formatadas(self):
        return " ".join(sorted(self.letras_erradas))


    def revelar_palavra(self):
        return self.palavra_escolhida