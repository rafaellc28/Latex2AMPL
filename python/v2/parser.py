#!/usr/bin/python -tt

import sys

from lexer import tokens
import ply.yacc as yacc

from Main import *
from LinearProgram import *
from LinearEquations import *
from Objectives import *
from Constraints import *
from ConstraintExpression import *
from LinearExpression import *
from NumericExpression import *
from SymbolicExpression import *
from IndexingExpression import *
from EntryIndexingExpression import *
from LogicalExpression import *
from EntryLogicalExpression import *
from SetExpression import *
from ValueList import *
from TupleList import *
from Tuple import *
from Range import *
from Value import *
from Variable import *
from ID import *

# Parsing rules
#parser2 = yacc.yacc()

precedence = (
    ('left', 'COMMA', 'DOTS', 'FOR', 'BACKSLASHES'),
    ('left', 'ID'),
    ('left', 'NUMBER'),
    ('left', 'LBRACE', 'RBRACE'),
    ('left', 'OR', 'AND', 'NOT'),
    ('left', 'FORALL', 'EXISTS'),
    ('right', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ', 'COLON', 'COMMA'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION', 'INTER', 'CROSS', 'BY'),
    ('left', 'UNDERLINE', 'CARET'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'PIPE', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'COS', 'ARCTAN', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'UPLUS', 'UMINUS'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'INTEGERSET', 'INTEGERSETPOSITIVE', 'INTEGERSETNEGATIVE', 'INTEGERSETWITHONELIMIT', 
      'REALSET', 'REALSETPOSITIVE', 'REALSETNEGATIVE', 'REALSETWITHONELIMIT', 'NATURALSET', 'BINARYSET', 'SYMBOLIC')
)

def p_Main(t):
  '''MAIN : LinearProgram 
          | LinearEquations'''
  t[0] = Main(t[1])

def p_LinearEquations(t):
    '''LinearEquations : ConstraintList'''
    t[0] = LinearEquations(Constraints(t[1]))

def p_LinearProgram(t):
    '''LinearProgram : Objectives
                     | Objectives Constraints
                     | Objectives BACKSLASHES Constraints'''

    if len(t) > 3:
        t[0] = LinearProgram(t[1], t[3])
    elif len(t) > 2:
        t[0] = LinearProgram(t[1], t[2])
    else:
        t[0] = LinearProgram(t[1], None)

#def p_LinearProgram_error(t):
#    'LinearProgram : error BACKSLASHES'
#    sys.stderr.write("Linear Program bad formatted at line %d\n" % t.lineno(2))

def p_Objectives(t):
    '''Objectives : Objectives BACKSLASHES Objective
                  | Objectives BACKSLASHES
                  | Objective'''

    if not isinstance(t[1], Objectives):
        t[0] = Objectives([t[1]])
    elif len(t) > 3:
        t[0] = t[1].addObjective(t[3])
    else:
        t[0] = t[1]

def p_Objective(t):
    '''Objective : MAXIMIZE LinearExpression
                 | MINIMIZE LinearExpression
                 | MAXIMIZE LinearExpression COMMA IndexingExpression
                 | MINIMIZE LinearExpression COMMA IndexingExpression'''

    if len(t) > 3:
        t[4].setStmtIndexing(True)

        obj = Objective.MINIMIZE
        if t[1] == "maximize":
            obj = Objective.MAXIMIZE

        t[0] = Objective(t[2], obj, t[4])
    else:
        if t[1] == "minimize":
            t[0] = Objective(t[2])
        else:
            t[0] = Objective(t[2], Objective.MAXIMIZE)

#def p_Objective_error(t):
#    '''Objective : MAXIMIZE error COMMA
#                 | MINIMIZE error COMMA'''
#    sys.stderr.write("Objective Function bad formatted at line %d\n" % t.lineno(1))

def p_Constraints(t):
    '''Constraints : SUBJECTTO ConstraintList
                   | SUBJECTTO ConstraintList BACKSLASHES'''
    t[0] = Constraints(t[2])

