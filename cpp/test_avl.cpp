// test_avl.cpp
// Pruebas de autocomprobacion del AVL en C++. No hay que modificarlo.
//
// Compilar (desde la carpeta cpp/):
//   g++ -std=c++17 -Wall test_avl.cpp -o test_avl
// Ejecutar todo, o solo algunos grupos:
//   ./test_avl
//   ./test_avl PruebasRotaciones PruebasEquilibrar
// Grupos, en el orden de trabajo:
//   obligatorio: PruebasRotaciones PruebasEquilibrar PruebasInsertar PruebasMemoria
//   ampliacion:  PruebasAmpliacion (opcional)

#include <cmath>
#include <random>
#include <set>
#include <sstream>
#include <string>

#include "avl.hpp"
#include "mini_test.hpp"

using std::string;
using std::vector;

// Forma completa del arbol como texto: (clave izq der), "." = vacio.
static string forma(const Nodo* n) {
    if (n == nullptr) return ".";
    if (n->izq == nullptr && n->der == nullptr) return std::to_string(n->clave);
    return "(" + std::to_string(n->clave) + " " + forma(n->izq) + " " + forma(n->der) + ")";
}

// Altura real si las guardadas son correctas en TODOS los nodos; -2 si no.
static int alturas_bien(const Nodo* n) {
    if (n == nullptr) return -1;
    int hi = alturas_bien(n->izq), hd = alturas_bien(n->der);
    if (hi == -2 || hd == -2) return -2;
    int r = 1 + std::max(hi, hd);
    return n->altura == r ? r : -2;
}

static int equilibrado(const Nodo* n) {
    if (n == nullptr) return -1;
    int hi = equilibrado(n->izq), hd = equilibrado(n->der);
    if (hi == -2 || hd == -2 || std::abs(hi - hd) > 1) return -2;
    return 1 + std::max(hi, hd);
}

static void punteros(const Nodo* n, std::set<const Nodo*>& s) {
    if (!n) return;
    s.insert(n);
    punteros(n->izq, s);
    punteros(n->der, s);
}

static void comprobar_avl_completo(const Nodo* raiz, vector<int> claves) {
    std::sort(claves.begin(), claves.end());
    claves.erase(std::unique(claves.begin(), claves.end()), claves.end());
    vector<int> in;
    inorden(raiz, in);
    COMPROBAR(in == claves, "deja de ser un BST o pierde claves");
    COMPROBAR(alturas_bien(raiz) != -2, "hay alturas guardadas sin actualizar");
    COMPROBAR(equilibrado(raiz) != -2, "hay un nodo con factor de equilibrio 2 o -2");
}

static vector<int> rango(int desde, int hasta) {      // [desde, hasta)
    vector<int> v;
    for (int i = desde; i < hasta; ++i) v.push_back(i);
    return v;
}

template <typename F>
static auto opcional(F f) -> decltype(f()) {
    try {
        return f();
    } catch (const std::logic_error& e) {
        if (string(e.what()).rfind("TODO", 0) == 0) throw mini_test::Saltar("ampliacion opcional");
        throw;
    }
}

// --------------------------------------------------------------- rotaciones

PRUEBA(PruebasRotaciones, derecha_minima) {
    Nodo* y = new Nodo(3, new Nodo(2, new Nodo(1)));
    Nodo* x = y->izq;
    Nodo* r = rotar_derecha(y);
    COMPROBAR(r == x, "debe devolver el antiguo hijo izquierdo como nueva raiz");
    COMPROBAR(forma(r) == "(2 1 3)", "forma tras rotar: " + forma(r));
    COMPROBAR(alturas_bien(r) == 1, "alturas sin actualizar");
    liberar(r);
}

PRUEBA(PruebasRotaciones, izquierda_minima) {
    Nodo* x = new Nodo(1, nullptr, new Nodo(2, nullptr, new Nodo(3)));
    Nodo* y = x->der;
    Nodo* r = rotar_izquierda(x);
    COMPROBAR(r == y, "debe devolver el antiguo hijo derecho como nueva raiz");
    COMPROBAR(forma(r) == "(2 1 3)", "forma tras rotar: " + forma(r));
    COMPROBAR(alturas_bien(r) == 1, "alturas sin actualizar");
    liberar(r);
}

PRUEBA(PruebasRotaciones, derecha_mueve_subarbol_central) {
    Nodo* y = new Nodo(60, new Nodo(40, new Nodo(30, new Nodo(20)), new Nodo(50)), new Nodo(70));
    Nodo* r = rotar_derecha(y);
    COMPROBAR(forma(r) == "(40 (30 20 .) (60 50 70))", "forma: " + forma(r));
    COMPROBAR(alturas_bien(r) != -2, "alturas sin actualizar (y antes que x)");
    liberar(r);
}

