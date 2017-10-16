# -*- coding: utf-8 -*-
'''
Created on 25.09.2017

@author: Leonard
'''
#from Expression import Expression,ExpressionBlock,NumberElement,VariableElement
#from OperatorElement import multiplyOperator
#from PredefinedObjects import functions
import Expression
import Tools
import PredefinedObjects
import warnings

STARTBLOCK = ['(','[']
ENDBLOCK = [')',']']

expression = Expression.Expression()

def ParseInput(input):
    global expression
    PredefinedObjects.SetupObjects()
    expression.expressions = ParseString(input).expressions
    return expression
        
def ParseString(s):
    exp = Expression.ExpressionBlock()
    cur_block,i = ParseBlock(s,0,0)
    for el in cur_block.expressions:
        exp.expressions.append(el)

        
    exp.expressions = PackFunctions(exp)
    exp.expressions = PackPowerBlocks(exp)
    exp.expressions = PackQuotientBlocks(exp)

    exp.expressions = AddMultiplyOperators(exp)

    return exp
def ParseBlock(input, start_index, depth):
    global expression
    cur_block = Expression.ExpressionBlock()
    i = start_index
    var_last = False
    while i<len(input):
        char = input[i]
        if char in STARTBLOCK:
            block,endIndex = ParseBlock(input,i+1,depth+1)
            cur_block.append(block)
            i = endIndex
            var_last = False
        elif char in ENDBLOCK:
            if (depth == 0):
                warnings.warn("Klammern Falsch")
            return cur_block,i
        
        elif (Tools.IsNumber(char)):
            number,endIndex = getNumber(input,i)
            i = endIndex-1
            if (var_last):
                cur_block.append(Expression.multiplyOperator)
            cur_block.append(Expression.NumberElement(number))
            if (i<=len(input)-2):
                if (Tools.IsChar(input[i+1])):
                    cur_block.append(Expression.multiplyOperator)
                    
            var_last = False
        elif (Tools.IsOperator(char)):
            op = Tools.IsOperator(char)
            cur_block.append(op)
            var_last = False
        elif (Tools.IsChar(char)):
            word,endIndex = getWord(input,i)
            
            endVariables = endIndex+1
            func = None
            
            vars = False
            
            # testet, ob die char-kette einen funktionennamen enthält
            for f in PredefinedObjects.functions:
                if f.name in word:
                    ind = word.index(f.name)
                    if func == None or len(f.name) >len(func.name):
                        endVariables = ind
                        func = f
                    #break
                
            if (func == None or endVariables != i): # fügt alle variablen vor der function mit multiply operator hinzu
                for k in range(endVariables-i):
                    vars = True
                    
                    var = word[k]
                    
                    variableElement = None
                    for variableEl in expression.variables:
                        if variableEl.variable == var:
                            variableElement = variableEl
                            break
                    if (variableElement == None):
                        variableElement = Expression.VariableElement(var)
                        expression.variables.append(variableElement)
                        
                        
                    cur_block.append(variableElement)
                    if (k!=endVariables-i-1):
                        cur_block.append(Expression.multiplyOperator)
            var_last = vars   
            if (func != None and vars): # und ggf. auch die function
                cur_block.append(Expression.multiplyOperator)
                cur_block.append(func)
            elif (func != None):
                cur_block.append(func)
            """ if (func):
                cur_block.append(func)
            else: # produkt von variablen
                for k in range(len(word)):
                    var = word[k]
                    cur_block.append(VariableElement(var))
                    if (k!=(len(word)-1)):
                        cur_block.append(multiplyOperator)"""
            i = endIndex
        i += 1
        
    return cur_block,i
        
def getNumber(input, i):
    num = 0
    isnum = True
    iscomma = False
    preComma = []
    comma = []
    index = i
    while isnum and index<len(input):
        char = input[index]
        if (Tools.IsNumber(char)):
            n = int(char)
            if (iscomma):
                comma.append(n)
            else:
                preComma.append(n)
        elif char == '.' or char == ',':
            if (iscomma):
                print("ERROR")
                raise Exception()
            iscomma = True
        else:
            isnum = False
        index += 1
    if (index==len(input)) and isnum:
        index += 1
    power = len(preComma)-1
    for k in preComma:
        num += k*(10**power)
        power -= 1
    for k in comma:
        num += k*(10**power)
        power -= 1
    return num,index-1

def getWord(input,i):
    index = i
    word = ""
    isChar = True
    while isChar and index<len(input):
        if Tools.IsChar(input[index]):
            word += input[index]
            index += 1
        else:
            isChar = False
  #  if (index==len(input)) and isChar:
   #     index += 1
    return word,index-1
    
def PackFunctions(expression):
    '''
        Wandelt Teile der Art <FunctionElement> <ExpressionBlock> in einen FunctionBlock um
    '''
    new_expressions = []
    i = 0
    while i<len(expression.expressions):
    #for el in expression.expressions:
        el = expression.expressions[i]
        #if type(el) == Expression.ExpressionBlock:
        if Expression.IsBlock(el):
            block = (type(el))()
            block.expressions = PackFunctions(el)
            new_expressions.append(block)
        elif type(el) == Expression.FunctionElement:
            new_block = Expression.FunctionBlock()
            new_block.append(el)
            if (i == len(expression.expressions)-1):
                raise Exception("KEIN FUNC ARGUMENT")
            new_block.append(expression.expressions[i+1])
            new_expressions.append(new_block)
            i+=1
        else:
            new_expressions.append(el)
        i+=1
    return new_expressions

