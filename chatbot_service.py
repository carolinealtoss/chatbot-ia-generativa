# Carrega os valores de .env antes de o LangChain ler as opções de rastreamento.
import os

from dotenv import load_dotenv
from langchain_core.pydantic_v1 import SecretStr
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI


load_dotenv()


# Gerencia o prompt, a chamada ao modelo e o histórico da conversa em memória.
class ChatbotService:
    # Configura o modelo e inicia o histórico da conversa vazio.
    def __init__(self, model: Runnable | None = None) -> None:
        self._history: list[BaseMessage] = []
        self._load_settings()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Você é um assistente especializado em programação Python. "
                    "Responda em português com explicações claras e detalhadas. "
                    "Inclua exemplos de código quando forem úteis e explique como funcionam.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )

        if model is None:
            if not self._openai_api_key:
                raise ValueError(
                    "A variável OPENAI_API_KEY não está configurada. "
                    "Crie um arquivo .env com sua chave da OpenAI."
                )
            if self._langsmith_tracing and not self._langsmith_api_key:
                raise ValueError(
                    "LANGSMITH_TRACING está habilitado, mas LANGSMITH_API_KEY "
                    "não foi configurada."
                )

            model = ChatOpenAI(
                api_key=SecretStr(self._openai_api_key),
                model=self._openai_model,
                temperature=0.2,
            )

        self._chain = prompt | model

    # Envia a pergunta com o histórico anterior e guarda a troca após sucesso.
    def ask(self, question: str) -> str:
        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("A pergunta não pode estar vazia.")

        response = self._chain.invoke(
            {"history": self._history, "question": cleaned_question}
        )
        if not isinstance(response, AIMessage) or not isinstance(response.content, str):
            raise TypeError("O modelo retornou uma resposta em formato inesperado.")

        self._history.extend(
            [
                HumanMessage(content=cleaned_question),
                AIMessage(content=response.content),
            ]
        )
        return response.content

    # Limpa as mensagens anteriores para iniciar uma nova conversa.
    def reset_conversation(self) -> None:
        self._history.clear()

    # Lê as configurações da aplicação diretamente das variáveis de ambiente.
    def _load_settings(self) -> None:
        self._openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self._openai_model = (
            os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
        )
        self._langsmith_tracing = (
            os.getenv("LANGSMITH_TRACING", "false").strip().lower()
            in {"1", "true", "yes", "on"}
        )
        self._langsmith_api_key = os.getenv("LANGSMITH_API_KEY", "").strip() or None
        self._langsmith_project = (
            os.getenv("LANGSMITH_PROJECT", "chatbot-python").strip()
            or "chatbot-python"
        )
