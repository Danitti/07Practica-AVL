# experimento.py
# Compara la altura de un BST normal y la de un AVL al insertar las mismas
# claves. Ya esta hecho: solo hay que ejecutarlo cuando insertar funcione.
#
#   python3 experimento.py
#
# Lo necesitas para la pregunta 3 de RESPUESTAS.md.

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avl import altura, construir  # noqa: E402


class NodoBST:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None


def altura_bst(claves):
    """Inserta en un BST SIN equilibrar (iterativo) y devuelve su altura."""
    raiz = None
    maxima = -1
    for clave in claves:
        if raiz is None:
            raiz = NodoBST(clave)
            maxima = 0
            continue
        nodo, profundidad = raiz, 0
        while True:
            profundidad += 1
            if clave < nodo.clave:
                if nodo.izq is None:
                    nodo.izq = NodoBST(clave)
                    break
                nodo = nodo.izq
            elif clave > nodo.clave:
                if nodo.der is None:
                    nodo.der = NodoBST(clave)
                    break
                nodo = nodo.der
            else:
                profundidad = -1
                break
        maxima = max(maxima, profundidad)
    return maxima


def main():
    rng = random.Random(707)
    print(f"{'claves':12} {'n':>6} {'log2 n':>7} {'BST':>6} {'AVL':>5}")
    for n in (100, 1000, 4000):
        aleatorias = rng.sample(range(10 * n), n)
        for nombre, claves in (("ordenadas", list(range(n))), ("aleatorias", aleatorias)):
            print(f"{nombre:12} {n:6} {math.log2(n):7.1f} "
                  f"{altura_bst(claves):6} {altura(construir(claves)):5}")


if __name__ == "__main__":
    main()
