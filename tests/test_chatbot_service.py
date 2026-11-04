# Importa utilitários de teste e componentes do LangChain.
import unittest

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from chatbot_service import ChatbotService


# Verifica o serviço sem realizar chamadas à API da OpenAI.
class ChatbotServiceTests(unittest.TestCase):
    # Cria um modelo simulado que captura prompts para verificar o histórico.
    def setUp(self) -> None:
        self.prompts = []

        def fake_response(prompt_value):
            # Captura o prompt e retorna uma resposta previsível sem acessar a rede.
            self.prompts.append(prompt_value.to_messages())
            return AIMessage(content="Resposta de teste")

        self.chatbot = ChatbotService(model=RunnableLambda(fake_response))

    # Confirma que a próxima chamada ao modelo recebe as mensagens anteriores.
    def test_ask_keeps_conversation_history(self) -> None:
        self.assertEqual(self.chatbot.ask("Como criar uma lista?"), "Resposta de teste")
        self.chatbot.ask("Como adicionar um item?")

        prior_messages = self.prompts[1]
        self.assertTrue(
            any(
                isinstance(message, HumanMessage)
                and message.content == "Como criar uma lista?"
                for message in prior_messages
            )
        )
        self.assertTrue(
            any(
                isinstance(message, AIMessage)
                and message.content == "Resposta de teste"
                for message in prior_messages
            )
        )

    # Rejeita perguntas vazias antes de chamar o modelo.
    def test_ask_rejects_empty_question(self) -> None:
        with self.assertRaises(ValueError):
            self.chatbot.ask("   ")

        self.assertEqual(self.prompts, [])

    # Confirma que limpar o histórico remove mensagens da próxima chamada.
    def test_reset_conversation_clears_history(self) -> None:
        self.chatbot.ask("Primeira pergunta")
        self.chatbot.reset_conversation()
        self.chatbot.ask("Nova conversa")

        self.assertFalse(
            any(
                isinstance(message, HumanMessage)
                and message.content == "Primeira pergunta"
                for message in self.prompts[1]
            )
        )


# Permite executar os testes diretamente pelo interpretador Python.
if __name__ == "__main__":
    unittest.main()
