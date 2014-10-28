********
Hojeada 
********

..
 The goal of the MyHDL project is to empower hardware designers with
 the elegance and simplicity of the Python language.

El objetivo del proyecto MyHDL es empoderar a los diseñadores de hardware
con la elegancia y simplicidad del lenguaje Python

..
 MyHDL is a free, open-source package for using Python as a
 hardware description and verification language. Python is a very high
 level language, and hardware designers can use its full power to model
 and simulate their designs.  Moreover, MyHDL can convert a design to
 Verilog or VHDL. This provides a path into a traditional design flow.

MyHDL es un paquete libre y de código abierto para usar a Python como un
lenguaje de descripción y verificación de hardware. Python es un lenguaje
de muy alto nivel, y los diseñadores de hardware pueden usar todo su poder
para modelar y simular sus diseños. Por otra parte, MyHDL puede convertir
un diseño a Verilog o VHDL. Esto suministra un camino en un flujo de diseño
tradicional.


*Modelando*

..
 Python's power and clarity make MyHDL an ideal solution for high level
 modeling.  Python is famous for enabling elegant solutions to complex
 modeling problems.  Moreover, Python is outstanding for rapid
 application development and experimentation.

El poder y la claridad de Python y la hacen a MyHDL una solución ideal para
modelamiento de alto nivel. Python es famoso por permitir soluciones
elegantes a problemas complejos de modelamiento . Sin embargo Python es
exepcionalmente bueno para el desarrollo de aplicaciones rápidas y la
experimentación.

..
 The key idea behind MyHDL is the use of Python generators to model
 hardware concurrency. Generators are best described as resumable
 functions.  MyHDL generators are similar to always blocks in Verilog
 and processes in VHDL.

La idea clave atrás de MyHDL es el uso de generadores Python para modelar
la concurrencia del hardware. Los generadores son mejor descritos como
funciones reanudables. los generadores MyHDL son similares a los bloques
*always* en Verilog y *processes* en VHDL.

..
 A hardware module is modeled as a function that returns
 generators. This approach makes it straightforward to support features
 such as arbitrary hierarchy, named port association, arrays of
 instances, and conditional instantiation.  Furthermore, MyHDL provides
 classes that implement traditional hardware description concepts. It
 provides a signal class to support communication between generators, a
 class to support bit oriented operations, and a class for enumeration
 types.

Un módulo de hardware se modela como un función que retorna generadores
generadores Python para modelar la concurrencia del hardware. Los
generadores son mejor descritos como funciones reanudables. los generadores
MyHDL son similares a los bloques *always* en Verilog y *processes* en
VHDL.
Un módulo de hardware se modela como un función que retorna generadores.
Esta visión hace que sean directas características tales como jerarquía
arbitraria, asociación de nombres a puertos, instancias de arreglos e
intanciación condicional. Luego, MyHDL suministra clases que implementan
los conceptos tradicionales descripción de hardware. Suministra una clase
de *signal* para permitir comunicación entre generadores, una clase para
permitir operaciones orientadas a bit, y una clase para enumeración de
tipos.

*Simulación y verificación*

..
 The built-in simulator runs on top of the Python interpreter. It supports
 waveform viewing by tracing signal changes in a VCD file.

El simulador construido se ejecuta sobre el interprete de Python. Él
permite la visulación de formas de onda dibujando los cambios de la señal
en un archivo VCD.

..
 With MyHDL, the Python unit test framework can be used on hardware designs.
 Although unit testing is a popular modern software verification technique, it is
 still uncommon in the hardware design world.

Con MyHDL, el marco de  pruebas unitarias de Python se pueden usar en
diseños de hardware. A pesar que las pruebas unitarias son una técnica
popular de verificación de software, aún no es muy común en el mundo de
diseño de hardware.

..
 MyHDL can also be used as hardware verification language for Verilog
 designs, by co-simulation with traditional HDL simulators.

MyHDL se puede usar también como lenguaje de verificación de hardware para
diseños de Verilog mediante la co-simulación con simuladores tradicionales
de HDL.



*Conversión a Verilog y VHDL*

..
 Subject to some limitations, MyHDL designs can be converted to Verilog
 or VHDL.  This provides a path into a traditional design flow,
 including synthesis and implementation.  The convertible
 subset is restricted, but much wider than the standard synthesis subset.
 It includes features that can be used for high level modeling and test benches.

Sujeto a algunas limitaciones, los diseños MyHDL pueden ser convertidos a
Verilog o VHDL. Esto suministra un camino en un flujo tradicional de
diseño, incluida síntesis e implementación.
Tes subconjunto convertible es restringido, pero mucho más amplio que las
síntesis normales. Incluye características que se pueden usar en
modelamiento de alto nivel y pruebas *benches*

..
 The converter works on an instantiated design that has been
 fully elaborated. Consequently, the original design structure can be
 arbitrarily complex. Moreover, the conversion limitations apply only
 to code inside generators. Outside generators, Python's full power can
 be used without compromising convertibility.

El conversor trabaja en una instancia del diseño que ha sido totalmente
elaborada. Por consiguiente, la estructura del diseño original puede ser
arbitrariamente compleja. Sin embargo, las limitaciones de conversión
involucran sólo a código dentro de los generadores. Fuera de los
generadores, se puede usar toda la potencia de Python sin comprometer la
covertibilidad.

..
 Finally, the converter automates a number of tasks that are hard in
 Verilog or VHDL directly. A notable feature is the automated handling of
 signed arithmetic issues.

Finalmente, el conversor automatiza un número de tareas que son
dispendiosas en Verilog y VHDL directamente. Una característica destacable
es el manejo automatizado de cuestiones de aritmética con signo.


