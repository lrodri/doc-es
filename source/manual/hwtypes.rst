.. currentmodule:: myhdl

.. _hwtypes:

****************************
Tipos orientados al hardware
****************************

.. _hwtypes-intbv:

La clase  :class:`intbv`
========================

.. index:: single: intbv; basic usage

..
 Hardware design involves dealing with bits and bit-oriented operations. The
 standard Python type :class:`int` has most of the desired features, but lacks
 support for indexing and slicing. For this reason, MyHDL provides the
 :class:`intbv` class. The name was chosen to suggest an integer with bit vector
 flavor.

El diseño de hardware involucra tratar con bits y operaciones orientadas a
bit. El tipo estándar de Python :class:`int` tiene la mayoría de las
características necesarias, pero adolece de indexado y corte. Por esta
razón MyHDL suministra la clase :class:`intbv`. El nombre se escogió para
sugerir un entero con un sabor a un vector de bits.


..
 :class:`intbv` works transparently with other integer-like types. Like
 class :class:`int`, it provides access to the underlying two's complement
 representation for bitwise operations. However, unlike :class:`int`, it is
 a mutable type. This means that its value can be changed after object
 creation, through methods and operators such as slice assignment.

La clase :class:`intbv` trabaja de forma transparente con otros tipos de datos
enteros. como la clase :class:`int`, suministra la representación de
complemento a dos subyacente para operaciones entre bits. Sin embargo, a
diferencia de :class:`int`, es un tipo mutable. Esto significa que su valor se
puede cambiar luego de la creación del objeto, a través de métodos y
operadores tales como una asignación cortada.

..
 :class:`intbv` supports the same operators as :class:`int` for arithmetic.
 In addition, it provides a number of features to make it suitable for
 hardware design. First, the range of allowed values can be constrained.
 This makes it possible to check the value at run time during simulation.
 Moreover, back end tools can determine the smallest possible bit width for
 representing the object.  Secondly, it supports bit level operations by
 providing an indexing and slicing interface.

La clase :class:`intvb` apoya los mismos operadores que la clase :class:`int`
para la artimética. Además, suministra una serie de características para
hacerla adecuada para el diseño de hardware. Primero, el rango de valores
permitidos se pueden restringir. Esto hace posible examinar el valor en tiempo
de ejecución durante la simulación. Sin embargo herramientas del motor pueden
determinar el ancho de bits más pequeño posible para la representación del
objeto.
Segundo, permite operaciones a nivel de bit suministrando una interfaz de
indexado y corte.

.. back end: motor --> wikipedia
.. front end: interfaz

.. :class:`intbv` objects are constructed in general as follows::

En general los objetos :class:`intbv` son construidos así::

    intbv([val=None] [, min=None]  [, max=None])

    
..
 *val* is the initial value. *min* and *max* can be used to constrain
 the value. Following the Python conventions, *min* is inclusive, and
 *max* is exclusive. Therefore, the allowed value range is *min* .. *max*-1.

*val* es el valor inicial. *min* y *max* se pueden usar para limitar el valor.
Siguiendo las convensiones de Python, *min* es incluyente y *max* es excluyente.
Por lo tanto los valores admitidos en el rango es *min* .. *max* -1.


..
 Let's us look at some examples. First, an unconstrained :class:`intbv`
 object is created as follows:

Veamos algunos ejemplos. Primero, para una clase :class:`intbv` sin
restricciones, el objeto es creado así::
 
  >>> a = intbv(24)
  
.. index::  
    single: intbv; min
    single: intbv; max
    single: intbv; bit width

..
 After object creation, *min* and *max* are available as attributes for
 inspection. Also, the standard Python function :func:`len` can be used
 to determine the bit width. If we inspect the previously created
 object, we get::

Luego de la creación del objeto, *min* y *max* están disponibles como
atributos para su inspección. También, se  puede utilizar la función estándar
de Python :func:`len`  para determinar el ancho de los bits. Si
inspeccionamos el objeto anteriormente creado obtendremos::


  >>> print a.min
  None
  >>> print a.max
  None
  >>> print len(a)
  0

