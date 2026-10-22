# Chris IA

Assistente inteligente desenvolvido por Chrinovic  com IBM Granite e Python, capaz de tomar decisões e utilizar ferramentas de forma autônoma.

## Sobre o projeto

Chris IA é um chatbot baseado em inteligência artificial agêntica (Agentic AI), desenvolvido para demonstrar a integração de modelos de linguagem com ferramentas externas.

O assistente analisa as perguntas dos usuários e decide quando utilizar ferramentas para obter informações.

## Funcionalidades

- Conversação com inteligência artificial.
- Consulta de condições meteorológicas em tempo real.
- Pesquisa de informações na internet.
- Seleção automática de ferramentas.
- Histórico de conversa durante a sessão.

## Tecnologias

- Python
- IBM Granite
- IBM watsonx.ai
- Streamlit
- Open-Meteo API
- DuckDuckGo Search

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure a variável de ambiente `IBM_API_KEY` no arquivo `.env` e os demais parâmetros IBM necessários no agente.

Execute:

```bash
streamlit run app.py
```

## Desenvolvedor

**Chris**

Projeto desenvolvido para demonstrar aplicações práticas de inteligência artificial e sistemas baseados em agentes.
