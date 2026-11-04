# test_avl.py
# Pruebas de autocomprobacion del AVL. No hay que modificarlo: hay que
# conseguir que pase entero.
#
# Se ejecuta por grupos, en el mismo orden en que se programa en clase:
#   python3 -m unittest -v test_avl.PruebasRotaciones
#   python3 -m unittest -v test_avl.PruebasEquilibrar
#   python3 -m unittest -v test_avl.PruebasInsertar
# Ampliacion (opcional; se salta mientras no este hecha):
#   python3 -m unittest -v test_avl.PruebasAmpliacion
# Todo:
#   python3 -m unittest -v test_avl

import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avl import (Nodo, altura, construir, equilibrar, es_avl,  # noqa: E402
                 inorden, insertar, rotar_derecha, rotar_izquierda)


def forma(n):
    """(clave, izq, der) recursivo: compara la forma completa del arbol."""
    return None if n is None else (n.clave, forma(n.izq), forma(n.der))


def h(clave, izq=None, der=None):
    return (clave, izq, der)


def alturas_guardadas_bien(n):
    """True si el campo altura de TODOS los nodos es el real."""
    def real(nodo):
        if nodo is None:
            return -1
        hi, hd = real(nodo.izq), real(nodo.der)
        if hi is None or hd is None:
            return None
        r = 1 + max(hi, hd)
        return r if nodo.altura == r else None
    return real(n) is not None


def equilibrado(n):
    """True si todos los nodos tienen |fe| <= 1 (alturas reales)."""
    def real(nodo):
        if nodo is None:
            return -1
        hi, hd = real(nodo.izq), real(nodo.der)
        if hi is None or hd is None or abs(hi - hd) > 1:
            return None
        return 1 + max(hi, hd)
    return real(n) is not None


def nodos(n):
    return [] if n is None else nodos(n.izq) + [n] + nodos(n.der)


class PruebaBase(unittest.TestCase):
    def comprobar_avl(self, raiz, claves):
        self.assertEqual(inorden(raiz), sorted(set(claves)), "deja de ser un BST o pierde claves")
        self.assertTrue(alturas_guardadas_bien(raiz), "hay alturas guardadas sin actualizar")
        self.assertTrue(equilibrado(raiz), "hay un nodo con factor de equilibrio 2 o -2")


# ---------------------------------------------------------------- ejercicio 1

class PruebasRotaciones(PruebaBase):
    def test_derecha_minima(self):
        #     3          2
        #    /          / \
        #   2     ->   1   3
        #  /
        # 1
        y = Nodo(3, Nodo(2, Nodo(1)))
        x = y.izq
        r = rotar_derecha(y)
        self.assertIs(r, x, "debe devolver el antiguo hijo izquierdo como nueva raiz")
        self.assertEqual(forma(r), h(2, h(1), h(3)))
        self.assertTrue(alturas_guardadas_bien(r), "alturas sin actualizar")
        self.assertEqual(r.altura, 1)

    def test_izquierda_minima(self):
        x = Nodo(1, None, Nodo(2, None, Nodo(3)))
        y = x.der
        r = rotar_izquierda(x)
        self.assertIs(r, y, "debe devolver el antiguo hijo derecho como nueva raiz")
        self.assertEqual(forma(r), h(2, h(1), h(3)))
        self.assertTrue(alturas_guardadas_bien(r), "alturas sin actualizar")

    def test_derecha_mueve_el_subarbol_central(self):
        # T2 (el 50) pasa de ser hijo derecho de x a hijo izquierdo de y.
        y = Nodo(60, Nodo(40, Nodo(30, Nodo(20)), Nodo(50)), Nodo(70))
        r = rotar_derecha(y)
        self.assertEqual(forma(r), h(40, h(30, h(20)), h(60, h(50), h(70))))
        self.assertTrue(alturas_guardadas_bien(r), "alturas sin actualizar (y antes que x)")

    def test_izquierda_mueve_el_subarbol_central(self):
        x = Nodo(20, Nodo(10), Nodo(40, Nodo(30), Nodo(50, None, Nodo(60))))
        r = rotar_izquierda(x)
        self.assertEqual(forma(r), h(40, h(20, h(10), h(30)), h(50, None, h(60))))
        self.assertTrue(alturas_guardadas_bien(r), "alturas sin actualizar (x antes que y)")

    def test_no_crea_ni_pierde_nodos(self):
        y = Nodo(60, Nodo(40, Nodo(30), Nodo(50)), Nodo(70))
        antes = {id(n) for n in nodos(y)}
        r = rotar_derecha(y)
        self.assertEqual({id(n) for n in nodos(r)}, antes, "las rotaciones solo cambian enlaces")
        r = rotar_izquierda(r)
        self.assertEqual({id(n) for n in nodos(r)}, antes)
        self.assertEqual(forma(r), h(60, h(40, h(30), h(50)), h(70)), "izquierda deshace derecha")


