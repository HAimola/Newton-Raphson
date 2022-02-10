#fazer um algoritmo que encripte e decodifique mensagens - por Heloísa Rades de Souza
from random import randint
from time import sleep

#definição de variáveis e listas
numeros = []
cripLetras = []
c = 0
comando = 4
str_comandos = 'Para utilizar a codificadora digite:\n      1: Criptografar uma mensagem\n      2: Decriptografar uma mensagem\n      3: Saber a chave de encriptação\n      0: Parar o programa'

#definição da tupla base do alfabeto
ALFABETO = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Ç', ' ')

#criação da lista chave para a codificação em relação alfabeto
while c != 28:
    letra = randint(0,27)   #gera numeros aleatórios
    if letra not in numeros:    #confere se o número ainda n está na lista
        numeros.append(letra)
        cripLetras.append(ALFABETO[letra])  #cria a lista de letras baseada na lista de números e no alfabeto
        c+=1
    
#cria um dicionário de criptografia relacionando o ALFABETO e a lista de letras randômicas
chaveCriptografar = {f"{ALFABETO[0]}":f"{cripLetras[0]}"}
for d in range(1,len(cripLetras)):
    chaveCriptografar[f"{ALFABETO[d]}"] = f"{cripLetras[d]}"
    
#cria um dicionário de descriptografia relacionando a lista de letras randômicas e o ALFABETO
chaveDescriptografar = {f"{cripLetras[0]}":f"{ALFABETO[0]}"}
for d in range(1,len(cripLetras)):
    chaveDescriptografar[f"{cripLetras[d]}"] = f"{ALFABETO[d]}"


#possibilidade de digitar várias mensagens
while comando != 0:
    print(str_comandos)
    comando=int(input('Digite o que deseja realizar? - '))
    
    if comando >=0 and comando<=3:
        
        if comando == 1:
            mensagem1 = str(input('Digite a mensagem a ser criptografada: ')).upper()    #lê a mensagem do usuário
            criptografia = ''
            for m in mensagem1:      #troca as letras da mensagem
                criptografia = criptografia + chaveCriptografar[m]
            sleep(1)
            print(f'A mensagem criptografada é: {criptografia}')

        elif comando == 2:
            mensagem2 = str(input('Digite a mensagem a ser criptografada: ')).upper()

            descriptografia = ''
            for m in mensagem2:      #troca as letras da mensagem
                descriptografia = descriptografia + chaveDescriptografar[m]
            sleep(1)
            print(f'A mensagem criptografada é: {descriptografia}')
            
        elif comando == 3:
            sleep(1)
            print(chaveCriptografar)
            
        elif comando == 0:
            sleep(1)
            print('Obrigado por utilizar nosso programa!')
        else:
            print('Comando inválido, digite novamente')
    sleep(3)