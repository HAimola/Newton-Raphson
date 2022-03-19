#Objetivo: Fazer um programa que ache a raiz a partir do algoritmo da bisseção
#Autor: Heloísa Rades de Souza      Data:18/03/2022

#importar bibliotecas
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

print('''Esta é uma calculadora de raízes pelo método da bisseção
Sua precisão é de 5 casas decimais
Digite seguindo o modelo: x² -2x + 3  -->  x**2 - 2*x +3
!ATENÇÃO: Para funções trigonométricas, digite a abreviação em inglês\n''')

#Ler intervalo e erro informados pelo usuário
funcao = input('Digite a função: ').lower()
a = float(input('Digite o início do intervalo: '))
b = float(input('Digite o final do intervalo: '))
erro = float(input('Digite o erro: '))

x = sp.symbols('x')

#Função para calcular x-barra (média)
def Media(a,b):
    med = (a+b)/2
    return med

#Ler e calcular a função
def f(num, exp):
    resultado = parse_expr(exp)   #Transforma a string informada pelo usuário em uma expressão "resolvível"
    return resultado.subs(x, num)


if f(a, funcao)*f(b, funcao) < 0: #Confere a principal definição para haver uma raíz no intervalo
    while True:   #Loop de repetição infinita
       x0 = Media(a,b)
       
       #Saída apresentando os valores de cada variável e valor de função com 5 casas decimais
       print(f'''a = {a:.5f} | b = {b:.5f} | x = {x0:.5f} | f(a) = {f(a, funcao):.5f} | f(x) = {f(x0, funcao):.5f} | sinal = {f(a, funcao)*f(b, funcao):.5f} | E = {(b-a):.5f}''')
       
       if (b-a) < erro:  #Confere se a diferença intervalo é menor que o erro informado e finaliza o programa
           print(f'{x0:.5f} é a raiz da função')
           break
       else:  #Caso não seja menor, o valor da média é atribuido ao começo ou fim do intervalo, dependendo do valor identificado como "sinal"
           if f(a, funcao)*f(x0, funcao) > 0: 
               a = x0
           else:
               b = x0
else:
    print('Não há raíz para este intervalo')
