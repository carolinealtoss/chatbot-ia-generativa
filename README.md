# Chatbot com IA Generativa

Chatbot de terminal para responder perguntas sobre programação em Python usando LangChain e um modelo da OpenAI. As conversas podem ser rastreadas no LangSmith quando essa opção é habilitada.

## Requisitos

- Python 3.10 ou superior
- Uma chave de API da OpenAI
- (Opcional) Uma chave de API do LangSmith para rastrear as conversas

## Instalação e configuração

1. Crie e ative um ambiente virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

   Se a instalação no Windows tentar compilar uma dependência e falhar por falta do Microsoft Visual C++ 14+, instale o Microsoft C++ Build Tools ou use uma versão do Python com wheel binário disponível para essa dependência.

3. Crie o arquivo local `.env` a partir do exemplo:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Edite `.env` e substitua `your-openai-api-key` pela sua chave da OpenAI. O modelo padrão é `gpt-4o-mini`; altere `OPENAI_MODEL` se quiser usar outro modelo disponível na sua conta.

5. (Opcional) Para rastrear execuções no LangSmith, configure `LANGSMITH_TRACING=true`, preencha `LANGSMITH_API_KEY` e ajuste `LANGSMITH_PROJECT`. Com o rastreamento desligado, a chave do LangSmith não é necessária.

O arquivo `.env` contém credenciais locais e não deve ser compartilhado ou enviado ao Git.

## Executar

```powershell
python app.py
```

Digite uma pergunta em português. O chatbot mantém o histórico durante a execução; digite `sair`, `exit` ou `quit` para encerrar.

## Exemplos

**Pergunta:** Como criar uma lista em Python?

**Resposta ilustrativa:**

```text
Você pode criar uma lista usando colchetes. Por exemplo:
frutas = ["maçã", "banana", "laranja"]

As listas mantêm os itens em ordem e podem ser alteradas. Para adicionar um
elemento, use frutas.append("uva"). Acesse um item pelo índice, como
frutas[0], lembrando que os índices começam em zero.
```

**Pergunta:** Como adiciono um item à lista que acabei de criar?

**Resposta ilustrativa:** Use `frutas.append("uva")`. Como o chatbot envia o histórico da conversa ao modelo, ele pode entender que a pergunta se refere à lista da pergunta anterior.

As respostas são geradas pelo modelo e podem variar entre execuções.

## Testes

Os testes unitários usam um modelo simulado e não precisam de uma chave de API:

```powershell
python -m unittest discover -s tests -v
```