..
 As the instantiation was unconstrained, the *min* and *max* attributes
 are undefined. Likewise, the bit width is undefined, which is indicated
 by a return value ``0``.

Como la instanciación fue sin restricciones, los atributos *min* y *max*
están sin definir. Igualmente, el ancho de los bits está indefinido, lo que se
indica mediante un valor de retorno de ``0``

.. A constrained :class:`intbv` object is created as follows:

Un objeto restringido de  :class:`intbv` se crea así::

  >>> a = intbv(24, min=0, max=25)


.. Inspecting the object now gives::

Inspeccionando el objeto ahora da::

  >>> a.min
  0
  >>> a.max
  25
  >>> len(a)
  5

..
 We see that the allowed value range is 0 .. 24,  and that 5 bits are
 required to represent the object.

Vemos que el rango de valores permitidos es 0 .. 24 y que se necesitan 5
bits para poder representar el objeto.

..
 Sometimes hardware engineers prefer to constrain an object by defining its
 bit width directly, instead of the range of allowed values.  The following
 example shows how to do that::

Algunas veces los ingenieros de hardware prefieren restringir un objeto
definiendo los bits directamente, en lugar del rango de valores permitidos.
El siguiente ejemplo muestra cómo hacer esto::

  >>> a = intbv(24)[5:]

..
 What actually happens here is that first an unconstrained :class:`intbv`
 is created, which is then sliced. Slicing an :class:`intbv` returns a new
 :class:`intbv` with the constraints set up appropriately.  Inspecting the
 object now shows::

Lo que sucede acá es que primero se crea una clase sin restricciones
:class:`intbv`, y luego se corta. Al cortar una clase :class:`intbv`
retorna una nueva clase :class:`intbv` con la restricción fijada
apropiadamente.  Inspeccionando el objeto muestra::

  >>> a.min
  0
  >>> a.max
  32
  >>> len(a)
  5


..
 Note that the *max* attribute is 32, as with 5 bits it is possible to represent
 the range 0 .. 31.  Creating an :class:`intbv` this way has the disadvantage
 that only positive value ranges can be specified. Slicing is described in more
 detail in :ref:`hwtypes-slicing`.

Observe que el atributo *max* es 32, ya que con 5 bits es posible representar
el rango de 0 .. 31. Creando un :class:`intbv` de esta forma tiene la desventaja
que sólo es  posible definir  rangos positivos. El corte es descrito en más detalle
en :ref:`hwtypes-slicing`.


..
 To summarize, there are two ways to constrain an :class:`intbv` object: by
 defining its bit width, or by defining its value range. The bit width
 method is more traditional in hardware design. However, there are two
 reasons to use the range method instead: to represent negative values as
 observed above, and for fine-grained control over the value range.


Para resumir, hay dos maneras de restringir un objeto :class:`intbv`,
definiendo su ancho en bits o definiendo el valor del rango. El ancho de bits
es el método más tradicional en del diseño de hardware. Sin embargo hay dos
razones para usar el método del rango: representar valores negativos como se
observó antes, y para un control más detallado sobre el rango de valores.

..
 Fine-grained control over the value range permits better error checking,
 as there is no need for the *min* and *max* bounds to be symmetric or
 powers of 2. In all cases, the bit width is set appropriately to represent
 all values in the range. For example::


El control detallado sobre el rango de valores permite un mejor control de
errores, debido a que no necesita que los límites  *min* y  *max* sean
potencias de dos o sean simétricos.  De todas formas, el ancho de bits se
fija apropiadamente para representar todos los los valores en el rango. Por
ejemplo:: 

    >>> a = intbv(6, min=0, max=7)
    >>> len(a)
    3
    >>> a = intbv(6, min=-3, max=7)
    >>> len(a)
    4
    >>> a = intbv(6, min=-13, max=7)
    >>> len(a)
    5


.. _hwtypes-indexing:

Índices de bits
===============

.. index:: single: bit indexing

..
 As an example, we will consider the design of a Gray encoder. The following code
 is a Gray encoder modeled in MyHDL::


