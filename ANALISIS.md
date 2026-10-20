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

Además de agregar casos nuevos, **reorganizamos** la suite por nivel: las pruebas
de `evaluator` y de `parser` que ejecutaban todo el pipeline se movieron a
`test_integracion.py` (son de integración), y escribimos pruebas unitarias
por componente (el parser recibe una lista de `Token`, el evaluador recibe un
AST). De esta forma un defecto del lexer no se disfraza de defecto del parser.

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

**Lexer — unit (texto → tokens)**

| Prueba (archivo::nombre)                              | Entrada | Esperado                  | Categoría | ¿Por qué esa categoría?       |
| ----------------------------------------------------- | ------- | ------------------------- | --------- | ----------------------------- |
| `test_lexer.py::test_rechaza_un_caracter_desconocido` | `"3 @"` | `ErrorDeSintaxis` (pos 2) | inválida  | `@` no pertenece al lenguaje. |

**Parser — unit (tokens → AST)**

| Prueba (archivo::nombre)                                     | Entrada               | Esperado                  | Categoría | ¿Por qué esa categoría?                                |
| ------------------------------------------------------------ | --------------------- | ------------------------- | --------- | ------------------------------------------------------ |
| `test_parser.py::test_un_numero_produce_una_hoja`            | `[NUMERO(42)]`        | `Numero(42)`              | normal    | un solo número.                                        |
| `test_parser.py::test_la_suma_agrupa_dos_numeros`            | `3 + 4`               | `(3 + 4)`                 | normal    | caso base de un operador.                              |
| `test_parser.py::test_la_resta_agrupa_dos_numeros`           | `10 - 3`              | `(10 - 3)`                | normal    | caso base.                                             |
| `test_parser.py::test_el_producto_agrupa_dos_numeros`        | `6 * 7`               | `(6 * 7)`                 | normal    | caso base.                                             |
| `test_parser.py::test_la_division_agrupa_dos_numeros`        | `10 / 2`              | `(10 / 2)`                | normal    | caso base.                                             |
| `test_parser.py::test_precedencia_suma_producto`             | `3 + 4 * 2`           | `3 + (4 * 2)`             | normal    | precedencia `*` sobre `+`.                             |
| `test_parser.py::test_precedencia_suma_producto_izq`         | `2 * 3 + 4`           | `(2 * 3) + 4`             | normal    | precedencia en el otro orden.                          |
| `test_parser.py::test_los_parentesis_cambian_precedencia`    | `(3 + 4) * 2`         | `(3 + 4) * 2`             | normal    | los paréntesis mandan.                                 |
| `test_parser.py::test_una_operacion_entre_parentesis`        | `(3 + 4)`             | `(3 + 4)`                 | normal    | paréntesis que no cambian la agrupación.               |
| `test_parser.py::test_la_resta_asocia_por_la_izquierda`      | `10 - 3 - 1`          | `(10 - 3) - 1`            | frontera  | cadena de la misma precedencia. **Reveló un defecto.** |
| `test_parser.py::test_la_division_asocia_por_la_izquierda`   | `12 / 6 / 2`          | `(12 / 6) / 2`            | frontera  | ídem con el nivel producto. **Reveló un defecto.**     |
| `test_parser.py::test_parentesis_anidados`                   | `((3))`               | `Numero(3)`               | frontera  | anidamiento.                                           |
| `test_parser.py::test_anidamiento_profundo`                  | `((2 + 3) * (4 - 1))` | árbol correspondiente     | frontera  | anidamiento profundo.                                  |
| `test_parser.py::test_rechaza_una_lista_de_tokens_vacia`     | `[]`                  | `ErrorDeSintaxis`         | inválida  | no hay expresión. **Reveló un defecto.**               |
| `test_parser.py::test_rechaza_un_token_inesperado_al_inicio` | `[+, 3]`              | `ErrorDeSintaxis` (pos 0) | inválida  | operador sin operando izquierdo.                       |
| `test_parser.py::test_rechaza_un_parentesis_sin_cerrar`      | `(3`                  | `ErrorDeSintaxis`         | inválida  | falta el `)`.                                          |
| `test_parser.py::test_rechaza_un_operador_sin_operando`      | `3 +`                 | `ErrorDeSintaxis`         | inválida  | falta el operando derecho.                             |
| `test_parser.py::test_rechaza_un_parentesis_de_mas`          | `3)`                  | `ErrorDeSintaxis`         | inválida  | token sobrante. **Reveló un defecto.**                 |
| `test_parser.py::test_rechaza_dos_expresiones_sin_operador`  | `(1)(2)`              | `ErrorDeSintaxis`         | inválida  | falta el operador entre grupos.                        |

