# Chuleta — Árboles AVL

```
AVL = BST  +  en TODOS los nodos:  fe = altura(izq) − altura(der) ∈ {−1, 0, +1}

Nodo:  clave | izq | der | altura        altura(vacío) = −1, hoja = 0
       altura(n) = 1 + max(altura(izq), altura(der))       ← se GUARDA en el nodo
```

## Rotaciones simples (O(1): solo se cambian 2 enlaces)

```
  rotar_derecha(y)                       rotar_izquierda(x)

        y              x                   x                  y
       / \            / \                 / \                / \
      x   T3   →    T1   y              T1   y      →       x   T3
     / \                / \                 / \            / \
    T1  T2            T2  T3              T2  T3          T1  T2

  x = y.izq                              y = x.der
  y.izq = x.der      (T2 cambia de padre) x.der = y.izq
  x.der = y                              y.izq = x
  actualizar(y); actualizar(x)           actualizar(x); actualizar(y)
  return x                               return y
```

Primero se actualiza el que ha quedado **abajo**: la altura del de arriba depende de él.

## Los cuatro casos de `equilibrar(nodo)`

| fe(nodo) | fe(hijo de ese lado) | Caso | Rotación |
|----------|----------------------|------|----------|
| +2 | izq ≥ 0 | izquierda-izquierda | `rotar_derecha(nodo)` |
| +2 | izq < 0 | izquierda-derecha | `nodo.izq = rotar_izquierda(nodo.izq)` y luego `rotar_derecha(nodo)` |
| −2 | der ≤ 0 | derecha-derecha | `rotar_izquierda(nodo)` |
| −2 | der > 0 | derecha-izquierda | `nodo.der = rotar_derecha(nodo.der)` y luego `rotar_izquierda(nodo)` |

Antes de mirar el fe, `equilibrar` actualiza la altura del nodo. Siempre **devuelve** la nueva raiz del subárbol.

## Insertar = insertar en BST + equilibrar a la vuelta

```python
def insertar(raiz, clave):
    if raiz is None:            return Nodo(clave)
    if clave < raiz.clave:      raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:    raiz.der = insertar(raiz.der, clave)
    else:                       return raiz          # repetida
    return equilibrar(raiz)                           # ¡devolver y reenganchar!
```

Error típico: llamar a `insertar(raiz.izq, clave)` **sin asignar** el resultado. La rotación cambia la raíz del subárbol y el padre sigue apuntando a la antigua.

## Costes

| | BST normal (peor caso) | AVL |
|---|---|---|
| Altura | n − 1 (claves ordenadas) | ≤ 1,44 · log₂ n |
| Buscar / insertar | O(n) | O(log n) |
| Rotación / equilibrar | — | O(1) |
| Recorrido completo | O(n) | O(n) |
