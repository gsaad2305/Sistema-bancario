# 🏦 Sistema Bancário em Python — v2

Este repositório contém a **segunda versão** do sistema bancário desenvolvido como parte do **bootcamp de Python da DIO**.  
A aplicação roda no terminal, agora com suporte a **clientes, múltiplas contas, operações de depósito, saque, extrato** e **persistência em banco de dados SQLite3**.

> **Status:** Versão 2 (v2) – sistema mais robusto, modular e persistente.

---

## ✨ Funcionalidades

- **Gerenciamento de clientes**
  - Criação de novos clientes com:
    - CPF  
    - Nome completo  
    - Data de nascimento  
    - Endereço  

- **Gerenciamento de contas**
  - Criação de contas vinculadas a clientes.  
  - Listagem de todas as contas registradas.  

- **Operações bancárias**
  - **Depósito**: valores positivos, adicionados ao saldo da conta e registrados no histórico.  
  - **Saque**: valida saldo disponível e registra a operação no histórico.  
  - **Extrato**: lista todas as transações com **data, tipo e valor**, além do saldo atual.  

- **Persistência em banco de dados**
  - Banco de dados `SQLite3` com duas tabelas:
    - `clientes`: informações pessoais.  
    - `contas`: número da conta, CPF vinculado e saldo.  
  - Carregamento e salvamento automático dos dados.  

- **Menu interativo**
  - `[d]` Depositar  
  - `[s]` Sacar  
  - `[e]` Extrato  
  - `[nu]` Novo Usuário  
  - `[lc]` Listar Contas  
  - `[q]` Salvar dados e sair  

---

## 🧠 Regras de Negócio (resumo)

- Um cliente pode ter **uma ou mais contas**.  
- Cada operação é registrada no **histórico de transações da conta**.  
- Depósitos aceitam apenas valores positivos.  
- Saques só são realizados caso haja saldo suficiente.  
- Os dados são persistidos em **SQLite3** a cada execução.  

---

## 🔄 Melhorias da v1 para v2

| **Versão 1** | **Versão 2 (atual)** |
|--------------|----------------------|
| Sistema simples em memória. | Suporte a **persistência com SQLite3**. |
| Apenas uma conta. | **Múltiplas contas por cliente**. |
| Somente saldo, depósito e saque. | **Criação de clientes, contas, extrato completo e listagem de contas**. |
| Histórico limitado (5 transações). | Histórico detalhado com **todas as operações**. |
| Variáveis globais simples. | Estrutura **orientada a objetos** (Cliente, ContaCorrente, Transação). |
| Menu básico (1,2,3). | Menu mais completo (`d, s, e, nu, lc, q`). |
| Sem tratamento robusto de erros. | Tratamento de **erros e exceções (ValueError, conexões SQLite, etc.)**. |

---

## 🗂️ Estrutura do Projeto

```
.
├── main.py          # Arquivo principal (menu e lógica)
├── cliente.py        # Classe PessoaFisica (nome, CPF, etc.)
├── conta.py          # Classe ContaCorrente
├── transacao.py      # Classes de operações (Depósito, Saque)
├── banco.db          # Banco de dados SQLite (gerado após execução)
```

---

## 👨‍💻 Tecnologias Utilizadas

| **Categoria**        | **Tecnologia** |
|-----------------------|----------------|
| Linguagem            | Python 3 |
| Banco de dados       | SQLite3 (`sqlite3`) |
| Manipulação de paths | `pathlib` |
| Organização de texto | `textwrap` |
| Sistema operacional  | `os` (limpar terminal) |

---

## ▶️ Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-bancario.git
   cd sistema-bancario
   ```

2. Certifique-se de ter o **Python 3** instalado.  

3. Execute o programa:
   ```bash
   python main.py
   ```

4. Use o **menu interativo** para criar clientes, abrir contas e realizar operações.

---

