'''
Created on 25.09.2017

@author: Leonard
'''
#from OperatorElement import multiplyOperator,allOperators
#from PredefinedObjects import functions
#from Expression import ExpressionBlock,FunctionBlock,FunctionElement
import PredefinedObjects
import Expression

        


## test funtions for strings
variables = list("abcdefghijklmnopqrstuvwxyz")

def IsNumber(s):
    try:
        t = float(s)
        t = int(s)
        return True
    except:
        return False
    
def IsOperator(s):
    for operator in Expression.allOperators:
        if (s == operator.sign):
            return operator
    return False
def IsFunction(s):
    for f in PredefinedObjects.functions:
        if (s==f.name):
            return f
    return False


def IsChar(s):
    return s in variables