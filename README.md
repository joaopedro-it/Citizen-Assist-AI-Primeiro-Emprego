# Citizen Assist AI — Primeiro Emprego

Assistente desenvolvido em Python para orientar jovens sobre documentação, primeiro emprego, estágios e formação profissional.

Projeto desenvolvido para a **Global Solution 2026.2 da FIAP**, na disciplina de **Pensamento Computacional e Automação com Python**.

O Citizen Assist AI funciona diretamente pelo terminal e utiliza um sistema de busca baseado em regras e palavras-chave. Não utiliza inteligência artificial generativa e não representa um canal oficial do governo.

## Integrantes

- João Pedro Soler — RM 569725
- Erick Banhos de Castro — RM 572131
- Cauã Paes Vivaldo — RM 569906

## Objetivos de Desenvolvimento Sustentável (ODS)

**ODS 4 — Educação de Qualidade:** facilitar o acesso a informações sobre formação, qualificação e oportunidades educacionais.

**ODS 8 — Trabalho Decente e Crescimento Econômico:** auxiliar jovens na preparação para o primeiro emprego, no entendimento de documentos e no acesso a informações profissionais.

## Objetivo do projeto

O Citizen Assist AI foi desenvolvido para ajudar jovens que possuem dúvidas sobre documentação, estágios, formação profissional e ingresso no mercado de trabalho.

A solução permite consultar orientações de maneira simples, sem necessidade de cadastro ou conexão com serviços externos.

O sistema também registra os atendimentos, permite avaliar as respostas e gera indicadores para analisar seu funcionamento.

## Tecnologias utilizadas

- Python 3.10+
- Programação Orientada a Objetos (POO)
- JSON para armazenamento de informações
- CSV para exportação dos atendimentos
- Biblioteca `re` para tratamento de textos
- Biblioteca `unicodedata` para normalização de palavras
- Biblioteca `datetime` para registro de datas
- Biblioteca `pathlib` para manipulação de arquivos
- VS Code para desenvolvimento

O projeto utiliza bibliotecas nativas do Python, sem necessidade de instalar dependências externas.

## Como executar

1. Instale o Python 3.10 ou superior.
2. Baixe ou clone o repositório.
3. Abra a pasta do projeto no VS Code.
4. Abra o terminal na pasta onde está localizado o arquivo `main.py`.
5. Execute o comando:

```bash
python main.py
```

No Windows, também é possível utilizar:

```bash
py main.py
```

## Menu principal

Ao executar o programa, o usuário encontra as seguintes opções:

**1. Fazer pergunta**

Permite digitar uma dúvida. O sistema analisa a pergunta e busca uma orientação correspondente na base de conhecimento.

**2. Navegar por categorias**

Permite consultar as orientações disponíveis por assunto.

**3. Indicadores**

Apresenta estatísticas dos atendimentos realizados.

**4. Exportar CSV**

Gera o arquivo `data/atendimentos.csv` com os registros dos atendimentos.

**0. Sair**

Encerra o programa e oferece a possibilidade de avaliar a facilidade de uso.

## Estrutura do projeto

```text
citizen-assist-ai/
├── main.py
├── assistente.py
├── base_conhecimento.py
├── orientacao.py
├── README.md
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    ├── avaliacoes.json
    └── atendimentos.csv
```

### Organização do código

**main.py**

Responsável pela execução do programa, apresentação do menu e integração entre as classes.

**assistente.py**

Contém a classe `Assistente`, responsável pelo atendimento, histórico, avaliações, indicadores e exportação CSV.

**base_conhecimento.py**

Contém a classe `BaseConhecimento`, responsável pelo carregamento do JSON, normalização dos textos, pontuação e busca das orientações.

**orientacao.py**

Contém a classe `Orientacao`, que representa cada registro da base de conhecimento.

**data/base_conhecimento.json**

Armazena as orientações utilizadas pelo assistente, organizadas em categorias.

**data/historico.json**

Armazena os registros dos atendimentos realizados.

**data/avaliacoes.json**

Armazena as notas de facilidade de uso atribuídas pelos usuários.

## Funcionamento do algoritmo de busca

O sistema utiliza um algoritmo de pontuação para identificar a orientação mais adequada à pergunta.

Primeiramente, o texto é normalizado:

- Conversão para letras minúsculas.
- Remoção de acentos.
- Remoção de pontuação.
- Padronização dos espaços.

Depois, o programa compara a pergunta com as palavras-chave e os títulos das orientações cadastradas.

### Critérios de pontuação

- **+3 pontos:** expressão-chave completa encontrada na pergunta.
- **+2 pontos por palavra:** correspondência parcial de palavras-chave com três ou mais caracteres, quando a expressão completa não é encontrada.
- **+1 ponto:** palavra da pergunta com três ou mais caracteres encontrada no título da orientação.

### Níveis de confiança

