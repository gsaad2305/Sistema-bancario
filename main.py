import textwrap
from cliente import PessoaFisica
from conta import ContaCorrente
from transacao import Deposito,Saque

def menu():
    menu = """"\n
    ========== Menu ==========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
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
     transacao = Deposito(valor)
     conta = recuperar_contas(cliente)
    except:
        print("Erro na digitação")
    
    if not conta:
        return 
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_conta(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    valor = float(input("Informe o valor do saque: R$ "))
    transacao = Saque(valor)
    conta = recuperar_contas(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)
    
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

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_conta(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


    print("\n=== Cliente criado com sucesso! ===")



def criar_conta(numero_conta, clientes, contas):
   cpf = input("Informe o CPF do cliente: ")
   cliente = filtrar_conta(cpf, clientes)
   if not cliente:
         print("\n@@@ Cliente não encontrado. @@@")
         return
   conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
   contas.append(conta) 
   cliente.adicionar_conta(conta)
   print("\n=== Conta criada com sucesso! ===")
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        
def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        
        if opcao =="d":
            depositar(clientes)
            
        elif opcao =="s":
            sacar(clientes)
        
        elif opcao=="e":
            exibir_extrato(clientes)
        
        elif opcao=="nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,clientes,contas)
            
        elif opcao=="nu":
            criar_cliente(clientes)
            
        elif opcao=="lc":
            listar_contas(contas)
        elif opcao=="q":
            break
        
        else:
            print("\n@@@ Opção inválida, por favor selecione novamente a opção do menu. @@@")

main()