#Objetivo: Fazer um programa que ache a raiz a partir do algoritmo da falsa posição
#Autor: Heloísa Rades de Souza      Data:18/03/2022

#importar bibliotecas
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

print('''Esta é uma calculadora de raízes pelo método da bisseção
Sua precisão é de 6 casas decimais
Digite seguindo o modelo: x² -2x + 3  -->  x**2 - 2*x +3
!ATENÇÃO: Para funções trigonométricas, digite a abreviação em inglês\n''')

#Ler intervalo e erro informados pelo usuário
funcao = input('Digite a função: ').lower()
a = float(input('Digite o início do intervalo: '))
b = float(input('Digite o final do intervalo: '))
erro1 = float(input('Digite o 1º erro: '))
erro2 = float(input('Digite o 2º erro: '))

x = sp.symbols('x')

#Ler e calcular a função
def f(num, exp):
    resultado = parse_expr(exp)   #Transforma a string informada pelo usuário em uma expressão "resolvível"
    return resultado.subs(x, num)

#Função para calcular x-barra (média)
def Media(a,b):
    med = (a*f(b, funcao)-b*f(a,funcao))/(f(b,funcao)-f(a,funcao))
    return med

#Início do Algoritmo da Falsa Posição
if f(a, funcao)*f(b, funcao) < 0: #Confere a principal definição para haver uma raíz no intervalo
    while True:   #Loop de repetição infinita
       x0 = Media(a,b)
       
       #Saída apresentando os valores de cada variável e valor de função com 5 casas decimais
       print(f'''a = {a:.6f} | b = {b:.6f} | x = {x0:.6f} | f(a) = {f(a, funcao):.6f} | f(x) = {f(x0, funcao):.6f} | sinal = {f(a, funcao)*f(b, funcao):.6f} | E1 = {(b-a):.6f} | E2 = {f(x0, funcao):.6f}''')
       
       if (b-a) < erro1 or abs(f(x0, funcao)) < erro2:  #Confere se a diferença intervalo é menor que o erro informado e finaliza o programa
           print(f'{x0:.6f} é a raiz da função')
           break
       else:  #Caso não seja menor, o valor da média é atribuido ao começo ou fim do intervalo, dependendo do valor identificado como "sinal"
           if f(a, funcao)*f(x0, funcao) > 0: 
               a = x0
           else:
               b = x0
else:
    print('Não há raíz para este intervalo')
