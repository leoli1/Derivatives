'''
Created on 25.09.2017

@author: Leonard
'''
#from Expression import ExpressionBlock,ExpressionElement,NumberElement
#import ExpressionElement
#from Tools import expDependOnVariable
#imported = False
#if (not imported):
 #   import Expression
  #  import Tools
   # imported = True
"""import sys
if 'Expression' not in sys.modules:
    import Expression
else:
    Expression = sys.modules['Expression']

class OperatorElement(Expression.ExpressionElement):
    def __init__(self):
        self.sign = ''
        
    def derive(self,left,right, variable):
        pass
    def __str__(self):
        return self.sign
    
class PlusOperator(OperatorElement):
    def __init__(self):
        self.sign = '+'
        
    def derive(self, left, right, variable):
        derivative = Expression.ExpressionBlock()
        derivative.append(left.derive(variable))
        derivative.append(plusOperator)
        derivative.append(right.derive(variable))
        
        return derivative
    
class MinusOperator(OperatorElement):
    def __init__(self):
        self.sign = '-'
        
    def derive(self, left, right, variable):
        OperatorElement.derive(self, left, right, variable)
class MultiplyOperator(OperatorElement):
    def __init__(self):
        self.sign = '*'
    def derive(self, factors, variable):
        derivative = Expression.ExpressionBlock()
        dependOnVariable = []
        dontDependOnVariable = []
        for factor in factors:
            if Tools.expDependOnVariable(factor, variable):
                dependOnVariable.append(factor)
            else:
                dontDependOnVariable.append(factor)
        
        for independet in dontDependOnVariable:
            derivative.append(independet)
            derivative.append(multiplyOperator)
            
        if len(dependOnVariable)>2:
            raise Exception("Can't handle this")
        elif len(dependOnVariable)==2: # fg'+f'g
            block = Expression.ExpressionBlock()
            block.append(dependOnVariable[0])
            block.append(multiplyOperator)
            block.append(dependOnVariable[1].derive(variable))
            block.append(plusOperator)
            block.append(dependOnVariable[0].derive(variable))
            block.append(multiplyOperator)
            block.append(dependOnVariable[1])
            derivative.append(block)
        elif len(dependOnVariable)==1:
            derivative.append(dependOnVariable[0])
        else:
            pass
        return derivative
        
            
class DivideOperator(OperatorElement):
    def __init__(self):
        self.sign = '/'
        
class PotentialOperator(OperatorElement):
    def __init__(self):
        self.sign = "^"
        
    def derive(self, base, exponent, variable):
        base_var = Tools.expDependOnVariable(base, variable)
        exponent_var = Tools.expDependOnVariable(exponent, variable)
        if (base_var and exponent_var):#x^x
            raise Exception("TO DO")
        elif (base_var and not exponent_var): #x^2
            #factor = ExpressionBlock()
            #factor.append(exponent_var)
            
            derivative = Expression.ExpressionBlock()
            #derivative.append(factor)
            derivative.append(exponent_var)
            derivative.append(multiplyOperator)
            derivative.append(base_var)
            derivative.append(potentialOperator)
            
            new_exponent = Expression.ExpressionBlock()
            new_exponent.append(exponent_var)
            new_exponent.append(minusOperator)
            new_exponent.append(Expression.NumberElement(1))
            
            derivative.append(new_exponent)
            
            derivative.append(multiplyOperator)
            derivative.append(base_var.derive(variable))
            
        elif (not base_var and exponent_var): #e^x
            raise Exception("TO DO")
        
            
minusOperator = MinusOperator()
plusOperator = PlusOperator()
multiplyOperator = MultiplyOperator()
divideOperator = DivideOperator()
potentialOperator = PotentialOperator()
allOperators = [
    minusOperator,
    plusOperator,
    multiplyOperator,
    divideOperator,
    potentialOperator
]"""