Como ejemplo, consideraremos el diseño de un codificador Gay. El siguiente
código es un codificador Gray en MyHDL::

   from myhdl import Signal, delay, Simulation, always_comb, instance, intbv, bin

   def bin2gray(B, G, width):
       """ Codificador Gray.

       B -- Señal de entrada intbv, codificada en binario natural
       G -- Señal de salida intbv, codificada en Gray
       width -- ancho de bits
       """

       @always_comb
       def logic():
           for i in range(width):
               G.next[i] = B[i+1] ^ B[i]

       return logic

..
 This code introduces a few new concepts. The string in triple quotes at
 the start of the function is a :dfn:`doc string`. This is standard Python
 practice for structured documentation of code.

Este código introduce unos pocos conceptos. La cadena en comillas triples
en el inicio de la función es un :dfn:`doc string`. Esta es una práctica
normal en Python para la documentación estructurada del código.


.. index::
   single: decorator; always_comb
   single: wait; for a signal value change
   single: combinatorial logic

..
 Furthermore, we introduce a third decorator: :func:`always_comb`.  It is
 used with a classic function and specifies that the  resulting generator
 should wait for a value change on any input signal. This is typically used
 to describe combinatorial logic. The :func:`always_comb` decorator
 automatically infers which signals are used as inputs.

Además, introdujimos un tercer decorador: :func:`always_comb`. Esto es usado
con una función clásica y especifica que el generador resultante debería
esperar el cambio de un valor ante cualquier señal de entrada. Esto es
típicamente usado para describir lógica combinacional. El decorador
:func:`always_comb` automáticamente infiere qué señales son usadas como
entrada.


..
 Finally, the code contains bit indexing operations and an exclusive-or
 operator as required for a Gray encoder. By convention, the lsb of an
 :class:`intbv` object has index ``0``.

Finalmente, el código contiene una operación con índices de bits y un
operador or-exclusivo como el que se necesta para un codificador Gray. Por
convención, el bit menos significativo en un objeto :class:`intbv` tiene un
índice ``0``.


..
 To verify the Gray encoder, we write a test bench that prints input and
 output for all possible input values::

Para verificar el codificador Gay, hemos escrito un banco de pruebas que
imprime la entrada y la salida de todos los posibles valores de entrada::

   def testBench(width):

       B = Signal(intbv(0))
       G = Signal(intbv(0))

       dut = bin2gray(B, G, width)

       @instance
       def stimulus():
           for i in range(2**width):
               B.next = intbv(i)
               yield delay(10)
               print "B: " + bin(B, width) + "| G: " + bin(G, width)

       return dut, stimulus

..
 We use the conversion function :func:`bin` to get a binary string
 representation of the signal values. This function is exported by the
 :mod:`myhdl` package and supplements the standard Python :func:`hex` and
 :func:`oct` conversion functions.

Usamos la función de conversión :func:`bin` para obtener una representación
binaria de los valores de la señal. Esta función es exportada por el
paquete :mod:`myhdl` y complementa las funciones de conversión estándar de
Python :func:`hex` y :func:`oct`.


.. As a demonstration, we set up a simulation for a small width::

Como una demostración, haremos una simulación para un ancho pequeño::

   sim = Simulation(testBench(width=3))
   sim.run()

.. The simulation produces the following output::

La simulación produce la siguiente salida::

   % python bin2gray.py
   B: 000 | G: 000
   B: 001 | G: 001
   B: 010 | G: 011
   B: 011 | G: 010
   B: 100 | G: 110
   B: 101 | G: 111
   B: 110 | G: 101
   B: 111 | G: 100
   StopSimulation: No more events


.. _hwtypes-slicing:

Cortar bits
============

.. index:: 
   single: bit slicing
   single: concat(); example usage

..
 For a change, we will use a traditional function as an example to illustrate
 slicing.  The following function calculates the HEC byte of an ATM header. ::


