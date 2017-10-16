# -*- coding: utf-8 -*-
from __future__ import division
'''
Created on 25.09.2017

@author: Leonard
'''
import Tools
import Derivative


class Expression(object):
    '''
    Klasse für den UserInput.
    enthält den geparsten input und die genutzten variablen
    '''


    def __init__(self):
        self.expressions = []
        self.variables = []
    
class ExpressionBlock(object):
    '''
    Ein Teil eines Terms, meistens durch ()-Klammern definiert
    '''
    def __init__(self, *args):#, _startChar):
        self.expressions = []
        for arg in args:
            self.expressions.append(arg)
   
   
    def append(self, el):
        '''
        fügt diesem Block ein Element hinzu
        '''
        self.expressions.append(el)
        
    def differentiate(self, variable):
        '''
        leitet diesen Block ab und gibt das Ergebnis zurück
        '''
        summands = [ExpressionBlock()] 
        signs = []
        i = 0

        for p in self.expressions:
            if p == plusOperator:
                if i!=0:
                    summands.append(ExpressionBlock())
                signs.append(plusOperator)
            elif p == minusOperator:
                if i!=0:
                    summands.append(ExpressionBlock())
                signs.append(minusOperator)
            else:
                summands[len(summands)-1].append(p)
            i += 1
                
        # jeden summanden einzeln ableiten
        derivatives = []
        for summ in summands:
            if not (expDependOnVariable(summ, variable)):
                derivatives.append(NumberElement(0))
                continue
            
            factors = []
            """for el in summ.expressions:
                if isinstance(el,OperatorElement) and el != multiplyOperator:
                    raise Exception("Not implemented yet")
                elif not isinstance(el, OperatorElement):
                    factors.append(el)"""
            i = 0
            while i<len(summ.expressions):
                el = summ.expressions[i]
              #  elif el == minusOperator:
               #     factors.append(NumberElement(-1))
                if el == divideOperator:
                    raise Exception("Divide Operator in expression")
                if not isinstance(el, OperatorElement):
                    factors.append(el)
                i+= 1
                
            if len(factors) == 2 and type(factors[0])==FunctionElement and IsBlock(factors[1]): # functionblock, faelschlicherweise zum expressionblock umgewandelt
                fblock = FunctionBlock()
                fblock.append(factors[0])
                fblock.append(factors[1])
                derivatives.append(fblock.differentiate(variable))
            else:
                if (len(factors)>1):
                    derivatives.append(multiplyOperator.differentiate(factors,variable))
                else:
                    derivatives.append(factors[0].differentiate(variable))
        
        sign_ordered_after = not isinstance(self.expressions[0],OperatorElement)
        derivative = []
        for i in list(range(len(derivatives))):
            if sign_ordered_after:
                derivative.append(derivatives[i])
                if len(signs)>i:
                    derivative.append(signs[i])
            else:
                if len(signs)>i:
                    derivative.append(signs[i])
                derivative.append(derivatives[i])
                
        d = ExpressionBlock()
        d.expressions = derivative
        return d
        

class PowerBlock(ExpressionBlock):
    def __init__(self):
        self.expressions = []
    def differentiate(self, variable):
        if (len(self.expressions)!=2):
            raise Exception("len of expressions in PowerBlock has to be 2")
        return powerOperator.differentiate(self.expressions[0], self.expressions[1], variable)
class QuotientBlock(ExpressionBlock):
    def __init__(self):
        self.expressions = []
    def differentiate(self, variable):
        if len(self.expressions)!=2:
            raise Exception("len of expressions in QuotiontBlock has to be 2")
        return divideOperator.differentiate(self.expressions[0],self.expressions[1],variable)
#class ProductBlock(ExpressionBlock):
    
class FunctionBlock(ExpressionBlock):
    def __init__(self):
        self.expressions = []
    def differentiate(self, variable):
        var = self.expressions[1]
        if (len(self.expressions) !=2):
            raise Exception("len of expressions in FunctionBlock has to be 2")
        return Derivative.ChainRule(self.expressions[0], self.expressions[1], variable)
class ExpressionElement(object):
    def __init__(self):
        pass
    def differentiate(self):
        pass


class NumberElement(ExpressionElement):
    def __init__(self, number):
        self.value = number
    def __str__(self):
        return str(self.value)
    def differentiate(self, variable):
        return NumberElement(0)
    
