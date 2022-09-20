from yanecis import Resistor,Voltage,Circuit

V1=Voltage(1,0,1)
R1=Resistor(1,2,1)
R2=Resistor(2,0,1)
R3=Resistor(2,0,1)

cir=Circuit()
cir.add(V1)
cir.add(R1)
cir.add(R2)
cir.add(R3)

cir.op()
