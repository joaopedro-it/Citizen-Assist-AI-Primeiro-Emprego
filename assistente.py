import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path

CAMPOS = ["data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou", "tentativas", "tempo_segundos"]


def contem_dados_pessoais(texto):
    # Bloqueio conservador exigido no enunciado: @ ou 8+ digitos no total.
    return "@" in texto or len(re.findall(r"\d", texto)) >= 8


class Assistente:
    def __init__(self, nome, base, caminho="data/historico.json"):
        self.nome = nome
        self.base = base
        self.caminho = Path(caminho)
        self.historico = []
        self.facilidade = []
        try:
            notas = json.loads(Path("data/avaliacoes.json").read_text(encoding="utf-8"))
            if isinstance(notas, list):
                self.facilidade = [n for n in notas if type(n) is int and 1 <= n <= 5]
        except (OSError, ValueError):
            pass
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
            if isinstance(dados, list):
                self.historico = dados
        except (OSError, ValueError):
            print("Historico ausente ou invalido; iniciando novo historico.")

    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, inicio):
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": bool(encontrou),
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1)
        }
        self.historico.append(registro)
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            self.caminho.write_text(json.dumps(self.historico, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as erro:
            print("Nao foi possivel salvar historico:", erro)

    def perguntar(self):
        tentativas = 0
        inicio = time.time()
        while True:
            pergunta = input("\nDigite sua duvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if not pergunta:
                print("Digite uma pergunta ou 0 para voltar.")
                continue
            if contem_dados_pessoais(pergunta):
                print("Atencao: nao digite CPF, telefone ou e-mail. Reescreva sua duvida.")
                continue  # Nao armazena dado pessoal.
            tentativas += 1
            resultados = self.base.buscar(pergunta)
            if not resultados:
                print("Nao encontrei uma orientacao. Tente outras palavras ou navegue por categoria.")
                self.registrar("pergunta", pergunta, None, False, False, tentativas, inicio)
                return
            pontos, melhor = resultados[0]
            print(f"Confianca: {'ALTA' if pontos >= 6 else 'MEDIA'} ({pontos} pontos)")
            melhor.exibir()
            if len(resultados) > 1:
                print("Alternativas:")
                for pontos_alt, alternativa in resultados[1:3]:
                    print(f" - {alternativa.titulo} ({pontos_alt} pontos)")
            ajudou = self.confirmar_ajuda()
            self.registrar("pergunta", pergunta, melhor, True, ajudou, tentativas, inicio)
            return

    def confirmar_ajuda(self):
        while True:
            resposta = input("Essa orientacao respondeu sua duvida? (s/n, 0 para voltar): ").strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            if resposta == "0":
                return None
            print("Digite s, n ou 0.")

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            print("\nCATEGORIAS")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i}. {categoria}")
            escolha = input("Categoria (0 para voltar): ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(categorias):
                print("Opcao invalida.")
                continue
            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f"\n{categoria}")
                for i, orientacao in enumerate(orientacoes, 1):
                    print(f"{i}. {orientacao.titulo}")
                opcao = input("Orientacao (0 para voltar): ").strip()
                if opcao == "0":
                    break
                if not opcao.isdigit() or not 1 <= int(opcao) <= len(orientacoes):
                    print("Opcao invalida.")
                    continue
                inicio = time.time()
                orientacao = orientacoes[int(opcao) - 1]
                orientacao.exibir()
                ajudou = self.confirmar_ajuda()
                self.registrar("categoria", orientacao.titulo, orientacao, True, ajudou, 1, inicio)

    def indicadores(self):
        total = len(self.historico)
        if not total:
            print("\nNenhum atendimento registrado.")
            return
        encontrados = sum(bool(r.get("encontrou")) for r in self.historico)
        avaliados = [r for r in self.historico if r.get("ajudou") is not None]
        ajudaram = sum(r.get("ajudou") is True for r in avaliados)
        media_tempo = sum(float(r.get("tempo_segundos", 0)) for r in self.historico) / total
        media_tentativas = sum(int(r.get("tentativas", 0)) for r in self.historico) / total
        print(f"\nAtendimentos: {total}")
        print(f"Resposta encontrada: {100 * encontrados / total:.1f}%")
        print(f"Ajudou (entre respostas avaliadas): {100 * ajudaram / len(avaliados):.1f}%" if avaliados else "Ajudou: sem avaliacoes")
        print(f"Tempo medio: {media_tempo:.1f} segundos")
        print(f"Tentativas por atendimento: {media_tentativas:.1f}")
        print(f"Facilidade (1 a 5): {sum(self.facilidade)/len(self.facilidade):.1f}" if self.facilidade else "Facilidade: ainda nao avaliada nesta sessao")
        print("Duvidas sem solucao:")
        for r in self.historico:
            if not r.get("encontrou"):
                print(" -", r.get("pergunta", ""))

    def exportar_csv(self, destino="data/atendimentos.csv"):
        try:
            caminho = Path(destino)
            caminho.parent.mkdir(parents=True, exist_ok=True)
            with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS, extrasaction="ignore")
                escritor.writeheader()
                escritor.writerows(self.historico)
            print("CSV exportado para", caminho)
        except OSError as erro:
            print("Erro ao exportar CSV:", erro)

    def avaliar_facilidade(self):
        while True:
            nota = input("Facilidade de uso (1 a 5, 0 para pular): ").strip()
            if nota == "0":
                return
            if nota in ("1", "2", "3", "4", "5"):
                self.facilidade.append(int(nota))
                # Persistir nota agregavel sem identificar usuario.
                destino = Path("data/avaliacoes.json")
                try:
                    anteriores = json.loads(destino.read_text(encoding="utf-8")) if destino.exists() else []
                    if not isinstance(anteriores, list):
                        anteriores = []
                    anteriores.append(int(nota))
                    destino.write_text(json.dumps(anteriores, indent=2), encoding="utf-8")
                except (OSError, ValueError):
                    print("Nao foi possivel salvar a avaliacao.")
                return
            print("Digite 1, 2, 3, 4, 5 ou 0.")