class FunctionElement(ExpressionElement):
    def __init__(self, _name,_function, _derivative, _derivative_variable):
        self.name = _name
        self.function = _function #<- useless
        self.derivative = _derivative
        self.dev_variable = _derivative_variable
    def __str__(self):
        return self.name
    
    def differentiate(self, variable):
        #f = Tools.IsFunction(self.derivative)
        #if (f!=False):
       #     return p
       # raise Exception("feels bad")
       import ParseInput
       deriv = ParseInput.ParseString(self.derivative)
      # print("part deriv "+self.name+" has quotientblock before replacing vars: "+str(hasBlockType(deriv)))
       deriv = replaceBlockWithExpr(deriv, self.dev_variable, variable, ExpressionBlock)
       #print("part deriv "+self.name+" has quotientblock after replacing vars: "+str(hasBlockType(deriv)))
       return deriv
   

class VariableElement(ExpressionElement):
    def __init__(self, _variable):
        self.variable = _variable
    def __str__(self):
        return self.variable
    
    def differentiate(self, var):
        if (var.variable == self.variable):
            return NumberElement(1)
        return NumberElement(0)
    
class OperatorElement(ExpressionElement):
    def __init__(self):
        self.sign = ''
        
    def differentiate(self,left,right, variable):
        pass
    def __str__(self):
        return self.sign
    
class PlusOperator(OperatorElement):
    def __init__(self):
        self.sign = '+'
        
    def differentiate(self, left, right, variable):
        derivative = Expression.ExpressionBlock()
        derivative.append(left.differentiate(variable))
        derivative.append(plusOperator)
        derivative.append(right.differentiate(variable))
        
        return derivative
    
class MinusOperator(OperatorElement):
    def __init__(self):
        self.sign = '-'
        
    def differentiate(self, left, right, variable):
        OperatorElement.differentiate(self, left, right, variable)
class MultiplyOperator(OperatorElement):
    def __init__(self):
        self.sign = '*'
    def differentiate(self, factors, variable):
        derivative = ExpressionBlock()
        dependOnVariable = []
        dontDependOnVariable = []
        for factor in factors:
            if expDependOnVariable(factor, variable):
                dependOnVariable.append(factor)
            else:
                dontDependOnVariable.append(factor)
        
        for independet in dontDependOnVariable:
            derivative.append(independet)
            derivative.append(multiplyOperator)
            
        if len(dependOnVariable)>2:
            first_block = ExpressionBlock()
            for i in list(range(len(dependOnVariable)-1)):
                first_block.append(dependOnVariable[i])
                if (i < len(dependOnVariable)-2):
                    first_block.append(multiplyOperator)
            derivative.append(multiplyOperator.differentiate([first_block,dependOnVariable[len(dependOnVariable)-1]],variable))
            #pass #TODO
        elif len(dependOnVariable)==2: # fg'+f'g
            block = ExpressionBlock()
            block.append(dependOnVariable[0])
            block.append(multiplyOperator)
            block.append(dependOnVariable[1].differentiate(variable))
            block.append(plusOperator)
            block.append(dependOnVariable[0].differentiate(variable))
            block.append(multiplyOperator)
            block.append(dependOnVariable[1])
            derivative.append(block)
        elif len(dependOnVariable)==1:
            derivative.append(dependOnVariable[0].differentiate(variable))
        else:
            pass
        return derivative
        
            
class DivideOperator(OperatorElement):
    def __init__(self):
        self.sign = '/'
    def differentiate(self, left, right, variable):
        left_var = expDependOnVariable(left, variable)
        right_var = expDependOnVariable(right, variable)
        derivative = ExpressionBlock()
        if (not left_var) and not right_var:
            derivative.append(left_var)
            derivative.append(divideOperator)
            derivative.append(right_var)
        elif left_var and not right_var:
            derivative.append(left.differentiate(variable))
            derivative.append(divideOperator)
            derivative.append(right)
        elif left_var and right_var:
            numerator = ExpressionBlock()
            numerator.append(left.differentiate(variable))
            numerator.append(multiplyOperator)
            numerator.append(right)
            numerator.append(minusOperator)
            numerator.append(left)
            numerator.append(multiplyOperator)
            numerator.append(right.differentiate(variable))
            
            denominator = PowerBlock()
            denominator.append(right)
            denominator.append(NumberElement(2))
            
            derivative = QuotientBlock()
            derivative.append(numerator)
            derivative.append(denominator)
            #raise Exception("not implemented yet")
        else:
            m_inv = FunctionElement("1/x","1/x","-(1/x^2)",'x')
            
            derivative.append(left)
            derivative.append(multiplyOperator)
            derivative.append(Derivative.ChainRule(m_inv, right, variable))
            #raise Exception("not implemented yet")
        return derivative