Por variar, usaremos una función tradicional como ejemplo para ilustrar
el corte.  La siguiente función calcula el valor HEC de una encabezado ATM.::

   from myhdl import intbv, concat

   COSET = 0x55

   def calculateHec(header):
       """ Retorna el HEC (Header Error Control/Check) de un encabezado
       ATM, prepresentado como un intbv

       El polinomio HEC es 1 + x + x**2 + x**8.
       """
       hec = intbv(0)
       for bit in header[32:]:
           hec[8:] = concat(hec[7:2],
                            bit ^ hec[1] ^ hec[7],
                            bit ^ hec[0] ^ hec[7],
                            bit ^ hec[7]
                           )
       return hec ^ COSET

..
 The code shows how slicing access and assignment is supported on the
 :class:`intbv` data type. In accordance with the most common hardware
 convention, and unlike standard Python, slicing ranges are downward. The code
 also demonstrates concatenation of :class:`intbv` objects.


El código muestra cómo se accede al corte y cómo se asigna el corte, lo que
es permitido por el tipo de dato :class:`intbv`. De acuerdo con la
convención más común de hardware, y a diferencia de la norma en Python, los
rangos de corte son descendentes. El código también demuestra la
concatenación de objetos :class:`intbv`.


..
 As in standard Python, the slicing range is half-open: the highest index
 bit is not included. Unlike standard Python however, this index
 corresponds to the *leftmost* item. Both indices can be omitted from the
 slice. If the leftmost index is omitted, the meaning is to access "all"
 higher order bits.  If the rightmost index is omitted, it is ``0`` by
 default.

Como en Python estándar, el rango de corte es medio-abierto: no se incluye
el índice mayor. A diferencia de Python estándar, este índice corresponde
al ítem del *extremo izquierdo*. Ambos índices se pueden omitir del corte.
Si el índice del extremo izquierdo se omite, el significado es acceder a
"todos" los bits de orden superior. Si el bit del extremo derecho se omite,
éste es ``0`` por omisión.

..
 The half-openness of a slice may seem awkward at first, but it helps to
 avoid one-off count issues in practice. For example, the slice ``hex[8:]``
 has exactly ``8`` bits. Likewise, the slice ``hex[7:2]`` has ``7-2=5``
 bits. You can think about it as follows: for a slice ``[i:j]``, only bits
 below index ``i`` are included, and the bit with index ``j`` is the last
 bit included.


La apertura media de un corte puede parecer ilógica en primera instancia,
pero ayuda a *one-off count issues in practice*. Por ejemplo, el corte
``hex[8:]`` tiene exactamente ``8`` bits. Igualmente el corte ``hex[7:2]``
tiene  ``7-2=5`` bits.  Puede pensar así: para un corte ``[i:j]``, sólo los
bits abajo del índice ``i`` son incluidos y el bit con índice ``j`` es el
último bit incluido. 

..
 When an :class:`intbv` object is sliced, a new :class:`intbv` object is
 returned.  This new :class:`intbv` object is always positive, and the
 value bounds are set up in accordance with the bit width specified by the
 slice. For example::

Cuando se corta un objeto :class:`intbv`, se retorna un nuevo objeto
:class:`intbv`. Este nuevo :class:`intbv` es siempre positivo, y los
límites se fijan de acuerdo con el ancho de bits especificado por el corte.
Por ejemplo::

  >>> a = intbv(6, min=-3, max=7)
    >>> len(a)
    4
    >>> b = a[4:]
    >>> b     
    intbv(6L)
    >>> len(b)
    4
    >>> b.min
    0
    >>> b.max
    16

..
 In the example, the original object is sliced with a slice equal to its
 bit width.  The returned object has the same value and bit width, but its
 value range consists of all positive values that can be represented by the
 bit width.

En el ejemplo, el objeto original es cortado con un corte igual a su ancho
de bits. El objeto retornado tiene el mismo valor y ancho de bits, pero su
rango de valores es positivo con el rango que se puede representar por el
ancho de bits.

..
 The object returned by a slice is positive, even when the original object
 is negative::

