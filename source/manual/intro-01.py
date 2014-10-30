from myhdl import Signal, delay, always, now, Simulation


def ClkDriver(clk):

       halfPeriod = delay(20)

       @always(halfPeriod)
       def driveClk():
           clk.next = not clk

       return driveClk


def HelloWorld(clk):

    # otra posibilidad es negedge
       @always(clk.negedge)
       def sayHello():
           print "%s Hello World!" % now()

       return sayHello


clk = Signal(0)
print "El valor de la senal es %d " % clk.val
# se declaran las instancias de las funciones

clkdriver_inst = ClkDriver(clk)
hello_inst = HelloWorld(clk)

## se ejecuta la simulacion con las dos funciones
## ejecutandose concurrentemente

sim = Simulation(clkdriver_inst, hello_inst)
sim.run(100)