**Evaluator — unit (AST → número)**

| Prueba (archivo::nombre)                                           | Entrada                    | Esperado            | Categoría | ¿Por qué esa categoría?                        |
| ------------------------------------------------------------------ | -------------------------- | ------------------- | --------- | ---------------------------------------------- |
| `test_evaluator.py::test_un_numero_se_evalua_a_si_mismo`           | `Numero(42)`               | `42`                | normal    | hoja.                                          |
| `test_evaluator.py::test_suma`                                     | `3 + 7`                    | `10`                | normal    | un operador.                                   |
| `test_evaluator.py::test_resta`                                    | `10 - 3`                   | `7`                 | normal    | un operador.                                   |
| `test_evaluator.py::test_multiplicacion`                           | `6 * 7`                    | `42`                | normal    | un operador.                                   |
| `test_evaluator.py::test_division`                                 | `10 / 2`                   | `5.0`               | normal    | un operador.                                   |
| `test_evaluator.py::test_operaciones_anidadas`                     | `(3 + 4) * 2`              | `14`                | normal    | subárboles.                                    |
| `test_evaluator.py::test_division_fraccionaria`                    | `10 / 4`                   | `2.5`               | frontera  | división real.                                 |
| `test_evaluator.py::test_division_entre_cero`                      | `1 / 0`                    | `ErrorDeEvaluacion` | frontera  | límite del dominio.                            |
| `test_evaluator.py::test_division_entre_cero_anidada`              | `1 + (1 / 0)`              | `ErrorDeEvaluacion` | frontera  | el error se propaga.                           |
| `test_evaluator.py::test_operador_desconocido_no_es_representable` | `Operador.de_simbolo("@")` | `ValueError`        | inválida  | un operador inexistente no se puede construir. |
| `test_evaluator.py::test_nodo_desconocido`                         | `"no soy un nodo"`         | `ErrorDeEvaluacion` | inválida  | nodo fuera del modelo.                         |

**Integración (texto → AST / texto → número)**

| Prueba (archivo::nombre)                        | Entrada      | Esperado          | Categoría | ¿Por qué esa categoría?                            |
| ----------------------------------------------- | ------------ | ----------------- | --------- | -------------------------------------------------- |
| `test_integracion.py::test_resta_asocia_izq`    | `10 - 3 - 1` | `6`               | frontera  | síntoma visible del defecto de asociatividad.      |
| `test_integracion.py::test_division_asocia_izq` | `12 / 6 / 2` | `1`               | frontera  | ídem en el nivel producto.                         |
| `test_integracion.py::test_simbolo_desconocido` | `3 @ + 3`    | `ErrorDeSintaxis` | inválida  | carácter fuera del lenguaje a través del pipeline. |

**Línea de comandos (despacho y errores)**

