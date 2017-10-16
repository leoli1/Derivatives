'''
Created on 26.09.2017

@author: Leonard
'''
import Expression

def differentiate(expression, variable, makeNice=True):
    block = Expression.ExpressionBlock()
    for el in expression.expressions:
        block.append(el)
    
    #return block.differentiate(variable)
    derivative = block.differentiate(variable)
    if (makeNice):
        derivative = Expression.removeOuterBlocks(derivative)
        derivative = Expression.removeOuterBlocks(derivative)
        derivative = Expression.calculateNumbers(derivative)
        derivative = Expression.removeNeutralElements(derivative) # TODO
    return derivative

        
def ChainRule(outer_function, inner_block, variable):
    deriv = Expression.ExpressionBlock()
    deriv.append(inner_block.differentiate(variable))
    deriv.append(Expression.multiplyOperator)
    deriv.append(outer_function.differentiate(inner_block))
   # deriv.append(inner_block)
    
    return deriv

if __name__ == "__main__":
    import Main
    Main.Main()