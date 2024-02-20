from tespy.components import Sink, Source, SimpleHeatExchanger, Compressor, CycleCloser, Valve
from tespy.connections import Connection
from tespy.networks import Network

# from neqsim.thermo import fluid, fluid_df, TPflash, PSflash, PHflash

import CoolProp.CoolProp as CP

nw = Network(T_unit='C', p_unit='bar', m_unit='kg / s', h_unit='kJ / kg')


#här körde han med lite olika komponenter. Fattade inte helt. Men bytte ut sink och refrigerator mot annat
#samt körde utan cycle closer för att kolla på komponenter

cp = Compressor("compressor")
refrigerator = SimpleHeatExchanger("refrigerator")
heat_sink = SimpleHeatExchanger("heat sink")
va = Valve("valve")
cc = CycleCloser("cycle closer")



c1 = Connection(refrigerator, "out1", cp, "in1", label="1")
c2 = Connection(cp, "out1", heat_sink, "in1", label="2")
c3 = Connection(heat_sink, "out1", va, "in1", label="3")
c4 = Connection(va, "out1", cc, "in1", label="4")
c0 = Connection(cc, "out1", refrigerator, "in1", label="0")

nw.add_conns(c1, c2, c3, c4, c0)

#kan sätta dessa på massa olika sätt. Gör helst inte direkt med eta_s, då räknar den tydligen dåligt.
#men t.ex. T och p bestämmer h, tänk på vilka man vill sätta. Kan även sätta Q t.ex. Detta kördes halvdant pga
#temperaturerna. Men kan utveckla
c1.set_attr(fluid={"CO2": 1}, m=1, T=10, p=70)
c2.set_attr(p=500, T=50)
c3.set_attr(p=500, T=40)
c4.set_attr(p=70)

cp.set_attr()#eta_s=0.8)

nw.solve("design")

c2.set_attr(T=None)
cp.set_attr(eta_s=0.8)

c3.set_attr(T=None)
refrigerator.set_attr(Q=1e4)

nw.solve("design")

nw.print_results()