| Prueba (archivo::nombre)                                        | Entrada                | Esperado                     | Categoría | ¿Por qué esa categoría?                              |
| --------------------------------------------------------------- | ---------------------- | ---------------------------- | --------- | ---------------------------------------------------- |
| `test_cli.py::test_sin_bandera_se_evalua`                       | `["3 + 4"]`            | `("evaluar", ["3 + 4"])`     | normal    | despacho por defecto.                                |
| `test_cli.py::test_la_bandera_arbol_selecciona_su_comando`      | `["--arbol", ...]`     | `("arbol", ...)`             | normal    | bandera → comando.                                   |
| `test_cli.py::test_la_bandera_puede_ir_despues_de_la_expresion` | `["3 + 4", "--arbol"]` | `("arbol", ["3 + 4"])`       | frontera  | la bandera en otra posición.                         |
| `test_cli.py::test_la_bandera_tokenizar_selecciona_su_comando`  | `["--tokenizar", ...]` | `("tokenizar", ...)`         | normal    | despacho.                                            |
| `test_cli.py::test_la_bandera_parsear_selecciona_su_comando`    | `["--parsear", ...]`   | `("parsear", ...)`           | normal    | despacho.                                            |
| `test_cli.py::test_una_bandera_inexistente_falla`               | `["--tokenizer", ...]` | `ErrorDeComando`             | inválida  | comando no implementado. **Reveló un defecto.**      |
| `test_cli.py::test_el_comando_evaluar`                          | `"3 + 4"`              | `"7"`                        | normal    | comando.                                             |
| `test_cli.py::test_el_comando_arbol`                            | `"3 + 4"`              | árbol de texto               | normal    | comando.                                             |
| `test_cli.py::test_el_comando_tokenizar`                        | `"3 + 4"`              | tokens, uno por línea        | normal    | comando.                                             |
| `test_cli.py::test_el_comando_parsear`                          | `"3 + 4"`              | `OperacionBinaria('+', ...)` | normal    | comando.                                             |
| `test_cli.py::test_main_evalua_y_sale_con_cero`                 | `["3 + 4"]`            | código `0`                   | normal    | código de salida en éxito.                           |
| `test_cli.py::test_una_expresion_invalida_sale_con_uno`         | `["3 @"]`              | código `1`                   | inválida  | código de salida en error.                           |
| `test_cli.py::test_el_modo_interactivo_propaga_el_error`        | stdin `"3 + 4\n3 @"`   | código `1`                   | inválida  | código de salida interactivo. **Reveló un defecto.** |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

El primero fue el **parser con una lista de tokens vacía**: `Parser([]).parsear()`
lanzaba un `IndexError` de Python en vez de rechazar la entrada. Lo reveló
`test_rechaza_una_lista_de_tokens_vacia`.

El más importante, sin embargo, fue la **asociatividad**: el parser agrupaba a la
derecha, lo que rompe toda cadena de operadores de igual precedencia.

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

En el README se declara la semántica objetivo:

- "los operadores de la misma precedencia se asocian **a la izquierda**" →
  `10 - 3 - 1` debe ser `(10 - 3) - 1 = 6`; daba `10 - (3 - 1) = 8`.
- "la entrada inválida debe rechazarse con **`ErrorDeSintaxis`**, **nunca con un
  error de Python**" → `""`, `(3` y `3 +` lanzaban `IndexError`.
- "la entrada inválida ... `ErrorDeSintaxis`" → `3)` y `(1)(2)` se aceptaban en
  silencio (devolvían `3` y `1`).
- "caracteres ... que no pertenecen al lenguaje" / "entrada inválida" → el lexer
  ignoraba los caracteres desconocidos (`3 @` daba `3`).
- En la CLI, un comando inexistente (`--tokenizer`) se interpretaba como texto y
  fallaba con un error de sintaxis en lugar de reportar que el comando no existe.

### 4.3 ¿Qué cambio realizaron?

