class Orientacao:
    def __init__(self, dados):
        for campo in ("id", "categoria", "titulo", "palavras_chave", "resposta", "documentos", "onde", "fonte", "verificado_em"):
            if campo not in dados:
                raise ValueError(f"Campo ausente: {campo}")
            setattr(self, campo, dados[campo])

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("Documentos / requisitos:")
        for documento in self.documentos:
            print(" -", documento)
        print("Onde:", self.onde)
        print("Fonte:", self.fonte)
        print("Verificado em:", self.verificado_em)
        if self.verificado_em == "PENDENTE":
            print("ATENCAO: fonte ainda nao conferida pela equipe.")
        print("Aviso: este assistente NAO e um canal oficial.\n")
