import numpy as np
import pyromat as pm
import tespy as ty
from tespy import components as tyc
from tespy.connections import Connection
'''
mass flow (m)

volumetric flow (v)

pressure (p)

enthalpy (h)

temperature (T)

a fluid vector (fluid)
'''

my_plant=ty.networks.Network()
my_plant.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

cc = tyc.CycleCloser('cycle closer')

# heat sink
co = tyc.SimpleHeatExchanger('condenser')
# heat source
ev = tyc.SimpleHeatExchanger('evaporator')

va = tyc.Valve('öalkwdmmklaw valve')
cp = tyc.Compressor('compressor')


c1 = Connection(cc, 'out1', ev, 'in1', label='1')
c2 = Connection(ev, 'out1', cp, 'in1', label='2')
c3 = Connection(cp, 'out1', co, 'in1', label='3')
c4 = Connection(co, 'out1', va, 'in1', label='4')
c0 = Connection(va, 'out1', cc, 'in1', label='0')

# this line is crutial: you have to add all connections to your network
my_plant.add_conns(c1, c2, c3, c4, c0)

co.set_attr(pr=0.98, Q=-1e6)
ev.set_attr(pr=0.98)
cp.set_attr(eta_s=0.85)

c2.set_attr(T=20, x=1, fluid={'R134a': 1})
c4.set_attr(T=80, x=0)

my_plant.solve(mode='design')
my_plant.print_results()

print(f'COP = {abs(co.Q.val) / cp.P.val}')