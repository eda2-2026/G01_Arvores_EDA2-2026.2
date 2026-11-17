# Orquestrador de Processamento de Documentos IA


**Disciplina:** Estruturas de Dados 2 — 2026.2  
**Trabalho:** Trabalho 3 — Aplicação Integrada de Árvores (Min-Heap, Árvore AVL e Árvore Rubro-Negra) 

## Aluno

| Matrícula | Nome |
|---|---|
| 20/2046040 | Dara Maria Barbosa de Sousa |

## Vídeo de Apresentação

Assista ao vídeo explicativo detalhando as decisões arquiteturais do projeto, a implementação das três estruturas de dados sob a metodologia TDD e a demonstração do fluxo na interface Streamlit:

[Apresentação do Projeto](https://youtu.be/Jg-lQ0E_TJs)



## Descrição do projeto
Este projeto implementa um simulador interativo de um pipeline de microsserviços voltado para o processamento assíncrono de documentos (como extração via OCR e LLM). Ele foi construído com foco acadêmico e arquitetural para demonstrar a aplicação prática e a interação entre três estruturas de dados avançadas: **Min-Heap**, **Árvore Red-Black** e **Árvore AVL**.

A interface visual, desenvolvida em Streamlit, simula um painel Kanban em tempo real, permitindo visualizar como os dados trafegam pela memória do sistema durante as etapas de enfileiramento, alocação de processamento e armazenamento em cache.



## Estruturas de Dados Utilizadas e Arquitetura

O núcleo do sistema orquestra o ciclo de vida dos documentos através de três módulos principais, cada um utilizando a estrutura matemática ideal para o seu cenário de uso:

### 1. Fila de Prioridade: `Min-Heap`
*   **Objetivo:** Gerenciar os documentos que dão entrada no sistema e aguardam processamento.
*   **Por que Min-Heap?** Em um pipeline real, arquivos menores ou com SLA (urgência) mais crítico precisam furar a fila. A Min-Heap garante que a extração do documento mais prioritário ocorra sempre no topo em tempo $O(1)$, enquanto as inserções e rebalanceamentos (`heapify_up` / `heapify_down`) custam apenas $O(\log n)$.
*   **Regra de Negócio:** A prioridade é um cálculo matemático combinando o peso do arquivo (MB) e sua tag de urgência (1 a 5). Quanto menor o valor numérico, maior a prioridade.

### 2. Pool de Workers (Processos Ativos): `Árvore Red-Black`
*   **Objetivo:** Rastrear os nós de processamento (*Workers*) que estão atualmente ocupados executando tarefas pesadas (ex: inferência de IA).
*   **Por que Red-Black?** *Workers* pegam documentos e concluem tarefas a cada milissegundo. Isso gera um cenário de **altíssima dinamicidade**, com um volume imenso de operações de *Write/Delete*. A Árvore Red-Black, com seu sistema de recoloração (nós vermelhos e pretos), exige menos rotações estruturais que a AVL para se manter balanceada, garantindo inserções e remoções rápidas em $O(\log n)$ sem sobrecarregar a CPU com reestruturações da árvore.

### 3. Cache / Histórico de Processados: `Árvore AVL`
*   **Objetivo:** Atuar como um banco de dados em memória para registrar os documentos já finalizados e prevenir reprocessamento de arquivos duplicados.
*   **Por que AVL?** Diferente do *Pool* de processos, o histórico de documentos sofre inserções apenas no final do ciclo, mas é **consultado massivamente** toda vez que um novo documento chega (para checar se ele já existe). Como a AVL é estritamente balanceada (fator de balanceamento -1, 0 ou 1), ela oferece a melhor performance matemática possível para buscas $O(\log n)$, sendo a estrutura ideal para *Read-Heavy operations*.



## Estrutura do Projeto

```text
doc_orchestrator/
├── app.py                            # Ponto de entrada do dashboard Streamlit
├── style.css                         # Estilização 
├── requirements.txt                  # Dependências do projeto
├── src/
│   ├── __init__.py
│   ├── entities.py                   # Entidades de domínio (Document, Worker)
│   ├── orchestrator.py               # Motor que integra as 3 estruturas
│   └── structures/
│       ├── __init__.py
│       ├── avl_tree.py               # Algoritmo da Árvore AVL (Rotações)
│       ├── min_heap.py               # Algoritmo da Min-Heap
│       └── red_black_tree.py         # Algoritmo da Árvore Red-Black
└── tests/
    ├── __init__.py
    ├── test_avl_tree.py              # Validação dos 4 casos de desbalanceamento
    ├── test_min_heap.py              # Validação de extração prioritária
    ├── test_orchestrator.py          # Validação do fluxo de integração
    └── test_red_black_tree.py        # Validação das regras de cores e ponteiros

```


## Como Executar Localmente

O projeto requer Python 3.10 ou superior. Recomenda-se a utilização de um ambiente virtual.

**1. Clone o repositório e acesse a pasta:**

```powershell
git clone <url-do-repositorio>
cd G01_Arvores_EDA2-2026.2

```

**2. Crie e ative o ambiente virtual (Exemplo para Windows PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```

**3. Instale as dependências:**

```powershell
pip install -r requirements.txt

```

**4. Inicie a aplicação visual:**

```powershell
streamlit run app.py

```

O navegador abrirá automaticamente no endereço `http://localhost:8501`.

---

## Como Rodar os Testes (TDD)

Toda a lógica matemática das árvores foi desenvolvida utilizando a metodologia de Test-Driven Development (TDD) para garantir a integridade dos ponteiros, regras de balanceamento e orquestração.

Para rodar a suíte completa de testes unitários e de integração, execute na raiz do projeto:

```powershell
pytest tests/ -v

```

---

## Fluxo de Utilização (Como usar o Dashboard)

A barra lateral esquerda fornece os controles de operação manual:

1. **Inserir Documento:** Gera um documento aleatório (com peso e urgência distintos) e tenta adicioná-lo ao sistema. O motor fará uma busca $O(\log n)$ na AVL; se não for duplicado, ele entra na Min-Heap.
2. **Alocar Worker:** Simula a inicialização de um *background job*. O motor extrai $O(1)$ o documento mais urgente da Min-Heap e o insere em $O(\log n)$ na Árvore Red-Black atrelando a um operário digital. O UI exibirá a cor real do nó (Vermelho ou Preto) calculada pela árvore no momento.
3. **Finalizar Processo:** Escolhe um *Worker* ativo aleatoriamente, faz o *soft-delete* dele na Red-Black e insere os metadados do documento no Cache Estrito da Árvore AVL, sinalizando o fim do ciclo.

## Referências
* CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. Algoritmos: Teoria e Prática. 3. ed. Rio de Janeiro: Elsevier, 2012. Capítulos 12, 13 e 14.

* SERRANO, Maurício. Material didático da disciplina Estruturas de Dados 2. Universidade de Brasília (UnB FGA), 2026.

* PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponível em: https://docs.python.org/3/

* STREAMLIT INC. Streamlit Documentation. Disponível em: https://docs.streamlit.io/
