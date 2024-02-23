import matplotlib as plt
import numpy as np

from tespy.networks import Network
from tespy.components import (
    CycleCloser, Condenser, Pump, SimpleHeatExchanger, Turbine,
)
from tespy.connections import Connection

my_plant = Network()

my_plant.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

cc = CycleCloser('cycle closer')

# heat sink
co = SimpleHeatExchanger('condenser')
# heat source
ev = SimpleHeatExchanger('evaporator')
# compressor
pu = Pump('pump')
# expander
tu = Turbine('turbine')

# connect components
c1 = Connection(cc, 'out1', ev, 'in1', label='1')
c2 = Connection(ev, 'out1', tu, 'in1', label='2')
c3 = Connection(tu, 'out1', co, 'in1', label='3')
c4 = Connection(co, 'out1', pu, 'in1', label='4')
c5 = Connection(pu, 'out1', cc, 'in1', label='0')

my_plant.add_conns(c1, c2, c3, c4, c5)

ev.set_attr(pr=1, Q=126e6)
co.set_attr(pr=1)
pu.set_attr(eta_s=1)

c2.set_attr(p=50, T=450, fluid={'water': 1})
c3.set_attr(p=4, x=1)
c4.set_attr(x=0)

my_plant.solve(mode='design')
my_plant.print_results()
print(f'W_turb = {(c2.m.val) * ((c2.h.val) - (c3.h.val))} MW')
print(f'c2_m = {c2.m.val} kg/s')
print(f'c2_h = {c2.h.val} kJ/kg')
print(f'c3_h =  {c3.h.val} kJ/kg')

print(f'Q_out = {c3.m.val * (c3.h.val - c4.h.val)} MW')

