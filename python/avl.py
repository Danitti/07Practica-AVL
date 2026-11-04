# avl.py
# Practica 07 - Arboles AVL.
#
# Un AVL es un arbol binario de busqueda (BST) en el que, en TODOS los nodos,
# las alturas de los dos subarboles se diferencian como mucho en 1:
#
#     factor_equilibrio(nodo) = altura(nodo.izq) - altura(nodo.der)  en {-1, 0, 1}
#
# Cada nodo guarda su altura para no tener que recalcularla (convenio de
# teoria: arbol vacio = -1, hoja = 0).
#
# Hay que completar las funciones marcadas con TODO (cada una lanza ahora
# NotImplementedError) y sustituir cada "O(?)" por el coste que consigue tu
# implementacion. Lo que ya esta escrito no se toca: los tests dependen de los
# nombres (clave, izq, der, altura).
#
# Orden de trabajo y tests de cada paso:
#   1. rotar_derecha, rotar_izquierda  -> test_avl.PruebasRotaciones
#   2. equilibrar                      -> test_avl.PruebasEquilibrar
#   3. insertar                        -> test_avl.PruebasInsertar
# Ampliacion (opcional): es_avl        -> test_avl.PruebasAmpliacion
#   (se salta mientras no la hagas).
#
# Ejecutar los tests:
#   python3 -m unittest -v test_avl
#
# Para ver tu arbol (utilidades.py ya esta hecho):
#   from utilidades import dibujar
#   print(dibujar(construir([1, 2, 3, 4, 5, 6, 7])))


class Nodo:
    # __slots__: cada nodo solo tiene hueco para estos cuatro campos.
    __slots__ = ("clave", "izq", "der", "altura")

    def __init__(self, clave, izq=None, der=None):
        self.clave = clave
        self.izq = izq
        self.der = der
        self.altura = 1 + max(altura(izq), altura(der))


# ------------------------------------------------------------ ya hechas

def altura(nodo):
    """Altura guardada en el nodo. Arbol vacio: -1. Coste O(1)."""
    return -1 if nodo is None else nodo.altura


def actualizar_altura(nodo):
    """Recalcula la altura de nodo a partir de la de sus hijos. Coste O(1).
    Solo es correcta si las alturas de los hijos ya estan bien."""
    nodo.altura = 1 + max(altura(nodo.izq), altura(nodo.der))


def factor_equilibrio(nodo):
    """altura(izq) - altura(der). Positivo: pesa mas la izquierda. O(1)."""
    return altura(nodo.izq) - altura(nodo.der)


def inorden(raiz):
    """Lista de claves en inorden: en un BST salen ordenadas."""
    salida = []

    def visitar(nodo):
        if nodo is not None:
            visitar(nodo.izq)
            salida.append(nodo.clave)
            visitar(nodo.der)

    visitar(raiz)
    return salida


def construir(claves):
    """Inserta las claves, en ese orden, en un AVL vacio y devuelve la raiz."""
    raiz = None
    for clave in claves:
        raiz = insertar(raiz, clave)
    return raiz


# ------------------------------------------------------------ ejercicio 1

def rotar_derecha(y):
    """Rotacion simple a la derecha sobre y (y.izq no es None).

            y                x
           / \\              / \\
          x   T3    ->     T1   y
         / \\                   / \\
        T1  T2                T2  T3

    Devuelve x, la nueva raiz del subarbol, con las alturas actualizadas.
    Coste: tiempo O(?), memoria extra O(?)."""
    raise NotImplementedError("TODO rotar_derecha")


def rotar_izquierda(x):
    """Rotacion simple a la izquierda sobre x (x.der no es None). Simetrica.
    Coste: tiempo O(?), memoria extra O(?)."""
    raise NotImplementedError("TODO rotar_izquierda")


# ------------------------------------------------------------ ejercicio 2

def equilibrar(nodo):
    """Actualiza la altura de nodo y, si su factor de equilibrio es 2 o -2,
    aplica la rotacion que corresponde (los cuatro casos). Los dos subarboles
    de nodo ya son AVL. Devuelve la raiz del subarbol ya equilibrado.
    Coste: tiempo O(?), memoria extra O(?)."""
    raise NotImplementedError("TODO equilibrar")


# ------------------------------------------------------------ ejercicio 3

def insertar(raiz, clave):
    """Inserta clave en el AVL de raiz `raiz` y devuelve la nueva raiz.
    Si la clave ya esta, el arbol no cambia.
    Coste: tiempo O(?), memoria extra O(?)."""
    raise NotImplementedError("TODO insertar")


# ------------------------------------------------------------ ampliacion

def es_avl(raiz):
    """True si el arbol es un BST (claves estrictamente crecientes en inorden)
    y TODOS sus nodos tienen factor de equilibrio -1, 0 o 1. No se fia del
    campo altura: lo calcula. Un solo recorrido.
    Coste: tiempo O(?), memoria extra O(?)."""
    raise NotImplementedError("TODO es_avl")
