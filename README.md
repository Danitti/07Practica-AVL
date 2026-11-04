# Práctica 07: Árboles AVL
**Asignatura**: Algoritmia y Estructuras de Datos (AED I) — Bloque II
**Titulación**: Ingeniería Informática – Inteligencia Artificial
**Duración**: 2 h en clase: ≈ 60 min de AVL + miniprueba individual en DomJudge (40 min)

> Este es el **enunciado**: qué hay que hacer. La explicación paso a paso está en las diapositivas (`diapositivas/`) y el resumen para tener a mano, en `chuleta.md`.

## Contexto

En la práctica 5 vimos que un árbol construido sin cuidado puede degenerar: si insertas `1, 2, 3, 4, 5` en un BST, cada nodo cuelga a la derecha del anterior y el árbol es, en realidad, una lista. Buscar deja de costar O(log n) y pasa a costar O(n).

```
   BST: 1, 2, 3, 4, 5            AVL: las mismas claves

   1                                   2
    \                                 / \
     2                               1   4
      \                                 / \
       3                               3   5
        \
         4                        altura 2
          \
           5      altura 4
```

Un **árbol AVL** es un BST que se mantiene equilibrado: en **todos** los nodos, las alturas de los dos subárboles se diferencian como mucho en 1.

```
factor_equilibrio(nodo) = altura(nodo.izq) − altura(nodo.der)   ∈ {−1, 0, +1}
```

Cuando una inserción deja un nodo con factor +2 o −2, se arregla con una **rotación** (simple o doble), que cuesta O(1) y conserva el orden del BST. Así la altura queda siempre por debajo de 1,44 · log₂ n.

En esta práctica vas a:

1. Programar las dos **rotaciones simples**.
2. Programar **`equilibrar`**: decidir cuál de los cuatro casos se da y aplicar la rotación (o las dos rotaciones) que corresponde.
3. Programar **`insertar`** en un AVL: la inserción de BST de siempre + `equilibrar` a la vuelta de la recursión.

La segunda parte de la sesión es la **miniprueba individual en DomJudge** (ver más abajo).

## Ficheros

Trabaja siempre desde la carpeta `python/` (`cd python`). En Windows, si `python3` no existe, usa `python` o `py`.

| Fichero | Qué es | ¿Lo modificas? |
|---------|--------|----------------|
| `python/avl.py` | `Nodo` y las funciones del AVL, con huecos (`TODO`) | **Sí** |
| `python/test_avl.py` | Pruebas de autocomprobación | No |
| `python/utilidades.py` | `dibujar(raiz)`, para ver el árbol en la terminal, ya hecho | No |
| `python/experimento.py` | Compara la altura de un BST y de un AVL, ya hecho | No |
| `RESPUESTAS.md` | Hoja con la tabla de costes y tres preguntas | **Sí** |
| `chuleta.md` | Resumen de una página: rotaciones, los cuatro casos, costes | No |
| `diapositivas/` | Diapositivas de la sesión en PDF | No |
| `cpp/` | La misma práctica en C++ | Solo si la haces en C++ |

## Qué hay que hacer

### La representación

```python
class Nodo:                  # ya hecho
    clave        # la clave (int)
    izq          # Nodo o None
    der          # Nodo o None
    altura       # altura del subárbol que empieza en este nodo (hoja = 0)

altura(nodo)                 # ya hecha: -1 si nodo es None; si no, nodo.altura   O(1)
actualizar_altura(nodo)      # ya hecha: recalcula nodo.altura con la de sus hijos O(1)
factor_equilibrio(nodo)      # ya hecha: altura(izq) - altura(der)               O(1)
construir([10, 20, 30])      # ya hecha: inserta las claves en un AVL vacío (usa tu insertar)
```

La altura se **guarda** en cada nodo para no tener que recorrer el subárbol cada vez que se necesita: así consultar el factor de equilibrio cuesta O(1). A cambio, cada vez que cambian los hijos de un nodo hay que llamar a `actualizar_altura`.

Completa las funciones marcadas con `TODO` **en este orden** y ejecuta el grupo de tests de cada paso:

| Orden | Funciones | Tests |
|-------|-----------|-------|
| 1 | `rotar_derecha(y)`, `rotar_izquierda(x)` | `python3 -m unittest -v test_avl.PruebasRotaciones` |
| 2 | `equilibrar(nodo)` | `... test_avl.PruebasEquilibrar` |
| 3 | `insertar(raiz, clave)` | `... test_avl.PruebasInsertar` |

Algunas indicaciones:

