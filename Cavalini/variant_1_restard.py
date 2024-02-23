import matplotlib.pyplot as plt
import numpy as np
from tespy.networks import Network


# create a network object with R134a as fluid
my_plant = Network(fluids=['CO2'])
# set the unitsystem for temperatures to °C and for pressure to bar
my_plant.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

from tespy.components import (
    CycleCloser, Compressor, Valve, SimpleHeatExchanger, Turbine,Source,Sink
)

cc = CycleCloser('cycle closer')

# heat sink
cond = SimpleHeatExchanger('condenser')
# heat source
evap = SimpleHeatExchanger('evaporator')

valv = Valve('expansion valve')#eta_ise=0.7
comp = Compressor('compressor')#eta_ise=0.8

sour= Source('source')
sink=Sink('sink')

from tespy.connections import Connection
c1=Connection(sour,'out1',comp,'in1',label='1')
c2=Connection(comp,'out1',sink,'in1',label='2')

my_plant.add_conns(c1, c2)
#exit temp cond =31
#evap temp=-10
p=np.linspace(30,100,12)
comp.set_attr(eta_s=0.8)
c1.set_attr(T=31,fluid={'CO2': 1},p=30)
c2.set_attr(T=31,p=100)
my_plant.solve(mode='design')
my_plant.print_results()