class PowerOperator(OperatorElement):
    def __init__(self):
        self.sign = "^"
        
    def differentiate(self, base, exponent, variable):
        base_var = expDependOnVariable(base, variable)
        exponent_var = expDependOnVariable(exponent, variable)
        derivative = ExpressionBlock()
        if (base_var and exponent_var):#x^x
            base_e = VariableElement('e')
            exp_factor = FunctionBlock()
            exp_factor.append(Tools.IsFunction('ln'))
            exp_factor.append(ExpressionBlock(base))
            
            new_exponent = ExpressionBlock()
            new_exponent.append(exp_factor)
            new_exponent.append(multiplyOperator)
            new_exponent.append(exponent)
            
            derivative.append(new_exponent.differentiate(variable))
            derivative.append(multiplyOperator)
            derivative.append(base)
            derivative.append(powerOperator)
            derivative.append(exponent)
          #  return powerOperator.differentiate(base_e,new_exponent,variable)
            #raise Exception("TO DO")
        elif (base_var and not exponent_var): #f(x)^k
            #factor = ExpressionBlock()
            #factor.append(exponent_var)
            
            derivative = ExpressionBlock()
            #derivative.append(factor)
            derivative.append(exponent)         #k
            derivative.append(multiplyOperator) #*
            derivative.append(base)             #f(x)
            derivative.append(powerOperator)    #^
            
            new_exponent = ExpressionBlock()    #(
            new_exponent.append(exponent)       #k
            new_exponent.append(minusOperator)  #-
            new_exponent.append(NumberElement(1))#1
            
            derivative.append(new_exponent) #)
            
            derivative.append(multiplyOperator) #*
            derivative.append(base.differentiate(variable)) #f'(x)
            
        elif (not base_var and exponent_var): #k^x
            base_e = False
            if (type(base) == VariableElement):
                if (base.variable == 'e'):
                    derivative = Derivative.ChainRule(Tools.IsFunction('e^x'), exponent, variable)
                    base_e = True
                    
            if not base_e:
                exp_factor = FunctionBlock()
                exp_factor.append(Tools.IsFunction('ln'))
                exp_factor.append(ExpressionBlock(base))
                
                
                new_exponent = ExpressionBlock()
                new_exponent.append(exp_factor)
                new_exponent.append(multiplyOperator)
                new_exponent.append(exponent)
                
               # exp_func = Tools.IsFunction('e^x')
                
               # derivative = Derivative.ChainRule(exp_func, new_exponent, variable)
               
                #derivative.append(exp_factor)
                #derivative.append(multiplyOperator)
                #derivative.append(exponent.differentiate(variable))
                derivative.append(new_exponent.differentiate(variable))
                derivative.append(multiplyOperator)
                derivative.append(base)
                derivative.append(powerOperator)
                derivative.append(exponent)
            
            #raise Exception("TO DO")
        else: #n^m
            derivative.append(base)
            derivative.append(powerOperator)
            derivative.append(exponent)
            
        return derivative
minusOperator = MinusOperator()
plusOperator = PlusOperator()
multiplyOperator = MultiplyOperator()
divideOperator = DivideOperator()
powerOperator = PowerOperator()
allOperators = [
    minusOperator,
    plusOperator,
    multiplyOperator,
    divideOperator,
    powerOperator
]
    
def expDependOnVariable(exp, variable):
    if type(exp) == NumberElement:
        return False
    elif type(exp) == VariableElement:
        if variable == None:
            return True
        return variable.variable == exp.variable
    elif isinstance(exp,OperatorElement):
        return False
    if exp == None:
        return False
    for expPart in exp.expressions:
        if IsBlock(expPart):
            if expDependOnVariable(expPart, variable):
                return True
        if (expPart == variable)or (variable == None and type(expPart)==VariableElement):
            return True
    return False

def expDependOnFunction(exp, function):
    if type(exp) == NumberElement:
        return False
    
    elif (type(exp)) == VariableElement:
        return False
    
    elif isinstance(exp, OperatorElement):
        return False
    
    if (type(exp) == FunctionBlock and function == None) or (type(exp) == FunctionElement and (exp==function or function == None)):
        return True
    
    
    for expPart in exp.expressions:
        if (IsBlock(expPart)):
            if (expDependOnFunction(expPart, function)):
                return True
        if (expPart == function) or (function == None and type(expPart) == FunctionElement):
            return True
        
    return False

def replaceBlockWithExpr(block, block_var, expr, functionBlockType):
    
    #new_block = FunctionBlock() if functionBlock else ExpressionBlock()
    new_block = (functionBlockType)()
       
    for el in block.expressions:
        if IsBlock(el):    
            #funcBlock = isinstance(el,FunctionBlock)
            new_block.append(replaceBlockWithExpr(el,block_var,expr,type(el)))
        elif type(el) == VariableElement:
            if el.variable == block_var:
                new_block.append(expr)
            else:
                new_block.append(el)
        else:
            new_block.append(el)
            
    return new_block

