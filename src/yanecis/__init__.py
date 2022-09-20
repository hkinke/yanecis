"""
Author: Heritier Kinke
Email: heritier.kinke@yandex.com
License: GNU Public License (GPL) v3.0
"""
import numpy as np
from typing import List

class Element:
    """I do not manage internal nodes. I will add the code to manage that"""
    def __init__(self,nodes,equation_number=0,variable_number=0,internal_node_number=0):
        self.nodes=nodes
        self.equation_number=equation_number
        self.internal_node_number=internal_node_number
        self.variable_number=variable_number
    def get_nodes(self):
        return self.nodes
    def set_equation_range(self,start,end):
        self.equations=range(start,end)
    def set_internal_node_offset(self,internal_node_offset):
        """ internal node are added by offset value """
        self.internal_node_offset=internal_node_offset
    def set_variable_range(self,start,end):
        self.variables=range(start,end)
    def get_equation_number(self):
        return self.equation_number
    def get_internal_node_number(self):
        return self.internal_node_number
    def get_variable_number(self):
        return self.variable_number
    def contribute(self,*args):
        self._contribute(*args)
    def _contribute(self,*args):
        raise NotImplementedError
        
class Diode(Element):
    def __init__(self,n1,n2):
        super(Diode,self).__init__([n1,n2])
        self.Is=1e-14
    def _contribute(self,A,b,x,node_dict):
        n1=node_dict[self.nodes[0]]
        n2=node_dict[self.nodes[1]]
        VT=0.025
        value=self.Is*np.expm1((x[n1,0]-x[n2,0])/VT)
        value2=self.Is/VT*np.exp((x[n1,0]-x[n2,0])/VT)
        value3=self.Is/VT*np.exp((x[n1,0]-x[n2,0])/VT)*(x[n1,0]-x[n2,0])
        A[n1,n1]+=value2
        A[n1,n2]-=value2
        A[n2,n2]+=value2
        A[n2,n1]-=value2
        b[n1,0]+=-value+value3
        b[n2,0]+=value-value3
        
class Resistor(Element):
    def __init__(self,n1,n2,value):
        super(Resistor,self).__init__([n1,n2])
        self.value=value
    def _contribute(self,A,b,x,node_dict):
        n1=node_dict[self.nodes[0]]
        n2=node_dict[self.nodes[1]]
        A[n1,n1]+=1/self.value
        A[n1,n2]+=-1/self.value
        A[n2,n2]+=1/self.value
        A[n2,n1]+=-1/self.value

# miss current contribution
class Voltage(Element):
    def __init__(self,n1,n2,value):
        super(Voltage,self).__init__([n1,n2],1,1)
        self.value=value
    def _contribute(self,A,b,x,node_dict):
        eq=self.equations[0]
        var=self.variables[0]
        n1=node_dict[self.nodes[0]]
        n2=node_dict[self.nodes[1]]
        A[n1,var]=-1
        A[n2,var]=1
        A[eq,n1]=1
        A[eq,n2]=-1
        b[eq,0]=self.value

# miss current contribution
class Ground(Element):
    def __init__(self):
        super(Ground,self).__init__([0],1)
    def _contribute(self,A,b,x,node_dict):
        eq=self.equations[0]
        n1=node_dict[self.nodes[0]]
        A[eq,n1]=1.
        b[eq,0]=0.0

class Current(Element):
    def __init__(self,n1,n2,value):
        super(Current,self).__init__([n1,n2])
        self.value=value
    def _contribute(self,A,b,x,node_dict):
        n1=node_dict[self.nodes[0]]
        n2=node_dict[self.nodes[1]]
        b[n1,0]+=self.value
        b[n2,0]+=-self.value


class Circuit:
    def __init__(self):
        self.elements:List[Element]=[Ground()]
    def add(self,el):
        self.elements.append(el)
    def op(self):
        """Compute the Operating Point"""
        nodes=set()
        for el in self.elements:
            nodes=nodes.union(el.get_nodes())

        nodes=sorted(nodes)

        number_nodes=len(nodes)

        node_dict={k:v for k,v in zip(nodes,range(number_nodes))}

        internal_equations=0

        for el in self.elements:
            internal_equations+=el.get_equation_number()

        number_equations=number_nodes+internal_equations

        start=number_nodes
        for el in self.elements:
            number=el.get_equation_number()
            if number > 0:
                end=start+number
                el.set_equation_range(start,end)
                start=end
            

        number_variables=number_nodes
        for el in self.elements:
            number=el.get_variable_number()
            if number > 0:
                end=number_variables+number
                el.set_variable_range(number_variables,end)
                number_variables=end

        A=np.zeros((number_equations,number_variables))
        b=np.zeros((number_equations,1))

        # operating point
        x0=np.zeros((number_variables,1))

        done = False
        while not done:

            for el in self.elements:
                el.contribute(A,b,x0,node_dict)
            x=np.linalg.lstsq(A,b,rcond=None)[0]
            # exit()
            if ((np.sum((x-x0)**2))**0.5) > 1e-8:
                x0=x
                A=np.zeros((number_equations,number_variables))
                b=np.zeros((number_equations,1))
            else:
                done = True
        reverse_node_dict={v:k for k,v in node_dict.items()}

        for i in range(number_nodes):
            print(f"node{reverse_node_dict[i]}: {x[i,0]}")