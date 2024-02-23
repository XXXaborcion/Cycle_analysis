import matplotlib.pyplot as plt
import numpy as np
from tespy.networks import Network

# create a network object with R134a as fluid
my_plant = Network(fluids=['CO2'])
# set the unitsystem for temperatures to °C and for pressure to bar
my_plant.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

from tespy.components import (
    CycleCloser, Compressor, Valve, SimpleHeatExchanger, Turbine
)

cc = CycleCloser('cycle closer')

# heat sink
co = SimpleHeatExchanger('condenser')
# heat source
ev = SimpleHeatExchanger('evaporator')

va = Valve('expansion valve')#eta_ise=0.7
cp = Compressor('compressor')#eta_ise=0.8

from tespy.connections import Connection

# connections of heat pump
c1 = Connection(cc, 'out1', ev, 'in1', label='1')
c2 = Connection(ev, 'out1', cp, 'in1', label='2')#här ska T=-10, x=1
c3 = Connection(cp, 'out1', co, 'in1', label='3')
c4 = Connection(co, 'out1', va, 'in1', label='4')
c0 = Connection(va, 'out1', cc, 'in1', label='0')

# this line is crutial: you have to add all connections to your network
my_plant.add_conns(c1, c2, c3, c4, c0)
#temp of isobaric evaporation T=-10 C dry saturated vapor at evap outlet
#adiabatic compression with isentropic efficiency eta_ise=0.8
#adiabatic expansion with isentropic efficiency eta_ise=0.7
#regenerator thermal efficiency 0.7
#CO2 exit temperature from high-and intermediate-pressure gas coolers 31°C. OPtimum pressures

p=np.linspace(70,90,10)
#x=1 torr ånga
#x=0 bara vätska
co.set_attr(pr=0.98, Q=-1e6)#kan behålla pr, kanske Q
ev.set_attr(pr=0.98)#kan behålla pr ut T/c2 måste vara -10, x=1
cp.set_attr(eta_s=0.8)#eta_s ska vara 0.8
#va.set_attr(eta_s=0.7)
c2.set_attr(T=-10,x=1, fluid={'CO2': 1})#fluid ska vara CO2 x=1,T=-10
c4.set_attr(T=31)
#c4.set_attr(T=31)#högst oklart vas som önskas, försök sätta andra param
COPS=[]

for i in range(len(p)):
    #c4.set_attr(T=30,p=p[i])
    c2.set_attr(p=p[i])  # fluid ska vara CO2 x=1,T=-10

    my_plant.solve(mode='design')
    #my_plant.print_results()
    COPS.append(abs(co.Q.val) / cp.P.val)

npCOPS=np.array(COPS)
plt.plot(p,npCOPS)
plt.show()