| Defecto                                                 | Entrada que lo revela | Daba              | Debería dar                          | Commit rojo | Commit verde |
| ------------------------------------------------------- | --------------------- | ----------------- | ------------------------------------ | ----------- | ------------ |
| Parser: se acaban los tokens (`_avanzar` sin comprobar) | `[]`, `(3`, `3 +`     | `IndexError`      | `ErrorDeSintaxis` (con posición)     | `8b444d0`   | `4162b16`    |
| Parser: no verifica que consumió toda la entrada        | `3)`, `(1)(2)`        | `3`, `1`          | `ErrorDeSintaxis`                    | `cc3aef8`   | `18b8e4b`    |
| Asociatividad derecha en el nivel `+ -`                 | `10 - 3 - 1`          | `8`               | `6`                                  | `5175d63`   | `155d2e9`    |
| Asociatividad derecha en el nivel `* /`                 | `12 / 6 / 2`          | `4.0`             | `1.0`                                | `51da91b`   | `13248cb`    |
| Lexer: ignora caracteres desconocidos                   | `3 @ 4`               | `3`               | `ErrorDeSintaxis` (pos del carácter) | `c2e7e59`   | `b6bf949`    |
| CLI: acepta banderas/comandos inexistentes              | `--tokenizer "3 + 4"` | error de sintaxis | `ErrorDeComando`                     | `bfc327d`   | `0df0783`    |
| CLI: el modo interactivo no propaga el fallo            | stdin `"3 + 4\n3 @"`  | código `0`        | código `1`                           | `bfc327d`   | `8fca0f4`    |

**Cambios concretos**

- **Parser / tokens agotados:** el método`_factor` verifica si `_actual()` es `None`
  antes de consumir y lanza `ErrorDeSintaxis` usando `_posicion_final()`.
  El `)` ausente también se comprueba antes de consumir.
- **Parser / tokens sobrantes:** `parsear()` verifica que `_actual() is None`
  después de parsear la expresión.
- **Asociatividad:** `_expresion`/`_termino` pasan de recursión derecha a un
  ciclo que reasigna el lado izquierdo.
- **Lexer:** la rama `else` no hacía nada, ahora lanza `ErrorDeSintaxis(caracter
inesperado, i)`.
- **CLI:** `_elegir_comando` lanza `ErrorDeComando` ante un argumento que empieza
  con `--` y no es una bandera conocida; `_procesar_entrada` acumula el código y
  devuelve `1` si alguna línea falló.

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

Ningún arreglo se hizo específicamente para que un test o ejemplo concreto pasara.

- La asociatividad cambia la forma de parsear el nivel de operadores, así que
  aplica a cualquier cadena de `+`, `-`, `*`, `/`. Se comprobó además con
  `20 / 2 / 5`, `1 - 2 - 3 - 4`, `2 - 3 + 4`.
- La validación de fin de entrada cubre cualquier token sobrante, no sólo
  `)`; el mismo `fix` arregló `(1)(2)` y `1 2`, que no estaban en la prueba roja.
- La comprobación de "se acabaron los tokens" arregló `(3` y `3 +` además del
  `[]` que sí estaba en la prueba.
- El lexer ahora rechaza cualquier carácter fuera de `SIMBOLOS` (`@`, `$`, …).

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

1. **Duplicación / condicionales repetidos:** `_expresion` y `_termino` en
   `parser.py` eran casi el mismo método copiado; sólo cambiaba el conjunto de
   operadores.
   Una consecuencia directa fue que arreglar la asociatividad se tuvo que hacer dos veces.
2. **Conocimiento de los operadores disperso (rigidez / _shotgun surgery_):** el
   conjunto de operadores estaba en `lexer.SIMBOLOS`, en `parser.OPERADORES_*`,
   en la cadena de `if` del `evaluator` y como cadenas mágicas en `ast`.
   Para agregar un operador era necesario tocar cuatro archivos.
3. **Acoplamiento de la CLI con el pipeline:** `cli.py` conocía el lexer, el
   parser y los nodos del AST (y hasta el dibujo del árbol).
   Cualquier cambio en el AST podía romper la CLI.
4. **Pruebas acopladas al pipeline:** las de `evaluator` usaban `interpretar(...)`,
   así que un defecto del lexer poría parecer un defecto del evaluador.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

