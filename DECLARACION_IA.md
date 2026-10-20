# Declaración de uso de Inteligencia Artificial

**Actividad:** Tarea 1 — Mini intérprete de expresiones
**Integrantes:** Contreras Morales Román Ismael
**Fecha:** 16 de octubre de 2026

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [x] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
| ----------- | ----------------------------- |
| OpenCode    | DeepSeek V4.1 Flash           |

---

## 2. Objetivo del uso

Usé la herramienta para tareas mecánicas o menores,
para contrastar y verificar el análisis que ya había hecho por mi cuenta,
también para preguntar detalles de uso de `pytest`
y para obtener alternativas de diseño.

| Para qué la usamos                                                                 | En qué parte del entregable                                                                        |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Un análisis **posterior** al mío, para ver si se me escapaba algo                  | `ANALISIS.md` §5.1 — halló la **duplicación `termino`/`expresion`**, que yo no había visto         |
| Revisar las pruebas que yo hice y sugerir/agregar casos que se me pudieron escapar | `tests/test_evaluator.py`, `test_parser.py`, `test_lexer.py`, `test_integracion.py`, `test_cli.py` |
| Resolver dudas puntuales de cómo probar el **IO** del CLI                          | `tests/test_cli.py`; `_procesar_entrada` en `cli.py`                                               |
| Agregar **anotaciones de tipo**                                                    | `src/mini_interprete/*`                                                                            |
| Revisión general (errores y áreas de oportunidad) después de cada fix/refactor     | reportes de cada paso                                                                              |

**Sobre la autoría de las decisiones de diseño:** las refactorizaciones que se
hicieron fueron idea mía (el desacoplamiento del CLI y el enum `Operador`);
la única refactorización que la herramienta propuso fue la de `termino`/`expresion`.

---

## 3. Prompts principales

Textuales, tal como los escribí:

```
analyze the codebase and the ANALISIS.md.

I have flagged some bugs and code smells in 'observaciones.md', do you see any other problems?
```

```
give me the pros/cons of adding another kind of error.
Something like ErrorLexico that inherits from ErrorInterprete
```

```
Please check the tests and tell me if you find any edge cases i might be missing.
```

```
Currently I use a table for dispatching the actual operation linked to an `Operator`
maybe I can encapsulate as a method in `Operador` that returns the actual python Callable.
What options are there to do this?
```

```
add type hints as much as possible without touching tests,
nor changing behaviour.
if there is a hard one, leave as is and report at the end.
```

```
how would it look to use a Protocol class, or ABC for `Operador`
so I can define subclasses `Mult`, `Menos`, `Div` etc.
Then use a factory pattern to dispatch the correct variant for each case?

is it overkill?
```

```
how could I use pytest for the IO in a cli?
```

```
is there a way to test IO with pytest without needing
monkeypatch nor capsys?
```

```
Do a final check of the codebase.
Tell me if the promised improvements in ANALISIS.md were actually delivered.
Is the test suite comprehensive?
```

---

## 4. Cómo se incorporó o se descartó lo obtenido

| Qué produjo la herramienta                                                                                         | ¿Aceptado, modificado o descartado?   | Por qué                                                                                                                                                                                                                   | Dónde quedó (archivo / commit)                                        |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Análisis posterior al mío → nombró la **duplicación `_expresion`/`_termino`** como señal de mal diseño             | Aceptado                              | Es lo que yo **no** había visto; también explica por qué el defecto de asociatividad se arregló dos veces (amplificación del cambio)                                                                                      | `ANALISIS.md` §5.1; `parser.py`, `d5bf9bd`                            |
| Revisión de mis pruebas y sugerencia de casos que se me escaparon                                                  | Modificado                            | La estrategia, las categorías y las pruebas rojas son mías; la herramienta completó la mecánica y sugirió casos faltantes                                                                                                 | `tests/test_*.py`                                                     |
| Para probar el IO del CLI propuso `monkeypatch` y `capsys`                                                         | Descartado                            | Me opuse y pedí otra forma más simple, sin fixtures; se inyectó el flujo                                                                                                                                                  | `_procesar_entrada` + `io.StringIO` en `cli.py` y `tests/test_cli.py` |
| Agregar anotaciones de tipo                                                                                        | Aceptado                              | Tarea mecánica                                                                                                                                                                                                            | `7df2f27`                                                             |
| Revisión general tras cada fix/refactor → señaló la **inconsistencia del código de salida** en el modo interactivo | Aceptado                              | Es una inconsistencia real que yo no había anotado en ese momento                                                                                                                                                         | `cli.py`, `8fca0f4`                                                   |
| **Refactor del `Operador`** (idea mía)                                                                             | Modificado                            | Propuse el enum; en su primera versión la función quedó en una tabla aparte del evaluador; **yo propuse** meter también la función en el enum, y la herramienta afinó la forma (`funcion` + traducir `ZeroDivisionError`) | `operadores.py`, `61216ed`                                            |
| **Refactor `termino`/`expresion` → `_nivel(siguiente, precedencia)`** (idea de la herramienta)                     | Rechazado al inicio; aceptado después | Le dije que no le veía el beneficio; lo retomé cuando el refactor `Operador` exhibió aún más la duplicación.                                                                                                              | `parser.py`, `d5bf9bd`                                                |
| Jerarquía `Protocol`/ABC de operadores + `Factory Method`                                                          | Descartado                            | Concluimos que es sobre-ingeniería para 4 operadores de una línea                                                                                                                                                         | `ANALISIS.md` §5.3                                                    |
| Unificar `TipoToken` con `Operador` (`Token.tipo: TipoToken \| Operador`)                                          | Descartado                            | No me convenció la unión de dos enums                                                                                                                                                                                     | —                                                                     |
| Subtipo `ErrorLexico(ErrorDeSintaxis)` para el error del lexer                                                     | Descartado                            | El README §7 fija `ErrorDeSintaxis`                                                                                                                                                                                       | — (se usó `ErrorDeSintaxis`)                                          |