def p_ConstraintList(t):
    '''ConstraintList : ConstraintList BACKSLASHES Constraint
                      | ConstraintList BACKSLASHES
                      | Constraint'''
    if len(t) > 3:
        t[0] = t[1] + [t[3]]
    elif len(t) > 2:
        t[0] = t[1]
    else:
        t[0] = [t[1]]

#def p_ConstraintList_error(t):
#    'ConstraintList : error BACKSLASHES'
#    sys.stderr.write("Constraints bad formatted at line %d\n" % t.lineno(2))

def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression COMMA IndexingExpression
                  | ConstraintExpression'''
    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])

#def p_Constraint_error(t):
#    '''Constraint : error FOR
#                  | error COMMA'''
#    sys.stderr.write("Constraint bad formatted at line %d\n" % t.lineno(2))

def p_ConstraintExpression(t):
    '''ConstraintExpression : NumericOrLinearExpression EQ NumericOrLinearExpression
                           |  NumericOrLinearExpression LE NumericOrLinearExpression
                           |  NumericOrLinearExpression GE NumericOrLinearExpression
                           |  NumericOrLinearExpression LE NumericOrLinearExpression LE NumericOrLinearExpression
                           |  NumericOrLinearExpression GE NumericOrLinearExpression GE NumericOrLinearExpression'''
    
    if len(t) > 4:
        if t[4] == "\\leq":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.LE)
        elif t[4] == "\\geq":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.GE)
    elif t[2] == "=":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.EQ)
    elif t[2] == "\\leq":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.LE)
    elif t[2] == "\\geq":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.GE)

#def p_ConstraintExpression_error(t):
#    '''ConstraintExpression : error EQ
#                            | error LE
#                            | error GE'''
#    sys.stderr.write("Constraint Expression bad formatted at line %d\n" % t.lineno(2))

def p_LinearExpression(t):
    '''LinearExpression : NUMBER
                        | Variable
                        | PLUS LinearExpression %prec UPLUS
                        | MINUS LinearExpression %prec UMINUS
                        | LPAREN LinearExpression RPAREN
                        | ConditionalLinearExpression'''

    if len(t) > 3:
        t[0] = LinearExpressionBetweenParenthesis(t[2])
    elif len(t) > 2:
        if t[1] == "\+":
            t[0] = PlusLinearExpression(t[2])
        else:
            t[0] = MinusLinearExpression(t[2])
    elif isinstance(t[1], ConditionalLinearExpression):
        t[0] = t[1]
    else:
        t[0] = ValuedLinearExpression(t[1])

#def p_LinearExpression_error(t):
#    'LinearExpression : LPAREN error RPAREN'
#    sys.stderr.write("Linear Expression bad formatted at line %d\n" % t.lineno(1))

def p_LinearExpression_binop(t):
    '''LinearExpression : LinearExpression PLUS LinearExpression
                        | LinearExpression PLUS NumericExpression
                        | LinearExpression MINUS LinearExpression
                        | LinearExpression MINUS NumericExpression
                        | NumericExpression TIMES LinearExpression
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

#def p_LinearExpression_binop_error(t):
#    '''LinearExpression : error PLUS
#                        | error MINUS
#                        | error TIMES
#                        | error DIVIDE'''
#    sys.stderr.write("Linear Expression bad formatted at line %d\n" % t.lineno(2))

def p_IteratedLinearExpression(t):
    '''LinearExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE LinearExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE LinearExpression'''
    if len(t) > 7:
        t[0] = IteratedLinearExpression(t[10], t[4], t[8])
    else:
        t[0] = IteratedLinearExpression(t[6], t[4])

#def p_IteratedLinearExpression_error(t):
#    'LinearExpression : SUM UNDERLINE LBRACE error RBRACE'
#    sys.stderr.write("Linear Expression bad formatted at line %d\n" % t.lineno(1))

def p_ConditionalLinearExpression(t):
    '''ConditionalLinearExpression : LPAREN LogicalExpression RPAREN QUESTION_MARK LinearExpression
                                   | ConditionalLinearExpression COLON LinearExpression'''
    if len(t) > 4:
        t[0] = ConditionalLinearExpression(t[2], t[5])
    else:
        t[1].addElseExpression(t[3])
        t[0] = t[1]

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

