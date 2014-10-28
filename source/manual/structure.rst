.. currentmodule:: myhdl


.. _model-structure:

************************
Modelamiento estructural
************************

.. index:: single: modeling; structural

Introducción
============

..
 Hardware descriptions need to support the concepts of module instantiation and
 hierarchy.  In MyHDL, an instance is recursively defined as being either a
 sequence of instances, or a generator. Hierarchy is modeled by defining
 instances in a higher-level function, and returning them.  The following is a
 schematic example of the basic case. ::

Las descripciones de  hardware necesitan permitir los conceptos de módulos,
instanciación y jerarquía. En MyHDL, una instancia está definida
recursivamente como una secuencia de instancias o un generador. La
jerarquía se modela definiendo instancias en una función de alto nivel, y
retornandola. El siguiente es un ejemplo esquemático de un caso elemental.  ::

   def top(...):
       ...
       instance_1 = module_1(...)
       instance_2 = module_2(...)
       ...
       instance_n = module_n(...)
       ... 
       return instance_1, instance_2, ... , instance_n

..
 Note that MyHDL uses conventional procedural techniques for modeling structure.
 This makes it straightforward to model more complex cases.


Observe que MyHDL usa técnicas procedimentales para modelar la estructura.
Esto hace que el modelamiento sea directo en casos complejos.
.. _model-conf:

Instnaciación condicional
=========================

.. index:: single: conditional instantiation

..
 To model conditional instantiation, we can select the returned instance under
 parameter control. For example::

Para modelar instanciación condicional, podemos seleccionar la instancia
retornada bajo el control del parámetro. Por ejemplo::

   SLOW, MEDIUM, FAST = range(3)

   def top(..., speed=SLOW):
       ...
       def slowAndSmall():
          ...
       ...
       def fastAndLarge():
          ...
       if speed == SLOW:
           return slowAndSmall()
       elif speed == FAST:
           return fastAndLarge()
       else:
           raise NotImplementedError


.. _model-instarray:

Listas de instancias y señales
------------------------------

.. index:: single: lists of instances and signals

.. Python lists are easy to create. We can use them to model lists of instances.

En Python las listas son fáciles de crear. Podemos usarlas para modelar
listas de instancias.

.. Suppose we have a top module that instantiates a single ``channel`` submodule,
 as follows::

Suponga que tenemos un módulo superior que instancia un solo submódulo
``channel`` así:::

   def top(...):

       din = Signal(0)
       dout = Signal(0)
       clk = Signal(bool(0))
       reset = Signal(bool(0))

       channel_inst = channel(dout, din, clk, reset)

       return channel_inst 

.. If we wanted to support an arbitrary number of channels, we can use lists of
 signals and a list of instances, as follows::

Si deseamos permitir un número arbitrario de canales, podemos usar listas
de señales y una lista de instancias así::
 
 def top(..., n=8):

       din = [Signal(0) for i in range(n)]
       dout = [Signal(0) for in range(n)]
       clk = Signal(bool(0))
       reset = Signal(bool(0))
       channel_inst = [None for i in range(n)]

       for i in range(n):
           channel_inst[i] = channel(dout[i], din[i], clk, reset)

       return channel_inst

.. _model-shadow-signals:

Convirtiendo entre listas de señales y arreglos de bits
=======================================================

.. Compared to HDLs such as VHDL and Verilog, MyHDL signals are less
 flexible for structural modeling. For example, slicing a signal
 returns a slice of the current value. For behavioral code, this is
 just fine. However, it implies that you cannot use such as slice in
 structural descriptions. In other words, a signal slice cannot be used
 as a signal.

Comparado con otros lenguajes de descripción de hardware como Verilog y
VHDL, las señales MyHDL son menos flexibles para el modelado estructural.
Por ejemplo, cortando una señal retorna un corte del valor acutal. Para el
código comportamental, esto está bien. Sin embargo, implica que no puede
usar esto como corte en descripciones estructurales. En otras palabras, un
corte de una señal no se puede usar como señal.

..
 In MyHDL, you can address such cases by a concept called
 shadow signals. A shadow signal is constructed out of
 other signals and follows their value changes automatically.
 For example, a :class:`_SliceSignal` follows the value of
 an index or a slice from another signal.  Likewise, 
 A :class:`ConcatSignal` follows the
 values of a number of signals as a concatenation.

En MyHDL, Ud. puede manejar estos casos por un concepto llamado señales
ocultas. Una señal oculta es construida fuera de las otras señales y sigue
sus cambios automáticamente. Por ejemplo, una :class:`_SliceSignal` sigue
el valor de un índice o un corte de otra señal. Asimismo, una
:class:`ConcatSignal` sigue los valores de un número de señales como una
concatenación.

..
 As an example, suppose we have a system with N requesters that
 need arbitration. Each requester has a ``request`` output
 and a ``grant`` input. To connect them in the system, we can
 use list of signals. For example, a list of request signals
 can be constructed as follows::

