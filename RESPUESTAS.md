# Práctica 07 · Árboles AVL · Hoja de respuestas

**Nombre(s):**

## 1 · Costes de tu implementación

Deben coincidir con los `O(?)` que has sustituido en el código. *n* es el número de nodos y *h* la altura del árbol.

| Operación | Tiempo | Memoria extra |
|-----------|--------|---------------|
| `rotar_derecha`, `rotar_izquierda` | | |
| `equilibrar` | | |
| `insertar` | | |
| `es_avl` (ampliación) | | |
| `buscar` en un BST **sin** equilibrar (peor caso) | | |
| `buscar` en un AVL (peor caso) | | |

## 2 · Preguntas

**1.** Inserta, en este orden, `10, 20, 30, 25, 28, 5` en un AVL vacío. ¿Qué rotaciones se aplican, en qué nodo y en qué inserción? Dibuja el árbol final (puedes comprobarlo con `dibujar(construir([...]))`).

>

**2.** En `rotar_derecha(y)`, ¿por qué hay que actualizar la altura de `y` **antes** que la de `x`? ¿Qué pasaría si lo hicieras al revés?

>

**3.** Ejecuta `python3 experimento.py` y copia la tabla. ¿Por qué el BST normal con claves **ordenadas** tiene altura *n* − 1? Un heap (práctica 6) tampoco se desequilibra nunca y no necesita rotaciones: ¿por qué?

>
