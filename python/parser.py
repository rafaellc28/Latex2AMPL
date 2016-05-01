#!/usr/bin/python -tt

import sys

from lexer import tokens
import ply.yacc as yacc
from LinearProgram import *

# Parsing rules

precedence = (
    ('left', 'COMMA', 'DOTS', 'FOR', 'BACKSLASHES'),
    ('left', 'ID'),
    ('left', 'NUMBER'),
    ('left', 'LBRACE', 'RBRACE'),
    ('left', 'OR', 'AND', 'NOT'),
    ('left', 'FORALL', 'EXISTS'),
    ('left', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ', 'COLON'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION', 'INTER', 'CROSS'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'PIPE', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'COS', 'ARCTAN', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'UPLUS', 'UMINUS'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'UNDERLINE', 'CARET'),
    ('left', 'INTEGERSET', 'REALSET', 'NATURALSET')
    )

def p_LinearProgram(t):
    '''LP : Objective
          | Objective Constraints
          | Objective BACKSLASHES Constraints'''

    if len(t) > 3:
        t[0] = LinearProgram(t[1], t[3])
    elif len(t) > 2:
        t[0] = LinearProgram(t[1], t[2])
    else:
        t[0] = LinearProgram(t[1], None)

def p_LinearProgram_error(t):
    'LP : error BACKSLASHES'
    sys.stderr.write( "Syntax error in LinearProgram")

def p_Objective(t):
    '''Objective : MAXIMIZE LinearExpression
                 | MINIMIZE LinearExpression
                 | MAXIMIZE LinearExpression COMMA IndexingExpression
                 | MINIMIZE LinearExpression COMMA IndexingExpression'''

    if len(t) > 3:
      if t[1] == "maximize":
        t[0] = Objective(t[2], Objective.MAXIMIZE, t[4])
      else:
        t[0] = Objective(t[2], Objective.MINIMIZE, t[4])
    else:
      if t[1] == "maximize":
        t[0] = Objective(t[2])
      else:
        t[0] = Objective(t[2], Objective.MINIMIZE)

def p_Constraints(t):
    '''Constraints : SUBJECTTO ConstraintList'''
    t[0] = Constraints(t[2])

def p_ConstraintList(t):
    '''ConstraintList : ConstraintList BACKSLASHES Constraint
                      | ConstraintList BACKSLASHES
                      | Constraint'''
    if len(t) > 3:
        t[0] = t[1] + [t[3]]
    elif len(t) > 2:
        t[0] = t[1] + [t[2]]
    else:
        t[0] = [t[1]]

def p_ConstraintList_error(t):
    'ConstraintList : error BACKSLASHES'
    sys.stderr.write( "Syntax error in ConstraintList.")