# ---------------------------------------------------------------- ejercicio 2

class PruebasEquilibrar(PruebaBase):
    def test_ya_equilibrado_no_cambia(self):
        n = Nodo(2, Nodo(1), Nodo(3))
        self.assertIs(equilibrar(n), n)
        self.assertEqual(forma(n), h(2, h(1), h(3)))
        hoja = Nodo(7)
        self.assertIs(equilibrar(hoja), hoja)

    def test_fe_uno_no_rota(self):
        n = Nodo(5, Nodo(3, Nodo(2)), Nodo(8))
        self.assertIs(equilibrar(n), n)
        self.assertEqual(forma(n), h(5, h(3, h(2)), h(8)))

    def test_actualiza_la_altura(self):
        n = Nodo(5)
        n.izq = Nodo(3)       # se cuelga un hijo sin actualizar la altura de n
        r = equilibrar(n)
        self.assertIs(r, n)
        self.assertEqual(r.altura, 1, "equilibrar debe actualizar la altura del nodo")

    def test_caso_izquierda_izquierda(self):
        n = Nodo(3, Nodo(2, Nodo(1)))
        self.assertEqual(forma(equilibrar(n)), h(2, h(1), h(3)))

    def test_caso_derecha_derecha(self):
        n = Nodo(1, None, Nodo(2, None, Nodo(3)))
        self.assertEqual(forma(equilibrar(n)), h(2, h(1), h(3)))

    def test_caso_izquierda_derecha(self):
        n = Nodo(3, Nodo(1, None, Nodo(2)))
        r = equilibrar(n)
        self.assertEqual(forma(r), h(2, h(1), h(3)), "rotacion doble: izquierda en el hijo y derecha en el nodo")
        self.assertTrue(alturas_guardadas_bien(r))

    def test_caso_derecha_izquierda(self):
        n = Nodo(1, None, Nodo(3, Nodo(2)))
        r = equilibrar(n)
        self.assertEqual(forma(r), h(2, h(1), h(3)), "rotacion doble: derecha en el hijo e izquierda en el nodo")
        self.assertTrue(alturas_guardadas_bien(r))

    def test_casos_dobles_con_subarboles(self):
        #        50                    40
        #       /  \                 /    \
        #     30    60     ->      30      50
        #    /  \                 /  \       \
        #   20  40              20   35      60
        #       /
        #      35
        n = Nodo(50, Nodo(30, Nodo(20), Nodo(40, Nodo(35))), Nodo(60))
        r = equilibrar(n)
        self.assertEqual(forma(r), h(40, h(30, h(20), h(35)), h(50, None, h(60))))
        self.assertTrue(alturas_guardadas_bien(r))
        self.assertTrue(equilibrado(r))


# ---------------------------------------------------------------- ejercicio 3

