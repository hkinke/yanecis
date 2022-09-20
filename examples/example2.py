from yanecis import Ground,Current,Resistor,Diode,Voltage,Circuit

d1=Diode(1,2)
R1=Resistor(2,0,1)
V1=Voltage(1,0,2)
R2=Resistor(1,3,1)
I1=Current(3,0,1)


cir=Circuit()
cir.add(d1)
cir.add(V1)
cir.add(R1)
cir.add(R2)
cir.add(I1)

cir.simulate()
# print solution