def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression COMMA IndexingExpression
                  | ConstraintExpression'''
    if len(t) > 3:
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])

def p_Constraint_error(t):
    '''Constraint : error FOR
                  | error COMMA'''
    sys.stderr.write( "Syntax error in Constraint.")

def p_ConstraintExpression(t):
    '''ConstraintExpression : LinearExpression EQ LinearExpression
                           |  LinearExpression LE LinearExpression
                           |  LinearExpression GE LinearExpression
                           |  LBRACKET NumericExpression RBRACKET LE LinearExpression LE NumericExpression
                           |  LBRACKET NumericExpression RBRACKET GE LinearExpression GE NumericExpression'''
    
    if len(t) > 4:
        if t[4] == "\\leq":
            t[0] = ConstraintExpression3(t[5], t[2], t[7], ConstraintExpression.LE)
        elif t[4] == "\\geq":
            t[0] = ConstraintExpression3(t[5], t[2], t[7], ConstraintExpression.GE)
    elif t[2] == "=":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.EQ)
    elif t[2] == "\\leq":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.LE)
    elif t[2] == "\\geq":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.GE)

def p_ConstraintExpression_error(t):
    '''ConstraintExpression : error EQ
                            | error LE
                            | error GE'''
    sys.stderr.write( "Syntax error in ConstraintExpression")

def p_LinearExpression(t):
    '''LinearExpression : Variable
                        | NUMBER
                        | PLUS LinearExpression %prec UPLUS
                        | MINUS LinearExpression %prec UMINUS
                        | LPAREN LinearExpression RPAREN'''

    if len(t) > 3:
        t[0] = LinearExpressionBetweenParenthesis(t[2])
    elif len(t) > 2:
        if t[1] == "\+":
            t[0] = PlusLinearExpression(t[2])
        else:
            t[0] = MinusLinearExpression(t[2])
    else:
        t[0] = ValuedLinearExpression(t[1])

def p_LinearExpression_error(t):
    'LinearExpression : LPAREN error RPAREN'
    sys.stderr.write( "Syntax error in LinearExpression.")

def p_LinearExpression_binop(t):
    '''LinearExpression : LinearExpression PLUS LinearExpression
                        | LinearExpression MINUS LinearExpression
                        | LBRACKET NumericExpression RBRACKET TIMES LinearExpression
                        | LinearExpression TIMES NumericExpression
                        | LinearExpression DIVIDE NumericExpression'''

    if t[2] == "+":
        op = LinearExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = LinearExpressionWithArithmeticOperation.MINUS
    elif t[2] == "*":
        op = LinearExpressionWithArithmeticOperation.TIMES
    elif t[2] == "/":
        op = LinearExpressionWithArithmeticOperation.DIV

    t[0] = LinearExpressionWithArithmeticOperation(op, t[1], t[3])

def p_LinearExpression_binop_error(t):
    '''LinearExpression : error PLUS
                        | error MINUS
                        | error TIMES
                        | error DIVIDE'''
    sys.stderr.write( "Syntax error in LinearExpression_binop.")

def p_IteratedLinearExpression(t):
    '''LinearExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE LinearExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE LinearExpression'''
    if len(t) > 7:
        t[0] = IteratedLinearExpression(t[10], t[4], t[8])
    else:
        t[0] = IteratedLinearExpression(t[6], t[4])

def p_IteratedLinearExpression_error(t):
    'LinearExpression : SUM UNDERLINE LBRACE error RBRACE'
    sys.stderr.write( "Syntax error in IteratedLinearExpression.")


def p_NumericExpression_binop(t):
    '''NumericExpression : NumericExpression PLUS NumericExpression
                         | NumericExpression MINUS NumericExpression
                         | NumericExpression TIMES NumericExpression
                         | NumericExpression DIVIDE NumericExpression
                         | NumericExpression MOD NumericExpression
                         | NumericExpression CARET NumericExpression'''

    if t[2] == "+":
        op = NumericExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = NumericExpressionWithArithmeticOperation.MINUS
    elif t[2] == "*":
        op = NumericExpressionWithArithmeticOperation.TIMES
    elif t[2] == "/":
        op = NumericExpressionWithArithmeticOperation.DIV
    elif t[2] == "%":
        op = NumericExpressionWithArithmeticOperation.MOD
    elif t[2] == "^":
        op = NumericExpressionWithArithmeticOperation.POW

    t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

def p_NumericExpression_binop_error(t):
    '''NumericExpression : error PLUS
                         | error MINUS
                         | error TIMES
                         | error DIVIDE
                         | error MOD
                         | error CARET'''
    sys.stderr.write( "Syntax error in NumericExpression_binop.")

def p_IteratedNumericExpression(t):
    '''NumericExpression : NumericOperator UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | NumericOperator UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression'''

    if t[1] == "\\sum":
        op = IteratedNumericExpression.SUM
    elif t[1] == "\\prod":
        op = IteratedNumericExpression.PROD
    elif t[1] == "\\max":
        op = IteratedNumericExpression.MAX
    elif t[1] == "\\min":
        op = IteratedNumericExpression.MIN

    if len(t) > 7:
        t[0] = IteratedNumericExpression(op, t[10], t[4], t[8])
    else:
        t[0] = IteratedNumericExpression(op, t[6], t[4])

def p_IteratedNumericExpression_error(t):
    'NumericExpression : NumericOperator UNDERLINE LBRACE error RBRACE'
    sys.stderr.write( "Syntax error in IteratedNumericExpression.")


def p_NumericExpression(t):
    '''NumericExpression : MINUS NumericExpression %prec UMINUS
                         | PLUS NumericExpression %prec UPLUS
                         | LPAREN NumericExpression RPAREN
                         | Variable
                         | NUMBER'''

    if len(t) > 3:
        t[0] = NumericExpressionBetweenParenthesis(t[2])
    elif t[1] == "+":
        t[0] = t[2]
    elif t[1] == "-":
        t[0] = MinusNumericExpression(t[2])
    else:
        t[0] = ValuedNumericExpression(t[1])

def p_NumericExpression_error(t):
    'NumericExpression : LPAREN error RPAREN'
    sys.stderr.write( "Syntax error in NumericExpression.")


def p_NumericOperator(t):
    '''NumericOperator : SUM
                       | PROD
                       | MAX
                       | MIN'''
    t[0] = t[1]

def p_FunctionNumericExpression(t):
    '''NumericExpression : SQRT LBRACE NumericExpression RBRACE
                         | LFLOOR NumericExpression RFLOOR
                         | LCEIL NumericExpression RCEIL
                         | PIPE NumericExpression PIPE
                         | MAX LPAREN NumericExpression RPAREN
                         | MIN LPAREN NumericExpression RPAREN
                         | SIN LPAREN NumericExpression RPAREN
                         | COS LPAREN NumericExpression RPAREN
                         | LOG LPAREN NumericExpression RPAREN
                         | LN LPAREN NumericExpression RPAREN
                         | EXP LPAREN NumericExpression RPAREN
                         | ARCTAN LPAREN NumericExpression RPAREN'''

    if t[1] == "\\sqrt":
        op = NumericExpressionWithFunction.SQRT
    elif t[1] == "\\lfloor":
        op = NumericExpressionWithFunction.FLOOR
    elif t[1] == "\\lceil":
        op = NumericExpressionWithFunction.CEIL
    elif t[1] == "\\vert":
        op = NumericExpressionWithFunction.ABS
    elif t[1] == "\\max":
        op = NumericExpressionWithFunction.MAX
    elif t[1] == "\\min":
        op = NumericExpressionWithFunction.MIN
    elif t[1] == "\\sin":
        op = NumericExpressionWithFunction.SIN
    elif t[1] == "\\cos":
        op = NumericExpressionWithFunction.COS
    elif t[1] == "\\log":
        op = NumericExpressionWithFunction.LOG10
    elif t[1] == "\\ln":
        op = NumericExpressionWithFunction.LOG
    elif t[1] == "\\exp":
        op = NumericExpressionWithFunction.EXP
    elif t[1] == "\\arctan":
        op = NumericExpressionWithFunction.ARCTAN

    if len(t) > 4:
        t[0] = NumericExpressionWithFunction(op, t[3])
    else:
        t[0] = NumericExpressionWithFunction(op, t[2])

def p_FunctionNumericExpression_error(t):
    '''NumericExpression : SQRT LBRACE error RBRACE
                         | LFLOOR error RFLOOR
                         | LCEIL error RCEIL'''
    sys.stderr.write( "Syntax error in FunctionNumericExpression.")

def p_IndexingExpression(t):
    '''IndexingExpression : EntryIndexingExpression
                          | IndexingExpression COLON LogicalExpression
                          | IndexingExpression COMMA EntryIndexingExpression
                          | IndexingExpression COMMA BACKSLASHES EntryIndexingExpression'''

    if len(t) > 4:
        t[0] = t[1].add(t[4])
    elif len(t) > 3:
        if t[2] == ":":
            t[0] = t[1].setLogicalExpression(t[3])
        else:
            t[0] = t[1].add(t[3])
    else:
        t[0] = IndexingExpression([t[1]])

def p_IndexingExpression_error(t):
    'IndexingExpression : error COMMA'
    sys.stderr.write( "Syntax error in IndexingExpression.")

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | TupleList IN SetExpression
                               | Variable IN SetExpression'''
    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_EntryIndexingExpressionWithSet_error(t):
    '''EntryIndexingExpression : error IN
                               | error COLON'''
    sys.stderr.write( "Syntax error in EntryIndexingExpressionWithSet.")

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Variable EQ NUMBER
                               | Variable EQ Variable
                               | Variable EQ Range
                               | Variable NEQ NumericExpression
                               | Variable LE NumericExpression
                               | Variable GE NumericExpression
                               | Variable LT NumericExpression
                               | Variable GT NumericExpression'''
    if t[2] == "=":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.EQ, t[1], t[3])
    elif t[2] == "\\neq":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.NEQ, t[1], t[3])
    elif t[2] == "\\leq":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LE, t[1], t[3])
    elif t[2] == "\\geq":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GE, t[1], t[3])
    elif t[2] == "<":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LT, t[1], t[3])
    elif t[2] == ">":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GT, t[1], t[3])

def p_EntryIndexingExpressionEq_error(t):
    '''EntryIndexingExpression : error EQ
                               | error NEQ
                               | error LE
                               | error GE
                               | error LT
                               | error GT'''
    sys.stderr.write( "Syntax error in EntryIndexingExpressionEq.")

def p_LogicalExpression(t):
    '''LogicalExpression : EntryLogicalExpression
                         | LogicalExpression OR EntryLogicalExpression
                         | LogicalExpression AND EntryLogicalExpression'''

    if len(t) > 3:
      if t[2] == "and":
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])
    else:
        t[0] = LogicalExpression([t[1]])

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NOT EntryLogicalExpression
                              | LPAREN LogicalExpression RPAREN'''

    if t[1] == "not":
        t[0] = EntryLogicalExpressionNot(t[2])
    else:
        t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