#def p_LogicalExpression_error(t):
#    '''LogicalExpression : error OR
#                         | error AND'''
#    sys.stderr.write("Logical Expression bad formatted at line %d\n" % t.lineno(2))

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NOT EntryLogicalExpression
                              | LPAREN LogicalExpression RPAREN'''

    if t[1] == "not":
        t[0] = EntryLogicalExpressionNot(t[2])
    else:
        t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

#def p_EntryLogicalExpression_error(t):
#    '''EntryLogicalExpression : LPAREN error RPAREN'''
#    sys.stderr.write("Logical Expression bad formatted at line %d\n" % t.lineno(1))

def p_EntryRelationalLogicalExpression(t):
    '''EntryLogicalExpression : NumericOrSymbolicExpression LT NumericOrSymbolicExpression
                              | NumericOrSymbolicExpression LE NumericOrSymbolicExpression
                              | NumericOrSymbolicExpression EQ NumericOrSymbolicExpression
                              | NumericOrSymbolicExpression GT NumericOrSymbolicExpression
                              | NumericOrSymbolicExpression GE NumericOrSymbolicExpression
                              | NumericOrSymbolicExpression NEQ NumericOrSymbolicExpression'''

    if t[2] == "<":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LT, t[1], t[3])
    elif t[2] == "\\leq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LE, t[1], t[3])
    elif t[2] == "=":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.EQ, t[1], t[3])
    elif t[2] == ">":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GT, t[1], t[3])
    elif t[2] == "\\geq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GE, t[1], t[3])
    elif t[2] == "\\neq":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.NEQ, t[1], t[3])

#def p_EntryRelationalLogicalExpression_error(t):
#    '''EntryLogicalExpression : error LT
#                              | error LE
#                              | error EQ
#                              | error GE
#                              | error NEQ'''
#    sys.stderr.write("Logical Expression bad formatted at line %d\n" % t.lineno(2))

def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList IN SetExpression
                              | Tuple IN SetExpression
                              | Variable IN SetExpression
                              | ValueList NOTIN SetExpression
                              | Tuple NOTIN SetExpression
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

#def p_EntryLogicalExpressionWithSet_error(t):
#    '''EntryLogicalExpression : error IN
#                              | error NOTIN
#                              | error SUBSET
#                              | error NOTSUBSET'''
#    sys.stderr.write("Logical Expression bad formatted at line %d\n" % t.lineno(2))

def p_EntryIteratedLogicalExpression(t):
    '''EntryLogicalExpression : FORALL LBRACE IndexingExpression RBRACE LogicalExpression
                              | EXISTS LBRACE IndexingExpression RBRACE LogicalExpression'''

    if t[1] == "\\forall":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])
    elif t[1] == "\\exists":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

#def p_EntryIteratedLogicalExpression_error(t):
#    '''EntryLogicalExpression : FORALL LBRACE error RBRACE
#                              | EXISTS LBRACE error RBRACE'''
#    sys.stderr.write("Logical Expression bad formatted at line %d\n" % t.lineno(2))

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

#def p_SetExpressionWithOperation_error(t):
#    '''SetExpression : error DIFF
#                     | error SYMDIFF
#                     | error UNION
#                     | error INTER
#                     | error CROSS'''
#    sys.stderr.write("Set Expression bad formatted at line %d\n" % t.lineno(2))

def p_SetExpressionWithValue(t):
    '''SetExpression : LBRACE ValueList RBRACE
                     | LBRACE Range RBRACE
                     | LBRACE SetExpression RBRACE
                     | LBRACE TupleList RBRACE
                     | LBRACE IndexingExpression RBRACE
                     | LPAREN SetExpression RPAREN
                     | Range
                     | Variable
                     | NATURALSET
                     | INTEGERSET
                     | INTEGERSETPOSITIVE
                     | INTEGERSETNEGATIVE
                     | INTEGERSETWITHONELIMIT
                     | INTEGERSETWITHTWOLIMITS
                     | REALSET
                     | REALSETPOSITIVE
                     | REALSETNEGATIVE
                     | REALSETWITHONELIMIT
                     | REALSETWITHTWOLIMITS
                     | BINARYSET
                     | SYMBOLIC'''

    if len(t) > 2:
        if t[1] == "(":
            t[0] = SetExpressionBetweenParenthesis(t[2])
        else:
            t[0] = SetExpressionWithValue(t[2])
    else:
        t[0] = SetExpressionWithValue(t[1])