- Todas las funciones **devuelven la nueva raíz** del subárbol: después de una rotación la raíz ya no es la misma. Quien llama tiene que reengancharla (`nodo.izq = rotar_izquierda(nodo.izq)`, `raiz.izq = insertar(raiz.izq, clave)`).
- **Rotaciones**: solo cambian dos enlaces, no crean ni borran nodos. Después, actualiza primero la altura del nodo que ha quedado **abajo** y luego la del que ha quedado arriba.
- **`equilibrar`**: empieza actualizando la altura del nodo. Si su factor es +2 pesa la izquierda: si además el hijo izquierdo pesa a la derecha (factor < 0) es el caso doble. Simétrico para −2. La tabla de los cuatro casos está en `chuleta.md`.
- **`insertar`**: si la clave ya está, el árbol no cambia.
- Para ver lo que construyes: `from utilidades import dibujar` y `print(dibujar(construir([10, 20, 30, 25, 28, 5]), detalles=True))` (muestra la altura y el factor de equilibrio de cada nodo).
- Sustituye cada `O(?)` del código por el coste que consigue tu implementación.

---

## Miniprueba individual en DomJudge (40 min)

En la segunda parte de la sesión hay una **miniprueba individual** en DomJudge: **dos problemas cortos e independientes** (puedes hacerlos en el orden que quieras), 10 puntos en total, en Python o en C++.

- **Contenido**: pilas, árboles binarios de búsqueda y heaps (prácticas 4 a 6).
- **Problema 1, `construirbst` (4 puntos)**: insertar en un BST. **Problema 2, `kmenores` (6 puntos)**: recorrer un BST con una pila. El árbol del problema 2 viene ya construido en la entrada, así que no depende del problema 1.
- **Formato**: entrada con *T* casos (la «solución 1» de la práctica 6). El código base de cada problema, con la lectura y la escritura ya hechas, se descarga desde la página del problema.
- **Puntuación**: en cada problema, unos puntos por conseguir *CORRECT* cumpliendo las condiciones del enunciado y otros por las preguntas de coste, que se responden en comentarios al principio del fichero.
- Hay casos **grandes**: además de ser correcta, la solución tiene que tener el coste adecuado o dará *TIMELIMIT*.
- Se corrige el **último** envío de cada problema. No dejes `print` de depuración: cualquier texto de más da *WRONG-ANSWER*.

Para prepararla, repasa: recorridos de árboles con y sin recursión, inserción en un BST, el top-k con heap de la práctica 6 y la lectura de casos de la práctica 6.

---

## Cierre (en casa, ≈ 10 min)

Rellena `RESPUESTAS.md`: la tabla de costes de tu implementación (deben coincidir con los `O(?)` del código) y tres preguntas cortas.

Antes de entregar:

- [ ] `python3 -m unittest -v test_avl` pasa (las pruebas de la ampliación salen como *skipped* si no la haces).
- [ ] No queda ningún `O(?)` en el código.

---

## Ampliación (opcional, no puntúa)

- **`es_avl(raiz)`** en `avl.py` (sus tests, `PruebasAmpliacion`, se saltan mientras no la hagas): decide si un árbol cualquiera es un AVL. Tiene que comprobar a la vez que es un BST (¡no basta con mirar cada padre con sus hijos!) y que **todos** los nodos tienen factor −1, 0 o +1, sin fiarse del campo `altura`. Hazlo con **un solo recorrido**: O(n).
- **La misma práctica en C++** (carpeta `cpp/`), ver abajo.

### Versión en C++

Mismos ejercicios y mismos nombres en `cpp/avl.hpp`, con `TODO`. Compilar y ejecutar las pruebas (desde `cpp/`):

```bash
g++ -std=c++17 -Wall test_avl.cpp -o test_avl && ./test_avl     # o ./test_avl PruebasRotaciones
```

En Windows: `.\test_avl.exe`. Cada prueba sale como `ok`, `FALLO`, `PENDIENTE` (aún lanza `TODO`) o `saltada` (ampliación). Diferencias con Python:

- `None` es `nullptr` y los nodos se crean con `new`. `liberar(raiz)` ya está hecha (recorrido postorden).
- `PruebasMemoria` comprueba con el contador `Nodo::vivos` que `insertar` crea exactamente un nodo por clave nueva y ninguno con las repetidas.

Entrega en C++: `avl.hpp` y `RESPUESTAS.md`.

---

## Recursos

| Recurso | Para qué |
|---------|----------|
| [VisuAlgo — BST / AVL](https://visualgo.net/en/bst) | Elige «AVL Tree» arriba para ver las rotaciones paso a paso |
| [Adelson-Velsky y Landis (1962)](https://es.wikipedia.org/wiki/%C3%81rbol_AVL) | Historia del AVL, el primer árbol de búsqueda autoequilibrado |
| [Python — `bisect` y `sortedcontainers`](https://grantjenks.com/docs/sortedcontainers/) | En la práctica, cómo se tiene un «conjunto ordenado» en Python |