def p_EntryRelationalLogicalExpression(t):
    '''EntryLogicalExpression : NumericExpression LT NumericExpression
                              | NumericExpression LE NumericExpression
                              | NumericExpression EQ NumericExpression
                              | NumericExpression GE NumericExpression
                              | NumericExpression NEQ NumericExpression'''

    if t[2] == "<":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LT, t[1], t[3])
    elif t[2] == "\\leq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LE, t[1], t[3])
    elif t[2] == "=":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.EQ, t[1], t[3])
    elif t[2] == "\\geq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GE, t[1], t[3])
    elif t[2] == "\\neq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.NEQ, t[1], t[3])

def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList IN SetExpression
                              | TupleList IN SetExpression
                              | Variable IN SetExpression
                              | ValueList NOTIN SetExpression
                              | TupleList NOTIN SetExpression
                              | Variable NOTIN SetExpression
                              | SetExpression SUBSET SetExpression
                              | SetExpression NOTSUBSET SetExpression'''

    if t[2] == "\\in":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])
    elif t[2] == "\\notin":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.NOTIN, t[1], t[3])
    elif t[2] == "subset":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])
    elif t[2] == "notsubset":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.NOTSUBSET, t[1], t[3])

def p_EntryIteratedLogicalExpression(t):
    '''EntryLogicalExpression : FORALL LBRACE IndexingExpression RBRACE LogicalExpression
                              | EXISTS LBRACE IndexingExpression RBRACE LogicalExpression'''

    if t[1] == "\\forall":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])
    elif t[1] == "\\exists":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

def p_SetExpressionWithOperation(t):
    '''SetExpression : SetExpression DIFF SetExpression
                     | SetExpression SYMDIFF SetExpression
                     | SetExpression UNION SetExpression
                     | SetExpression INTER SetExpression
                     | SetExpression CROSS SetExpression'''

    if t[2] == "DIFF":
        op = SetExpressionWithOperation.DIFF
    elif t[2] == "SYMDIFF":
        op = SetExpressionWithOperation.SYMDIFF
    elif t[2] == "UNION":
        op = SetExpressionWithOperation.UNION
    elif t[2] == "INTER":
        op = SetExpressionWithOperation.INTER
    elif t[2] == "CROSS":
        op = SetExpressionWithOperation.CROSS

    t[0] = SetExpressionWithOperation(op, t[1], t[3])

def p_SetExpressionWithOperation_error(t):
    '''SetExpression : error DIFF
                     | error SYMDIFF
                     | error UNION
                     | error INTER
                     | error CROSS'''
    sys.stderr.write( "Syntax error in SetExpressionWithOperation.")

def p_SetExpressionWithValue(t):
    '''SetExpression : LBRACE ValueList RBRACE
                     | LBRACE Range RBRACE
                     | Range
                     | Variable
                     | NATURALSET
                     | INTEGERSET
                     | REALSET'''

    if len(t) > 2:
        t[0] = SetExpressionWithValue(t[2])
    else:
        t[0] = SetExpressionWithValue(t[1])

def p_SetExpressionWithValue_error(t):
    '''SetExpression : LBRACE error RBRACE'''
    sys.stderr.write( "Syntax error in SetExpressionWithValue.")

def p_SetExpressionWithIndices(t):
    '''SetExpression : Variable LPAREN ValueList RPAREN
                     | Variable LBRACE ValueList RBRACE
                     | Variable LBRACE Variable RBRACE
                     | Variable LPAREN Variable RPAREN'''
    
    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_SetExpressionWithIndices_error(t):
    '''SetExpression : error LBRACE
                     | error LPAREN'''
    sys.stderr.write( "Syntax error in SetExpressionWithIndices.")

def p_Range(t):
    '''Range : Variable DOTS NumericExpression
             | NUMBER DOTS NumericExpression'''

    if len(t) > 4:
        t[0] = Range(t[1], t[5])
    elif len(t) > 2:
        t[0] = Range(t[1], t[3])
    else:
        t[0] = Value(t[1])

def p_Range_error(t):
    '''Range : error DOTS
             | error COMMA'''
    sys.stderr.write( "Syntax error in Range.")

def p_Variable(t):
    '''Variable : ID UNDERLINE LBRACE ValueList RBRACE
                | ID UNDERLINE LBRACE Variable RBRACE
                | ID UNDERLINE LBRACE NUMBER RBRACE
                | ID'''

    if len(t) > 2:
        if isinstance(t[4], ValueList):
          t[0] = Variable(ID(t[1]), t[4].getValues())
        else:
          t[0] = Variable(ID(t[1]), t[4])
    else:
        t[0] = Variable(ID(t[1]))

def p_ValueList(t):
    '''ValueList : NUMBER COMMA NUMBER
                 | Variable COMMA Variable
                 | NUMBER COMMA Variable
                 | Variable COMMA NUMBER
                 | ValueList COMMA NUMBER
                 | ValueList COMMA Variable'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([t[1], t[3]])
    else:
        t[0] = t[1].add(t[3])

def p_ValueList_error(t):
    'ValueList : error COMMA'
    sys.stderr.write( "Syntax error in ValueList.")

def p_TupleList(t):
    '''TupleList : LPAREN ValueList RPAREN'''

    t[0] = TupleList(t[2].getValues())

def p_TupleList_error(t):
    'ValueList : error RPAREN'
    sys.stderr.write( "Syntax error in TupleList.")

#def p_Value(t):
#    '''Value : Variable
#             | NUMBER'''
#    t[0] = Value(t[1])


def p_error(t):
    sys.stderr.write("Syntax error at '%s'" % t.value)
    yacc.errok()
