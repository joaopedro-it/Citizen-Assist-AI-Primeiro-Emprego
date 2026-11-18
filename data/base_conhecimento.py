import json
import re
import unicodedata
from orientacao import Orientacao


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("A base deve ser uma lista")
            self.orientacoes = [Orientacao(item) for item in dados]
            print(f"Base carregada: {len(self.orientacoes)} orientacoes.")
        except (OSError, ValueError, TypeError, KeyError) as erro:
            self.orientacoes = []
            print("Nao foi possivel carregar a base:", erro)

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_normalizada = normalizar(pergunta)
        titulo_normalizado = normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            chave_normalizada = normalizar(chave)
            if chave_normalizada.strip() and chave_normalizada in pergunta_normalizada:
                pontos += 3
                continue

            palavras_chave = set(chave_normalizada.split())
            palavras_pergunta = set(pergunta_normalizada.split())
            correspondencias = {
                palavra for palavra in palavras_chave
                if len(palavra) >= 3 and palavra in palavras_pergunta
            }
            if correspondencias:
                pontos += 2 * len(correspondencias)
        for palavra in set(pergunta_normalizada.split()):
            if len(palavra) >= 3 and f" {palavra} " in titulo_normalizado:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted((item for item in resultados if item[0] >= 3), key=lambda x: (-x[0], x[1].id))
