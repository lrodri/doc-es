.. currentmodule:: myhdl

.. _intro:

*********************
Introducción a MyHDL 
*********************

.. _intro-basic:

Una simulación básica de MyHDL
===============================

..
 We will introduce MyHDL with a classic ``Hello World`` style example. All
 example code can be found in the distribution directory under
 :file:`example/manual/`.  Here are the contents of a MyHDL simulation script
 called :file:`hello1.py`::

Introduciremos MyHDL con el clásico ejemplo  ``Hello World`` Todo el
código del ejemplo se puede encontrar en el directorio de la distribución
bajo :func:`example/manual/` A continuación   el contenido de un guión de
simulación MyHDL llamado :func:`hello1.py`::

   from myhdl import Signal, delay, always, now, Simulation

   def HelloWorld():

       interval = delay(10)

       @always(interval)
       def sayHello():
           print "%s Hello World!" % now()

       return sayHello


   inst = HelloWorld()
   sim = Simulation(inst)
   sim.run(30)

.. When we run this simulation, we get the following output::

Cuando ejecutamos esta simulación, tendremos la siguiente salida::

   % python hello1.py
   10 Hello World!
   20 Hello World!
   30 Hello World!
   _SuspendSimulation: Simulated 30 timesteps

..
 The first line of the script imports a number of objects from the
 ``myhdl`` package. In Python we can only use identifiers that are
 literally defined in the source file   [#]_.

La primera línea del guión importa varios objetos desde el paquete
``myhdl``. En Python sólo podemos usar identificadores
que estén definidos literalmente en el archivo fuente [#]_.

 

..
 Then, we define a function called :func:`HelloWorld`. In MyHDL, hardware
 modules can be modeled using classic functions.  In particular, the
 parameter list is then used to define the interface. In this first
 example, the interface is empty.


Entonces, definimos una función llamada :func:`HelloWorld`
En MyHDL, los módulos de hardware se pueden modelar usando funciones
clásicas. En particular, la lista de parámetros se usa para
definir la interface. En el primer ejemplo, la interface está vacía.


.. index:: single: decorator; always

..
 Inside the top level function we declare a local function called
 :func:`sayHello` that defines the desired behavior. This function is
 decorated with an :func:`always` decorator that has a delay  object as its
 parameter.  The meaning is that the function will be executed whenever the
 specified delay interval has expired.

Dentro de la función de  nivel superior declaramos una función local
llamada :func:`sayHello` que define el comportamiento deseado. Esta función
está decorada con un decorador :func:`always` que tiene como parámetro un
objeto retardo. Su significado es que la función será ejecutada cuando
expire el intervalo de retardo especificado.

..
 Behind the curtains, the :func:`always` decorator creates a Python
 *generator* and reuses the name of the decorated function for it.
 Generators are the fundamental objects in MyHDL, and we will say much more
 about them further on.

Tras bambalinas, el decorador `always()` crea un *generador* Python y
reutiliza el nombre de la función decorada para ella. Los generadores son
objetos fundamentales en MyHDL, diremos mucho más sobre ellos en el futuro.

..
 Finally, the top level function returns the local generator. This is the
 simplest case of the basic MyHDL code pattern to define the contents of a
 hardware module. We will describe the general case further on.

Finalmente, la función de nivel superior retorna el generador local. Este es
el caso más simple en la plantilla de código de MyHDL para definir el
contenido de un módulo de hardware. Describiremos el caso general más
adelante.

..
 In MyHDL, we create an *instance* of a hardware module by calling the
 corresponding function. In the example, variable ``inst`` refers to an
 instance of :func:`HelloWorld`.  To simulate the instance, we pass it as
 an argument to a :class:`Simulation` object constructor.  We then run the
 simulation for the desired amount of timesteps.

En MyHDL, creamos una *instancia* de un módulo de hardware invocando la
función correspondiente. En el ejemplo la variable ``inst`` se refiere a
una instancia de :func:`HellowWorld`. Para simular la instancia la pasamos
como un argumento al objeto constructor :class:`Simulation`. Entonces
ejecutamos la simulación la cantidad deseada de intervalos de tiempo.


.. _intro-conc:

Señales, puertos y concurrencia
===============================

..
 In the previous section, we simulated a design with a single generator and
 no concurrency. Real hardware descriptions are typically massively
 concurrent. MyHDL supports this by allowing an arbitrary number of
 concurrently running generators.

En la sección anterior, simulamos un diseño con un sólo generador y sin
concurrencia. Las descripciones de hardware reales son típicamente
masivamente concurrentes . MyHDL apoya esto permitiendo un número arbitrario
de generadores ejecutandose concurrentemente.

..
 With concurrency comes the problem of deterministic communication. Hardware
 languages use special objects to support deterministic communication between
 concurrent code. In particular, MyHDL  has a :class:`Signal` object which is
 roughly modeled after VHDL signals.

Con la concurrencia viene el problema de la comunicación determinística.
Los lenguajes de hardware usan objetos especiales para apoyar la
comunicación deterministica entre código concurrente. En particular,  MyHDL
tiene un objeto  :class:`Signal`  que es modelado de forma parecida a
las señales VHDL.


..
 We will demonstrate signals and concurrency by extending and modifying our
 first example. We define two hardware modules, one that drives a clock
 signal, and one that is sensitive to a positive edge on a clock signal::

Mostraremos señales y concurrencia extendiendo y modificando nuestro primer
ejemplo.  Definiremos dos módulos de hardware, uno que maneja una señal de
reloj, y otro  que es sensible al flanco ascendente de una señal de reloj::


   from myhdl import Signal, delay, always, now, Simulation


   def ClkDriver(clk):

       halfPeriod = delay(10)

       @always(halfPeriod)
       def driveClk():
           clk.next = not clk

       return driveClk


   def HelloWorld(clk):

       @always(clk.posedge)
       def sayHello():
           print "%s Hello World!" % now()

       return sayHello


   clk = Signal(0)
   clkdriver_inst = ClkDriver(clk)
   hello_inst = HelloWorld(clk)
   sim = Simulation(clkdriver_inst, hello_inst)
   sim.run(50)

.. index::
   single: VHDL; signal assignment
   single: Verilog; non-blocking assignment

..
 The clock driver function :func:`ClkDriver` has a clock signal as its
 parameter.  This is how a *port* is modeled in MyHDL. The function defines
 a generator that continuously toggles a clock signal after a certain
 delay. A new value of a signal is specified by assigning to its ``next``
 attribute. This is the MyHDL equivalent of  the VHDL signal assignment and
 the  Verilog non-blocking assignment.


La función :func:`ClkDriver` tiene una señal de reloj como su parámetro.
Así es cómo se modela un *puerto* en MyHDL. La función define un generador
que continuamente cambia una señal de reloj luego de cierto retardo. Se
especifica un nuevo valor de una señal  asignando al atributo ``next``.
Esto es el equivalente en MyHDL a la asignación de señales en VHDL y la
asignación de no-bloqueo en Verilog.


.. index:: single: wait; for a rising edge

..
 The :func:`HelloWorld` function is modified from the first example. It now
 also takes a clock signal as parameter. Its generator is made sensitive to
 a rising edge of the clock signal. This is specified by the ``posedge``
 attribute of a signal. The edge specifier is the argument of the
 ``always`` decorator. As a result, the decorated function will be executed
 on every rising clock edge.

La función :func:`HelloWorld` se modifica a partir del primer ejemplo.
Ahora también toma una señal de reloj como parámetro. El generador se hace
sensible al flanco de subida de la señal de reloj. Esto es especificado por
el atributo ``postedge`` de una señal. El especificador de flanco es el
argumento del decorador ``always``. Como consecuencia, la función decorada
será ejecutada en cada flanco de subida del reloj.


..
 The ``clk`` signal is constructed with an initial value ``0``. When
 creating an instance of each  hardware module, the same clock signal is
 passed as the argument. The result is that the instances are now connected
 through the clock signal. The :class:`Simulation` object is constructed
 with the two instances.


La señal ``clk`` se construye con un valor inicial de ``0``. Cuando se crea una
instancia de cada módulo de hardware, la misma señal de reloj se pasa como
argumento. El resultado es que las instancias están ahora conectadas a través
de la señal de reloj. El objeto :class:`Simulation` está construido con las dos
instancias.

..
 When we run the simulation, we get::

Cuando ejecutamos la simulación obtendremos::

   % python hello2.py
   10 Hello World!
   30 Hello World!
   50 Hello World!
   _SuspendSimulation: Simulated 50 timesteps


.. _intro-hier:

Parámetros y jerarquía
========================

..
 We have seen that MyHDL uses functions to model hardware modules. We have also
 seen that ports are modeled by using signals as parameters. To make designs
 reusable we will also want to use other objects as parameters. For example, we
 can change the clock generator function to make it more general and reusable, by
 making the clock period parametrizable, as follows::

Hemos visto que MyHDL usa funciones para modelar módulos de hardware.
También hemos visto que los puertos se modelan usando señales como
parámetros. Para hacer diseños reutilizables también podremos usar objetos
como parámetros. Por ejemplo, podemos cambiar la función generadora de
reloj para hacer más general y reutilizable, haciendo el periodo de reloj
parametrizable, así::


   from myhdl import Signal, delay, instance, always, now, Simulation

   def ClkDriver(clk, period=20):

       lowTime = int(period/2)
       highTime = period - lowTime

       @instance
       def driveClk():
           while True:
               yield delay(lowTime)
               clk.next = 1
               yield delay(highTime)
               clk.next = 0

       return driveClk

..
 In addition to the clock signal, the clock period is a parameter, with a default
 value of ``20``.

Además de la señal de reloj, el perido de reloj es un parámetro con un
valor por omisión de ``20``.

.. index:: single: decorator; instance

..
 As the low time of the clock may differ from the high time in case of an
 odd period, we cannot use the :func:`always` decorator with a single delay
 value anymore. Instead, the :func:`driveClk` function is now a generator
 function with an explicit definition of the desired behavior. It is
 decorated with the :func:`instance` decorator.  You can see that
 :func:`driveClk` is a generator function because it contains ``yield``
 statements.


Como el valor tiempo de bajo del reloj puede diferir del tiempo de alto en
el caso de un periodo impar, no podemos usar más el decorador
:func:`always` con un solo valor de retardo. En su lugar, la función
:func:`driveClk` es una función generadora con una definición
explícita del comportamiento deseado.  Es decorada con el decorador
:func:`instance`.  Se puede ver que :func:`driveClk` es una función
generadora porque contiene instrucciones ``yield``.

..
 When a generator function is called, it returns a generator object. This
 is basically what the :func:`instance` decorator does. It is less
 sophisticated than the :func:`always` decorator, but it can be used to
 create a generator from any local generator function.

Cuando se invoca una función generadora, retorna un objeto generador.
Esto es básicamente que el decorador :func:`instance`  realiza. Esto es
menos sofisticado que el decorador :func:`always`, pero se puede usar para
crear un generador de cualquier función generadora local.



..
 The ``yield`` statement is a general Python construct, but MyHDL uses it in a
 dedicated way.  In MyHDL, it has a similar meaning as the wait statement in
 VHDL: the statement suspends execution of a generator, and its clauses specify
 the conditions on which the generator should wait before resuming. In this case,
 the generator waits for a certain delay.

La instrucción ``yield`` es un constructor general de Python  pero MyHDL lo
usa de una manera dedicada. En MyHDL, él tiene un significado similar que la
instrucción wait en VHDL: la instrucción suspende la ejecución de un
generador, y esto causa específicamente condiciones en las cuales el
generarador debería esperar antes de continuar. En este caso, el generador
espera por un cierto retardo.

..
 Note that to make sure that the generator runs "forever", we wrap its
 behavior in a ``while True`` loop.

Esté seguro que el generador se ejecute "indefinidamente" ,
nosotros encerramos este comportamiento en un bucle ``while True``.

..
 Similarly, we can define a general :func:`Hello` function as follows::

De igual forma, podemos definir una función general :func:`Hello` así::

   def Hello(clk, to="World!"):

       @always(clk.posedge)
       def sayHello():
           print "%s Hello %s" % (now(), to)

       return sayHello

.. index:: single: instance; defined

..
 We can create any number of instances by calling the functions with the
 appropriate parameters. Hierarchy can be modeled by defining the instances in a
 higher-level function, and returning them. This pattern can be repeated for an
 arbitrary number of hierarchical levels. Consequently, the general definition of
 a MyHDL instance is recursive: an instance is either a sequence of instances, or
 a generator.

Podemos crear cualquier número de instancias invocando las funciones con el
número apropiado de parámetros. La jerarquía se puede modelar definiendo
las instancias en una función de alto nivel y retornándola. Este patrón
puede ser repetido para un número arbitrario de niveles de jerarquía.
Por lo tanto, la definición general de una instancia MyHDL es
recursiva: una instancia es una secuencia de instancias, o un generador.


..
 As an example, we will create a higher-level function with four instances of the
 lower-level functions, and simulate it::

Como ejemplo, crearemos una función de alto nivel con cuatro instancias
de la función de bajo nivel, y las simulamos::

   def greetings():

       clk1 = Signal(0)
       clk2 = Signal(0)

       clkdriver_1 = ClkDriver(clk1) # asocación posicional: por omision
       clkdriver_2 = ClkDriver(clk=clk2, period=19) # asociación por nombre
       hello_1 = Hello(clk=clk1) # asociación posicional: por omisión
       hello_2 = Hello(to="MyHDL", clk=clk2) # asociación por nombre

       return clkdriver_1, clkdriver_2, hello_1, hello_2


   inst = greetings()
   sim = Simulation(inst)
   sim.run(50)

..
 As in standard Python, positional or named parameter association can be used in
 instantiations, or a mix of both [#]_. All these styles are demonstrated in the
 example above. Named association can be very useful if there are a lot of
 parameters, as the argument order in the call does not matter in that case.

Como en el Python estándar, la asociación posicional o parámetros con con
nombre se puede usar en instanciaciones, o un mezcla de las dos [#]_. Todos
estos estilos están demostrados en el ejemplo de arriba. La asociación con
nombres puede ser muy útil si hay muchos parámetros, ya que el orden de los
parámetros o importa en este caso.

.. The simulation produces the following output::

La simulación produce la siguiente salida::

   % python greetings.py
   9 Hello MyHDL
   10 Hello World!
   28 Hello MyHDL
   30 Hello World!
   47 Hello MyHDL
   50 Hello World!
   _SuspendSimulation: Simulated 50 timesteps


..
   Some commonly used terminology has different meanings in Python versus hardware
   design. Rather than artificially changing terminology, I think it's best to keep
   it and explicitly describing the differences.

.. warning::
 
 Alguna terminología usada comunmente tiene significados diferentes en
 Python y en el diseño de hardware. En lugar de cambiar artifialmente la
 terminología, pienso que es mejor dejarla y explícitamente describir las
 diferencias.

   .. index:: single: module; in Python versus hardware design

..
  A :dfn:`module` in Python refers to all source code in a particular file.
  A module can be reused by other modules by importing. In hardware design,
  a module is  a reusable block of hardware with a well defined interface.
  It can be reused in  another module by :dfn:`instantiating` it.

 Un :dfn:`module` en Python se refiere a todo el código fuente en un
 archivo en particular. Un módulo  puede ser reusado por otros módulos
 importandolos. En el diseño de hardware, un módulo es un bloque
 reutilizable con una interfaz completamente definida. Puede ser
 reutilizada en otro módulo por medio de la :dfn:`instantiating`.

  .. index:: single: instance; in Python versus hardware design


..
  An :dfn:`instance` in Python (and other object-oriented languages) refers
  to the object created by a class constructor. In hardware design, an
  instance is a particular incarnation of a hardware module.

Una :dfn:`instance` en Python (y otros lenguajes orientados a objetos) se
refiere a los objetos creados por una clase constructora. En el diseño de
hardware, una instancia es una encarnación particular de un módulo de
hardware.

..   
   Normally, the meaning should be clear from the context. Occasionally, I may
   qualify terms  with the words "hardware" or "MyHDL" to  avoid ambiguity.

 Normalmente, el significado debería ser claro a partir del contexto.
 Ocasionalmente, puedo cualificar términos con las palabras hardware o
 MyHDL para evitar ambigüedades.

.. _intro-python:

Algunas cosas para resaltar  en MyHDL y Python
==============================================


..
 To conclude this introductory chapter, it is useful to stress that MyHDL is not
 a language in itself. The underlying language is Python,  and MyHDL is
 implemented as a Python package called ``myhdl``. Moreover, it is a design goal
 to keep the ``myhdl`` package as minimalistic as possible, so that MyHDL
 descriptions are very much "pure Python".

Para concluir este capítulo introductorio, es útil recalcar que MyHDL no es
un lenguaje en sí mismo. El lenguaje subyacente es Python y MyHDL está
implementado como un paquete llamado ``myhdl``. Sin embargoi, un objetivo de
diseño es dejar el paquete ``myhdl`` tan pequeño que las descripciones MyHDL sean 
"puro Python".




.. To have Python as the underlying language is significant in several ways:

Tener Python como lenguaje subyacente es significativo de varias formas:

..
 * Python is a very powerful high level language. This translates into high
  productivity and elegant solutions to complex problems.

* Python es un lenguaje de alto nivel muy potente. Este se traduce en
  soluciones altamente productivas y elegantes para problemas complejos.

..
 * Python is continuously improved by some very clever  minds, supported by a
  large and fast growing user base. Python profits fully from the open source
  development model.

* Python es mejorando continuamente por muchas mentes brillantes,
  apoyados por una creciente base de usuarios. Python cumple
  completamente con el modelo de desarrollo de software abierto.

..
 * Python comes with an extensive standard library. Some functionality is
   likely to be of direct interest to MyHDL users: examples include string
   handling, regular expressions, random number generation, unit test
   support, operating system interfacing and GUI development. In addition,
   there are modules for mathematics, database connections, networking
   programming, internet data handling, and so on.

* Python viene con una biblioteca estándar grande. Es probable que Algunas
  funcionalidades sean de interés directo para los usuarios de MyHDL: por
  ejemplo se incluyen: manipulación de cadenas, expresiones regulares,
  generación de números aleatorios, pruebas unitarias, interfaces con el
  sistema operativo  y desarrollo de interfaces gráficas de usuario. Además
  existen módulos de matemáticas, conexiones a bases de datos, programación
  de redes, manipulación de datos por internet y aún más.


..
 * Python has a powerful C extension model. All built-in types are written
   with the same C API that is available for custom extensions. To a module
   user, there is no difference between a standard Python module and a C
   extension module --- except performance. The typical Python development
   model is to prototype everything in Python until the application is
   stable, and (only) then rewrite performance critical modules in C if
   necessary.

* Python tiene un modelo poderoso de extensión de C. Todos los tipos
  primitivos están escritos en el mismo API de C que está disponible en
  extensiones a la medida. Para un usuario de un módulo, no hy diferencia
  entre Python estándar y un módulo de extensión de C -excepto en el
  desempeño. El modelo típico de desarrollo de Python es desarrollar un
  prototipo para todo en Python hasta que la aplicación sea estable, y sólo
  entonces, si es necesario reescribir los módulos críticos en C.



.. _intro-summary:

Resumen y perspectiva
=======================

.. Here is an overview of what we have learned in this chapter:

A continuación un repaso a lo que se aprendió en este capítulo

..
  * Generators are the basic building blocks of MyHDL models. They provide
    the way to model massive concurrency and sensitivity lists.

* Los generadores son los bloques constructores básicos en los modelos
  MyHDL. Ellos suministran la manera de modelar listas de sensibilidad y
  concurrencia masiva.

.. * MyHDL provides decorators that create useful generators from local functions.

  * MyHDL suminstra decoradores que crean generadores útiles a partir de
  funciones locales


.. * Hardware structure and hierarchy is described with classic Python functions.

*  La estructura del hardware y su jerarquía se describen con funciones
   típicas de Python.

..
 * :class:`Signal` objects are used to communicate between concurrent
   generators.

* Los objetos :class:`Signal` se usan para comunicar generadores concurrentes.

.. * A :class:`Simulation` object is used to simulate MyHDL models.

* Un objeto :class:`Simulación` se usa para simular modelos MyHDL.

..
 These concepts are sufficient to start modeling and simulating with MyHDL.

Estos conceptos son suficientes para iniciar a modelar y simular con MyHDL

..
 However, there is much more to MyHDL. Here is an overview of what can be
 learned from the following chapters:

Sin embargo hay mucho más en MyHDL. A continuación lo que viene en los
siguientes capítulos


..
 * MyHDL supports hardware-oriented types that make it easier to write
  typical hardware models. These are described in Chapter :ref:`hwtypes`.

* MyHDL apoya tipos orientados al hardware que hacen fácil escribir modelos
  típicos de hardware. Estos son descritos en el capítulo :ref:`hwtypes`
  .


..
 * MyHDL supports sophisticated and high level modeling techniques. This is
  described in Chapter :ref:`model-hl`.

* MyHDL apoya técnicas sofisticadas y de alto nivel de  modelamiento. Esto
  es descrito en el capítulo de :ref:`model-hl`.


..
 * MyHDL enables the use of modern software verification techniques, such
   as unit testing, on hardware designs. This is the topic of Chapter
   :ref:`unittest`.

* MyHDL habilita el uso de técnicas modernas de verificación de software
  tales como las pruebas unitarias, en los diseños de hardware. Este tópico
  se encuentra en el capítulo de :ref:`unittest` 

..
 * It is possible to co-simulate MyHDL models with other HDL languages such as
  Verilog and VHDL. This is described in Chapter :ref:`cosim`.

* Es posible co-simular modelos MyHDL con otros lenguajes de HDL tales como
  Verilog y VHDL. Esto es descrito en el capítulo co-simulación con Verilog

..
 * Last but not least, MyHDL models can be converted to Verilog, providing
   a path to a silicon implementation. This is the topic of Chapter
   :ref:`conv`.

* Por último si bien no menos importante, los modelos MyHDL se pueden
  convertir en Verilog, suministrando un camino a la implementación en
  silicio. Este tópico se ve en el capítulo conversión a Verilog y VHDL.

.. rubric:: Footnotes

..
 .. [#] The exception is the ``from module import *`` syntax, that imports
 all the symbols from a module. Although this is generally considered bad
 practice, it can be tolerated for large modules that export a lot of
 symbols. One may argue that ``myhdl`` falls into that category.


.. [#] La excepción es la sintaxis de ``from module import *``
 que importa todos los símbolos de un módulo. Sin embargo esto es
 en general considerado una mala práctica, puede ser tolerado para módulos
 grandes que exportan una gran cantidad de símbolos. Un podría argumentar
 que  ``myhdl`` cae en esta categoría


.. [#] All positional parameters have to go before any named parameter.

[#] Todos los parámetros posicionales tienen que ir antes de cualquier
parámetro con nombre
