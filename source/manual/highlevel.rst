.. currentmodule:: myhdl

.. _model-hl:

**************************
Modelamiento de alto nivel
**************************

Introducción
=============

.. index:: single: modeling; high level

..
 To write synthesizable models in MyHDL, you should stick to
 the RTL templates shown in :ref:`model-rtl`. However,
 modeling in MyHDL is much more powerful than that.
 Conceptually, MyHDL is a library for general event-driven
 modeling and simulation of hardware systems.

Escribir modelos sintetizables en  MyHDL debería parecerse a las plantillas
mostradas en :ref:`model-rtl`. Sin embargo, el modelado con MyHDL es mucho más
poderoso que esto.  Conceptualmente, MyHDL es una biblioteca para modelado
general manipulado por eventos y simulación de sistemas de hardware.

..
 There are many reasons why it can be useful to model at a
 higher abstraction level than RTL. For example, you can
 use MyHDL to verify architectural features, such as system
 throughput, latency and buffer sizes. You can also write
 high level models for specialized technology-dependent cores
 that are not going through synthesis. Last but not least,
 you can use MyHDL to write test benches that verify a system
 model or a synthesizable description.

Hay muchas razones por las cuales puede ser útil modelar en un mayor nivel
de abstracción que RTL. Por ejemplo, puede usar MyHDL para verificar
caracterísiticas estructurales, como el desempeño del sistema, latencia y
tamaño de los búferes. También puede escribir modelos de alto nivel para
núcleos especializados dependientes de determinada tecnología que no son
suceptibles de sintetizarse. Por último pero no menos importante, puede
usar MyHDL para escribir bancos de pruebas que verifiquen un modelo de un
sistema o una descripción sintetizable.

..
 This chapter explores some of the options for high level
 modeling with MyHDL.

Este capítulo explora algunas de las opciones del modelamiento de alto nivel
con MyHDL.

.. _model-bfm:

.. Modeling with bus-functional procedures

Modelando con procedimientos funcionales
=========================================

.. index:: single: bus-functional procedure

..
 A :dfn:`bus-functional procedure` is a reusable encapsulation of the low-level
 operations needed to implement some abstract transaction on a physical
 interface. Bus-functional procedures are typically used in flexible verification
 environments.

Un :dfn:`bus-functional procedure` es una encapsulación reutilizable de las
operaciones de bajo nivel necesarias para implementar algunas transacciones
abstractas en una interfaz física. Los procedimientos bus-functional son
usados típicamente en ambientes de verificación flexible

.. % 

..
 Once again, MyHDL uses generator functions to support bus-functional
 procedures.  In MyHDL, the difference between instances and bus-functional
 procedure calls comes from the way in which a generator function is used.

Una vez más, MyHDL usa funciones generadores para permitir procedimientos
bus-functional.  En MyHDL, la diferencia entre instancias e invocaciones
procedimientos bus-functional viene de la manera en que se utiliza una
función generadora.

..
 As an example, we will design a bus-functional procedure of a simplified
 UART transmitter. We assume 8 data bits, no parity bit, and a single stop
 bit, and we add print statements to follow the simulation behavior::

Como ejemplo, diseñaremos un procedimiento bus-functional de un transmisor
UART simplificado. Asumimos datos de 8 bits, sin bit de paridad y un sólo
bit de parada y añadimos instrucciones de impresión para seguir el
comportamiento de la simulación::

   T_9600 = int(1e9 / 9600)

   def rs232_tx(tx, data, duration=T_9600):

       """ Procedimiento elemental de un transmisor rs232.

       tx -- dato de salida serial
       data -- dato de entrada. Byte a ser transmitido
       duration -- duración del bit transmitido

       """

       print "-- Transmitiendo %s --" % hex(data)
       print "TX: bit de inicio"      
       tx.next = 0
       yield delay(duration)

       for i in range(8):
           print "TX: %s" % data[i]
           tx.next = data[i]
           yield delay(duration)

       print "TX: bit de parada"      
       tx.next = 1
       yield delay(duration)

..
 This looks exactly like the generator functions in previous sections. It
 becomes a bus-functional procedure when we use it differently. Suppose
 that in a test bench, we want to generate a number of data bytes to be
 transmitted. This can be modeled as follows::


