.. currentmodule:: myhdl

.. _background:

**********************
Información previa
**********************


.. _prerequisites:

Pre requisitos
==============

..
 You need a basic understanding of Python to use MyHDL. If you don't know Python,
 don't worry: it is is one of the easiest programming languages to learn  [#]_.
 Learning Python is one of the best time investments that engineering
 professionals can make  [#]_.

Se necesita una comprensión básica de Python para usar MyHDL. Si no conoce
Python no se preocupe: es uno de los lenguajes de programación más fáciles
[#]_.
Aprender Python es uno de las mejores inversiones en tiempo que un
ingeniero o profesional puede hacer [#]_. 

..
 For starters, http://docs.python.org/tutorial is probably the
 best choice for an on-line tutorial. For alternatives, see
 http://wiki.python.org/moin/BeginnersGuide.

Para novatos, http://docs.Pythonthon.org/tutorial es probablemente la
mejor elección de un tutorial en línea. Para otras alternativas vea
http://wiki.Pythonthon.org/moin/BeginnersGuide


..
 A working knowledge of a hardware description language such as Verilog or VHDL
 is helpful.

Un conocimiento práctico de un lenguaje de descripción de hardware como
Verilog o VHDL es de ayuda.

..
 Code examples in this manual are sometimes shortened for clarity. Complete
 executable examples can be found in the distribution directory at

Por claridad algunas veces se recortan los códigos por claridad. Los
ejecutable completos se pueden encontrar en la distribución directamente en
:file:`example/manual/`.


.. _tutorial:

Un pequeño tutorial en generadores 
==================================

.. index:: single: generators; tutorial on

..
 Generators were introduced in
 Python 2.2. Because generators are the key concept in MyHDL, a small tutorial is
 included here.

Los generadores se introdujeron en Python 2.2. Debido a que son un concepto
clave en MyHDL, se incluye acá un pequeño tutorial.

..
   Consider the following nonsensical function::

Considere la siguiente función ilógica::

   def function():
       for i in range(5):
           return i

..
 You can see why it doesn't make a lot of sense. As soon as the first loop
 iteration is entered, the function returns::

Ud. puede ver por qué no tiene mucho sentido. Cuando el primer bucle de
iteración se ingrese, la función retorna::

   >>> function()
   0

..
   Returning is fatal for the function call. Further loop iterations never get a
 chance, and nothing is left over from the function call when it returns.

Retornar es fatal para la llamada a la función. Por lo tanto las iteraciones del
bucle nunca tienen oportunidad de ejecutarse, y nada se deja sobre el llamado a la
función cuando ella retorna.

..
 To change the function into a generator function, we replace :keyword:`return`
 with :keyword:`yield`::

Para cambiar la función en una función generadora, reemplazamos
:keyword:`return` por :keyword:`yield`::


   def generator():
       for i in range(5):
           yield i

.. Now we get::

ahora obtenemos::

   >>> generator()
   <generator object at 0x815d5a8>

..
 When a generator function is called, it returns a generator object. A generator
 object supports the iterator protocol, which is an expensive way of saying that
 you can let it generate subsequent values by calling its :func:`next` method::

Cuando una función generadora se invoca, ella retorna un objeto generador.
Un objeto generador permite el protocolo iterador, que es una manera
costosa de decir que Ud. puede generar valores subsecuentes invocando el
método
:func:`next`::

   >>> g = generator()
   >>> g.next()
   0
   >>> g.next()
   1
   >>> g.next()
   2
   >>> g.next()
   3
   >>> g.next()
   4
   >>> g.next()
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   StopIteration

..
 Now we can generate the subsequent values from the for loop on demand, until
 they are exhausted. What happens is that the :keyword:`yield` statement is like
 a :keyword:`return`, except that it is non-fatal: the generator remembers its
 state and the point in the code when it yielded. A higher order agent can decide
 when to get the next value by calling the generator's :func:`next` method. We
 say that generators are :dfn:`resumable functions`.

Ahora podremos generar los valores subsecuentes de el bucle for por
demanda, hasta que ellos estén exaustos. Qué pasa cuando la instrucción
:keyword:`yield` es como una instrucción :keyword:`return` excepto que no
es fatal: el generador recuerda su estado y el punto en el código cuando él
entrega. Un agente de alto orden puede decidir cuándo tomar el próximo
valor llamando el método del generador :func:`next` Decimos que los
generadores son  :dfn:`resumables functions`

.. index::
   single: VHDL; process
   single: Verilog; always block

..
 If you are familiar with hardware description languages, this may ring a bell.
 In hardware simulations, there is also a higher order agent, the Simulator, that
 interacts with such resumable functions; they are called  :dfn:`processes` in
 VHDL and  :dfn:`always blocks` in Verilog.  Similarly, Python generators provide
 an elegant and efficient method to model concurrency, without having to resort
 to some form of threading.

Si Ud. está familiarizado con los lenguajes de descripción de hardware,
esto le puede sonar familiar. En simulaciones de hardware, hay también un
agente de alto orden,  el simulador, que interactúa con funciones que
reanudan; ellas son llamadas :dfn:`procesos` en VHDL y :dfn:`blocks always`
en Verilog. Igualmente, Los generadores Python suministran un método
elegante y eficiente para modelar concurrencia, sin tener recurrir a algo
como los hilos.


.. index:: single: sensitivity list

The use of generators to model concurrency is the first key concept in MyHDL.
The second key concept is a related one: in MyHDL, the yielded values are used
to specify the conditions on which the generator should wait before resuming. In
other words, :keyword:`yield` statements work as general  sensitivity lists.

El uso de generadores para modelar la concurrencia es el primer concepto
clave en MyHDL. El segundo concepto clave  es uno relacionado: en MyHDL,
los valores *yieled* son usados para especificar las condiciones bajo las
cuales el generador debería esperar antes volver a entrar. En otras
palabras las instrucciones :keyword:`yield` trabajan como listas sensibles

.. _deco:

Sobre los decoradores
=====================

.. index:: single: decorators; about

..
 Python 2.4 introduced a feature called decorators. MyHDL takes advantage
 of this feature by defining a number of decorators that facilitate hardware
 descriptions. However, some users may not yet be familiar with decorators.
 Therefore, an introduction is included here.

Python 2.4 introdujo una característica llamada decoradores. MyHDL toma
ventaja de esta característica mediante la definición de un número de
decoradores que facilitan las descripciones de hardware.
Sin embargo, algunos usuarios pueden no estar familiarizados con los
decoradores. Por lo tanto se incluye una introducción acá.

..
 A decorator consists of special syntax in front of a function declaration. It
 refers to a decorator function. The decorator function automatically transforms
 the declared function into some other callable object.

Un está compuesto de una sintaxis especial al frente de la declaración de
una función. Se refiere a una función decorada. La función decorada
automáticamente transforma la función declarada  en algún otro objeto
invocable.

A decorator function :func:`deco` is used in a decorator statement as follows::

Una función decorada :func:`deco()`
usada en una instrucción de decorado así::

   @deco
   def func(arg1, arg2, ...):
       <body>

.. This code is equivalent to the following::

Este código es equivalente al siguiente::

   def func(arg1, arg2, ...):
       <body>
   func = deco(func)

..
 Note that the decorator statement goes directly in front of the function
 declaration, and that the function name :func:`func` is automatically reused for
 the final result.


Observe que la instrucción decoradora va directamente en frente de la
declaración de la función, y entonces el nombre de la función :func:`func` es
automáticamente reutilizada para el resultado final.
 
..
 MyHDL uses decorators to create ready-to-simulate generators from local
 function definitions. Their functionality and usage will be described
 extensively in this manual.


MyHDL usa decoradores para crear generadores listos para simular a partir de las definiciones de funciones locales. Su funcionalidad y uso serán descritos extensivamente en este manual.

.. rubric:: Footnotes

.. [#] Debe estar aburrido de afirmaciones de este tipo pero en este
 caso es verdad.

.. You must be bored by such claims, but in Python's case it's true.

.. [#] No estoy parcializado

.. I am not biased.