El objeto retornado por un corte es positivo, aún cuando el objeto original
sea negativo::

    >>> a = intbv(-3)
    >>> bin(a, width=5)
    '11101'
    >>> b = a[5:]
    >>> b
    intbv(29L)
    >>> bin(b)
    '11101'

..
 The bit pattern of the two objects is identical within the bit width,
 but their values have opposite sign.

El patrón de bits de los dos objetos tienen igual número  de bits, pero sus
valores son de signo opuesto.

.. _hwtypes-modbv:

The :class:`modbv` class
========================

..
 In hardware modeling, there is often a need for the elegant modeling of
 wrap-around behavior. :class:`intbv` instances do not support this
 automatically, as they assert that any assigned value is within the bound
 constraints. However, wrap-around modeling can be straightforward.  For
 example, the wrap-around condition for a counter is often decoded
 explicitly, as it is needed for other purposes. Also, the modulo operator
 provides an elegant one-liner in many scenarios::

En el modelamiento de hardware, existe a menudo la necesidad del
modelamiento elegante de comportamiento envolvente. La instancias de
:class:`intbv` no permiten esto automáticamente, debido a que ellas afirman
que cualquier valor asignado están dentro de los límites de su restricción.
Sin embargo el modelado envolvente puede ser directo. Por ejemplo, la
condición envolvente para un contador es a menudo decodificada
explícitamente, debido a que es necesario para otros propósitos. También,
el operador módulo suministra una línea elegante en muchos aspectos::
 
 count.next = (count + 1) % 2**8

..
 However, some interesting cases are not supported by the :class:`intbv` type.
 For example, we would like to describe a free running counter using a variable
 and augmented assignment as follows::

Sin embargo, algunos casos interesantes no están permitidos por
el tipo :class:`intbv`. Por ejemplo, podríamos describir un contador usando
una variable e incrementar su valor así::

    count_var += 1

..
 This is not possible with the :class:`intbv` type, as we cannot add the modulo
 behavior to this description. A similar problem exist for an augmented left
 shift as follows::

Esto no es posible con el tipo :class:`intbv`, ya que no podemos añadir el
comportamiento del módulo a esta descripción. Un problema similar existe
para desplazamiento a la derecha aumentado así::

    shifter <<= 4

..
 To support these operations directly, MyHDL provides the :class:`modbv`
 type. :class:`modbv` is implemented as a subclass of  :class:`intbv`.
 The two classes have an identical interface and work together
 in a straightforward way for arithmetic operations.
 The only difference is how the bounds are handled: out-of-bound values
 result in an error with :class:`intbv`, and in wrap-around with
 :class:`modbv`. For example, the modulo counter as above can be
 modeled as follows::

Para permitir estas operaciones directamente, MyHDL suministra el tipo
:class:`modbv`. :class:`modbv` está implementada como una subclase de
:class:`intbv`. Las dos clases tienen interfaces idénticas y trabajan
juntas, de forma directa para operaciones aritméticas.
La única diferencia es cómo se manipulan los límites: los límites fuera de
producen error en la clase :class:`intbv`, y en envolvente con la clase
:class:`modbv`. Por ejemplo, el cóntador de módulo anterior  se puede
modelar así::

    count = Signal(modbv(0, min=0, max=2**8))
    ...
    count.next = count + 1

.. The wrap-around behavior is defined in general as follows::

El comportamiento envolvente está defnido en general así::

    val = (val - min) % (max - min) + min

.. In a typical case when ``min==0``, this reduces to::

En un caso tipico cuado ``min=0``, esto se reduce a::

    val = val % max

.. _hwtypes-signed:

Representación con y sin signo
==============================

.. index:: 
    single: intbv; intbv.signed

..
 :class:`intbv` is designed to be as high level as possible. The underlying
 value of an :class:`intbv` object is a Python :class:`int`, which is
 represented as a two's complement number with "indefinite" bit
 width. The range bounds are only used for error checking, and to
 calculate the minimum required bit width for representation. As a
 result, arithmetic can be performed like with normal integers.


