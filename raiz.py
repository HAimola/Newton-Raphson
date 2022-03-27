from enum import Enum, auto
from typing import Callable, Union
import math

import sys
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd


class Metodo(Enum):
    BISSECAO = auto()
    FALSA_POSICAO = auto()
    NEWTON_RAPHSON = auto()


x = sp.Symbol("x")


def media(a: float, b: float, met: Metodo, f: Callable = None, prec: float = 15):
    if met == Metodo.BISSECAO:
        return (a + b) / 2
    elif met == Metodo.FALSA_POSICAO:
        return (a * f(b) - b * f(a)) / (f(b) - f(a))


def acabou(a: float, b: float = 0, met: Metodo = None, f: Callable = None, erros: list[float] = None):
    assert isinstance(met, Metodo)
    if met == Metodo.BISSECAO:
        return abs((a - b) / 2) <= erros[0]

    if met == Metodo.FALSA_POSICAO:
        assert len(erros) == 1 or len(erros) == 2

        if len(erros) == 2:
            erros[1] = erros[0]

        e1 = erros[0]
        e2 = erros[1]

        return abs(f(a)) < e2 or abs(f(b)) < e2 or (b - a) < e1 or abs(f(media(a, b, met, f))) < e2

    if met == Metodo.NEWTON_RAPHSON:
        return abs(f(a)) < erros[0]


def main(plot: bool = False) -> tuple[sp.Float, list[sp.Float]]:
    print("Esta é uma calculadora de raízes"
          "Digite seguindo o modelo: x² -2x + 3  -->  x**2 - 2*x +3"
          "!ATENÇÃO: Para funções trigonométricas, digite a abreviação em inglês\n")

    print("Escolha o método para utilizar: \n"
          "[1] Bisseção\n"
          "[2] Falsa Posição\n"
          "[3] Newton-Raphson\n")

    met_num = int(input("Método: "))
    assert 0 < met_num <= 3, "Método inválido"
    met = Metodo(met_num)

    func = sp.parse_expr(input('Digite a função: ').lower())
    erros = []
    menor_erro = 0

    if met == Metodo.BISSECAO:
        a = float(input('Digite o início do intervalo: '))
        b = float(input('Digite o final do intervalo: '))
        erros.append(float(input('Digite o erro: ')))
        erros.append(0)
        menor_erro = erros[0]
    elif met == Metodo.FALSA_POSICAO:
        a = float(input('Digite o início do intervalo: '))
        b = float(input('Digite o final do intervalo: '))
        erros.append(float(input('Digite o 1º erro: ')))
        erros.append(float(input('Digite o 2º erro: ')))
        menor_erro = min(erros[0], erros[1])
    else:
        b = float(input('Digite o primeiro X: '))
        a = 0
        erros.append(float(input('Digite o erro: ')))
        erros.append(0)
        menor_erro = erros[0]

    precision = math.ceil(abs(math.log(menor_erro, 10)) + abs(math.log(b, 10)) + 2)
    f = lambda num: sp.Float(func.subs(x, num), precision)
    a = sp.Float(a, precision)
    b = sp.Float(b, precision)

    assert a < b, "Intervalo Inválido!"
    assert abs(a) > erros[0] or abs(b) > erros[1], "Erro 1 muito grande!"

    if met != Metodo.NEWTON_RAPHSON:
        table = pd.DataFrame(columns=["a", "b", "x", "f(a)", "f(b)", "f(x)", "sinal", "E1", "E2"])

        if f(a) * f(b) > 0:
            print('Não há raíz para este intervalo')
            return

        while not acabou(a, b, met, f, erros):
            x0 = media(a, b, met, f)

            table = table.append(pd.Series([a, b, x0, f(a), f(b), f(x0), math.copysign(1, f(a) * f(b)), round(b - a, precision),
                           f(x0)], index=table.columns), ignore_index=True)

            # Caso não seja menor, o valor da média é atribuido ao começo ou fim do intervalo, dependendo do valor identificado como "sinal"
            if f(a) * f(x0) > 0:
                a = sp.Float(x0, precision)
            else:
                b = sp.Float(x0, precision)


    else:  # Se for Newton-Raphson
        x0 = b
        # Cria uma tabela para impressão de variáveis
        table = pd.DataFrame(columns=["Xk", "Xk+1", "f(x)", "f'(x)", "E"])

        # Derivada da função
        def f_linha(num): return sp.Float(sp.diff(func, x).subs(x, num), precision)

        # Função acabou verifica se erro < f(x0)
        while not acabou(x0, f=f, met=Metodo.NEWTON_RAPHSON, erros=erros):

            # Impresão de variáveis em formato de tabela
            table = table.append(pd.Series([x0, x0 - (f(x0) / f_linha(x0)), f(x0),
                                            f_linha(x0), f(x0)], index=table.columns), ignore_index=True)

            x0 = x0 - (f(x0) / f_linha(x0))

        # Colocar ultima linha na tabela
        table = table.append(pd.Series([x0, x0 - (f(x0) / f_linha(x0)), f(x0),
                                        f_linha(x0), f(x0)], index=table.columns), ignore_index=True)


    # Saída apresentando os valores de cada variável e valor de função
    table.index = range(1, table.shape[0] + 1)
    table.index.name = "K"
    with pd.option_context("display.max_columns", table.shape[1]):
        print(table)

    if plot:
        if met == Metodo.NEWTON_RAPHSON:
            raiz = table["Xk"].iloc[-1]
            tentativas = list(table["Xk"])
        else:
            raiz = table["x"].iloc[-1]
            tentativas = list(table["x"])

        i = (float(raiz) / 1.5, float(raiz) * 1.5)

        x_arr = np.linspace(float(i[0]), float(i[1]), 100)
        y_arr = np.array([], dtype=float)
        for j in x_arr:
            y_arr = np.append(y_arr, f(j))

        _, ax = plt.subplots()
        ax.plot(x_arr, y_arr, linewidth=2.0, color="red")
        ax.set(xlim=i)

        plt.axhline(0, color="black", linewidth=0.75)

        for x_point in tentativas:
            plt.plot(x_point, f(x_point), "og")
        plt.show()

if __name__ == "__main__":
    main("-plot" in sys.argv)