PRUEBA(PruebasRotaciones, izquierda_mueve_subarbol_central) {
    Nodo* x = new Nodo(20, new Nodo(10), new Nodo(40, new Nodo(30), new Nodo(50, nullptr, new Nodo(60))));
    Nodo* r = rotar_izquierda(x);
    COMPROBAR(forma(r) == "(40 (20 10 30) (50 . 60))", "forma: " + forma(r));
    COMPROBAR(alturas_bien(r) != -2, "alturas sin actualizar (x antes que y)");
    liberar(r);
}

PRUEBA(PruebasRotaciones, no_crea_ni_pierde_nodos) {
    Nodo* y = new Nodo(60, new Nodo(40, new Nodo(30), new Nodo(50)), new Nodo(70));
    std::set<const Nodo*> antes, despues;
    punteros(y, antes);
    int vivos = Nodo::vivos;
    Nodo* r = rotar_izquierda(rotar_derecha(y));
    punteros(r, despues);
    COMPROBAR(antes == despues && Nodo::vivos == vivos, "las rotaciones solo cambian enlaces");
    COMPROBAR(forma(r) == "(60 (40 30 50) 70)", "izquierda deshace derecha");
    liberar(r);
}

// --------------------------------------------------------------- equilibrar

PRUEBA(PruebasEquilibrar, ya_equilibrado_no_cambia) {
    Nodo* n = new Nodo(2, new Nodo(1), new Nodo(3));
    COMPROBAR(equilibrar(n) == n, "sin desequilibrio no se rota");
    Nodo* m = new Nodo(5, new Nodo(3, new Nodo(2)), new Nodo(8));
    COMPROBAR(equilibrar(m) == m && forma(m) == "(5 (3 2 .) 8)", "fe = 1 no rota");
    liberar(n);
    liberar(m);
}

PRUEBA(PruebasEquilibrar, actualiza_la_altura) {
    Nodo* n = new Nodo(5);
    n->izq = new Nodo(3);          // se cuelga un hijo sin actualizar la altura
    Nodo* r = equilibrar(n);
    COMPROBAR(r == n && r->altura == 1, "equilibrar debe actualizar la altura del nodo");
    liberar(r);
}

PRUEBA(PruebasEquilibrar, casos_simples) {
    Nodo* a = equilibrar(new Nodo(3, new Nodo(2, new Nodo(1))));
    COMPROBAR(forma(a) == "(2 1 3)", "izquierda-izquierda: " + forma(a));
    Nodo* b = equilibrar(new Nodo(1, nullptr, new Nodo(2, nullptr, new Nodo(3))));
    COMPROBAR(forma(b) == "(2 1 3)", "derecha-derecha: " + forma(b));
    liberar(a);
    liberar(b);
}

PRUEBA(PruebasEquilibrar, casos_dobles) {
    Nodo* a = equilibrar(new Nodo(3, new Nodo(1, nullptr, new Nodo(2))));
    COMPROBAR(forma(a) == "(2 1 3)", "izquierda-derecha: " + forma(a));
    Nodo* b = equilibrar(new Nodo(1, nullptr, new Nodo(3, new Nodo(2))));
    COMPROBAR(forma(b) == "(2 1 3)", "derecha-izquierda: " + forma(b));
    COMPROBAR(alturas_bien(a) != -2 && alturas_bien(b) != -2, "alturas sin actualizar");
    liberar(a);
    liberar(b);
}

PRUEBA(PruebasEquilibrar, caso_doble_con_subarboles) {
    Nodo* n = new Nodo(50, new Nodo(30, new Nodo(20), new Nodo(40, new Nodo(35))), new Nodo(60));
    Nodo* r = equilibrar(n);
    COMPROBAR(forma(r) == "(40 (30 20 35) (50 . 60))", "forma: " + forma(r));
    COMPROBAR(alturas_bien(r) != -2 && equilibrado(r) != -2, "alturas o equilibrio");
    liberar(r);
}

// --------------------------------------------------------------- insertar

PRUEBA(PruebasInsertar, vacio_y_sin_rotaciones) {
    Nodo* r = insertar(nullptr, 10);
    COMPROBAR(forma(r) == "10" && r->altura == 0, "un nodo");
    liberar(r);
    r = construir({20, 10, 30, 5, 25});
    COMPROBAR(forma(r) == "(20 (10 5 .) (30 25 .))", "sin rotaciones: " + forma(r));
    liberar(r);
}