Como ejemplo, suponga que tenemos un sistema con N registros  que necesitan
arbritrio. Cada registro tiene una salida ``solicitud`` y una entrada
``concesion``. Para conectarlos en el sistema, usamos una lista de señales.
Por ejemplo, una lista de señales de solicitud se puede construir así::

    request_list = [Signal(bool()) for i in range(M)]

.. Suppose that an arbiter module is available that is
 instantiated as follows::

Suponga que un módulo arbitrio está disponible esto instanciado así::

    arb = arbiter(grant_vector, request_vector, clock, reset)

..
 The ``request_vector`` input is a bit vector that can have
 any of its bits asserted. The ``grant_vector`` is an output
 bit vector with just a single bit asserted, or none.
 Such a module is typically based on bit vectors because
 they are easy to process in RTL code. In MyHDL, a bit vector
 is modeled using the :class:`intbv` type.

La entrada ``request_vector`` es un arreglo de bits que puede tener
cuaquiera de sus bits afirmados. ``grant_vector`` es arreglo de bits de salida con un solo bit afirmado, o ninguno. Como un modulo se basa típicamente en arreglos de bits porque ellos son fáciles de procesar en código RTL. En MyHDL, un arreglo de bits se modela usando el tipo :class:`intbv`.


..
 We need a way to "connect" the list of signals to the 
 bit vector and vice versa. Of course, we can do this with explicit
 code, but shadow signals can do this automatically. For
 example, we can construct a ``request_vector`` as a
 :class:`ConcatSignal` object::

Necesitamos una manera de "conectar" la lista de señales al arreglo de bits
y vice versa. Claro está, podemos hacer esto con un código explícito, pero
las señales ocultas pueden hacer esto automáticamente. Por ejemplo, podemos
construir un ``request_vector`` como un objeto :class:`ConcatSignal`::

    request_vector = ConcatSignal(*reversed(request_list)

..
 Note that we reverse the list first. This is done because the index range
 of lists is the inverse of the range of :class:`intbv` bit vectors.
 By reversing, the indices correspond to the same bit.

Observe que podemos invertir primero la lista. Esto se hace debido a que el
rango del índice de la lista es inverso al rango de los arreglos de bits de
:class:`intbv`. Invirtiendolos, los índices corresponden al mismo bit.

..
 The inverse problem exist for the ``grant_vector``. It would be defined as follows::
 
El problema contrario existe para ``grant_vector``. Se puede definir así::

    grant_vector = Signal(intbv(0)[M:])

..
 To construct a list of signals that are connected automatically to the
 bit vector, we can use the :class:`Signal` call interface to construct
 :class:`_SliceSignal` objects::

Para constuir una lista de señales que estén conectadas automáticamente al
arreglo de bits, podemos usar el llamado interface :class:`Signal` para
construir objetos :class:`_SliceSignal`::

    grant_list = [grant_vector(i) for i in range(M)]

..
 Note the round brackets used for this type of slicing. Also, it may not be
 necessary to construct this list explicitly. You can simply use
 ``grant_vector(i)`` in an instantiation.

Observe los paréntesis redondos para este tipo de corte. También, pude ser
innecesario construir esta lista explícitamente. Puede simplemente usar
``grant_vector(i)`` en una instanciación.

To decide when to use normal or shadow signals, consider the data
flow. Use normal signals to connect to *outputs*. Use shadow signals to
transform these signals so that they can be used as *inputs*.

Para decidir cuándo usar una señal normal u oculta, considere el flujo de
datos. Use señales normales para conectar a las *salidas*. Use señales
ocultas para transformar estas señales a ellas que sean usadas como
*entradas*

.. _model-infer-instlist:

Infiriendo listas de instancias
===============================

..
 In MyHDL, instances have to be returned explicitly by a top level function. It
 may be convenient to assemble  the list of instances automatically. For this
 purpose, MyHDL  provides the function :func:`instances`. Using the first example
 in this section, it is used as follows::

En MyHDL, las instancias tienen que ser retornadas explícitamente por una
función de nivel superior. Puede ser conveniente para construir la lista de
instancias automáticamente. Para este propósito MyHDL suministra la función
:func:`instances`. Usando el primer ejemplo en esta sección. Se usa así::

   from myhdl import instances

   def top(...):
       ...
       instance_1 = module_1(...)
       instance_2 = module_2(...)
       ...
       instance_n = module_n(...)
       ...
       return instances()

..
 Function :func:`instances` uses introspection to inspect the type of the local
 variables defined by the calling function. All variables that comply with the
 definition of an instance are assembled in a list, and that list is returned.

La función :func:`instances` usa la introspección para inspeccionar el tipo
de las variable locales definidas por la función que invoca. Todas las
variables cumplen con a definición de una instancia son construidas en una
lista, y esta lista es retornada

