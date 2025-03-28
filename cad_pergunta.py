import os

def menu():
    global op
    print("Selecione uma das opcoes:")
    print("1. Listar perguntas")
    print("2. Criar nova pergunta")
    print("3. ...")
    op = int(input())
def escolha():
    global op
    match op:
        case 1:
            print("1. Listar perguntas")
        case 2:
            print("2. Criar nova pergunta")
        case 3:
            print("3. ...")


# print("Bem vindo ao prototipo do pyquiz \nUm site de quiz feito em python \n\n")
menu()
print("----------TESTE--------")
print(op)
escolha()