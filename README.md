# Projeto de Análise e Processamento de Linguagem Natural

Este repositório contém notebooks interativos para análise descritiva de dados e processamento de linguagem natural (NLP). Os notebooks fornecem uma abordagem prática para a exploração de dados e técnicas de NLP aplicadas a diferentes conjuntos de dados.

## Estrutura do Repositório

- `descriptive.ipynb` - Notebook com análise descritiva de dados, incluindo estatísticas sumarizadas e visualização.
- `NLP.ipynb` - Notebook focado em técnicas de Processamento de Linguagem Natural, como tokenização, remoção de stopwords, e modelagem de texto.
- `pyproject.toml` - Arquivo de configuração do projeto, contendo informações sobre dependências e ambiente.
- `llm/` - Pacote responsável por operações de processamento de texto utilizando modelos de linguagem.
  - `save_utils.py` - Módulo que gerencia o salvamento e carregamento de dados intermediários.
  - `spell_check.py` - Módulo que aplica correção ortográfica e gramatical em textos utilizando LLM.
- `data/` - Diretório que armazena os arquivos de dados necessários para o processamento.
  - **Observação:** É necessário baixar o arquivo `reviews_processed_llm.json` do Kaggle antes de executar o projeto. O arquivo pode ser encontrado no seguinte link:
    [Kaggle - Reviews Enigma do Medo](https://www.kaggle.com/datasets/jojojmo/reviews-enigma-do-medo-20-12-2024?select=reviews_processed_llm.json)

## Como foi abordada a correção ortográfica

Para escolher o método de correção ortográfica, foram consideradas várias opções, como `pyspellchecker`, `cyhunspell` e `spaCy`. No entanto, essas abordagens apresentaram algumas limitações:

- Dificuldades na instalação e uso do `hunspell` com a biblioteca `cyhunspell`.
- Falta de cobertura de palavras e termos específicos nas bibliotecas disponíveis.
- Correções inadequadas, alterando o significado original das palavras.
- Dificuldade em lidar com a estrutura sintática do texto.

Diante dessas limitações, optou-se por abordar a correção ortográfica utilizando o modelo `llama3.1`. Essa abordagem resolveu os problemas mencionados, mas introduziu um trade-off: a possibilidade de gerar alucinações ou alterar o sentido das frases. Para mitigar esse risco, foram adotadas as seguintes precauções:

1. Construção de um prompt cuidadoso para guiar a correção.
2. Uso de respostas estruturadas no formato JSON para evitar interpretações indesejadas.

Vale ressaltar que este projeto é um experimento, com foco em aprendizado. O uso de um modelo de IA para correção ortográfica é uma alternativa viável, mas exige supervisão para garantir a qualidade dos dados gerados.

## Requisitos

O projeto utiliza `pyproject.toml` para gerenciar dependências. Para instalar os pacotes necessários, utilize:

```bash
pip install .
```

Caso prefira usar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
pip install .
```

## Como Usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/Jojojmo/review-steam-analysis.git
   ```
2. Navegue até o diretório:
   ```bash
   cd review-steam-analysis
   ```
3. Com o Kernel do seu ambiente formado, abra os notebooks `descriptive.ipynb` e `NLP.ipynb` para explorar as análises.

### Utilizando o Pacote `llm`

O pacote `llm` contém utilitários para processamento de texto com modelos de linguagem.

- Para processar e salvar dados corrigidos:
  ```python
  from pathlib import Path
  from llm.spell_check import use_model

  content_path = Path('data/reviews_raw.json')
  file_path = Path('data/reviews_processed_llm.json')
  last_save_file = Path('llm/last_save.txt')

  use_model(content_path, file_path, last_save_file, batch=5, final_range=100)
  ```

