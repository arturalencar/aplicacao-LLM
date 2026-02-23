# Gerador de Receitas com Inteligência Artificial 🍳

Este repositório contém uma aplicação web interativa que utiliza Inteligência Artificial para gerar receitas culinárias personalizadas. O usuário informa o prato que deseja comer e suas restrições alimentares (alergias), e a aplicação retorna uma receita sob medida.

## Equipe do Projeto

- Carlos Artur Alencar Cruz
- Guilherme Inácio Santos Paes
- Irwing Felipe Pereira Vieira
- Raphael Matos da Silva Gonçalves
- Renan Nunes Andrade Sampaio

## 💻 Sobre o Projeto

A aplicação integra o framework **Streamlit** (para a construção do front-end e interface de usuário) com a API do **Google Gemini** (modelo `gemini-2.5-flash`). O objetivo é demonstrar como criar prompts dinâmicos a partir de inputs do usuário em uma interface limpa e reativa, lidando com chamadas de API de IA generativa.

### Funcionalidades da Interface (Front-end)

- **Inputs Textuais:** Campos dedicados para a entrada do nome da receita desejada e das alergias/restrições.
- **Geração Dinâmica:** Um botão de ação que constrói o prompt estruturado e aciona a API apenas quando solicitado.
- **Renderização de Texto Formatado:** Exibição da receita gerada pela IA, aproveitando o suporte nativo do Streamlit para formatação (Markdown) retornada pelo modelo.

## 🛠️ Tecnologias Utilizadas

- **Python 3:** Linguagem base da aplicação.
- **Streamlit:** Framework para a construção rápida da interface web.
- **Google GenAI SDK (`google-genai`):** Biblioteca oficial mais recente para comunicação com a API do Gemini.
- **OS (Built-in):** Gerenciamento de variáveis de ambiente para segurança da chave de API.

## 🚀 Como Executar

### 1. Pré-requisitos

- Ter o Python instalado.
- Obter uma chave de API (API Key) gratuita no [Google AI Studio](https://aistudio.google.com/).

### 2. Instalação das Dependências

Execute o comando abaixo no seu terminal para instalar o Streamlit e o SDK do Gemini:

```bash
pip install streamlit google-genai
```

### 3. Configurando a Chave de API

O código busca a chave de API em uma variável de ambiente por questões de segurança. Antes de rodar o código, você precisa exportar a sua chave no terminal:

No Linux/macOS/WSL:

```bash
export GEMINI_API_KEY="cole_sua_chave_aqui"
```

No Windows (PowerShell):

```bash
$env:GEMINI_API_KEY="cole_sua_chave_aqui"
```

### 4. Rodando a Aplicação

Inicie o servidor local do Streamlit executando o arquivo principal:

```bash
python -m streamlit run gerador-de-receitas.py
```

(Ou apenas ```streamlit run gerador-de-receitas.py```, caso o atalho já esteja no seu PATH).

Acesse a interface no seu navegador através do endereço gerado no terminal (geralmente ```http://localhost:8501```).

### 🧠 Estrutura da Lógica

- **Inicialização do Cliente:** O cliente da API do Gemini é instanciado uma única vez no início do script, capturando a variável de ambiente de forma segura.

- **Coleta de Dados:** O front-end captura as intenções do usuário (receita e alergias).

- **Engenharia de Prompt:** Quando o botão é clicado, os inputs são interpolados em uma string de instrução clara para a IA.

- **Requisição e Resposta:** O prompt é enviado ao modelo gemini-2.5-flash (otimizado para velocidade e tarefas de texto), e a resposta é renderizada em um subcabeçalho na tela.