#def p_SetExpressionWithValue_error(t):
#    '''SetExpression : LBRACE error RBRACE'''
#    sys.stderr.write("Set Expression bad formatted at line %d\n" % t.lineno(1))

def p_SetExpressionWithIndices(t):
    '''SetExpression : Variable LPAREN ValueList RPAREN
                     | Variable LBRACE ValueList RBRACE
                     | Variable LBRACE NumericExpression RBRACE
                     | Variable LPAREN NumericExpression RPAREN'''
    
    t[0] = SetExpressionWithIndices(t[1], t[3])

#def p_SetExpressionWithIndices_error(t):
#    '''SetExpression : error LBRACE
#                     | error LPAREN'''
#    sys.stderr.write("Set Expression bad formatted at line %d\n" % t.lineno(2))

def p_ConditionalSetExpression(t):
    '''SetExpression : LPAREN LogicalExpression RPAREN QUESTION_MARK SetExpression COLON SetExpression'''
    t[0] = ConditionalSetExpression(t[2], t[5], t[7])

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

#def p_IndexingExpression_error(t):
#    'IndexingExpression : error COMMA'
#    sys.stderr.write("Indexing Expression bad formatted at line %d\n" % t.lineno(2))

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | Tuple IN SetExpression
                               | Variable IN SetExpression'''
    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

#def p_EntryIndexingExpressionWithSet_error(t):
#    '''EntryIndexingExpression : error IN
#                               | error COLON'''
#    sys.stderr.write("Indexing Expression bad formatted at line %d\n" % t.lineno(2))

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

#def p_EntryIndexingExpressionEq_error(t):
#    '''EntryIndexingExpression : error EQ
#                               | error NEQ
#                               | error LE
#                               | error GE
#                               | error LT
#                               | error GT'''
#    sys.stderr.write("Indexing Expression bad formatted at line %d\n" % t.lineno(2))

def p_StringSymbolicExpression(t):
    '''SymbolicExpression : LPAREN SymbolicExpression RPAREN
                          | STRING'''

    if len(t) > 2:
        t[0] = SymbolicExpressionBetweenParenthesis(t[2])
    else:
        t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : SymbolicExpression AMPERSAND SymbolicExpression'''
    if t[2] == "AMP":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

#def p_SymbolicExpression_binop_error(t):
#    '''SymbolicExpression : error AMPERSAND'''
#    sys.stderr.write("Symbolic Expression bad formatted at line %d\n" % t.lineno(2))


def p_FunctionSymbolicExpression(t):
    '''SymbolicExpression : SUBSTR LPAREN NumericOrSymbolicExpression COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericOrSymbolicExpression COMMA NumericExpression RPAREN
                          | TIME2STR LPAREN NumericExpression COMMA NumericOrSymbolicExpression RPAREN'''

    if t[1] == "substr":
        op = SymbolicExpressionWithFunction.SUBSTR
    elif t[1] == "time2str":
        op = SymbolicExpressionWithFunction.TIME2STR

    if len(t) > 7:
        t[0] = SymbolicExpressionWithFunction(op, t[3], t[5], t[7])
    else:
        if t[1] == "substr":
            t[0] = SymbolicExpressionWithFunction(op, t[3], t[5])
        else:
            t[0] = SymbolicExpressionWithFunction(op, t[5], t[3])

#def p_FunctionSymbolicExpression_error(t):
#    '''SymbolicExpression : error COMMA'''
#    sys.stderr.write("Bad function call at line %d\n" % t.lineno(1))


def p_ConditionalSymbolicExpression(t):
    '''SymbolicExpression : LPAREN LogicalExpression RPAREN QUESTION_MARK SymbolicExpression COLON SymbolicExpression'''
    t[0] = ConditionalSymbolicExpression(t[2], t[5], t[7])

def p_NumericExpression_binop(t):
    '''NumericExpression : NumericExpression PLUS NumericExpression
                         | NumericExpression MINUS NumericExpression
                         | NumericExpression TIMES NumericExpression
                         | NumericExpression DIVIDE NumericExpression
                         | NumericExpression MOD NumericExpression
                         | NumericExpression QUOTIENT NumericExpression
                         | NumericExpression LESS NumericExpression
                         | NumericExpression CARET NumericExpression'''

    if t[2] == "+":
        op = NumericExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = NumericExpressionWithArithmeticOperation.MINUS
    elif t[2] == "*":
        op = NumericExpressionWithArithmeticOperation.TIMES
    elif t[2] == "/":
        op = NumericExpressionWithArithmeticOperation.DIV
    elif t[2] == "\%":
        op = NumericExpressionWithArithmeticOperation.MOD
    elif t[2] == "^":
        op = NumericExpressionWithArithmeticOperation.POW
    elif t[2] == "quot":
        op = NumericExpressionWithArithmeticOperation.QUOT
    elif t[2] == "less":
        op = NumericExpressionWithArithmeticOperation.LESS

    t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

#def p_NumericExpression_binop_error(t):
#    '''NumericExpression : error PLUS
#                         | error MINUS
#                         | error TIMES
#                         | error DIVIDE
#                         | error MOD
#                         | error CARET'''
#    sys.stderr.write("Numeric Expression bad formatted at line %d\n" % t.lineno(2))