- **ALTA:** 6 pontos ou mais.
- **MÉDIA:** entre 3 e 5 pontos.
- **Sem orientação:** pontuação inferior a 3.

Os resultados são organizados por pontuação, utilizando tuplas no formato `(pontos, orientacao)`.

Em caso de empate, a orientação com menor ID possui prioridade.

O programa também pode apresentar até duas orientações alternativas.

## Segurança e tratamento de erros

O sistema possui mecanismos básicos para evitar o armazenamento de informações pessoais.

Perguntas que contenham o caractere `@` ou oito ou mais dígitos são recusadas antes do registro do atendimento.

O programa também trata entradas inválidas, problemas no carregamento dos arquivos e situações em que nenhuma orientação é encontrada.

Esses mecanismos são preventivos e não substituem soluções completas de proteção de dados.

## Base de conhecimento

A base de conhecimento utiliza um arquivo JSON com orientações relacionadas a:

- Documentação pessoal
- Primeiro emprego
- Estágios
- Formação e qualificação profissional

Cada orientação possui informações como ID, categoria, título, palavras-chave, resposta, documentos necessários, local de atendimento, fonte e data de verificação.

Entre as referências utilizadas estão portais e instituições públicas, como:

- Gov.br
- Ministério do Trabalho e Emprego
- Receita Federal
- Tribunal Superior Eleitoral
- Ministério da Educação
- Inep
- Escola Virtual de Governo
- Lei nº 11.788/2008 — Lei do Estágio

As informações devem ser conferidas nas fontes oficiais. Registros marcados como `PENDENTE` ainda não possuem verificação concluída.

## Testes e validação

Foram registrados **11 atendimentos** no histórico do sistema, incluindo testes realizados pela equipe e por pessoas externas.

Os testes envolveram perguntas livres, navegação por categorias, avaliação das respostas e análise do comportamento do algoritmo.

### Indicadores obtidos

| Indicador | Resultado |
|---|---|
| Total de atendimentos | 11 |
| Respostas encontradas | 7 |
| Respostas não encontradas | 4 |
| Taxa de respostas encontradas | 63,6% |
| Avaliações positivas | 5 de 9 registros avaliados |
| Percentual de avaliações positivas | 55,6% |
| Tempo médio por atendimento | 48,7 segundos |
| Tentativas médias por atendimento | 1,0 |

### Problemas identificados

Durante os testes, algumas perguntas relacionadas ao título de eleitor não retornaram orientações, apesar de o assunto estar presente na base de conhecimento.

Também foi identificada uma entrada inválida, contendo apenas o número `1`.

### Melhoria realizada

Foi identificado e corrigido um problema de carregamento do arquivo JSON da base de conhecimento.

Após a correção, o sistema passou a localizar orientações que anteriormente não eram encontradas, incluindo perguntas relacionadas ao título de eleitor.

Os testes demonstraram a importância de verificar a configuração dos arquivos e avaliar diferentes formas de formular perguntas.

### Limitações observadas

O sistema depende das palavras-chave cadastradas na base de conhecimento e pode apresentar dificuldades com perguntas que utilizam termos diferentes dos previstos.

Além disso, o tempo de atendimento depende da interação do usuário e não apenas do processamento do algoritmo.

## Indicadores e exportação

O Citizen Assist AI calcula automaticamente:

- Quantidade de atendimentos.
- Percentual de respostas encontradas.
- Percentual de avaliações positivas.
- Tempo médio de atendimento.
- Média de tentativas por atendimento.
- Dúvidas sem solução.
- Média das avaliações de facilidade de uso, quando disponíveis.

Os atendimentos podem ser exportados para CSV, permitindo análises posteriores em planilhas.

## Possíveis melhorias futuras

- Ampliar a base de conhecimento.
- Melhorar a interpretação de diferentes formulações de perguntas.
- Desenvolver uma interface gráfica.
- Implementar testes automatizados.
- Aprimorar a proteção de dados pessoais.
- Atualizar periodicamente as fontes das orientações.

## Vídeo de apresentação

O vídeo apresenta a proposta do projeto, as tecnologias utilizadas, a arquitetura do sistema, o algoritmo de busca e uma demonstração das funcionalidades implementadas.

**Link do vídeo no YouTube:** (https://youtu.be/DCrjg4qDofM)

## Conclusão

O desenvolvimento do Citizen Assist AI permitiu aplicar conceitos de programação em Python, orientação a objetos, manipulação de arquivos JSON e CSV, estruturas de dados, tratamento de erros e algoritmos de busca.

Os testes demonstraram que o sistema consegue localizar orientações e registrar atendimentos, além de gerar indicadores úteis para avaliar seu desempenho.

O projeto também permitiu identificar limitações e realizar melhorias a partir dos resultados obtidos.

Dessa forma, o Citizen Assist AI representa uma solução educacional que utiliza a programação para facilitar o acesso de jovens a informações importantes para sua formação e entrada no mercado de trabalho.