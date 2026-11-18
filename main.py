from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI - Primeiro Emprego", base)
    print("\nCitizen Assist AI - Primeiro Emprego")
    print("Aviso: este assistente NAO e um canal oficial.")
    while True:
        print("\n1. Fazer pergunta")
        print("2. Navegar por categorias")
        print("3. Indicadores")
        print("4. Exportar CSV")
        print("0. Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.avaliar_facilidade()
            assistente.exportar_csv()
            print("Ate logo!")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