def calculateNumbers(block):
    from ParseInput import blockToStr

    return __cNumbers(block,blockToStr, True)

def __cNumbers(block,blockToStr, isArgument):
    if canEvaluate(block):
   #     print(blockToStr(block,""))
        if (isArgument):
            string = blockToStr(block,"")
            string = string.replace("^","**")

            return ExpressionBlock(NumberElement(eval(string)))
        
        else:
            return NumberElement(eval(blockToStr(block,"")))
    if not IsBlock(block) and type(block)!=Expression:
        return block
    
    new_block = type(block)()
    
    i_a = False
    if (len(block.expressions)==2):
        if type(block.expressions[0]) == FunctionElement and type(block.expressions[1]) == ExpressionBlock:
            i_a = True
    for block_element in block.expressions:
        #if can_evaluate
        new_block.append(__cNumbers(block_element,blockToStr, i_a))
        
    return new_block

def canEvaluate(block):
    return not isinstance(block,OperatorElement) and not expDependOnFunction(block, None) and not expDependOnVariable(block, None)


def removeNeutralElements(block):
    new_block = type(block)()
    if IsBlock(block):
        i = 0
        while i<len(block.expressions):
            el = block.expressions[i]
            if IsBlock(el):
                new_block.append(removeNeutralElements(el))
            else:
                preElement = None
                aftElement = None
                if i>0:
                    preElement = block.expressions[i-1]
                if i< len(block.expressions)-1:
                    aftElement = block.expressions[i+1]
                   
                removeElement = False 
                before = False
                if type(el) == NumberElement:
                    if el.value == 1:
                        if preElement == multiplyOperator:
                            removeElement = True
                            before = True
                        elif preElement == divideOperator:
                            removeElement = True
                            before = True
                        elif preElement  == powerOperator:
                            removeElement = True
                            before = True
                        
                        if aftElement == multiplyOperator:
                            removeElement = True
                if removeElement:
                    if before:
                        new_block.expressions.pop(len(new_block.expressions)-1)
                    else:
                        i += 1
                else:
                    new_block.append(el)
                
            i += 1
        return new_block
                
def removeOuterBlocks(exp,functionArgument=False):
   # if not IsBlock(exp):
    #    k = ExpressionBlock()
     #   k.expressions.append(exp)
      #  return k
    if (len(exp.expressions)==1):
        b = exp.expressions[0]
        if IsBlock(b):
            return removeOuterBlocks(b)
        else:
            if functionArgument:
                return exp
            else:
                #print("only element in block ")
                return b
    #return exp
    newExp = type(exp)()
    f_a = False
    if (len(exp.expressions) == 2):
        if type(exp.expressions[0]) == FunctionElement and type(exp.expressions[1]) == ExpressionBlock:
            f_a = True

    pow_quot_block = type(exp) == QuotientBlock or type(exp) == PowerBlock
    
    for el in exp.expressions:
        if IsBlock(el):
            if f_a:
                newExp.append(ExpressionBlock(removeOuterBlocks(el,functionArgument=f_a)))
            elif pow_quot_block:
                newExp.append(ExpressionBlock(removeOuterBlocks(el,functionArgument=f_a)))
            else:
                newExp.append(removeOuterBlocks(el,functionArgument=f_a))
        else:
            newExp.append(el)
            
    return newExp
    """  else:
        summands = [ExpressionBlock()]
        for s in exp.expressions:
            if s == plusOperator:
                summands.append(ExpressionBlock())
            else:
                summands[len(summands)-1].append(s)
        
        newSumms = []
        for s in summands:
            if (len(s.expressions) == 1):
                b = s.expressions[0]
                newSumms.append(removeOuterBlocks(b))
        exp.expressions = []
        for k in range(len(newSumms)):
            exp.expressions.append(newSumms[k])
            if k != len(newSumms)-1:
                exp.expressions.append(plusOperator)
        return exp"""

def IsBlock(k):
    return type(k) == ExpressionBlock or type(k) == FunctionBlock or type(k) == PowerBlock or type(k) == QuotientBlock
   
def hasBlockType(exp, blockType):
    if type(exp) == blockType:
        return exp
    elif not (IsBlock(exp)) and not type(exp) == Expression:
        return False
    for e in exp.expressions:
        h = hasBlockType(e,blockType)
        if h != False:
            return h
    return False 
    
if __name__ == "__main__":
    import Main
    Main.Main()