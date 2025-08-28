import textwrap
import os
from cliente import PessoaFisica
from conta import ContaCorrente
from transacao import Deposito,Saque

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
def menu():
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

def salvar_dados(clientes, contas):
    # Salva os clientes
    with open("clientes.txt", "w") as arquivo_clientes:
        for cliente in clientes:
            linha = f"{cliente.cpf};{cliente.nome};{cliente.data_nascimento};{cliente.endereco}\n"
            arquivo_clientes.write(linha)
    print("\n✅ Dados de clientes salvos com sucesso!")
    
    # Salva as contas
    with open("contas.txt", "w") as arquivo_contas:
        for conta in contas:
            linha = f"{conta.numero};{conta.cliente.cpf};{conta.saldo}\n"
            arquivo_contas.write(linha)
    print("✅ Dados de contas salvos com sucesso!")
     
# main.py

def carregar_dados():
    clientes = []
    contas = []

    # Carrega os clientes
    try:
        with open("clientes.txt", "r") as arquivo_clientes:
            for linha in arquivo_clientes:
                # Ignora linhas em branco
                if not linha.strip():
                    continue

                cpf, nome, data_nascimento, endereco = linha.strip().split(';')
                cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
                clientes.append(cliente)
        print("✅ Clientes carregados com sucesso!")
    except FileNotFoundError:
        print("❌ Arquivo de clientes não encontrado. Iniciando com dados vazios.")
    
    # Carrega as contas
    try:
        with open("contas.txt", "r") as arquivo_contas:
            for linha in arquivo_contas:
                # Corrigido: Verifica se a linha não está vazia e se tem 3 partes
                partes = linha.strip().split(';')
                if len(partes) != 3:
                    print(f"❌ Erro de formato na linha: '{linha.strip()}' - ignorando.")
                    continue
                
                numero_str, cpf_cliente, saldo_str = partes
                
                numero = int(numero_str)
                saldo = float(saldo_str)
                
                # Encontra o cliente correspondente para vincular a conta
                cliente = filtrar_conta(cpf_cliente, clientes)
                if cliente:
                    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
                    conta._saldo = saldo # Acessa a propriedade privada para manter o saldo
                    contas.append(conta)
                    cliente.adicionar_conta(conta)
        print("✅ Contas carregadas com sucesso!")
    except FileNotFoundError:
        print("❌ Arquivo de contas não encontrado. Iniciando com dados vazios.")

    return clientes, contas

def main():
    clientes, contas = carregar_dados()
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

main()