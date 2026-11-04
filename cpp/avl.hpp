// avl.hpp
// Practica 07 - Arboles AVL (version C++). Mismos ejercicios y mismos nombres
// que en Python.
//
// Un AVL es un BST en el que, en TODOS los nodos,
//     factor_equilibrio(nodo) = altura(nodo->izq) - altura(nodo->der)  en {-1, 0, 1}
// Cada nodo guarda su altura (arbol vacio = -1, hoja = 0).
//
// Completa las funciones marcadas con TODO (ahora lanzan logic_error("TODO ..."))
// y sustituye cada "O(?)" por el coste de tu implementacion.
//
// Orden de trabajo y grupos de pruebas:
//   1. rotar_derecha, rotar_izquierda  -> ./test_avl PruebasRotaciones
//   2. equilibrar                      -> ./test_avl PruebasEquilibrar
//   3. insertar                        -> ./test_avl PruebasInsertar
//   Ampliacion (opcional): es_avl      -> ./test_avl PruebasAmpliacion
//
// Compilar y ejecutar (desde cpp/):
//   g++ -std=c++17 -Wall test_avl.cpp -o test_avl && ./test_avl
#pragma once

#include <algorithm>
#include <cstdlib>
#include <stdexcept>
#include <vector>

struct Nodo {
    int clave;
    Nodo* izq = nullptr;
    Nodo* der = nullptr;
    int altura = 0;
    static inline int vivos = 0;     // nodos creados y no liberados (pruebas)

    Nodo(int c, Nodo* i = nullptr, Nodo* d = nullptr);
    ~Nodo() { --vivos; }
};

// ------------------------------------------------------------ ya hechas

// Altura guardada en el nodo. Arbol vacio: -1. O(1).
inline int altura(const Nodo* n) { return n == nullptr ? -1 : n->altura; }

inline Nodo::Nodo(int c, Nodo* i, Nodo* d) : clave(c), izq(i), der(d) {
    altura = 1 + std::max(::altura(i), ::altura(d));
    ++vivos;
}

// Recalcula la altura a partir de la de los hijos (que ya deben estar bien). O(1).
inline void actualizar_altura(Nodo* n) {
    n->altura = 1 + std::max(altura(n->izq), altura(n->der));
}

// altura(izq) - altura(der). Positivo: pesa mas la izquierda. O(1).
inline int factor_equilibrio(const Nodo* n) { return altura(n->izq) - altura(n->der); }

inline void liberar(Nodo* raiz) {      // postorden: hijos antes que el padre
    if (raiz == nullptr) return;
    liberar(raiz->izq);
    liberar(raiz->der);
    delete raiz;
}

inline void inorden(const Nodo* raiz, std::vector<int>& salida) {
    if (raiz == nullptr) return;
    inorden(raiz->izq, salida);
    salida.push_back(raiz->clave);
    inorden(raiz->der, salida);
}

Nodo* insertar(Nodo* raiz, int clave);

// Inserta las claves, en ese orden, en un AVL vacio y devuelve la raiz.
inline Nodo* construir(const std::vector<int>& claves) {
    Nodo* raiz = nullptr;
    for (int c : claves) raiz = insertar(raiz, c);
    return raiz;
}

// ------------------------------------------------------------ ejercicio 1

/*        y                x
         / \              / \
        x   T3    ->     T1  y
       / \                  / \
      T1  T2               T2  T3
   Devuelve x, la nueva raiz del subarbol, con las alturas actualizadas. */
// Coste: tiempo O(?), memoria extra O(?).
inline Nodo* rotar_derecha(Nodo* y) {
    (void)y;
    throw std::logic_error("TODO rotar_derecha");
}

// Simetrica. Coste: tiempo O(?), memoria extra O(?).
inline Nodo* rotar_izquierda(Nodo* x) {
    (void)x;
    throw std::logic_error("TODO rotar_izquierda");
}

// ------------------------------------------------------------ ejercicio 2

// Actualiza la altura de n y, si su factor de equilibrio es 2 o -2, aplica la
// rotacion que corresponde (cuatro casos). Los subarboles de n ya son AVL.
// Devuelve la raiz del subarbol equilibrado.
// Coste: tiempo O(?), memoria extra O(?).
inline Nodo* equilibrar(Nodo* n) {
    (void)n;
    throw std::logic_error("TODO equilibrar");
}

// ------------------------------------------------------------ ejercicio 3

// Inserta clave y devuelve la nueva raiz. Si ya esta, el arbol no cambia.
// Coste: tiempo O(?), memoria extra O(?).
inline Nodo* insertar(Nodo* raiz, int clave) {
    (void)raiz; (void)clave;
    throw std::logic_error("TODO insertar");
}

// ------------------------------------------------------------ ampliacion

// true si es un BST (claves estrictamente crecientes en inorden) y TODOS los
// nodos tienen |fe| <= 1. No se fia del campo altura. Un solo recorrido.
// Coste: tiempo O(?), memoria extra O(?).
inline bool es_avl(const Nodo* raiz) {
    (void)raiz;
    throw std::logic_error("TODO es_avl");
}
