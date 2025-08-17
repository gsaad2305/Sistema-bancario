# 🏦 Sistema Bancário em Python — v1 (`banco.py`)

Este repositório contém o **primeiro sistema bancário** que desenvolvi como parte de um **desafio do botcamp de python da Dio**.  
A aplicação roda no terminal e permite **depositar**, **sacar** e **consultar saldo**, mantendo um **histórico das últimas transações**.

> **Status:** Primeira versão (v1) – focada no funcionamento básico e nas regras principais do desafio.

---

## ✨ Funcionalidades

- **Consultar saldo e transações recentes**
  - Exibe o saldo atual.
  - Lista as **últimas 5 transações** com **data/hora**, **tipo** e **valor**.

- **Depositar**
  - Solicita o valor, atualiza o saldo e registra no histórico.

- **Sacar**
  - Realiza saques respeitando:
    - **Limite diário de saques:** até **3** saques por dia.
    - **Limite por saque:** até **R$ 1.000,00**.
    - **Saldo disponível**.
  - Cada saque é registrado no histórico.

- **Menu interativo (loop)**
  - `1` — Saldo e últimas transações  
  - `2` — Depósito  
  - `3` — Saque

---

## 🧠 Regras de Negócio (resumo)

- `limite_diario = 3`: no máximo três saques por dia.  
- `limite = 1000`: valor máximo permitido por saque.  
- Validações básicas para **saldo insuficiente** e **estouro de limite**.  
- As transações são armazenadas em uma lista de dicionários, incluindo **tipo**, **valor** e **timestamp**.

---

## 🗂️ Estrutura (principais variáveis e funções)

- **Variáveis**
  - `saldo`: valor atual da conta.
  - `limite_diario`: quantidade máxima de saques por dia.
  - `saques_realizados`: contador de saques efetuados.
  - `limite`: teto de valor por saque.
  - `trasacao`: lista com o histórico (últimas operações).

- **Funções**
  - `mostrar_o_saldo()`: mostra saldo + últimas 5 transações.
  - `depositar()`: lê o valor, soma ao saldo e registra no histórico.
  - `sacar()`: valida limites/saldo, subtrai e registra no histórico.
  - Laço principal com menu de opções para interação via terminal.

---
