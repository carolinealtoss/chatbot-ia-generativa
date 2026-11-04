# Importa o serviço de conversa usado pela interface de terminal.
from chatbot_service import ChatbotService


# Recebe perguntas e exibe respostas até o usuário encerrar a aplicação.
def main() -> None:
    chatbot = ChatbotService()
    print("Seu professor de python está pronto! Digite 'sair' para encerrar.")

    try:
        while True:
            question = input("\nVocê: ").strip()
            if question.lower() in {"sair", "exit", "quit"}:
                print("Professor: Até logo!")
                break
            if not question:
                continue

            print(f"\nProfessor: {chatbot.ask(question)}")
    except (EOFError, KeyboardInterrupt):
        print("\nProfessor: Até logo!")


# Inicia a aplicação interativa quando este arquivo é executado diretamente.
if __name__ == "__main__":
    main()