class PruebasInsertar(PruebaBase):
    def test_vacio_y_uno(self):
        r = insertar(None, 10)
        self.assertEqual(forma(r), h(10))
        self.assertEqual(r.altura, 0)

    def test_sin_rotaciones(self):
        r = construir([20, 10, 30, 5, 25])
        self.assertEqual(forma(r), h(20, h(10, h(5)), h(30, h(25))))
        self.comprobar_avl(r, [20, 10, 30, 5, 25])

    def test_los_cuatro_casos(self):
        for claves in ([3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]):
            with self.subTest(claves=claves):
                self.assertEqual(forma(construir(claves)), h(2, h(1), h(3)))

    def test_repetidas_no_cambian_el_arbol(self):
        r = construir([5, 3, 8])
        antes = forma(r)
        r = insertar(r, 3)
        r = insertar(r, 5)
        self.assertEqual(forma(r), antes)
        self.assertEqual(len(nodos(r)), 3)

    def test_ordenadas_dan_arbol_perfecto(self):
        r = construir(range(1, 8))
        self.assertEqual(forma(r), h(4, h(2, h(1), h(3)), h(6, h(5), h(7))))
        r = construir(range(1, 1024))
        self.assertEqual(altura(r), 9, "1..1023 en orden: arbol perfecto de altura 9")
        self.comprobar_avl(r, range(1, 1024))

    def test_traza_de_las_diapositivas(self):
        # 10, 20, 30, 25, 28, 5: simple a la izquierda en 10, doble en 30.
        r = construir([10, 20, 30, 25, 28, 5])
        self.assertEqual(forma(r), h(20, h(10, h(5)), h(28, h(25), h(30))))

    def test_descendentes_y_zigzag(self):
        for claves in (list(range(500, 0, -1)),
                       [x for i in range(250) for x in (i, 1000 - i)]):
            r = construir(claves)
            self.comprobar_avl(r, claves)
            self.assertLessEqual(altura(r), 1.45 * math.log2(len(claves) + 2))

    def test_aleatorios(self):
        rng = random.Random(7)
        for n in (10, 100, 2000):
            claves = [rng.randrange(-5000, 5000) for _ in range(n)]
            r = construir(claves)
            self.comprobar_avl(r, claves)
            self.assertLessEqual(altura(r), 1.45 * math.log2(len(set(claves)) + 2))

    def test_muchas_claves_ordenadas(self):
        # Un BST normal tendria altura 19 999 (y la recursion reventaria).
        r = construir(range(20000))
        self.assertLessEqual(altura(r), 15)


# ---------------------------------------------------------------- ampliacion

class PruebasAmpliacion(PruebaBase):
    def es_avl(self, raiz):
        try:
            return es_avl(raiz)
        except NotImplementedError:
            self.skipTest("ampliacion opcional sin implementar")

    def test_vacio_hoja_y_pequenos(self):
        self.assertIs(self.es_avl(None), True)
        self.assertIs(self.es_avl(Nodo(1)), True)
        self.assertIs(self.es_avl(Nodo(2, Nodo(1), Nodo(3))), True)
        self.assertIs(self.es_avl(Nodo(2, Nodo(1))), True)

    def test_desequilibrado(self):
        self.assertIs(self.es_avl(Nodo(3, Nodo(2, Nodo(1)))), False)
        # La raiz tiene fe 0, pero el 2 tiene fe 2: hay que mirar TODOS los nodos.
        r = Nodo(5, Nodo(2, Nodo(1, Nodo(0))), Nodo(8, None, Nodo(9, None, Nodo(10))))
        self.assertIs(self.es_avl(r), False)

    def test_no_es_bst(self):
        self.assertIs(self.es_avl(Nodo(2, Nodo(3), Nodo(1))), False)
        # Cada padre esta bien con sus hijos, pero el 6 esta a la izquierda del 5.
        self.assertIs(self.es_avl(Nodo(5, Nodo(3, Nodo(1), Nodo(6)), Nodo(8))), False)
        self.assertIs(self.es_avl(Nodo(5, Nodo(5))), False, "claves repetidas")

    def test_no_se_fia_del_campo_altura(self):
        r = Nodo(3, Nodo(2, Nodo(1)))
        for n in nodos(r):
            n.altura = 0           # alturas falsas: el arbol NO es AVL
        self.assertIs(self.es_avl(r), False)
        r = Nodo(2, Nodo(1), Nodo(3))
        r.altura = 7               # altura falsa: el arbol SI es AVL
        self.assertIs(self.es_avl(r), True)

    def test_arboles_construidos(self):
        rng = random.Random(3)
        claves = [rng.randrange(10 ** 6) for _ in range(3000)]
        self.assertIs(self.es_avl(construir(claves)), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