def PackPowerBlocks(expression):
    new_expressions = []
    i = 0
    while i<len(expression.expressions):
        el = expression.expressions[i]
        if Expression.IsBlock(el):
            block = (type(el))()
            block.expressions = PackPowerBlocks(el)
            new_expressions.append(block)
        elif el == Expression.powerOperator:
            if (i==0):
                raise Exception("Error: No base before power operator")
            elif (i == len(expression.expressions)-1):
                raise Exception("Error: No exponent after power operator")
            powerBlock = Expression.PowerBlock()
            
      #      before_el = expression.expressions[i-1]
            before_el = new_expressions[len(new_expressions)-1]
            after_el = expression.expressions[i+1]
            
            exp = after_el
            
            if isinstance(after_el, Expression.OperatorElement):
                exp = Expression.ExpressionBlock(after_el,expression.expressions[i+2])
                i += 1
            
            new_expressions.pop(len(new_expressions)-1)
            
            powerBlock.append(before_el)
            powerBlock.append(exp)
            new_expressions.append(powerBlock)
            i += 1
        else:
            new_expressions.append(el)
        i += 1
    return new_expressions;  
def PackQuotientBlocks(expression):
    i = 0
    new_expressions = []
    while i<len(expression.expressions):
        
        el = expression.expressions[i]
        if Expression.IsBlock(el):
            
            block = (type(el))()
            block.expressions = PackQuotientBlocks(el)
            new_expressions.append(block)
        elif el == Expression.divideOperator:
            if (i==0):
                raise Exception("Error: No numerator before divide operator")
            elif (i == len(expression.expressions)-1):
                raise Exception("Error: No denominator after divide operator")
            quotientBlock = Expression.QuotientBlock()
           # before_el = expression.expressions[i-1]
            before_el = new_expressions[len(new_expressions)-1]
            after_el = expression.expressions[i+1]
            denom = Expression.ExpressionBlock(after_el)
            
            
            if isinstance(after_el, Expression.OperatorElement):
                denom = Expression.ExpressionBlock(after_el,expression.expressions[i+2])
                i += 1
            
            new_expressions.pop(len(new_expressions)-1)
            
            quotientBlock.append(before_el)
            quotientBlock.append(denom)
            new_expressions.append(quotientBlock)
            i += 1
        else:
            new_expressions.append(el)
        i += 1
    return new_expressions

def AddMultiplyOperators(expression):
    i = 0
    new_expressions = []
    while i<len(expression.expressions):
        
        el = expression.expressions[i]
        if not isinstance(el, Expression.OperatorElement) and (type(expression) == Expression.ExpressionBlock or type(expression) == Expression.Expression):
            before = None
            if (i!=0):
                before = new_expressions[len(new_expressions)-1]
            if before!= None:
                if not isinstance(before, Expression.OperatorElement) and not isinstance(before, Expression.FunctionElement):
                    new_expressions.append(Expression.multiplyOperator)
            
        if (Expression.IsBlock(el)):
            block = (type(el))()
            block.expressions = AddMultiplyOperators(el)

            new_expressions.append(block)
        else:
            new_expressions.append(el)
        
        if not isinstance(el, Expression.OperatorElement) and (type(expression) == Expression.ExpressionBlock or type(expression) == Expression.Expression):
            after = None
            if (i<len(expression.expressions)-1):
                after = expression.expressions[i+1]
            if after!= None:
                if not isinstance(after, Expression.OperatorElement) and not isinstance(el, Expression.FunctionElement):
                    new_expressions.append(Expression.multiplyOperator)
                    
        i += 1
    return new_expressions

def blockToStr(block, string):
    if not (Expression.IsBlock(block)) and not type(block) == Expression.Expression:
        return string+str(block)
    if type(block) == Expression.PowerBlock:
        pars = type(block.expressions[1]) == Expression.ExpressionBlock#Expression.IsBlock(block.expressions[1]) # wenn der nenner ein block ist, klammern setzen
        if pars:
            return blockToStr(block.expressions[0], string)+"^("+blockToStr(block.expressions[1], "")+")"
        else:
            return blockToStr(block.expressions[0], string)+"^"+blockToStr(block.expressions[1], "")
    elif type(block) == Expression.QuotientBlock:
        pars = type(block.expressions[1]) == Expression.ExpressionBlock#Expression.IsBlock(block.expressions[1]) # wenn der nenner ein block ist, klammern setzen
        if pars:
            return blockToStr(block.expressions[0], string)+"/("+blockToStr(block.expressions[1], "")+")"
        else:
            return blockToStr(block.expressions[0], string)+"/"+blockToStr(block.expressions[1], "")
    for el in block.expressions:
        if Expression.IsBlock(el):
            string += "("
            string = blockToStr(el, string)
            string += ")"
        else:
            string += str(el)
    return string
if __name__ == "__main__":
    import Main
    Main.Main()