Esto se ve exactamente como las funciones generadoras de las secciones
anteriores. Se convierte en un procedimiento bus-functional cuando la
usamos de forma diferente. Suponga que en un banco de pruebas, deseamos
generar un número de bytes de datos a ser transmitidos. Esto se puede
modelar así::

   testvals = (0xc5, 0x3a, 0x4b)

   def stimulus():
       tx = Signal(1)
       for val in testvals:
           txData = intbv(val)
           yield rs232_tx(tx, txData)

.. index:: single: wait; for the completion of a generator

..
 We use the bus-functional procedure call as a clause in a ``yield``
 statement.  This introduces a fourth form of the ``yield`` statement:
 using a generator as a clause. Although this is a more dynamic usage than
 in the previous cases, the meaning is actually very similar: at that
 point, the original generator should wait for the completion of a
 generator.  In this case, the original generator resumes when the
 ``rs232_tx(tx, txData)`` generator returns.


Usamos este llamado al procedimiento bus-functional como una sentencia en
una instrucción ``yield``. Esto introduce una cuarta forma de la
instrucción ``yield``: usando un generador como sentencia. Sin embargo este
es un uso más dinámico que en los casos anteriores, el significado es
actualmente muy similar: en este punto, el generador original debería
esperar para la finalización del generador. En este caso, el generador
original reinicia cuando el generador retorna ``rs232_tx(tx, txData)``.

.. % 

.. When simulating this, we get::

Cuando se simula esto, obtenemos::

   -- Transmitting 0xc5 --
   TX: start bit
   TX: 1
   TX: 0
   TX: 1
   TX: 0
   TX: 0
   TX: 0
   TX: 1
   TX: 1
   TX: stop bit
   -- Transmitting 0x3a --
   TX: start bit
   TX: 0
   TX: 1
   TX: 0
   TX: 1
   ...

..
 We will continue with this example by designing the corresponding UART
 receiver bus-functional procedure. This will allow us to introduce further
 capabilities of MyHDL and its use of the ``yield`` statement.


Continuaremos con este ejemplo diseñando el correspondiente
procedimiento bus-functional del receptor UART. Esto nos permitirá
introducir nuevas capacidades de MyHDL y el uso de la instrucción
``yield``.

.. index:: single: sensitivity list

..
 Until now, the ``yield`` statements had a single clause. However, they can
 have multiple clauses as well. In that case, the generator resumes as soon
 as the wait condition specified by one of the clauses is satisfied. This
 corresponds to the functionality of sensitivity lists in Verilog and VHDL.

Hasta ahora las instruccines ``yield`` tienen una sola instrucción, ellas
pueden tener multiples instrucciones también. En este caso, el generador
continúa, tan pronto como la condición de espera especificada por una de
las instrucciones se satisfaga. Esto corresponde a la funcionalidad de las
listas sensitivas en Verilog y VHDL.

.. % 

..
 For example, suppose we want to design an UART receive procedure with a
 timeout.  We can specify the timeout condition while waiting for the start
 bit, as in the following generator function::

