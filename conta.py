from abc import ABC, abstractmethod
from datetime import datetime
from transacao import Saque
import textwrap
class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo        
        
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia
    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo = self.saldo
        execedeu_saldo = valor > saldo
        
        if execedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            
        elif valor>0:
            self._saldo -=valor
            print("\n=== ✅ Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ A operação falhou! Valor inválido. @@@")
            
        return False
    
    def depositar(self,valor):
        if valor>0:
            self._saldo += valor
            print("\n=== ✅ Deposito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ A operação falhou! Valor inválido. @@@")
            return False
        
    
class ContaCorrente(Conta):
    def __init__(self, numero,cliente, limite =1000, limite_saque = 5):
        super().__init__(numero,cliente)
        self._limite = limite
        self._limite_saque = limite_saque
        
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"]== Saque.__name__]
        )
        
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saque > self._limite_saque
        
        if excedeu_limite:
            print("\n@@@ Operação falhou! Valor do saque excedeu o limite de R$ 1000. @@@")
            
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número de saques excedeu o limite. @@@")
            
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
Agência:\t\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t\t{self.cliente.nome}"""    
            
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo":transacao.__class__.__name__,
                "valor":transacao.valor,
                "data":datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )