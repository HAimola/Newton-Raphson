#fazer um algoritmo que encripte e decodifique mensagens
from random import randint

#definição de variáveis e listas
numeros = []
cripLetras = []
c = 0
#definição da tupla base do alfabeto
ALFABETO = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Ç', ' ')

#criação da lista chave para a codificação em relação alfabeto
while c != 27:
    letra = randint(0,26)   #gera numeros aleatórios
    if letra not in numeros:    #confere se o número ainda n está na lista
        numeros.append(letra)
        cripLetras.append(ALFABETO[letra])  #cria a lista de letras baseada na lista de números e no alfabeto
        c+=1
cripLetras.append(' ')
    
#cria um dicionário de criptografia relacionando o ALFABETO e a lista de letras randômicas
chaveCriptografar = {f"{ALFABETO[0]}":f"{cripLetras[0]}"}
for d in range(1,len(cripLetras)):
    chaveCriptografar[f"{ALFABETO[d]}"] = f"{cripLetras[d]}"
    
#cria um dicionário de descriptografia relacionando a lista de letras randômicas e o ALFABETO
chaveDescriptografar = {f"{cripLetras[0]}":f"{ALFABETO[0]}"}
for d in range(1,len(cripLetras)):
    chaveDescriptografar[f"{cripLetras[d]}"] = f"{ALFABETO[d]}"

mensagem1 = str(input('Digite a mensagem a ser criptografada: ')).upper()    #lê a mensagem do usuário

criptografia = ''
for m in mensagem1:      #troca as letras da mensagem
    criptografia = criptografia + chaveCriptografar[m]
print(f'A mensagem criptografada é: {criptografia}')

mensagem2 = str(input('Digite a mensagem a ser criptografada: ')).upper()

descriptografia = ''
for m in mensagem2:      #troca as letras da mensagem
    descriptografia = descriptografia + chaveDescriptografar[m]
print(f'A mensagem criptografada é: {descriptografia}')