**(a) `Operador` como catálogo único** (`operadores.py`). Un enum con `simbolo`,
`precedencia` y `funcion`. El parser, el evaluador y el AST trabajan con
`Operador` en vez de comparar cadenas.
Esto es equivalente pues el conjunto de
operadores y su resultado son los mismos; sólo cambia _de dónde_ salen el símbolo
y la operación.

**(b) Un solo `_nivel(siguiente, precedencia)`** en el parser.
No cambia el comportamiento pues los dos métodos tenían flujo de control idéntico.
Lo único que variaba era el nivel, que ahora se pasa por parámetro.

**(c) Desacoplamiento de la CLI.**
Este cambio fue de fondo: cli.py concentraba tres responsabilidades: componer el pipeline (interpretar), dibujar el AST (formatear_arbol) y todo el IO (recorrer argv, leer stdin, imprimir y traducir errores).
Como consecuencia, importaba `lexer`, `parser`, `evaluator` y `ast`.
Cualquier cambio en el AST o en el pipeline obligaba a tocarla.
Se separó por responsabilidad: `interpretar` pasó a la fachada del paquete (**init**.py),
`formatear_arbol` a ast.py y los comandos a comandos.py con la tabla `COMANDOS`.
El archivo cli.py quedó reducido a mapear banderas a comandos, hacer el IO y atrapar ErrorDelInterprete/ErrorDeComando.
Gracias a este cambio, la CLI ya no conoce los nodos ni el pipeline, y agregar un comando unicamente requiere agregar una función más en la tabla y una bandera.

El comportamiento no cambió por que esencialmente se sigue usando la misma pipeline de `interpretar` o `formatear_arbol` para el caso donde se pasa la bandera `--arbol`.

Este cambio permitió agregar nuevas características de forma sencilla: ahora se permiten los comandos de _tokenizar_ y _parsear_.

**(d) Reorganización de la suite** en unitarias por componente e integración.
Se conservaron todas las pruebas, sólo cambiaron de archivo.

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

**Ninguno.** No hay que adaptar una interfaz ajena por lo que no es necesario usar un Adapter
y no hay familias de productos que justifiquen usar un Factory Method.
En cierta forma el "factory" ya existe y es `POR_SIMBOLO`, un diccionario `simbolo → Operador`,
pero no consideramos que amerite implementar todo el patrón completo.

La cadena de `if` del evaluador se mejoró con una tabla (la `funcion`
dentro del enum), que es más simple que una jerarquía de clases.

**¿Qué tendría que cambiar para que empezara a convenir?** Si cada operador
tuviera comportamiento muy diferente (aridad variable, reglas de tipo, mensajes
propios, asociatividad) o si los operadores llegaran de **plugins**,
entonces un Factory/registry sí se justificaría.
Con cuatro operadores estáticos y una sola operación cada uno no lo consideramos apropiado.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

Agregar `%` (después de la refactorización) implica modificar:

| Archivo         | Qué agregar                           | Por qué                                            |
| --------------- | ------------------------------------- | -------------------------------------------------- |
| `tokens.py`     | `TipoToken.MODULO`                    | El lexer clasifica el símbolo como un `TipoToken`. |
| `lexer.py`      | `"%": TipoToken.MODULO` en `SIMBOLOS` | Reconocer el carácter.                             |
| `operadores.py` | `MODULO = ("%", 2, operator.mod)`     | Símbolo, precedencia y operación.                  |
| `evaluator.py`  | — (nada)                              | Se resuelve por `operador.funcion`.                |

Ya no hay que tocar el parser (la precedencia sale de `Operador`) ni el
evaluador. Lo que queda duplicado es la representación del operador entre
`TipoToken` (nivel léxico) y `Operador` (nivel semántico); unificarlas dejaría
`%` en dos lugares, pero no lo hicimos porque implicaba que `Token.tipo` fuera la
unión de dos enums. Con lo actual, el punto más molesto es tener que registrar el
operador en dos enumeraciones.