PRUEBA(PruebasInsertar, los_cuatro_casos) {
    for (const vector<int>& c : vector<vector<int>>{{3, 2, 1}, {1, 2, 3}, {3, 1, 2}, {1, 3, 2}}) {
        Nodo* r = construir(c);
        COMPROBAR(forma(r) == "(2 1 3)", "insertar en orden distinto 1, 2, 3: " + forma(r));
        liberar(r);
    }
}

PRUEBA(PruebasInsertar, repetidas) {
    Nodo* r = construir({5, 3, 8});
    int vivos = Nodo::vivos;
    r = insertar(insertar(r, 3), 5);
    COMPROBAR(forma(r) == "(5 3 8)" && Nodo::vivos == vivos, "una clave repetida no cambia nada");
    liberar(r);
}

PRUEBA(PruebasInsertar, ordenadas_dan_arbol_perfecto) {
    Nodo* r = construir(rango(1, 8));
    COMPROBAR(forma(r) == "(4 (2 1 3) (6 5 7))", "1..7: " + forma(r));
    liberar(r);
    r = construir(rango(1, 1024));
    COMPROBAR(altura(r) == 9, "1..1023 en orden: arbol perfecto de altura 9");
    comprobar_avl_completo(r, rango(1, 1024));
    liberar(r);
}

PRUEBA(PruebasInsertar, traza_de_las_diapositivas) {
    Nodo* r = construir({10, 20, 30, 25, 28, 5});
    COMPROBAR(forma(r) == "(20 (10 5 .) (28 25 30))", "forma: " + forma(r));
    liberar(r);
}

PRUEBA(PruebasInsertar, aleatorios) {
    std::mt19937 rng(7);
    std::uniform_int_distribution<int> d(-5000, 5000);
    for (int n : {10, 100, 2000}) {
        vector<int> c(n);
        for (int& x : c) x = d(rng);
        Nodo* r = construir(c);
        comprobar_avl_completo(r, c);
        std::set<int> distintas(c.begin(), c.end());
        COMPROBAR(altura(r) <= 1.45 * std::log2(distintas.size() + 2.0), "demasiado alto");
        liberar(r);
    }
}

PRUEBA(PruebasInsertar, muchas_claves_ordenadas) {
    Nodo* r = construir(rango(0, 100000));
    COMPROBAR(altura(r) <= 17, "un BST normal tendria altura 99 999");
    liberar(r);
}

// --------------------------------------------------------------- memoria

PRUEBA(PruebasMemoria, no_se_pierden_nodos) {
    int antes = Nodo::vivos;
    Nodo* r = construir({50, 20, 70, 10, 30, 25, 27, 26, 80, 90, 85, 50, 20});
    COMPROBAR(Nodo::vivos - antes == 11, "debe haber exactamente un nodo por clave distinta");
    liberar(r);
    COMPROBAR(Nodo::vivos == antes, "liberar debe dejar el contador como estaba");
}

// --------------------------------------------------------------- ampliacion

PRUEBA(PruebasAmpliacion, pequenos) {
    COMPROBAR(opcional([] { return es_avl(nullptr); }), "vacio");
    Nodo* a = new Nodo(2, new Nodo(1), new Nodo(3));
    Nodo* b = new Nodo(3, new Nodo(2, new Nodo(1)));
    COMPROBAR(opcional([&] { return es_avl(a); }), "(2 1 3) es AVL");
    COMPROBAR(!opcional([&] { return es_avl(b); }), "(3 (2 1 .) .) no es AVL");
    liberar(a);
    liberar(b);
}

PRUEBA(PruebasAmpliacion, todos_los_nodos_y_bst) {
    Nodo* a = new Nodo(5, new Nodo(2, new Nodo(1, new Nodo(0))),
                       new Nodo(8, nullptr, new Nodo(9, nullptr, new Nodo(10))));
    COMPROBAR(!opcional([&] { return es_avl(a); }), "la raiz tiene fe 0 pero sus hijos no");
    Nodo* b = new Nodo(5, new Nodo(3, new Nodo(1), new Nodo(6)), new Nodo(8));
    COMPROBAR(!opcional([&] { return es_avl(b); }), "el 6 esta a la izquierda del 5");
    Nodo* c = new Nodo(5, new Nodo(5));
    COMPROBAR(!opcional([&] { return es_avl(c); }), "claves repetidas");
    liberar(a);
    liberar(b);
    liberar(c);
}

PRUEBA(PruebasAmpliacion, no_se_fia_del_campo_altura) {
    Nodo* a = new Nodo(3, new Nodo(2, new Nodo(1)));
    a->altura = a->izq->altura = 0;
    COMPROBAR(!opcional([&] { return es_avl(a); }), "alturas falsas: NO es AVL");
    liberar(a);
}

int main(int argc, char** argv) { return mini_test::ejecutar(argc, argv); }