Por ejemplo, suponga que desea diseñar un procedimiento para receptor UART
con un tiempo de espera.  Podemos especificar la condición de tiempo de
espera mientras esperamos el bit de inicio, como se indica en la siguiente
función generadora::

   def rs232_rx(rx, data, duration=T_9600, timeout=MAX_TIMEOUT):

       """ Procedimiento elemental de un receptor rs232.

       rx -- dato serial de entrada
       data -- dato recibido
       duration -- duración del bit recibido

       """

       # se espera el bit de inicio hasta que acabe el tiempo de espera
       yield rx.negedge, delay(timeout)
       if rx == 1:
           raise StopSimulation, "RX error de tiempo de espera"

       # muestra en la mitad de la duración del bit
       yield delay(duration // 2)
       print "RX: bit de inicio"

       for i in range(8):
           yield delay(duration)
           print "RX: %s" % rx
           data[i] = rx

       yield delay(duration)
       print "RX: stop bit"
       print "-- se recibio %s --" % hex(data)

..
 If the timeout condition is triggered, the receive bit ``rx`` will still
 be ``1``. In that case, we raise an exception to stop the simulation. The
 ``StopSimulation`` exception is predefined in MyHDL for such purposes. In
 the other case, we proceed by positioning the sample point in the middle
 of the bit duration, and sampling the received data bits.

Si la condición de tiempo de espera se dispara, el bit de recepción ``rx``
continuará en ``1``. En este caso, elevaremos una excepción para detener la
simulación. La excepción ``StopSimulation`` está predefinida en MyHDL para
estos proóstos. En otro caso, procedemos colocando el punto de muestra en
la mitad de la duración del bit, y muestreando los bits de datos recibidos.

..
 When a ``yield`` statement has multiple clauses, they can be of any type
 that is supported as a single clause, including generators. For example,
 we can verify the transmitter and receiver generator against each other by
 yielding them together, as follows::

Cuando una instrucción ``yield`` tiene múltiples instrucciones, ellas
pueden ser de cualquier tipo que soporte una sola intrucción, incluidos los
generadores. Por ejemplo, podemos verificar el generador del transmsor y
del receptor uno contra otro usando instrucciones ``yield`` así::

   def test():
       tx = Signal(1)
       rx = tx
       rxData = intbv(0)
       for val in testvals:
           txData = intbv(val)
           yield rs232_rx(rx, rxData), rs232_tx(tx, txData)

..
 Both forked generators will run concurrently, and the original generator will
 resume as soon as one of them finishes (which will be the transmitter in this
 case).  The simulation output shows how the UART procedures run in lockstep::

Los dos generadores se ejecutarán concurrentemente, y el generador original
continuará hasta que uno de ellos finalice (que será el transmisor en este
caso). La salida de la simulación muestrá cómo se ejecutan los
procedimientos UART en un seguimiento paso a paso::

 -- Transmitting 0xc5 --
   TX: start bit
   RX: start bit
   TX: 1
   RX: 1
   TX: 0
   RX: 0
   TX: 1
   RX: 1
   TX: 0
   RX: 0
   TX: 0
   RX: 0
   TX: 0
   RX: 0
   TX: 1
   RX: 1
   TX: 1
   RX: 1
   TX: stop bit
   RX: stop bit
   -- Received 0xc5 --
   -- Transmitting 0x3a --
   TX: start bit
   RX: start bit
   TX: 0
   RX: 0
   ...

..
 For completeness, we will verify the timeout behavior with a test bench that
 disconnects the ``rx`` from the ``tx`` signal, and we specify a small timeout
 for the receive procedure::

Siendo exhaustivos, verificaremos el comportamiento de tiempo de espera con
un banco de pruebas que desconecte la señal  ``rx`` de la señal ``tx``, y
especificaremos un pequeño tiempo de espera para el procedimiento
receptor::

   def testTimeout():
       tx = Signal(1)
       rx = Signal(1)
       rxData = intbv(0)
       for val in testvals:
           txData = intbv(val)
           yield rs232_rx(rx, rxData, timeout=4*T_9600-1), rs232_tx(tx, txData)

.. The simulation now stops with a timeout exception after a few transmit cycles::

La simulación ahora se detene con una execpción de tiempo de espera luego
de unos pocos ciclos de transmisión::

   -- Transmitting 0xc5 --
   TX: start bit
   TX: 1
   TX: 0
   TX: 1
   StopSimulation: RX time out error

..
 Recall that the original generator resumes as soon as one of the forked
 generators returns. In the previous cases, this is just fine, as the
 transmitter and receiver generators run in lockstep. However, it may be
 desirable to resume the caller only when *all* of the forked generators
 have finished. For example, suppose that we want to characterize the
 robustness of the transmitter and receiver design to bit duration
 differences. We can adapt our test bench as follows, to run the
 transmitter at a faster rate::

Recuerde que el generador original se reinicia tan pronto como uno de los
generadores se bifurca retorna. En los casos anteriors, esto está bien, ya
que el transmisor y el receptor se ejecutan acompasados. Sin embargo, puede
ser deseable reiniciar el llamador sólo cuando *todos* los generadores
bifurcados han finalizado. Por ejemplo, suponga que deseamos caracterizar
la fortaleza del transmisor y del receptor diseñandolo para duraciones de
bit diferentes. Podemos adaptar nuestro banco de pruebas así: para ejecutar
el transmisor a una velocidad mayor::

  T_10200 = int(1e9 / 10200)

   def testNoJoin():
       tx = Signal(1)
       rx = tx
       rxData = intbv(0)
       for val in testvals:
           txData = intbv(val)
           yield rs232_rx(rx, rxData), rs232_tx(tx, txData, duration=T_10200)

..
 Simulating this shows how the transmission of the new byte starts before the
 previous one is received, potentially creating additional transmission errors::

Simulando esto muestra cómo la transmisión de un nuevo byte inicia antes
que el anterior se halla recibido, potencialmente creando errores
adicionales de transmisión::

   -- Transmitting 0xc5 --
   TX: start bit
   RX: start bit
   ...
   TX: 1
   RX: 1
   TX: 1
   TX: stop bit
   RX: 1
   -- Transmitting 0x3a --
   TX: start bit
   RX: stop bit
   -- Received 0xc5 --
   RX: start bit
   TX: 0

..
 It is more likely that we want to characterize the design on a byte by byte
 basis, and align the two generators before transmitting each byte. In MyHDL,
 this is done with the :func:`join` function. By joining clauses together in a
 ``yield`` statement, we create a new clause that triggers only when all of its
 clause arguments have triggered. For example, we can adapt the test bench as
 follows::

Es más probable que deseemos caracterízar el diseño byte por byte, y
alienar dos generadores antes de transimitir cada byte. En MyHDL, esto se
logra con la :func:`join`. Uniendo clausulas juntas en una instrucción
``yield``, creamos una nueva clausula que se dispara sólo cuando todos los
argumentos de la cláusula se han disparados. Por ejemplo, podemos adaptar
el banco de pruebas así::

   def testJoin():
       tx = Signal(1)
       rx = tx
       rxData = intbv(0)
       for val in testvals:
           txData = intbv(val)
           yield join(rs232_rx(rx, rxData), rs232_tx(tx, txData, duration=T_10200))

.. Now, transmission of a new byte only starts when the previous one is received::

Ahora, la transmisión de un nuevo byte sólo inicia cuando el anterior se ha
recibido::

   -- Transmitting 0xc5 --
   TX: start bit
   RX: start bit
   ...
   TX: 1
   RX: 1
   TX: 1
   TX: stop bit
   RX: 1
   RX: stop bit
   -- Received 0xc5 --
   -- Transmitting 0x3a --
   TX: start bit
   RX: start bit
   TX: 0
   RX: 0


.. _model-mem:

.. Modeling memories with built-in types

Modelando memorias con tipos integrados
=======================================

.. index:: single: modeling; memories

..
 Python has powerful built-in data types that can be useful to model hardware
 memories. This can be merely a matter of putting an interface around some data
 type operations.

Python tiene tipos de datos integrados poderosos, que pueden ser útiles
para modelar hardware. Esto puede ser simplemente una cuestion de colocar
una interfaz al rededor de algunos operaciones de tipos de datos

..
 For example, a :dfn:`dictionary` comes in handy to model sparse memory
 structures. (In other languages, this data type is called  :dfn:`associative
 array`, or :dfn:`hash table`.) A sparse memory is one in which only a small part
 of the addresses is used in a particular application or simulation. Instead of
 statically allocating the full address space, which can be large, it is better
 to dynamically allocate the needed storage space. This is exactly what a
 dictionary provides. The following is an example of a sparse memory model::

Por ejemplo, un :dfn:`diccionario` es conveniente para modelar estructuras
de matrices dispersas (en otros lenguajes estos tipos de datos se llaman
:dfn:`arraglos asociativos` o :dfn:`tablas hash`). Una memoria dispersa es
aquella que sólo una pequeña parte de las celdas se usan en una aplicación
en particular o simulación. En lugar de estaticamente asignar todo el
espacio de direcciones, que puede ser grande, es mejor dinámicamente
asignar el espacio de almacenamiento necesario. Esto es exactamente lo que
suministra un diccionario. Lo siguiente es un ejemplo de un modoelo de
matriz dispersa::

   def sparseMemory(dout, din, addr, we, en, clk):

       """ Modelo de memoria dispersa basado en un diccionario

       Ports:
       dout -- dato de salida
       din -- dato de entrada
       addr -- bus de direcciones
       we -- write enable: escribe si es 1, lee en otro caso
       en -- interface enable: se habilita si es 1
       clk -- reloj de entrada

       """

       memory = {}

       @always(clk.posedge)
       def access():
           if en:
               if we:
                   memory[addr.val] = din.val
               else:
                   dout.next = memory[addr.val]

       return access

..
 Note how we use the ``val`` attribute of the ``din`` signal, as we don't
 want to store the signal object itself, but its current value. Similarly,
 we use the ``val`` attribute of the ``addr`` signal as the dictionary key.

Observe cómo usamos el atributo ``val`` de la señal ``din``, ya que no
queremos almacenar el objeto de la señal en sí mismo, pero sí su valor. De
igual forma, usamos el atributo ``val`` para la señal ``addr`` como la
clave del diccionario.

..
 In many cases, MyHDL code uses a signal's current value automatically when
 there is no ambiguity: for example, when a signal is used in an
 expression. However, in other cases, such as in this example, you have to
 refer to the value explicitly: for example, when the Signal is used as a
 dictionary key, or when it is not used in an expression.  One option is to
 use the ``val`` attribute, as in this example.  Another possibility is to
 use the ``int()`` or ``bool()`` functions to typecast the Signal to an
 integer or a boolean value. These functions are also useful with
 :class:`intbv` objects.


En muchos casos, el código MyHDL usa el valor presente de la señal
automáticamente  cuando no hay ambigüedad: por ejemplo, cuando una señal se
usa en una expresión. Sin embargo, en otros casos, tal como en este
ejemplo, se tiene que referir al valor explícitamente: por ejemplo, cuano
la señal se una como una clave de diccionario, o cuando no se usa en una
expresión. Una opción es usar el atributo ``val`` como en este ejemplo.
Otra posibilidad es usa funciones ``int()`` o ``bool()`` para la conversión
del tipo Signal a un valor entero o boleano. Estas funciones son también
útiles con objetos :class:`intbv`.


..
 As a second example, we will demonstrate how to use a list to model a
 synchronous fifo::

Como un segundo ejemplo, demostraremos cómo usar una lista para modelar una
fifo síncrona::

 def fifo(dout, din, re, we, empty, full, clk, maxFilling=sys.maxint):

       """ Modelo de cola fifo síncrona basada en una lista 

       Ports:
       dout -- dato de salida
       din -- dato de entrada
       re -- read enable
       we -- write enable
       empty -- bandera de indicación de vacío
       full -- bandera de indicación de lleno
       clk -- entrada de reloj

       Optional parameter:
       maxFilling -- tamaño máximo, "infinite" por omisión

       """

       memory = []

       @always(clk.posedge)
       def access():
           if we:
               memory.insert(0, din.val)
           if re:
               dout.next = memory.pop()
           filling = len(memory)
           empty.next = (filling == 0)
           full.next = (filling == maxFilling)

       return access

..
 Again, the model is merely a MyHDL interface around some operations on a list:
 :func:`insert` to insert entries, :func:`pop` to retrieve them, and :func:`len`
 to get the size of a Python object.

Una vez más, el modelo es solamente una interfaz MyHDL al rededor de
algunas operaciones en una lista::func:`insert` para insertar elementos,
:func:`pop` para obtenerlos, y :func:`len` para saber el tamaño de un
objeto Python.

.. _model-err:

.. Modeling errors using exceptions

Modelando errores usando excepciones
====================================

..
 In the previous section, we used Python data types for modeling. If such a type
 is used inappropriately, Python's run time error system will come into play. For
 example, if we access an address in the :func:`sparseMemory` model that was not
 initialized before, we will get a traceback similar to the following (some lines
 omitted for clarity)::

En la sección anterior, usamos los tipos de datos de Python para modelar.
Si un tipo de estos se usa inapropiadamente, el sistema de errores de
Python entrará en escena. Por ejemplo, si accedemos a una dirección en el
modelo 
:func:`sparseMemory` que no fue inicializado antes, tendremos un mensaje
similar al siguiente (algunas líneas se han omitido por claridad)::


   Traceback (most recent call last):
   ...
     File "sparseMemory.py", line 31, in access
       dout.next = memory[addr.val]
   KeyError: Signal(51)

..  Similarly, if the ``fifo`` is empty, and we attempt to read from it, we get::

Similarmente, si la ``fifo`` está vacía, e intentamos leerla, obtendremos::
  
  Traceback (most recent call last):
   ...
     File "fifo.py", line 34, in fifo
       dout.next = memory.pop()
   IndexError: pop from empty list

..
 Instead of these low level errors, it may be preferable to define errors at the
 functional level. In Python, this is typically done by defining a custom
 ``Error`` exception, by subclassing the standard ``Exception`` class. This
 exception is then raised explicitly when an error condition occurs.



En lugar de estos errores de bajo nivel, pude ser preferible definir
errores al nivel de la función. En Python esto se realiza típícamente
definiendo una excepción de  ``Error`` a la medida, haciendo una subclase
de la clase ``Exception``. Esta excepción se lanza explícitamente cuando
una condición de error ocurre.

..
 For example, we can change the :func:`sparseMemory` function as follows (with
 the doc string is omitted for brevity)::

Por ejemplo, podemos cambiar la función :func:`sparseMemory` así (la cadena
doc se omite por brevedad)::

   class Error(Exception):
       pass

   def sparseMemory2(dout, din, addr, we, en, clk):

       memory = {}

       @always(clk.posedge)
       def access():
           if en:
               if we:
                   memory[addr.val] = din.val
               else:
                   try:
                       dout.next = memory[addr.val]
                   except KeyError:
                       raise Error, "Dirección sin iniciar %s" % hex(addr)

       return access


..
 This works by catching the low level data type exception, and raising the custom
 exception with an appropriate error message instead.  If the
 :func:`sparseMemory` function is defined in a module with the same name, an
 access error is now reported as follows::

Esto trabaja atrapando la execpción de bajo nivel, y lanzando en su lugar la exepción a
la medida  con un mensaje de error apropiado. Si la función
:func:`sparseMemory` se define en un módulo con algún nombre, un error de
acceso se reporta así::

   Traceback (most recent call last):
   ...
     File "sparseMemory.py", line 61, in access
       raise Error, "Uninitialized address %s" % hex(addr)
   Error: Uninitialized address 0x33


..
 Likewise, the :func:`fifo` function can be adapted as follows, to report
 underflow and overflow errors::

Igualmente la función :func:`fifo` se puede adaptar así, para reportar un
error de desborde por exceso o por deficit::

   class Error(Exception):
       pass


   def fifo2(dout, din, re, we, empty, full, clk, maxFilling=sys.maxint):

       memory = []

       @always(clk.posedge)
       def access():
           if we:
               memory.insert(0, din.val)
           if re:
               try:
                   dout.next = memory.pop()
               except IndexError:
                   raise Error, "Underflow -- Read from empty fifo"
           filling = len(memory)
           empty.next = (filling == 0)
           full.next = (filling == maxFilling)
           if filling > maxFilling:
               raise Error, "Overflow -- Max filling %s exceeded" % maxFilling

       return access

..
 In this case, the underflow error is detected as before, by catching a low level
 exception on the list data type. On the other hand, the overflow error is
 detected by a regular check on the length of the list.

En este caso, el error de desborde por déficit se detecta antes, atrapando
una excepción de bajo nivel en la lista de datos. Por otra parte, el error
de desborde por exceso es detectado por una prueba regular de la longitud
de la lista.


.. _model-obj:

.. Object oriented modeling

Modelado orientado a objetos
============================


.. index:: single: modeling; object oriented

..
 The models in the previous sections used high-level built-in data types
 internally. However, they had a conventional RTL-style interface.  Communication
 with such a module is done through signals that are attached to it during
 instantiation.

Los modelos en las secciones anteriores usan tipos tipos integrados
internamente. Sin embargo, ellos tienen una interface del estilo RTL. La
comunicación con un módulo de estos  se hace a través de señales que se
unen durante la instanciación.

..
 A more advanced approach is to model hardware blocks as objects. Communication
 with objects is done through method calls. A method encapsulates all details of
 a certain task performed by the object. As an object has a method interface
 instead of an RTL-style hardware interface, this is a much  higher level
 approach.

Una aproximación más avanzada es modelar bloques de hardware como objetos.
La comunicación con objetos se hace a traves de invocación de métodos. Un
método encapsula
As an example, we will design a synchronized queue object.  Such an object can
be filled by producer, and independently read by a consumer. When the queue is
empty, the consumer should wait until an item is available. The queue can be
modeled as an object with a :meth:`put(item)` and a :meth:`get` method, as
follows::

   from myhdl import *

   def trigger(event):
       event.next = not event

   class queue:
       def __init__(self):
          self.l = []
          self.sync = Signal(0)
          self.item = None
       def put(self,item):
          # non time-consuming method
          self.l.append(item)
          trigger(self.sync)
       def get(self):
          # time-consuming method
          if not self.l:
             yield self.sync
          self.item = self.l.pop(0)

..
 The :class:`queue` object constructor initializes an internal list to hold
 items, and a *sync* signal to synchronize the operation between the methods.
 Whenever :meth:`put` puts an item in the queue, the signal is triggered.  When
 the :meth:`get` method sees that the list is empty, it waits on the trigger
 first. :meth:`get` is a generator method because  it may consume time. As the
 ``yield`` statement is used in MyHDL for timing control, the method cannot
 "yield" the item. Instead, it makes it available in the *item* instance
 variable.


El objeto constructor  :class:`queue` inicia una lista interna que almacena
ítems y una señal *sync* para sincronizar la operación entre los métodos.
Siempre que :meth:`put` coloque un ítem en la cola, la señal es disparada.
Cuando el método :meth:`get` es un método generador porque puede consumir
tiempo. Como la instrucción ``yield`` se usa en MyHDL para el control del
tiempo, el método no "puede" ceder el ítem. En su lugar, lo hace disponible
en la instancia de la variable *item*.


..
 To test the queue operation, we will model a producer and a consumer in the test
 bench.  As a waiting consumer should not block a whole system, it should run in
 a concurrent "thread". As always in MyHDL, concurrency is modeled by Python
 generators. Producer and consumer will thus run independently, and we will
 monitor their operation through some print statements::


Para probar la operación de la cola, modelaremos un productor y un
consumidor en el banco de pruebas. Como consumidor no debería bloquear todo
un sistema, debería ejecutarse en un "hilo" concurrente . Como siempre en
MyHDL, la concurrencia se modela por los generadores Python. El productor y
el consumidor se ejecutarán independientemente, y observaremos su operación
a través de algunas instrucciones print::

   q = queue()

   def Producer(q):
       yield delay(120)
       for i in range(5):
           print "%s: PUT item %s" % (now(), i)
           q.put(i)
           yield delay(max(5, 45 - 10*i))

   def Consumer(q):
       yield delay(100)
       while 1:
           print "%s: TRY to get item" % now()
           yield q.get()
           print "%s: GOT item %s" % (now(), q.item)
           yield delay(30)

   def main():
       P = Producer(q)
       C = Consumer(q)
       return P, C 

   sim = Simulation(main())
   sim.run()

..
 Note that the generator method :meth:`get` is called in a ``yield`` statement in
 the :func:`Consumer` function. The new generator will take over from
 :func:`Consumer`, until it is done. Running this test bench produces the
 following output::

Observe que el método generador :meth:`get` es invocado en una instrucción
``yield`` en la función :func:`Consumer`. El nuevo generador tomará el
control de :func:`Consumer` hasta que culmine. Ejecutando este banco de
pruebas produce la siguiente salida::

   % python queue.py
   100: TRY to get item
   120: PUT item 0
   120: GOT item 0
   150: TRY to get item
   165: PUT item 1
   165: GOT item 1
   195: TRY to get item
   200: PUT item 2
   200: GOT item 2
   225: PUT item 3
   230: TRY to get item
   230: GOT item 3
   240: PUT item 4
   260: TRY to get item
   260: GOT item 4
   290: TRY to get item
   StopSimulation: No more events

.. rubric:: Footnotes

..
 .. [#] The name :func:`always_comb` refers to a construct with similar semantics in
   SystemVerilog.

.. [#] El  nombre :func:`always_comb` se refiere a un constructor con una
       semántica similar en SystemVerilog

..
 .. [#] It also possible to have a reproducible random output, by explicitly providing a
   seed value. See the documentation of the ``random`` module.

.. [#] También es posible tener una salida aleatoria reproducible, mediante
  el suministro explícito de un valor de semillla. Vea la documentación del
  módulo ``random``.
