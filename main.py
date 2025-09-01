import textwrap
import os
from cliente import PessoaFisica
from conta import ContaCorrente
from transacao import Deposito,Saque
import sqlite3
from pathlib import Path

#Limpa a tela a cada operação
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu():
    #Menu de opções
    menu = """"\n
    ========== Menu ==========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [lc] Listar Contas
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def filtrar_conta(cpf, clientes):
            clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
            return clientes_filtrados[0] if clientes_filtrados else None
 
def recuperar_contas(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas. @@@")
        return None
    return cliente.contas[0]     

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_conta(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    try:
      valor = float(input("Informe o valor do depósito: R$ "))
      
      if valor <=0:
         print("❌Valor inválido. O depósito deve ser positivo.")
         return
      transacao = Deposito(valor)
      conta = recuperar_contas(cliente)
      if not conta:
         return 
      cliente.realizar_transacao(conta, transacao)
    except  ValueError:
       print("\n@@@ Erro na digitação. Por favor insera um valor númerico")
    except Exception as e:
        print(f"\n@@@ Ocorreu um erro inesperado: {e} @@@")

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_conta(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado. Cpf invalido ou inexistente.  @@@")
        return
    try:
     valor = float(input("Informe o valor do saque: R$ "))
     transacao = Saque(valor)
     conta = recuperar_contas(cliente)
     if not conta:
        return
     cliente.realizar_transacao(conta, transacao)
    except ValueError:
       print("\n@@@ Erro na digitação. Por favor insera um valor númerico")
       
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_conta(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    conta = recuperar_contas(cliente)
    
    if not cliente:
        return
    print("\n================ Extrato ================")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = ("\n@@@ Não foram realizadas transações. @@@")
    else:
        for transacao in transacoes:
            extrato+= f"\n{transacao['data']} - {transacao['tipo']} - R$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")
    
##Cria o cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_conta(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ")
    
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)

    print("\n=== ✅ Cliente criado com sucesso! ===")
    return novo_cliente

def criar_conta(cliente,contas,numero_conta):
   numero_conta = len(contas) + 1
   conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
   contas.append(conta)
   cliente.adicionar_conta(conta)
   print("\n=== ✅ Conta criada com sucesso! === ")
   
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        
        
#Conecta ao banco de dados
def conectar_banco():
    #Informando onde o arquivo de banco de dados ficará localizado
    ROOT_PATH = Path(__file__).parent
    caminho_banco = ROOT_PATH / 'banco.db'
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    
    #Cria a tabela de clientes com nome, data_nascimento, endereco
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS clientes (
                       cpf TEXT PRIMARY KEY, 
                       nome TEXT NOT NULL, 
                       data_nascimento TEXT,
                       endereco TEXT
                   );
                   ''')
    #Cria a tabela de contas com o  numero da conta, cpf do cliente e o saldo na conta.
    cursor.execute('''
                   CREATE TABLE IF NOT  EXISTS contas(
                       numero INTEGER PRIMARY KEY,
                       cpf_cliente TEXT NOT NULL,
                       saldo REAL NOT NULL,
                       FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf)
                       );
                       ''')
    conexao.commit()
    return conexao,cursor


def salvar_dados(clientes, contas):
    #Salva os dados no banco de dados ao final
    conexao,cursor = conectar_banco()
    cursor.execute("DELETE FROM clientes")
    cursor.execute("DELETE FROM contas")
    
    for cliente in clientes:
        cursor.execute("INSERT INTO clientes (cpf,nome,data_nascimento, endereco) VALUES (?,?,?,?);", (cliente.cpf, cliente.nome, cliente.data_nascimento, cliente.endereco))
        
    for conta in contas:
        cursor.execute("INSERT INTO contas (numero, cpf_cliente, saldo) VALUES (?,?,?);", (conta.numero, conta.cliente.cpf, conta.saldo))
        
    conexao.commit()
    conexao.close()
    print("Dados salvos com sucesso.")

def carregar_dados():
    #Carrega os dados do banco de dados, caso esteja registrado no banco de dados
    clientes = []
    contas = []
    
    try:
        conexao, cursor = conectar_banco()
    except sqlite3.OperationalError:
        print("❌ Não foi possivel conectar ao banco de dados")
        return clientes,contas
    cursor.execute("SELECT cpf,nome,data_nascimento, endereco FROM clientes;")
    clientes_salvos = cursor.fetchall()
    
    for cpf,nome,data_nascimento, endereco in clientes_salvos:
        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes.append(cliente)
        
    cursor.execute("SELECT numero, cpf_cliente, saldo FROM contas;")
    contas_salvas = cursor.fetchall()
    
    for numero, cpf_cliente, saldo in contas_salvas:
        cliente = filtrar_conta(cpf_cliente, clientes)
        if cliente:
            conta = ContaCorrente(cliente=cliente, numero=numero)
            conta._saldo = saldo
            contas.append(conta)
            cliente.adicionar_conta(conta)
    conexao.close()
    print("✅ Dados carregados com sucesso.")
    return clientes, contas

def main():
    clientes,contas = carregar_dados()
    while True:
        opcao = menu()
        limpar_tela()
        
        if opcao =="d":
            depositar(clientes)
            
        elif opcao =="s":
            sacar(clientes)
        
        elif opcao=="e":
            exibir_extrato(clientes)
    
        elif opcao=="nu":
            novo_cliente = criar_cliente(clientes)
            if novo_cliente:
                numero_conta = len(contas) + 1
                criar_conta(novo_cliente, contas, numero_conta)
            
        elif opcao=="lc":
            listar_contas(contas)
        elif opcao=="q":
            salvar_dados(clientes, contas)
            break
        
        else:
            print("\n@@@ Opção inválida, por favor selecione novamente a opção do menu. @@@")
        input("\n--- Pressione ENTER para continuar... ---")
main()