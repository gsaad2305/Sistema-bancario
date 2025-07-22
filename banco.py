import datetime
saldo = 0
limite_diario = 3
saques_realizados = 0
limite = 1000
trasacao = []
print("=====Bem vindo ao Bankdaas=====")
def mostrar_o_saldo():
    print(f"O saldo da sua conta é:  R${saldo:.2f}")
    for t in trasacao[-5:]:
        print(f"Data:{t['data']} - Tipo: {t['tipo']} - Valor: R${t['valor']:.2f}")
    
def depositar():
    global saldo
    deposito = float(input("Quanto deseja depositar? R$"))
    saldo += deposito
    print(f"Depósito realizado com sucesso o seu saldo agora é: R${saldo}")
    trasacao.append({
        "tipo":"Depósito",
        "valor":deposito,
        "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
def sacar():
    global saldo, saques_realizados
    valor = float(input(f"Digite o valor a ser sacado: R$"))
    if saques_realizados > limite_diario:
        print("Você ultrapassou o limite diario de saques")
        return
    elif valor> saldo or valor >= limite:
        print("Saldo insuficiente ou valor acima do limite")
    else:
        saldo -= valor
        saques_realizados +=1
        print(f"Você sacou R${valor} agora seu saldo é: R${saldo}")
        trasacao.append({
         "tipo":"Saque",
         "valor":sacar,
         "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
         })

while True:
    print("""Digite uma das opções abaixo:
          1-Saldo da conta e saques ou depositos feitos 
          2-Para deposito
          3-Para saques""")
    opção = int(input("Digite uma opção: "))
    if opção ==1:
        mostrando_saldo = mostrar_o_saldo()
    elif opção ==2:
        depositando = depositar()
    elif opção ==3:
        sacando = sacar()
    else:
        print('Não existe essa opção')