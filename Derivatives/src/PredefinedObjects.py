'''
Created on 25.09.2017

@author: Leonard
'''
imported = False
if (not imported):
    import Expression
    import types
    imported = True
    
def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


functions = []
constants = []

def SetupObjects():
    global functions,e,pi,constants
    Sin = Expression.FunctionElement('sin','sin','cos(x)','x')
    Cos = Expression.FunctionElement('cos','cos','-sin(x)','x')
    Tan = Expression.FunctionElement('tan','tan','1/(cos(x)^2)','x')
    
    Arcsin = Expression.FunctionElement('arcsin','arcsin','1/sqrt(1-x^2)','x')
    Arccos = Expression.FunctionElement('arccos','arccos','-1/sqrt(1-x^2)','x')
    Arctan = Expression.FunctionElement('arctan','arctan','1/(1+x^2)','x')
    
    Sinh = Expression.FunctionElement('sinh', 'sinh', 'cosh(x)','x')
    Cosh = Expression.FunctionElement('cosh','cosh','sinh(x)','x')
    
    
    Sqrt = Expression.FunctionElement('sqrt','sqrt','1/(2sqrt(x))','x')
    
    Ln = Expression.FunctionElement('ln','ln','1/x','x')
    Exp = Expression.FunctionElement('e^x','e^x','e^x','x')
    
    
    
    functions = [
        Sin,
        Cos,
        Tan,
        Arcsin,
        Arccos,
        Arctan,
        Sinh,
        Cosh,
        Sqrt,
        Ln,
        Exp
    ]
    
    e = Expression.NumberElement(2.7182818)
    pi = Expression.NumberElement(3.14159265358)
    
    constants = [
        e,
        pi
    ]
