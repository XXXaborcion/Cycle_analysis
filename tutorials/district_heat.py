from tespy.components.basics.cycle_closer import CycleCloser
from tespy.networks import Network
from tespy.components import (
    CycleCloser, Pipe, Pump, Valve, SimpleHeatExchanger
)
from tespy.connections import Connection

nw = Network()
nw.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

# central heating plant
hs = SimpleHeatExchanger('heat source')
cc = CycleCloser('cycle closer')
pu = Pump('feed pump')

# consumer
cons = SimpleHeatExchanger('consumer')
val = Valve('control valve')

# pipes
pipe_feed = Pipe('feed pipe')
pipe_return = Pipe('return pipe')

# connections
c0 = Connection(cc, "out1", hs, "in1", label="0")
c1 = Connection(hs, "out1", pu, "in1", label="1")
c2 = Connection(pu, "out1", pipe_feed, "in1", label="2")
c3 = Connection(pipe_feed, "out1", cons, "in1", label="3")
c4 = Connection(cons, "out1", val, "in1", label="4")
c5 = Connection(val, "out1", pipe_return, "in1", label="5")
c6 = Connection(pipe_return, "out1", cc, "in1", label="6")
nw.add_conns(c0, c1, c2, c3, c4, c5, c6)
# inte klar