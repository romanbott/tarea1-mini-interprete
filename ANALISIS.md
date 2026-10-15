# Análisis — Tarea 1

**Integrantes:**

1. Contreras Morales Román Ismael

**Fork:** https://github.com/romanbott/tarea1-mini-interprete
**Rama:** tarea1-pruebas-refactorizacion

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente  | Qué recibe                 | Qué entrega                                | De qué es responsable                                                                                                                                               |
| ----------- | -------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lexer`     | una cadena de texto        | una lista de `Token`.                      | el análisis léxico: reconocer las "palabras" (números, operadores, paréntesis), ignorar espacios y rechazar caracteres que no pertenecen al lenguaje.               |
| `parser`    | una lista de `Token`       | un árbol de sintaxis abstracta (ASA o AST) | el análisis sintáctico: comprobar que los tokens forman una oración válida según la gramática y agruparlos respetando precedencia y asociatividad.                  |
| `ast`       | — (el parser lo construye) | -                                          | representar la estructura de la expresión como árbol.                                                                                                               |
| `evaluator` | un AST                     | un número o un `ErrorDeEvaluacion`.        | recorrer el árbol hasta llegar a las hojas, para luego aplicar la semántica de cada operador regresando el resultado hacia arriba hasta obtener el resultado final. |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

`(3 + 4) * 2`

| Etapa     | Cómo se ve `(3 + 4) * 2` aquí                                                                                                                |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| texto     | `"(3 + 4) * 2"`                                                                                                                              |
| tokens    | `[Token(PAR_IZQ,'(',0), Token(NUMERO,3,1), Token(MAS,'+',3), Token(NUMERO,4,5), Token(PAR_DER,')',6), Token(POR,'*',8), Token(NUMERO,2,10)]` |
| AST       | `OperacionBinaria('*', OperacionBinaria('+', Numero(3), Numero(4)), Numero(2))`                                                              |
| resultado | `14`                                                                                                                                         |

El dibujo que imprime `python3 interprete.py --arbol "(3 + 4) * 2"` es:

```
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```

que lee: la raíz es el `*`, y su hijo izquierdo es el `+`. Coincide con el AST que dimos.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas? (las 13)

| Prueba                                                               | Componente | Comportamiento que verifica                               | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
| -------------------------------------------------------------------- | ---------- | --------------------------------------------------------- | ------------------------ | ----------------------------- |
| `test_lexer.py::test_tokeniza_un_numero_solo`                        | lexer      | `"42"` produce un único token `NUMERO(42)` con posición 0 | 0                        | normal                        |
| `test_lexer.py::test_tokeniza_una_suma`                              | lexer      | `"3+4"` produce 3 tokens con valor y posición correctos   | 1                        | normal                        |
| `test_lexer.py::test_los_espacios_no_producen_tokens`                | lexer      | los espacios en cualquier cantidad se ignoran             | 1                        | normal                        |
| `test_lexer.py::test_tokeniza_parentesis`                            | lexer      | `"(3)"` produce `PAR_IZQ, NUMERO, PAR_DER`                | 0                        | normal                        |
| `test_parser.py::test_construye_el_arbol_de_una_suma`                | parser     | `"3 + 4"` → `OperacionBinaria("+", Numero(3), Numero(4))` | 1                        | normal                        |
| `test_parser.py::test_la_multiplicacion_se_agrupa_antes_que_la_suma` | parser     | `*` se agrupa antes que `+` (precedencia)                 | 2                        | normal                        |
| `test_parser.py::test_los_parentesis_cambian_la_agrupacion`          | parser     | los paréntesis cambian la agrupación                      | 2                        | normal                        |
| `test_evaluator.py::test_suma`                                       | evaluator  | `interpretar("3 + 4") == 7`                               | 1                        | normal                        |
| `test_evaluator.py::test_resta`                                      | evaluator  | `interpretar("10 - 3") == 7`                              | 1                        | normal                        |
| `test_evaluator.py::test_multiplicacion`                             | evaluator  | `interpretar("6 * 7") == 42`                              | 1                        | normal                        |
| `test_evaluator.py::test_division`                                   | evaluator  | `interpretar("10 / 2") == 5`                              | 1                        | normal                        |
| `test_evaluator.py::test_precedencia_sin_parentesis`                 | evaluator  | `interpretar("3 + 4 * 2") == 11`                          | 2                        | normal                        |
| `test_evaluator.py::test_precedencia_con_parentesis`                 | evaluator  | `interpretar("(3 + 4) * 2") == 14`                        | 2                        | normal                        |

### Observaciones

- Las 13 son "normales". No hay ni una de frontera ni una inválida.
- El máximo de operadores es **2**, y siempre distintos o de distinta precedencia.
  Nunca hay una cadena de operadores de la misma precedencia (`a - b - c`, `a / b / c`), que es justo donde se ve la asociatividad.
- Las pruebas de `parser` utilizan `tokenizar`, por lo que podrían fallar si el _lexer_ falla.
  Deberían recibir una cadena de _tokens_.
- Similarmente, las pruebas de `evaluator` llaman a `interpretar(...)`, es decir ejecutan el _pipeline_ completo,
  por lo que podrían mezclar fallas del lexer, del parser o del intérprete.
  Deberían en vez de eso construir un AST y evaluarlo.
- No se prueba ningún error, ni la posición de los errores, ni la división
  entre cero, ni una división con resultado no entero.

### 2.2 ¿Qué comportamientos **no** estaban probados?

1. Asociatividad a la izquierda con operadores encadenados de la misma precedencia (`10 - 3 - 2`, `20 / 2 / 5`).
2. División real: sólo se prueba `10 / 2 == 5`.
   No se prueba un resultado fraccionario como `10 / 4 == 2.5`.
3. División entre cero debe lanzar un `ErrorDeEvaluacion`.
4. Probar exhaustivamente las posibles entradas inválidas que deberían producir `ErrorDeSintaxis`:
   - carácter desconocido (`3 @ 4`),
   - cadena vacía,
   - sólo espacios,
   - paréntesis no balanceados: (`(3`, `((3`, o `3)`),
   - operador sin operando (`3 +`),
   - dos expresiones sin operador (`(1)(2)`),
   - menos unario (`-3`).
5. Que la entrada inválida nunca lance un error de Python.
6. Que los mensajes de error indiquen la posición.
7. Números con ceros a la izquierda.
8. Paréntesis anidados.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
| ------------------------ | ------- | -------- | --------- | ----------------------- |
|                          |         |          |           |                         |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

> No basta con "daba mal". Digan contra qué lo están comparando: qué regla,
> qué línea de la semántica declarada del README.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
| ------- | --------------------- | ---- | ----------- | ----------- | ------------ |
|         |                       |      |             |             |              |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

> Por ejemplo `%`. ¿Cuántos archivos hay que tocar? ¿Por qué?

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué _no_ encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. _"No usamos"_ es una declaración válida y completa; _"lo
descartamos porque..."_ es de las mejores respuestas posibles.
