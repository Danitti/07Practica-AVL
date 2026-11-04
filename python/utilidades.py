# utilidades.py
# Ayudas para ver lo que construyes. Ya esta hecho: no hay que modificarlo.
#
#   from avl import construir
#   from utilidades import dibujar
#   print(dibujar(construir([1, 2, 3, 4, 5, 6, 7])))
#   print(dibujar(construir([1, 2, 3, 4, 5, 6, 7]), detalles=True))


def dibujar(raiz, detalles=False):
    """Dibuja el arbol tumbado: la raiz a la izquierda, el subarbol derecho
    arriba y el izquierdo abajo. Con detalles=True anade la altura guardada
    (h) y el factor de equilibrio (fe) de cada nodo."""
    if raiz is None:
        return "(arbol vacio)"
    lineas = []

    def alt(n):
        return -1 if n is None else n.altura

    def visitar(nodo, prefijo, conector):
        if nodo is None:
            return
        visitar(nodo.der, prefijo + ("    " if conector in ("", "┌── ") else "│   "), "┌── ")
        texto = str(nodo.clave)
        if detalles:
            fe = alt(nodo.izq) - alt(nodo.der)
            texto += f"  (h={nodo.altura}, fe={fe:+d})" if fe else f"  (h={nodo.altura}, fe=0)"
        lineas.append(prefijo + conector + texto)
        visitar(nodo.izq, prefijo + ("    " if conector in ("", "└── ") else "│   "), "└── ")

    visitar(raiz, "", "")
    return "\n".join(lineas)


if __name__ == "__main__":
    # Demostracion: python3 utilidades.py
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from avl import Nodo

    ejemplo = Nodo(4, Nodo(2, Nodo(1), Nodo(3)), Nodo(6, Nodo(5), Nodo(7)))
    print(dibujar(ejemplo, detalles=True))