def p_IteratedNumericExpression(t):
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression'''

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

#def p_IteratedNumericExpression_error(t):
#    '''NumericExpression : SUM UNDERLINE LBRACE error RBRACE
#                         | PROD UNDERLINE LBRACE error RBRACE
#                         | MAX UNDERLINE LBRACE error RBRACE
#                         | MIN UNDERLINE LBRACE error RBRACE'''
#    sys.stderr.write("Numeric Expression bad formatted at line %d\n" % t.lineno(2))


def p_NumericExpression(t):
    '''NumericExpression : MINUS NumericExpression %prec UMINUS
                         | PLUS NumericExpression %prec UPLUS
                         | LPAREN NumericExpression RPAREN
                         | ConditionalNumericExpression
                         | Variable
                         | NUMBER'''

    if len(t) > 3:
        t[0] = NumericExpressionBetweenParenthesis(t[2])
    elif t[1] == "+":
        t[0] = t[2]
    elif t[1] == "-":
        t[0] = MinusNumericExpression(t[2])
    elif isinstance(t[1], ConditionalNumericExpression):
        t[0] = t[1]
    else:
        t[0] = ValuedNumericExpression(t[1])

#def p_NumericExpression_error(t):
#    'NumericExpression : LPAREN error RPAREN'
#    sys.stderr.write("Numeric Expression bad formatted at line %d\n" % t.lineno(1))


def p_FunctionNumericExpression(t):
    '''NumericExpression : SQRT LBRACE NumericExpression RBRACE
                         | LFLOOR NumericExpression RFLOOR
                         | LCEIL NumericExpression RCEIL
                         | PIPE NumericExpression PIPE
                         | MAX LPAREN ValueList RPAREN
                         | MIN LPAREN ValueList RPAREN
                         | SIN LPAREN NumericExpression RPAREN
                         | COS LPAREN NumericExpression RPAREN
                         | LOG LPAREN NumericExpression RPAREN
                         | LN LPAREN NumericExpression RPAREN
                         | EXP LPAREN NumericExpression RPAREN
                         | ARCTAN LPAREN NumericExpression RPAREN
                         | ARCTAN LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | CARD LPAREN SetExpression RPAREN
                         | LENGTH LPAREN NumericOrSymbolicExpression RPAREN
                         | ROUND LPAREN NumericExpression RPAREN
                         | ROUND LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | TRUNC LPAREN NumericExpression RPAREN
                         | TRUNC LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | UNIFORM LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | NORMAL LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | GMTIME LPAREN RPAREN
                         | IRAND224 LPAREN RPAREN
                         | UNIFORM01 LPAREN RPAREN
                         | NORMAL01 LPAREN RPAREN'''

    if t[1] == "card":
        op = NumericExpressionWithFunction.CARD
    elif t[1] == "length":
        op = NumericExpressionWithFunction.LENGTH
    elif t[1] == "round":
        op = NumericExpressionWithFunction.ROUND
    elif t[1] == "trunc":
        op = NumericExpressionWithFunction.TRUNC
    elif t[1] == "\\sqrt":
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
        op = NumericExpressionWithFunction.ATAN

    if len(t) > 5:
        t[0] = NumericExpressionWithFunction(op, t[3], t[5])
    elif len(t) > 4:
        t[0] = NumericExpressionWithFunction(op, t[3])
    else:
        if t[2] == "(":
          t[0] = NumericExpressionWithFunction(op)
        else:
          t[0] = NumericExpressionWithFunction(op, t[2])

