from tespy.networks import Network

# create a network object with R134a as fluid
my_plant = Network(fluids=['CO2'])
# set the unitsystem for temperatures to °C and for pressure to bar
my_plant.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

from tespy.components import (
    CycleCloser, Compressor, Valve, SimpleHeatExchanger
)

cc = CycleCloser('cycle closer')

# heat sink
co = SimpleHeatExchanger('condenser')
# heat source
ev = SimpleHeatExchanger('evaporator')

va = Valve('expansion valve')
cp = Compressor('compressor')

from tespy.connections import Connection

# connections of heat pump
c1 = Connection(cc, 'out1', ev, 'in1', label='1')
c2 = Connection(ev, 'out1', cp, 'in1', label='2')
c3 = Connection(cp, 'out1', co, 'in1', label='3')
c4 = Connection(co, 'out1', va, 'in1', label='4')
c0 = Connection(va, 'out1', cc, 'in1', label='0')

# this line is crutial: you have to add all connections to your network
my_plant.add_conns(c1, c2, c3, c4, c0)

#x=1 torr ånga
#x=0 bara vätska
co.set_attr(pr=0.98, Q=-1e6)
ev.set_attr(pr=0.98)
cp.set_attr(eta_s=0.85)

c2.set_attr(T=20, x=1, fluid={'CO2': 1})
c4.set_attr(T=80, x=0)
