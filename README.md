# Kubeo Corpus Annotator: Ferramenta de anotação e visualização linguística na língua Kubeo

---

Este projeto foi desenvolvido como trabalho final para a disciplina de **Língua e Programação** no **semestre de 2025.2** da **Universidade de Brasília (UnB)**.

O trabalho foi orientado pelo **Professor Dr. CLAUDIO CORREA E CASTRO GONCALVES**.

---

## Sobre o Projeto

O **Kubeo Corpus Annotator** é uma aplicação web simples, construída em **Python** e **Flask**, dedicada à visualização, busca e anotação morfológica de sentenças na língua Kubeo (família Tukano Oriental).

### Principais Funcionalidades

* **Visualização Interlinear:** Exibição das frases Kubeo com glosa (tradução) e POS (Classe Gramatical) alinhados verticalmente (estilo interlinear).
* **Busca em Tempo Real:** Mecanismo de busca por forma e lema e glosa(tradução), realizado diretamente na página inicial.
* **Anotação Dinâmica (CRUD):**
    * **Criação (Adicionar):** Interface dinâmica que altera os campos de anotação (Modo, Tempo, Aspecto, Gênero, Contável) com base na Classe Gramatical (Verbo vs. Nome) selecionada.
    * **Persistência de Dados:** O novo conteúdo é salvo diretamente no arquivo TSV do corpus.
* **Estrutura de Dados:** Utiliza **Dataclasses** em Python para modelar o corpus, frases e palavras, garantindo tipagem e robustez.

### Fonte dos Dados

Os dados linguísticos e a análise morfológica (Modo, Aspecto, etc.) são baseados em materiais acadêmicos fornecidos, principalmente a **Tese de Doutorado** de Thiago Costa Chacon (2012) e o **Resumo Tipológico** da língua Kubeo.

---
## Instalação e Execução

Para rodar este projeto localmente, siga os passos abaixo no seu terminal (PowerShell ou Bash):

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.x** e o `git` instalados em seu sistema.

### 2. Clonar o Repositório

```bash
git clone https://github.com/PedroPauloFreire/Projeto_LeP_Corpus_Kubeo.git
```

### 3. Configurar o Ambiente e Instalar Dependências

Crie e ative o ambiente virtual para isolar as bibliotecas do projeto e instale o Flask:

```bash
python3 -m venv venv
```
```bash
.\venv\Scripts\Activate
```
```bash
pip install Flask
```
