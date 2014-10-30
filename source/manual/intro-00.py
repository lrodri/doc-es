from myhdl import Signal, delay, always, now, Simulation

def HelloWorld():

       interval = delay(15)

       @always(interval)
       def sayHello():
           print "%s Hello World!" % now()

       return sayHello


inst = HelloWorld()
sim = Simulation(inst)
sim.run(50)