### 4.1 Si la usaron para el análisis: el contraste

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

|                                                                      |                                                                                                                                                                                                                                                                                                  |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ¿Qué encontró la herramienta que ustedes **no** habían notado?       | La **duplicación de `_expresion`/`_termino`** en el parser, y que por eso el mismo defecto de asociatividad se tuvo que arreglar dos veces (una por nivel). Yo había detectado el defecto de asociatividad, pero no había visto que los dos métodos eran prácticamente el mismo código repetido. |
| ¿Qué **no** encontró, que en este curso sí consideramos un problema? | No detectó los problemas en la cli: baja cohesión y alto acoplamiento con el resto de los módulos. Tampoco detectó el problema con los operadores: la lógica estaba dispersa en cuatro lugares, y se recurría a cadenas mágicas para manejarlos.                                                 |

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

- Leyendo y analizando críticamente el código propuesto por la herramienta, antes de incorporarlo al repositorio.

- Ejecutando la suite completa (`pytest`) después de cada cambio. El estado
  final es 60 pruebas en verde, y cada refactor se hizo con las mismas pruebas
  pasando antes y después (p. ej. `_nivel`: 47 → 47).

- Contrastando contra el punto 7 del README (semántica declarada).
  Ahí están la asociatividad a la izquierda, la división real, la división entre cero como
  `ErrorDeEvaluacion` y "nunca un error de Python". No acepté nada que violara esas reglas.

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

En general la herramienta funcionó bien y no dio problemas.
En todo caso, la limitación es de profundidad, no de corrección.
Se quedó en la capa de las pruebas y de los defectos más evidentes del intérprete: los errores léxicos, la asociatividad por la izquierda y la duplicación de termino/expresion.
No fue más a fondo hacia el diseño: no propuso el refactor del Operador ni señaló los problemas de la CLI (el acoplamiento y la falta de un punto de extensión).
Esos no son defectos de funcionamiento, pero sí importan si a futuro se quiere agregar funcionalidad.
Una segunda limitación, de método: insistió en un refactor que a mi parecer era prematuro: colapsar termino/expresion.
A mi parecer, ese cambio cayó de forma mucho más natural después de refactorizar el Operador.
Una vez que la precedencia pasó a ser un dato del enum fue más directo hacer la refactorización por niveles.
La herramienta lo propuso casi desde el inicio, antes de que existiera esta condición necesaria.

### 5.2 ¿Qué harían distinto la próxima vez?

A decir verdad, creo que el método que seguí me sirvió bastante bien.
Primero hice el análisis por mi cuenta (en observaciones.md ya estaban casi todos los defectos),
usé la IA como contraste y no como sustituto, y decidí yo qué se aceptaba y qué se descartaba.
La herramienta me ahorró trabajo mecánico (pruebas, tipos) y me dio un contraste útil, pero el criterio de diseño y las implementaciones fueron mías.

En términos generales la refactorización no presentó problemas, no hubieron regresiones
y los tests fueron pasando de rojo a verde incrementalmente.

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre                         | Número de cuenta |
| ------------------------------ | ---------------- |
| Contreras Morales Román Ismael | 306049851        |