#def p_FunctionNumericExpression_error(t):
#    '''NumericExpression : SQRT LBRACE error RBRACE
#                         | LFLOOR error RFLOOR
#                         | LCEIL error RCEIL'''
#    sys.stderr.write("Bad function call at line %d\n" % t.lineno(1))

def p_ConditionalNumericExpression(t):
    '''ConditionalNumericExpression : LPAREN LogicalExpression RPAREN QUESTION_MARK NumericExpression
                                    | ConditionalNumericExpression COLON NumericExpression'''
    if len(t) > 4:
        t[0] = ConditionalNumericExpression(t[2], t[5])
    else:
        t[1].addElseExpression(t[3])
        t[0] = t[1]

def p_NumericOrLinearExpression(t):
    '''NumericOrLinearExpression : NumericExpression
                                 | LinearExpression'''
    t[0] = t[1]

def p_NumericOrSymbolicExpression(t):
    '''NumericOrSymbolicExpression : NumericExpression
                                   | SymbolicExpression'''
    t[0] = t[1]


def p_Range(t):
    '''Range : NumericExpression DOTS NumericExpression BY NumericExpression
             | NumericExpression DOTS NumericExpression'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

#def p_Range_error(t):
#    '''Range : error DOTS
#             | error COMMA'''
#    sys.stderr.write("Bad range declaration at line %d\n" % t.lineno(2))

def p_Variable(t):
    '''Variable : ID UNDERLINE LBRACE ValueList RBRACE
                | ID UNDERLINE LBRACE NumericOrSymbolicExpression RBRACE
                | ID'''

    if len(t) > 2:
        if isinstance(t[4], ValueList):
          t[0] = Variable(ID(t[1]), t[4].getValues())
        else:
          t[0] = Variable(ID(t[1]), t[4])
    else:
        t[0] = Variable(ID(t[1]))

#def p_Variable_error(t):
#    '''Variable : ID UNDERLINE LBRACE error RBRACE'''
#    sys.stderr.write("Bad sub-indice declaration at line %d\n" % t.lineno(1))

def p_ValueList(t):
    '''ValueList : ValueList COMMA NumericOrSymbolicExpression
                 | NumericOrSymbolicExpression'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([t[1]])
    else:
        t[0] = t[1].add(t[3])

#def p_ValueList_error(t):
#    'ValueList : error COMMA'
#    sys.stderr.write( "Bad value list declaration at line %d\n" % t.lineno(2))

def p_Tuple(t):
    '''Tuple : LPAREN ValueList RPAREN'''
    t[0] = Tuple(t[2].getValues())

#def p_Tuple_error(t):
#    'Tuple : error RPAREN'
#    sys.stderr.write( "Bad tuple declaration at line %d\n" % t.lineno(2))

def p_TupleList(t):
    '''TupleList : TupleList COMMA Tuple
                 | Tuple'''

    if not isinstance(t[1], TupleList):
        t[0] = TupleList([t[1]])
    else:
        t[0] = t[1].add(t[3])

#def p_TupleList_error(t):
#    'TupleList : error COMMA'
#    sys.stderr.write( "Bad tuple list declaration at line %d\n" % t.lineno(2))

def p_error(t):
  if t:
    print("Syntax error at line %d, position %d: '%s'" % (t.lineno, t.lexpos, t.value))
  else:
    print("Syntax error at EOF")