:class:`intbv` está diseñado para ser del más alto nivel posible. El valor
subyacente de un objeto :class:`intbv` es en Python :class:`int`, que es
representado como un número en complemento a dos con un ancho de bit
"indefinido". Los límites se usan sólo para la detección de errores, y para
calcular el mínimo ancho de bit para su representación. Como resultado, la
artimética se puede hacer como con enteros normales.


..
 In contrast, HDLs such as Verilog and VHDL typically require designers
 to deal with representational issues, especially for synthesizable code.
 They provide low-level types like ``signed`` and ``unsigned`` for
 arithmetic. The rules for arithmetic with such types are much more
 complicated than with plain integers.

A diferencia de otros lenguajes de descripción de hardware como Verilog y
VHDL que necesitan que el diseñador trate con cuestieones de
representación, especialmente para el código sintetizable. Ellos
suministran tipos de bajo nivel como ``signed`` y ``unisgned`` para la
artimética. Las reglas para la aritmética con estos tipos son mucho más
complicadas que las de los enteros planos.

..
 In some cases it can be useful to interpret :class:`intbv` objects
 in terms of "signed" and "unsigned". Basically, it depends on attribute *min*.
 if *min* < 0, then the object is "signed", otherwise it is "unsigned".
 In particular, the bit width of a "signed" object will account for
 a sign bit, but that of an "unsigned" will not, because that would
 be redundant. From earlier sections, we have learned that the
 return value from a slicing operation is always "unsigned".


En algunos casos puede ser útil interpretar objetos :class:`intbv` en
términos de "son signo" y "sin signo". Básicamente, depende de los
atributos *min* si *min* < 0, entonces el objeto es "con signo", de otra
forma es un objeto "sin signo". En particular, el ancho de bit de un objeto
"con signo" se tendrá en cuenta el bit de signo, pero para uno "sin signo"
no lo hará, porque sería redundante. De las secciones anteriores, hemos
aprendido que el valor de retorno de una operación de corte es siempre "con
signo".



..
 In some applications, it is desirable to convert an "unsigned"
 :class:`intbv` to  a "signed", in other words, to interpret the msb bit
 as a sign bit.  The msb bit is the highest order bit within the object's
 bit width.  For this purpose, :class:`intbv` provides the
 :meth:`intbv.signed` method. For example::


En algunas aplicaciones, es deseable convertir un :class:`intbv` "sin
signo" a uno "con signo", en otras palabras, interpretar el bit más
significativo como el bit de signo. Para este propósito :class:`intbv`
suministra el método :meth:`intbv.signed`. Por ejemplo::

    >>> a = intbv(12, min=0, max=16)
    >>> bin(a)
    '1100'
    >>> b = a.signed()
    >>> b
    -4
    >>> bin(b, width=4)
    '1100'

..
 :meth:`intbv.signed` extends the msb bit into the higher-order bits of the 
 underlying object value, and returns the result as an integer.
 Naturally, for a "signed" the return value will always be identical
 to the original value, as it has the sign bit already.

:meth:`intbv.signed` exitiende el bit de mayor peso en los bits de mayor
orden del valor del objeto subyacente, y retorna el resultado como un
entero. Naturalmente, para un entero "con signo" el valor de retorno será
siempre idéntico al valor original, ya que el bit de signo está incluido.


..
 As an example let's take a 8 bit wide data bus that would be modeled as
 follows::


Como un ejemplo, tomemos un bus de 8 bits de ancho que se podría modelar
así::

  data_bus = intbv(0)[8:]

..
 Now consider that a complex number is transferred over this data
 bus. The upper 4 bits of the data bus are used for the real value and
 the lower 4 bits for the imaginary value. As real and imaginary values
 have a positive and negative value range, we can slice them off from
 the data bus and convert them as follows::

Ahora consideremosque un número complejo se transfiere sobre este bus de
datos. Los 4 bits superiores del bus de datos se usan para el valor real y
los cuatro bits inferiores la parte imaginaria . Debido a que las partes
real e imaginaria tienen valores positivos y negativos, los podemos cortar
del bus de datos y convertirlos así::

 real.next = data_bus[8:4].signed()
 imag.next = data_bus[4:].signed()


