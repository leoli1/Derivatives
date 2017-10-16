'''
Created on 25.09.2017

@author: Leonard
'''
#from ParseInput import ParseInput
#from Derivative import differentiate
#from Tools import IsBlock
import ParseInput
import Derivative
import Expression
import sys


def Main():
    while True:
        usrInput = None
        if sys.version_info < (3,0):
            usrInput = raw_input("Input: ").lower()
        else:
            usrInput = input("Input: ").lower()
            
        if (usrInput == ""):
            break

        exp = ParseInput.ParseInput(usrInput)
        
        print("--------------")
        variable = None
        for var in exp.variables:
            if var.variable == 'x':
                variable = var
                break
        if variable == None:
            if len(exp.variables) >0:
                variable = exp.variables[0]
            else:
                variable = Expression.VariableElement('x')
                
        print("f("+str(variable)+") = "+ParseInput.blockToStr(exp,""))
        derivative = Derivative.differentiate(exp,variable,makeNice=True)
        print("f'("+str(variable)+") = "+ ParseInput.blockToStr(derivative, ""))

    
    
        
def printBlock(block, indents):
    for el in block.expressions:
        if Expression.IsBlock(el):
            #print(type(el))
            printBlock(el,indents+2)
            continue
        print(indents*'-'+str(el))
        
        
if __name__ == '__main__':
    Main()