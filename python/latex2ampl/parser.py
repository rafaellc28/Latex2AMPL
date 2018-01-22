#!/usr/bin/python -tt

from lexer import tokens

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
from Identifier import *
from ID import *
from SyntaxException import *
from Declarations import *
from DeclarationExpression import *

import objects as obj

precedence = (
    ('left', 'ID'),
    ('left', 'NUMBER', 'INFINITY'),
    ('right', 'COMMA'),
    ('left', 'FOR', 'WHERE', 'COLON'),
    ('right', 'PIPE'),
    ('right', 'DEFAULT', 'DIMEN', 'ASSIGN'),
    ('right', 'LPAREN', 'RPAREN', 'LLBRACE', 'RRBRACE', 'LBRACKET', 'RBRACKET'),
    ('right', 'LBRACE', 'RBRACE', 'UNDERLINE', 'FRAC'),
    ('left', 'MAXIMIZE', 'MINIMIZE'),
    ('right', 'SLASHES', 'SEMICOLON'),
    ('right', 'IF', 'THEN', 'ELSE'),
    ('left', 'OR'),
    ('left', 'FORALL', 'EXISTS', 'NEXISTS'),
    ('left', 'AND'),
    ('right', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ'),
    ('right', 'IMPLIES', 'ISIMPLIEDBY', 'IFANDONLYIF'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'SUBSET', 'NOTSUBSET'),
    ('left', 'NOT'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION'),
    ('left', 'INTER'),
    ('left', 'CROSS'),
    ('left', 'SETOF', 'COUNT', 'ATMOST', 'ATLEAST', 'EXACTLY', 'NUMBEROF', 'ALLDIFF', 'DOTS', 'BY'),
    ('right', 'AMPERSAND'),
    ('left', 'PLUS', 'MINUS', 'LESS'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'QUOTIENT'),
    ('left', 'UPLUS', 'UMINUS'),
    ('right', 'CARET'),
    ('left', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'ASIN', 'SINH', 'ASINH', 'COS', 'ACOS', 'COSH', 'ACOSH', 'ARCTAN', 'TAN', 'ARCTANH', 'TANH', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'INTEGERSET', 'INTEGERSETPOSITIVE', 'INTEGERSETNEGATIVE', 'INTEGERSETWITHONELIMIT', 'INTEGERSETWITHTWOLIMITS', 
      'REALSET', 'REALSETPOSITIVE', 'REALSETNEGATIVE', 'REALSETWITHONELIMIT', 'REALSETWITHTWOLIMITS', 
      'NATURALSET', 'NATURALSETWITHONELIMIT', 'NATURALSETWITHTWOLIMITS', 'BINARYSET', 'SYMBOLIC', 'LOGICAL')
)

def p_Main(t):
  '''MAIN : LinearEquations'''
  t[0] = Main(t[1])

def p_LinearEquations(t):
    '''LinearEquations : ConstraintList'''
    t[0] = LinearEquations(Constraints(t[1]))

def p_Objective(t):
    '''Objective : MAXIMIZE NumericSymbolicExpression
                 | MAXIMIZE Identifier
                 | MINIMIZE NumericSymbolicExpression
                 | MINIMIZE Identifier
                 | MAXIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MAXIMIZE Identifier FOR IndexingExpression
                 | MINIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MINIMIZE Identifier FOR IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MAXIMIZE Identifier WHERE IndexingExpression
                 | MINIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MINIMIZE Identifier WHERE IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MAXIMIZE Identifier COLON IndexingExpression
                 | MINIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MINIMIZE Identifier COLON IndexingExpression'''

    _type = t.slice[1].type

    if len(t) > 3:
        t[4].setStmtIndexing(True)

        obj = Objective.MINIMIZE
        
        if _type == "MAXIMIZE":
            obj = Objective.MAXIMIZE

        t[0] = Objective(t[2], obj, t[4])

    else:

        if _type == "MINIMIZE":
            t[0] = Objective(t[2])
        else:
            t[0] = Objective(t[2], Objective.MAXIMIZE)

def p_ConstraintList(t):
    '''ConstraintList : ConstraintList Objective SLASHES
                      | ConstraintList Constraint SLASHES
                      | ConstraintList Declarations SLASHES
                      | ConstraintList Objective
                      | ConstraintList Constraint
                      | ConstraintList Declarations
                      | Objective SLASHES
                      | Constraint SLASHES
                      | Declarations SLASHES
                      | Objective
                      | Constraint
                      | Declarations'''

    if len(t) > 2 and not isinstance(t[2], str):
        t[0] = t[1] + [t[2]]

    else:
        t[0] = [t[1]]

def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression WHERE IndexingExpression
                  | ConstraintExpression COLON IndexingExpression
                  | ConstraintExpression
                  | EntryConstraintLogicalExpression FOR IndexingExpression
                  | EntryConstraintLogicalExpression WHERE IndexingExpression
                  | EntryConstraintLogicalExpression COLON IndexingExpression
                  | EntryConstraintLogicalExpression
                  | AllDiffExpression FOR IndexingExpression
                  | AllDiffExpression WHERE IndexingExpression
                  | AllDiffExpression COLON IndexingExpression
                  | AllDiffExpression
                  | IteratedConstraintLogicalExpression FOR IndexingExpression
                  | IteratedConstraintLogicalExpression WHERE IndexingExpression
                  | IteratedConstraintLogicalExpression COLON IndexingExpression
                  | IteratedConstraintLogicalExpression
                  | ConnectedConstraintLogicalExpression FOR IndexingExpression
                  | ConnectedConstraintLogicalExpression WHERE IndexingExpression
                  | ConnectedConstraintLogicalExpression COLON IndexingExpression
                  | ConnectedConstraintLogicalExpression'''
    
    if not isinstance(t[1], ConstraintExpression):
      t[1] = LogicalExpression([t[1]])

    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])


def p_ConstraintExpressionLogical(t):
    '''ConstraintExpression : ConstraintExpression AND ConstraintExpression
                            | ConstraintExpression AND ConnectedConstraintLogicalExpression
                            | ConstraintExpression AND IteratedConstraintLogicalExpression
                            | ConstraintExpression AND EntryConstraintLogicalExpression
                            | ConstraintExpression AND AllDiffExpression
                            | IteratedConstraintLogicalExpression AND ConstraintExpression
                            | EntryConstraintLogicalExpression AND ConstraintExpression
                            | AllDiffExpression AND ConstraintExpression
                            | ConstraintExpression OR ConstraintExpression
                            | ConstraintExpression OR ConnectedConstraintLogicalExpression
                            | ConstraintExpression OR IteratedConstraintLogicalExpression
                            | ConstraintExpression OR EntryConstraintLogicalExpression
                            | ConstraintExpression OR AllDiffExpression
                            | IteratedConstraintLogicalExpression OR ConstraintExpression
                            | EntryConstraintLogicalExpression OR ConstraintExpression
                            | AllDiffExpression OR ConstraintExpression
                            | FORALL LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | NFORALL LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | EXISTS LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | NEXISTS LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | NOT ConstraintExpression
                            | LPAREN ConstraintExpression RPAREN'''

    if t.slice[1].type == "LPAREN":
        entry = LogicalExpression([t[2]])
        t[0] = EntryLogicalExpressionBetweenParenthesis(entry)

    elif t.slice[1].type == "NOT":
        entry = EntryLogicalExpressionNot(t[2])
        t[0] = LogicalExpression([entry])

    elif len(t) > 2 and (t.slice[2].type == "AND" or t.slice[2].type == "OR"):

        #entry = EntryLogicalExpressionNumericOrSymbolic(t[1])
        entry = LogicalExpression([t[1]])

        if t.slice[2].type == "AND":
          entry = entry.addAnd(t[3])
        else:
          entry = entry.addOr(t[3])

        t[0] = entry

    else:
        entry = None
        _type = t.slice[1].type
        if _type == "FORALL":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])

        elif _type == "NFORALL":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])

        elif _type == "EXISTS":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

        elif _type == "NEXISTS":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])
        else:
            entry = t[1]

        t[0] = LogicalExpression([entry])

def p_ConstraintExpressionConditional(t):
    '''ConstraintExpression : Identifier IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | Identifier IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | Identifier IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | Identifier IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | ConstraintExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | LogicalExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | LogicalExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | AllDiffExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | AllDiffExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | AllDiffExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | AllDiffExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression ELSE AllDiffExpression


                            
                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression



                            | Identifier IMPLIES ConstraintExpression
                            | Identifier IMPLIES ConnectedConstraintLogicalExpression
                            | Identifier IMPLIES IteratedConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression
                            | Identifier IMPLIES AllDiffExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression
                            | NumericSymbolicExpression IMPLIES ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES AllDiffExpression

                            | ConstraintExpression IMPLIES ConstraintExpression
                            | ConstraintExpression IMPLIES ConnectedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES IteratedConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES AllDiffExpression

                            | LogicalExpression IMPLIES ConstraintExpression
                            | LogicalExpression IMPLIES ConnectedConstraintLogicalExpression
                            | LogicalExpression IMPLIES IteratedConstraintLogicalExpression
                            | LogicalExpression IMPLIES EntryConstraintLogicalExpression
                            | LogicalExpression IMPLIES AllDiffExpression

                            | ConnectedConstraintLogicalExpression IMPLIES ConstraintExpression
                            | ConnectedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IMPLIES AllDiffExpression

                            | IteratedConstraintLogicalExpression IMPLIES ConstraintExpression
                            | IteratedConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IMPLIES AllDiffExpression

                            | AllDiffExpression IMPLIES ConstraintExpression
                            | AllDiffExpression IMPLIES ConnectedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES IteratedConstraintLogicalExpression
                            | AllDiffExpression IMPLIES EntryConstraintLogicalExpression
                            | AllDiffExpression IMPLIES AllDiffExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES AllDiffExpression



                            | Identifier ISIMPLIEDBY ConstraintExpression
                            | Identifier ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY AllDiffExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY AllDiffExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY AllDiffExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | LogicalExpression ISIMPLIEDBY AllDiffExpression

                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression

                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression

                            | AllDiffExpression ISIMPLIEDBY ConstraintExpression
                            | AllDiffExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | AllDiffExpression ISIMPLIEDBY AllDiffExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY AllDiffExpression



                            | Identifier IFANDONLYIF ConstraintExpression
                            | Identifier IFANDONLYIF ConnectedConstraintLogicalExpression
                            | Identifier IFANDONLYIF IteratedConstraintLogicalExpression
                            | Identifier IFANDONLYIF EntryConstraintLogicalExpression
                            | Identifier IFANDONLYIF AllDiffExpression

                            | NumericSymbolicExpression IFANDONLYIF ConstraintExpression
                            | NumericSymbolicExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | NumericSymbolicExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | NumericSymbolicExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IFANDONLYIF AllDiffExpression

                            | ConstraintExpression IFANDONLYIF ConstraintExpression
                            | ConstraintExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | ConstraintExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | ConstraintExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | ConstraintExpression IFANDONLYIF AllDiffExpression

                            | LogicalExpression IFANDONLYIF ConstraintExpression
                            | LogicalExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | LogicalExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | LogicalExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | LogicalExpression IFANDONLYIF AllDiffExpression

                            | ConnectedConstraintLogicalExpression IFANDONLYIF ConstraintExpression
                            | ConnectedConstraintLogicalExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression IFANDONLYIF AllDiffExpression

                            | IteratedConstraintLogicalExpression IFANDONLYIF ConstraintExpression
                            | IteratedConstraintLogicalExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | IteratedConstraintLogicalExpression IFANDONLYIF AllDiffExpression

                            | AllDiffExpression IFANDONLYIF ConstraintExpression
                            | AllDiffExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | AllDiffExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | AllDiffExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | AllDiffExpression IFANDONLYIF AllDiffExpression

                            | EntryConstraintLogicalExpression IFANDONLYIF ConstraintExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF AllDiffExpression'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])

    if not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    _type = t.slice[2].type

    if _type == "IMPLIES":
      op = ConditionalConstraintExpression.IMPLIES
    elif _type == "ISIMPLIEDBY":
      op = ConditionalConstraintExpression.ISIMPLIEDBY
    elif _type == "IFANDONLYIF":
      op = ConditionalConstraintExpression.IFANDONLYIF

    if len(t) > 4:
      t[0] = ConditionalConstraintExpression(op, t[1], t[3], t[5])
    else:
      t[0] = ConditionalConstraintExpression(op, t[1], t[3])

def p_ConstraintExpression(t):
    '''ConstraintExpression : NumericSymbolicExpression LE NumericSymbolicExpression LE NumericSymbolicExpression
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE Identifier
                            | NumericSymbolicExpression LE Identifier LE NumericSymbolicExpression
                            | Identifier LE NumericSymbolicExpression LE NumericSymbolicExpression
                            | Identifier LE NumericSymbolicExpression LE Identifier
                            | Identifier LE Identifier LE NumericSymbolicExpression
                            | Identifier LE Identifier LE Identifier
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE NumericSymbolicExpression
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE Identifier
                            | NumericSymbolicExpression GE Identifier GE NumericSymbolicExpression
                            | NumericSymbolicExpression GE Identifier GE Identifier
                            | Identifier GE NumericSymbolicExpression GE NumericSymbolicExpression
                            | Identifier GE NumericSymbolicExpression GE Identifier
                            | Identifier GE Identifier GE NumericSymbolicExpression
                            | Identifier GE Identifier GE Identifier'''

    if len(t) > 4:
        if t.slice[4].type == "LE":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.LE)

        elif t.slice[4].type == "GE":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.GE)

    elif t.slice[2].type == "EQ":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.EQ)

    elif t.slice[2].type == "LE":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.LE)

    elif t.slice[2].type == "GE":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.GE)


def p_EntryConstraintLogicalExpression(t):
    '''EntryConstraintLogicalExpression : NumericSymbolicExpression LE NumericSymbolicExpression
                                        | NumericSymbolicExpression LE Identifier
                                        | NumericSymbolicExpression EQ NumericSymbolicExpression
                                        | NumericSymbolicExpression EQ Identifier
                                        | NumericSymbolicExpression GE NumericSymbolicExpression
                                        | NumericSymbolicExpression GE Identifier
                                        | Identifier LE NumericSymbolicExpression
                                        | Identifier LE Identifier
                                        | Identifier EQ NumericSymbolicExpression
                                        | Identifier EQ Identifier
                                        | Identifier GE NumericSymbolicExpression
                                        | Identifier GE Identifier
                                        | NumericSymbolicExpression LT NumericSymbolicExpression
                                        | NumericSymbolicExpression LT Identifier
                                        | NumericSymbolicExpression GT NumericSymbolicExpression
                                        | NumericSymbolicExpression GT Identifier
                                        | NumericSymbolicExpression NEQ NumericSymbolicExpression
                                        | NumericSymbolicExpression NEQ Identifier
                                        | Identifier LT NumericSymbolicExpression
                                        | Identifier LT Identifier
                                        | Identifier GT NumericSymbolicExpression
                                        | Identifier GT Identifier
                                        | Identifier NEQ NumericSymbolicExpression
                                        | Identifier NEQ Identifier
                                        | LPAREN EntryConstraintLogicalExpression RPAREN
                                        | NOT EntryConstraintLogicalExpression'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      _type = t.slice[2].type
      if _type == "LE":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LE, t[1], t[3])

      elif _type == "EQ":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.EQ, t[1], t[3])

      elif _type == "GE":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GE, t[1], t[3])

      elif _type == "LT":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LT, t[1], t[3])

      elif _type == "GT":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GT, t[1], t[3])

      elif _type == "NEQ":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.NEQ, t[1], t[3])

def p_IteratedConstraintLogicalExpression(t):
    '''IteratedConstraintLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | NFORALL LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | EXISTS LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | NEXISTS LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | FORALL LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                                           | NFORALL LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                                           | EXISTS LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                                           | NEXISTS LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                                           | FORALL LLBRACE IndexingExpression RRBRACE AllDiffExpression
                                           | NFORALL LLBRACE IndexingExpression RRBRACE AllDiffExpression
                                           | EXISTS LLBRACE IndexingExpression RRBRACE AllDiffExpression
                                           | NEXISTS LLBRACE IndexingExpression RRBRACE AllDiffExpression
                                           | FORALL LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                                           | NFORALL LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                                           | EXISTS LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                                           | NEXISTS LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                                           | LPAREN IteratedConstraintLogicalExpression RPAREN
                                           | NOT IteratedConstraintLogicalExpression'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      entry = None
      _type = t.slice[1].type
      if _type == "FORALL":
          entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])

      elif _type == "NFORALL":
          entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])

      elif _type == "EXISTS":
          entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

      elif _type == "NEXISTS":
          entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])
      else:
          entry = t[1]

      t[0] = LogicalExpression([entry])

def p_ConnectedConstraintLogicalExpression(t):
    '''ConnectedConstraintLogicalExpression : EntryConstraintLogicalExpression AND EntryConstraintLogicalExpression
                                            | EntryConstraintLogicalExpression AND AllDiffExpression
                                            | EntryConstraintLogicalExpression AND IteratedConstraintLogicalExpression
                                            | EntryConstraintLogicalExpression AND ConnectedConstraintLogicalExpression
                                            | EntryConstraintLogicalExpression OR EntryConstraintLogicalExpression
                                            | EntryConstraintLogicalExpression OR AllDiffExpression
                                            | EntryConstraintLogicalExpression OR IteratedConstraintLogicalExpression
                                            | EntryConstraintLogicalExpression OR ConnectedConstraintLogicalExpression
                                            | AllDiffExpression AND EntryConstraintLogicalExpression
                                            | AllDiffExpression AND AllDiffExpression
                                            | AllDiffExpression AND IteratedConstraintLogicalExpression
                                            | AllDiffExpression AND ConnectedConstraintLogicalExpression
                                            | AllDiffExpression OR EntryConstraintLogicalExpression
                                            | AllDiffExpression OR AllDiffExpression
                                            | AllDiffExpression OR IteratedConstraintLogicalExpression
                                            | AllDiffExpression OR ConnectedConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression AND EntryConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression AND AllDiffExpression
                                            | IteratedConstraintLogicalExpression AND IteratedConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression AND ConnectedConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression OR EntryConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression OR AllDiffExpression
                                            | IteratedConstraintLogicalExpression OR IteratedConstraintLogicalExpression
                                            | IteratedConstraintLogicalExpression OR ConnectedConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression AND EntryConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression AND AllDiffExpression
                                            | ConnectedConstraintLogicalExpression AND IteratedConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression AND ConnectedConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression OR EntryConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression OR AllDiffExpression
                                            | ConnectedConstraintLogicalExpression OR IteratedConstraintLogicalExpression
                                            | ConnectedConstraintLogicalExpression OR ConnectedConstraintLogicalExpression
                                            | LPAREN ConnectedConstraintLogicalExpression RPAREN
                                            | NOT ConnectedConstraintLogicalExpression'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      if not isinstance(t[1], LogicalExpression):
        t[1] = LogicalExpression([t[1]])

      if t.slice[2].type == "AND":
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])


def _getDeclarationExpression(entryConstraintLogicalExpression):

    attr = None
    op = entryConstraintLogicalExpression.op
    expr1 = entryConstraintLogicalExpression.numericExpression1
    expr2 = entryConstraintLogicalExpression.numericExpression2

    if op == EntryLogicalExpressionRelational.LT:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.LT)

    elif op == EntryLogicalExpressionRelational.GT:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.GT)

    elif op == EntryLogicalExpressionRelational.NEQ:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.NEQ)

    if op == EntryLogicalExpressionRelational.LE:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.LE)

    elif op == EntryLogicalExpressionRelational.GE:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.GE)

    elif op == EntryLogicalExpressionRelational.EQ:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.EQ)

    if isinstance(expr1, NumericExpression) or isinstance(expr1, SymbolicExpression) or isinstance(expr1, Identifier):
      entryConstraintLogicalExpression = ValueList([expr1])
    else:
      entryConstraintLogicalExpression = expr1

    declarationExpression = DeclarationExpression(entryConstraintLogicalExpression)
    declarationExpression.addAttribute(attr)

    return declarationExpression


def p_Declarations(t):
  '''Declarations : DeclarationList'''

  i = 1
  length = len(t[1])
  lastDecl = t[1][length-i]
  while (not lastDecl or lastDecl.indexingExpression == None) and i < length:
    i += 1
    lastDecl = t[1][length-i]
  
  if lastDecl and lastDecl.indexingExpression != None:
    for i in range(length-i):
      decl = t[1][i]
      if decl.indexingExpression == None:
        decl.setIndexingExpression(lastDecl.indexingExpression)

  t[0] = Declarations(t[1])

def p_DeclarationList(t):
    '''DeclarationList : DeclarationList SEMICOLON Declaration
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression
                       | EntryConstraintLogicalExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression
                       | Declaration'''
    if len(t) > 3:
      if isinstance(t[1], EntryLogicalExpressionRelational):
        t[1] = Declaration(_getDeclarationExpression(t[1])) # turn into Declaration
        t[1] = [t[1]] # turn into DeclarationList

      if isinstance(t[3], EntryLogicalExpressionRelational):
        t[3] = Declaration(_getDeclarationExpression(t[3])) # turn into Declaration

      t[0] = t[1] + [t[3]]

    else:
      t[0] = [t[1]]

def p_Declaration(t):
    '''Declaration : DeclarationExpression FOR IndexingExpression
                   | DeclarationExpression WHERE IndexingExpression
                   | DeclarationExpression COLON IndexingExpression
                   | NumericSymbolicExpression FOR IndexingExpression
                   | NumericSymbolicExpression WHERE IndexingExpression
                   | NumericSymbolicExpression COLON IndexingExpression
                   | Identifier FOR IndexingExpression
                   | Identifier WHERE IndexingExpression
                   | Identifier COLON IndexingExpression
                   | ValueList FOR IndexingExpression
                   | ValueList WHERE IndexingExpression
                   | ValueList COLON IndexingExpression
                   | DeclarationExpression'''

    if isinstance(t[1], EntryLogicalExpressionRelational):
      t[1] = _getDeclarationExpression(t[1])

    if len(t) > 3:
        t[3].setStmtIndexing(True)
        if isinstance(t[1], ValueList):
          t[1] = DeclarationExpression(t[1], [])
        elif isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
          t[1] = DeclarationExpression(ValueList([t[1]]), [])

        t[0] = Declaration(t[1], t[3])
    else:
        t[0] = Declaration(t[1])

def p_DeclarationExpression(t):
    '''DeclarationExpression : ValueList IN SetExpression
                             | ValueList IN Range
                             | NumericSymbolicExpression IN SetExpression
                             | NumericSymbolicExpression IN Range
                             | Identifier IN SetExpression
                             | Identifier IN Range
                             | ValueList IN Identifier
                             | NumericSymbolicExpression IN Identifier
                             | Identifier IN Identifier
                             | ValueList SUBSET SetExpression
                             | ValueList SUBSET Range
                             | NumericSymbolicExpression SUBSET SetExpression
                             | NumericSymbolicExpression SUBSET Range
                             | Identifier SUBSET SetExpression
                             | Identifier SUBSET Range
                             | ValueList SUBSET Identifier
                             | NumericSymbolicExpression SUBSET Identifier
                             | Identifier SUBSET Identifier
                             | ValueList DEFAULT NumericSymbolicExpression
                             | ValueList DEFAULT Identifier
                             | NumericSymbolicExpression DEFAULT NumericSymbolicExpression
                             | NumericSymbolicExpression DEFAULT Identifier
                             | Identifier DEFAULT NumericSymbolicExpression
                             | Identifier DEFAULT Identifier
                             | ValueList DEFAULT SetExpression
                             | ValueList DEFAULT Range
                             | NumericSymbolicExpression DEFAULT SetExpression
                             | NumericSymbolicExpression DEFAULT Range
                             | Identifier DEFAULT SetExpression
                             | Identifier DEFAULT Range
                             | ValueList DIMEN NumericSymbolicExpression
                             | ValueList DIMEN Identifier
                             | NumericSymbolicExpression DIMEN NumericSymbolicExpression
                             | NumericSymbolicExpression DIMEN Identifier
                             | Identifier DIMEN NumericSymbolicExpression
                             | Identifier DIMEN Identifier
                             | ValueList ASSIGN NumericSymbolicExpression
                             | ValueList ASSIGN Identifier
                             | NumericSymbolicExpression ASSIGN NumericSymbolicExpression
                             | NumericSymbolicExpression ASSIGN Identifier
                             | Identifier ASSIGN NumericSymbolicExpression
                             | Identifier ASSIGN Identifier
                             | ValueList ASSIGN SetExpression
                             | ValueList ASSIGN Range
                             | NumericSymbolicExpression ASSIGN SetExpression
                             | NumericSymbolicExpression ASSIGN Range
                             | Identifier ASSIGN SetExpression
                             | Identifier ASSIGN Range
                             | ValueList LE NumericSymbolicExpression
                             | ValueList LE Identifier
                             | ValueList GE NumericSymbolicExpression
                             | ValueList GE Identifier
                             | ValueList EQ NumericSymbolicExpression
                             | ValueList EQ Identifier
                             | ValueList LT NumericSymbolicExpression
                             | ValueList LT Identifier
                             | ValueList GT NumericSymbolicExpression
                             | ValueList GT Identifier
                             | ValueList NEQ NumericSymbolicExpression
                             | ValueList NEQ Identifier
                             | ValueList COMMA DeclarationAttributeList
                             | NumericSymbolicExpression COMMA DeclarationAttributeList
                             | Identifier COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList'''

    
    if isinstance(t[1], DeclarationExpression):
      if t.slice[2].type == "COMMA":
        t[1].addAttribute(t[3])
      else:
        t[1].addAttribute(t[2])

      t[0] = t[1]

    else:
      _type = t.slice[2].type

      attr = None
      if _type == "COMMA":
        attr = t[3]

      elif _type == "IN":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.IN)

      elif _type == "SUBSET":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.WT)

      elif _type == "DEFAULT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DF)

      elif _type == "DIMEN":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DM)

      elif _type == "ASSIGN":
        if isinstance(t[3], Range):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.ST)

      elif _type == "LT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LT)

      elif _type == "GT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GT)

      elif _type == "NEQ":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.NEQ)

      elif _type == "LE":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LE)

      elif _type == "GE":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GE)

      elif _type == "EQ":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.EQ)


      if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
        t[1] = ValueList([t[1]])

      t[0] = DeclarationExpression(t[1])
      t[0].addAttribute(attr)

def p_DeclarationAttributeList(t):
  '''DeclarationAttributeList : DeclarationAttribute
                              | DeclarationAttributeList COMMA DeclarationAttribute'''
  if len(t) > 3:
    t[0] = t[1] + [t[3]]
  else:
    t[0] = [t[1]]

def p_DeclarationAttribute(t):
  '''DeclarationAttribute : IN SetExpression
                          | IN Range
                          | IN Identifier
                          | SUBSET SetExpression
                          | SUBSET Range
                          | SUBSET Identifier
                          | DEFAULT NumericSymbolicExpression
                          | DEFAULT Identifier
                          | DEFAULT SetExpression
                          | DEFAULT Range
                          | DIMEN NumericSymbolicExpression
                          | DIMEN Identifier
                          | ASSIGN NumericSymbolicExpression
                          | ASSIGN Identifier
                          | ASSIGN SetExpression
                          | ASSIGN Range
                          | LT NumericSymbolicExpression
                          | LT Identifier
                          | LE NumericSymbolicExpression
                          | LE Identifier
                          | EQ NumericSymbolicExpression
                          | EQ Identifier
                          | GT NumericSymbolicExpression
                          | GT Identifier
                          | GE NumericSymbolicExpression
                          | GE Identifier
                          | NEQ NumericSymbolicExpression
                          | NEQ Identifier'''

  _type = t.slice[1].type
  if _type == "IN":
    if not isinstance(t[2], SetExpression):
      t[2] = SetExpressionWithValue(t[2])    

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.IN)

  elif _type == "SUBSET":
    if not isinstance(t[2], SetExpression):
      t[2] = SetExpressionWithValue(t[2])    

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.WT)

  elif _type == "DEFAULT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DF)

  elif _type == "DIMEN":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DM)

  elif _type == "ASSIGN":
    if isinstance(t[2], Range):
      t[2] = SetExpressionWithValue(t[2])

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.ST)

  elif _type == "LT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LT)

  elif _type == "LE":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LE)

  elif _type == "GT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GT)

  elif _type == "GE":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GE)

  elif _type == "NEQ":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.NEQ)

  elif _type == "EQ":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.EQ)


def p_LogicalExpression(t):
    '''LogicalExpression : EntryLogicalExpression
                         | LogicalExpression OR EntryLogicalExpression
                         | LogicalExpression OR ConnectedConstraintLogicalExpression
                         | LogicalExpression OR IteratedConstraintLogicalExpression
                         | LogicalExpression OR AllDiffExpression
                         | LogicalExpression OR EntryConstraintLogicalExpression
                         | LogicalExpression OR NumericSymbolicExpression
                         | LogicalExpression OR Identifier
                         | ConnectedConstraintLogicalExpression OR LogicalExpression
                         | ConnectedConstraintLogicalExpression OR NumericSymbolicExpression
                         | ConnectedConstraintLogicalExpression OR Identifier
                         | IteratedConstraintLogicalExpression OR LogicalExpression
                         | IteratedConstraintLogicalExpression OR NumericSymbolicExpression
                         | IteratedConstraintLogicalExpression OR Identifier
                         | AllDiffExpression OR LogicalExpression
                         | AllDiffExpression OR NumericSymbolicExpression
                         | AllDiffExpression OR Identifier
                         | EntryConstraintLogicalExpression OR LogicalExpression
                         | EntryConstraintLogicalExpression OR NumericSymbolicExpression
                         | EntryConstraintLogicalExpression OR Identifier
                         | NumericSymbolicExpression OR LogicalExpression
                         | NumericSymbolicExpression OR ConnectedConstraintLogicalExpression
                         | NumericSymbolicExpression OR IteratedConstraintLogicalExpression
                         | NumericSymbolicExpression OR AllDiffExpression
                         | NumericSymbolicExpression OR EntryConstraintLogicalExpression
                         | NumericSymbolicExpression OR NumericSymbolicExpression
                         | NumericSymbolicExpression OR Identifier
                         | Identifier OR LogicalExpression
                         | Identifier OR ConnectedConstraintLogicalExpression
                         | Identifier OR IteratedConstraintLogicalExpression
                         | Identifier OR AllDiffExpression
                         | Identifier OR EntryConstraintLogicalExpression
                         | Identifier OR NumericSymbolicExpression
                         | Identifier OR Identifier
                         | LogicalExpression AND EntryLogicalExpression
                         | LogicalExpression AND ConnectedConstraintLogicalExpression
                         | LogicalExpression AND IteratedConstraintLogicalExpression
                         | LogicalExpression AND AllDiffExpression
                         | LogicalExpression AND EntryConstraintLogicalExpression
                         | LogicalExpression AND NumericSymbolicExpression
                         | LogicalExpression AND Identifier
                         | ConnectedConstraintLogicalExpression AND LogicalExpression
                         | ConnectedConstraintLogicalExpression AND NumericSymbolicExpression
                         | ConnectedConstraintLogicalExpression AND Identifier
                         | IteratedConstraintLogicalExpression AND LogicalExpression
                         | IteratedConstraintLogicalExpression AND NumericSymbolicExpression
                         | IteratedConstraintLogicalExpression AND Identifier
                         | AllDiffExpression AND LogicalExpression
                         | AllDiffExpression AND NumericSymbolicExpression
                         | AllDiffExpression AND Identifier
                         | EntryConstraintLogicalExpression AND LogicalExpression
                         | EntryConstraintLogicalExpression AND NumericSymbolicExpression
                         | EntryConstraintLogicalExpression AND Identifier
                         | NumericSymbolicExpression AND LogicalExpression
                         | NumericSymbolicExpression AND ConnectedConstraintLogicalExpression
                         | NumericSymbolicExpression AND IteratedConstraintLogicalExpression
                         | NumericSymbolicExpression AND AllDiffExpression
                         | NumericSymbolicExpression AND EntryConstraintLogicalExpression
                         | NumericSymbolicExpression AND NumericSymbolicExpression
                         | NumericSymbolicExpression AND Identifier
                         | Identifier AND LogicalExpression
                         | Identifier AND ConnectedConstraintLogicalExpression
                         | Identifier AND IteratedConstraintLogicalExpression
                         | Identifier AND AllDiffExpression
                         | Identifier AND EntryConstraintLogicalExpression
                         | Identifier AND NumericSymbolicExpression
                         | Identifier AND Identifier'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])

    if not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    if len(t) > 3:
      if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
        t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

      if t.slice[2].type == "AND":
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])

    else:
        t[0] = t[1]

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NOT NumericSymbolicExpression
                              | NOT Identifier
                              | NOT LogicalExpression
                              | LPAREN LogicalExpression RPAREN'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    _type = t.slice[1].type
    if _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    elif _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    else:
      t[0] = t[2]


def p_AllDiffExpression(t):
    '''AllDiffExpression : ALLDIFF LLBRACE IndexingExpression RRBRACE Identifier
                         | ALLDIFF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                         | LPAREN AllDiffExpression RPAREN
                         | NOT AllDiffExpression'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:
      t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.ALLDIFF, t[3], t[5])

def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList IN SetExpression
                              | ValueList IN Range
                              | NumericSymbolicExpression IN SetExpression
                              | NumericSymbolicExpression IN Range
                              | Identifier IN SetExpression
                              | Identifier IN Range
                              | ValueList IN Identifier
                              | NumericSymbolicExpression IN Identifier
                              | Identifier IN Identifier
                              | Tuple IN SetExpression
                              | Tuple IN Range
                              | Tuple IN Identifier
                              | ValueList NOTIN SetExpression
                              | ValueList NOTIN Range
                              | NumericSymbolicExpression NOTIN SetExpression
                              | NumericSymbolicExpression NOTIN Range
                              | Identifier NOTIN SetExpression
                              | Identifier NOTIN Range
                              | ValueList NOTIN Identifier
                              | NumericSymbolicExpression NOTIN Identifier
                              | Identifier NOTIN Identifier
                              | Tuple NOTIN SetExpression
                              | Tuple NOTIN Range
                              | Tuple NOTIN Identifier
                              | SetExpression SUBSET SetExpression
                              | Range SUBSET Range
                              | Identifier SUBSET SetExpression
                              | Identifier SUBSET Range
                              | SetExpression SUBSET Identifier
                              | Range SUBSET Identifier
                              | SetExpression NOTSUBSET SetExpression
                              | Range NOTSUBSET Range
                              | Identifier NOTSUBSET SetExpression
                              | Identifier NOTSUBSET Range
                              | SetExpression NOTSUBSET Identifier
                              | Range NOTSUBSET Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], ValueList):
      t[1] = ValueList([t[1]])

    _type = t.slice[2].type
    if _type == "IN":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])

    elif _type == "NOTIN":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.NOTIN, t[1], t[3])

    elif _type == "SUBSET":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])

    elif _type == "NOTSUBSET":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.NOTSUBSET, t[1], t[3])

def p_EntryIteratedLogicalExpression(t):
    '''EntryLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | FORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | NFORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | EXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | NEXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression'''

    if isinstance(t[5], Identifier) or isinstance(t[5], NumericExpression) or isinstance(t[5], SymbolicExpression):
      t[5] = EntryLogicalExpressionNumericOrSymbolic(t[5])

    if not isinstance(t[5], LogicalExpression):
      t[5] = LogicalExpression([t[5]])

    _type = t.slice[1].type
    if _type == "FORALL":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])

    elif _type == "NFORALL":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])

    elif _type == "EXISTS":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

    elif _type == "NEXISTS":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])


def p_SetExpressionWithOperation(t):
    '''SetExpression : Identifier DIFF Identifier
                     | SetExpression DIFF SetExpression
                     | Range DIFF Range
                     | Identifier DIFF SetExpression
                     | Identifier DIFF Range
                     | SetExpression DIFF Identifier
                     | Range DIFF Identifier
                     | SetExpression SYMDIFF SetExpression
                     | Range SYMDIFF Range
                     | Identifier SYMDIFF Identifier
                     | Identifier SYMDIFF SetExpression
                     | Identifier SYMDIFF Range
                     | SetExpression SYMDIFF Identifier
                     | Range SYMDIFF Identifier
                     | SetExpression UNION SetExpression
                     | Range UNION Range
                     | Identifier UNION Identifier
                     | Identifier UNION SetExpression
                     | Identifier UNION Range
                     | SetExpression UNION Identifier
                     | Range UNION Identifier
                     | SetExpression INTER SetExpression
                     | Range INTER Range
                     | Identifier INTER Identifier
                     | Identifier INTER SetExpression
                     | Identifier INTER Range
                     | SetExpression INTER Identifier
                     | Range INTER Identifier
                     | SetExpression CROSS SetExpression
                     | Range CROSS Range
                     | Identifier CROSS Identifier
                     | Identifier CROSS SetExpression
                     | Identifier CROSS Range
                     | SetExpression CROSS Identifier
                     | Range CROSS Identifier'''

    _type = t.slice[2].type
    if _type == "DIFF":
        op = SetExpressionWithOperation.DIFF

    elif _type == "SYMDIFF":
        op = SetExpressionWithOperation.SYMDIFF

    elif _type == "UNION":
        op = SetExpressionWithOperation.UNION

    elif _type == "INTER":
        op = SetExpressionWithOperation.INTER

    elif _type == "CROSS":
        op = SetExpressionWithOperation.CROSS

    if not isinstance(t[1], SetExpression):
      t[1] = SetExpressionWithValue(t[1])

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    t[0] = SetExpressionWithOperation(op, t[1], t[3])

def p_SetExpressionWithValue(t):
    '''SetExpression : LLBRACE ValueList RRBRACE
                     | LLBRACE NumericSymbolicExpression RRBRACE
                     | LLBRACE Identifier RRBRACE
                     | LLBRACE Range RRBRACE
                     | LLBRACE SetExpression RRBRACE
                     | LLBRACE TupleList RRBRACE
                     | LLBRACE IndexingExpression RRBRACE
                     | LLBRACE RRBRACE
                     | LPAREN SetExpression RPAREN
                     | LPAREN Range RPAREN
                     | EMPTYSET
                     | NATURALSET
                     | NATURALSETWITHONELIMIT
                     | NATURALSETWITHTWOLIMITS
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
                     | SYMBOLIC
                     | LOGICAL
                     | PARAMETERS
                     | SETS
                     | VARIABLES
                     | ConditionalSetExpression'''

    _type = t.slice[1].type
    if len(t) > 2:

        if isinstance(t[1], str) and _type == "LLBRACE":

          if not (isinstance(t[2], str) and t.slice[2].type == "RRBRACE"):
            if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
              t[2] = ValueList([t[2]])

            t[0] = SetExpressionBetweenBraces(SetExpressionWithValue(t[2]))

          else:
            t[0] = SetExpressionBetweenBraces(None)

        elif _type == "LPAREN":
          t[0] = SetExpressionBetweenParenthesis(t[2])

        else:
          if not isinstance(t[2], SetExpression):
            t[2] = SetExpressionWithValue(t[2])

          t[0] = SetExpressionWithValue(t[2])

    elif _type == "EMPTYSET":
        t[0] = SetExpressionBetweenBraces(None)

    else:

        if t.slice[1].type == "ConditionalSetExpression":
          t[0] = t[1]

        else:
          value = t[1]
          if hasattr(t.slice[1], 'value2'):
            value = t.slice[1].value2
          
          t[0] = SetExpressionWithValue(value)


def p_SetExpressionWithIndices(t):
    '''SetExpression : Identifier LBRACKET ValueList RBRACKET
                     | Identifier LBRACKET NumericSymbolicExpression RBRACKET
                     | Identifier LBRACKET Identifier RBRACKET'''

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = ValueList([t[3]])

    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE Identifier
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression'''
    
    _type = t.slice[1].type
    if _type == "UNION":

      if len(t) > 7:
        t[0] = IteratedSetExpression(IteratedSetExpression.UNION, t[4], t[10], t[8])
      else:
        t[0] = IteratedSetExpression(IteratedSetExpression.UNION, t[4], t[6])

    elif _type == "INTER":

      if len(t) > 7:
        t[0] = IteratedSetExpression(IteratedSetExpression.INTER, t[4], t[10], t[8])
      else:
        t[0] = IteratedSetExpression(IteratedSetExpression.INTER, t[4], t[6])

    else:
      t[0] = IteratedSetExpression(IteratedSetExpression.SETOF, t[3], t[5])


def p_ConditionalSetExpression(t):
    '''ConditionalSetExpression : IF Identifier THEN SetExpression ELSE SetExpression
                                | IF Identifier THEN SetExpression ELSE Identifier
                                | IF Identifier THEN Identifier ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression ELSE Identifier
                                | IF NumericSymbolicExpression THEN Identifier ELSE SetExpression
                                | IF LogicalExpression THEN SetExpression ELSE SetExpression
                                | IF LogicalExpression THEN SetExpression ELSE Identifier
                                | IF LogicalExpression THEN Identifier ELSE SetExpression
                                | IF ConnectedConstraintLogicalExpression THEN SetExpression ELSE SetExpression
                                | IF ConnectedConstraintLogicalExpression THEN SetExpression ELSE Identifier
                                | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE SetExpression
                                | IF IteratedConstraintLogicalExpression THEN SetExpression ELSE SetExpression
                                | IF IteratedConstraintLogicalExpression THEN SetExpression ELSE Identifier
                                | IF IteratedConstraintLogicalExpression THEN Identifier ELSE SetExpression
                                | IF AllDiffExpression THEN SetExpression ELSE SetExpression
                                | IF AllDiffExpression THEN SetExpression ELSE Identifier
                                | IF AllDiffExpression THEN Identifier ELSE SetExpression
                                | IF EntryConstraintLogicalExpression THEN SetExpression ELSE SetExpression
                                | IF EntryConstraintLogicalExpression THEN SetExpression ELSE Identifier
                                | IF EntryConstraintLogicalExpression THEN Identifier ELSE SetExpression
                                | IF Identifier THEN SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression
                                | IF LogicalExpression THEN SetExpression
                                | IF ConnectedConstraintLogicalExpression THEN SetExpression
                                | IF IteratedConstraintLogicalExpression THEN SetExpression
                                | IF AllDiffExpression THEN SetExpression
                                | IF EntryConstraintLogicalExpression THEN SetExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
    
    if isinstance(t[4], Identifier):
      t[4] = SetExpressionWithValue(t[4])

    if len(t) > 5 and isinstance(t[6], Identifier):
      t[6] = SetExpressionWithValue(t[6])

    t[0] = ConditionalSetExpression(t[2], t[4])

    if len(t) > 5:
      t[0].addElseExpression(t[6])



def p_IndexingExpression(t):
    '''IndexingExpression : EntryIndexingExpression
                          | LogicalIndexExpression
                          | IndexingExpression PIPE LogicalExpression
                          | IndexingExpression PIPE ConnectedConstraintLogicalExpression
                          | IndexingExpression PIPE IteratedConstraintLogicalExpression
                          | IndexingExpression PIPE AllDiffExpression
                          | IndexingExpression PIPE EntryConstraintLogicalExpression
                          | IndexingExpression PIPE NumericSymbolicExpression
                          | IndexingExpression PIPE Identifier
                          | IndexingExpression COMMA EntryIndexingExpression'''

    if len(t) > 3:

        if t.slice[2].type == "PIPE":

            if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
              t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

            if not isinstance(t[3], LogicalExpression):
              t[3] = LogicalExpression([t[3]])

            t[0] = t[1].setLogicalExpression(t[3])

        else:
            t[0] = t[1].add(t[3])

    else:
        t[0] = IndexingExpression([t[1]])

def p_LogicalIndexExpression(t):
    '''LogicalIndexExpression : IF Identifier
                              | IF NumericSymbolicExpression
                              | IF LogicalExpression
                              | IF ConnectedConstraintLogicalExpression
                              | IF IteratedConstraintLogicalExpression
                              | IF AllDiffExpression
                              | IF EntryConstraintLogicalExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])

    t[0] = ConditionalLinearExpression(t[2])

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | ValueList IN Range
                               | NumericSymbolicExpression IN SetExpression
                               | NumericSymbolicExpression IN Range
                               | Identifier IN SetExpression
                               | Identifier IN Range
                               | ValueList IN Identifier
                               | NumericSymbolicExpression IN Identifier
                               | Identifier IN Identifier
                               | Tuple IN SetExpression
                               | Tuple IN Range
                               | Tuple IN Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])

    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Identifier EQ NumericSymbolicExpression
                               | Identifier EQ Identifier
                               | Identifier EQ Range
                               | Identifier NEQ NumericSymbolicExpression
                               | Identifier NEQ Identifier
                               | Identifier LE NumericSymbolicExpression
                               | Identifier LE Identifier
                               | Identifier GE NumericSymbolicExpression
                               | Identifier GE Identifier
                               | Identifier LT NumericSymbolicExpression
                               | Identifier LT Identifier
                               | Identifier GT NumericSymbolicExpression
                               | Identifier GT Identifier'''

    _type = t.slice[2].type
    if _type == "EQ":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.EQ, t[1], t[3])

    elif _type == "NEQ":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.NEQ, t[1], t[3])

    elif _type == "LE":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LE, t[1], t[3])

    elif _type == "GE":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GE, t[1], t[3])

    elif _type == "LT":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LT, t[1], t[3])

    elif _type == "GT":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GT, t[1], t[3])


def p_StringSymbolicExpression(t):
    '''SymbolicExpression : STRING'''
    t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : NumericSymbolicExpression AMPERSAND NumericSymbolicExpression
                          | NumericSymbolicExpression AMPERSAND Identifier
                          | Identifier AMPERSAND NumericSymbolicExpression
                          | Identifier AMPERSAND Identifier'''

    if t.slice[2].type == "AMPERSAND":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

def p_FunctionSymbolicExpression(t):
    '''SymbolicExpression : SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier RPAREN
                          | ALIAS LPAREN Identifier RPAREN
                          | CHAR LPAREN NumericSymbolicExpression RPAREN
                          | CHAR LPAREN Identifier RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA ValueList RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SPRINTF LPAREN Identifier COMMA ValueList RPAREN
                          | SPRINTF LPAREN Identifier COMMA Identifier RPAREN
                          | SPRINTF LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | CTIME LPAREN NumericSymbolicExpression RPAREN
                          | CTIME LPAREN Identifier RPAREN
                          | CTIME LPAREN RPAREN'''

    _type = t.slice[1].type

    if _type == "SUBSTR":
        op = SymbolicExpressionWithFunction.SUBSTR

    elif _type == "TIME2STR":
        op = SymbolicExpressionWithFunction.TIME2STR

    elif _type == "ALIAS":
        op = SymbolicExpressionWithFunction.ALIAS

    elif _type == "CTIME":
        op = SymbolicExpressionWithFunction.CTIME

    elif _type == "CHAR":
        op = SymbolicExpressionWithFunction.CHAR

    elif _type == "SPRINTF":
        op = SymbolicExpressionWithFunction.SPRINTF

    elif _type == "SUB":
        op = SymbolicExpressionWithFunction.SUB

    elif _type == "GSUB":
        op = SymbolicExpressionWithFunction.GSUB

    if len(t) > 7:
        t[0] = SymbolicExpressionWithFunction(op, t[3], t[5], t[7])

    elif len(t) > 5:
        t[0] = SymbolicExpressionWithFunction(op, t[3], t[5])

    elif len(t) > 4:
        t[0] = SymbolicExpressionWithFunction(op, t[3])

    else:

        if isinstance(t[3], str) and t.slice[3].type == "RPAREN":
          t[0] = SymbolicExpressionWithFunction(op)
        else:
          t[0] = SymbolicExpressionWithFunction(op, t[3])


def p_NumericSymbolicExpression(t):
    '''NumericSymbolicExpression : NumericExpression
                                 | SymbolicExpression
                                 | LPAREN NumericSymbolicExpression RPAREN'''

    if len(t) > 2:
        t[0] = NumericExpressionBetweenParenthesis(t[2])

    else:
        t[0] = t[1]

def p_NumericExpression_binop(t):
    '''NumericExpression : NumericSymbolicExpression PLUS NumericSymbolicExpression
                         | NumericSymbolicExpression PLUS Identifier
                         | Identifier PLUS NumericSymbolicExpression
                         | Identifier PLUS Identifier
                         | NumericSymbolicExpression MINUS NumericSymbolicExpression
                         | NumericSymbolicExpression MINUS Identifier
                         | Identifier MINUS NumericSymbolicExpression
                         | Identifier MINUS Identifier
                         | NumericSymbolicExpression TIMES NumericSymbolicExpression
                         | NumericSymbolicExpression TIMES Identifier
                         | Identifier TIMES NumericSymbolicExpression
                         | Identifier TIMES Identifier
                         | NumericSymbolicExpression DIVIDE NumericSymbolicExpression
                         | NumericSymbolicExpression DIVIDE Identifier
                         | Identifier DIVIDE NumericSymbolicExpression
                         | Identifier DIVIDE Identifier
                         | NumericSymbolicExpression MOD NumericSymbolicExpression
                         | NumericSymbolicExpression MOD Identifier
                         | Identifier MOD NumericSymbolicExpression
                         | Identifier MOD Identifier
                         | NumericSymbolicExpression QUOTIENT NumericSymbolicExpression
                         | NumericSymbolicExpression QUOTIENT Identifier
                         | Identifier QUOTIENT NumericSymbolicExpression
                         | Identifier QUOTIENT Identifier
                         | NumericSymbolicExpression LESS NumericSymbolicExpression
                         | NumericSymbolicExpression LESS Identifier
                         | Identifier LESS NumericSymbolicExpression
                         | Identifier LESS Identifier
                         | NumericSymbolicExpression CARET LBRACE NumericSymbolicExpression RBRACE
                         | NumericSymbolicExpression CARET LBRACE Identifier RBRACE
                         | Identifier CARET LBRACE NumericSymbolicExpression RBRACE
                         | Identifier CARET LBRACE Identifier RBRACE'''

    _type = t.slice[2].type
    if _type == "PLUS":
        op = NumericExpressionWithArithmeticOperation.PLUS

    elif _type == "MINUS":
        op = NumericExpressionWithArithmeticOperation.MINUS

    elif _type == "TIMES":
        op = NumericExpressionWithArithmeticOperation.TIMES

    elif _type == "QUOTIENT":
        op = NumericExpressionWithArithmeticOperation.QUOT

    elif _type == "DIVIDE":
        op = NumericExpressionWithArithmeticOperation.DIV

    elif _type == "MOD":
        op = NumericExpressionWithArithmeticOperation.MOD

    elif _type == "CARET":
        op = NumericExpressionWithArithmeticOperation.POW

    elif _type == "LESS":
        op = NumericExpressionWithArithmeticOperation.LESS

    if len(t) > 4 and isinstance(t[4], Identifier):
      t[4] = ValuedNumericExpression(t[4])

    elif len(t) > 3 and isinstance(t[3], Identifier):
      t[3] = ValuedNumericExpression(t[3])

    elif isinstance(t[1], Identifier):
      t[1] = ValuedNumericExpression(t[1])

    if _type == "CARET":
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[4])
    else:
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

def p_IteratedNumericExpression(t):
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE Identifier'''

    _type = t.slice[1].type
    if _type == "SUM":
        op = IteratedNumericExpression.SUM
    elif _type == "PROD":
        op = IteratedNumericExpression.PROD
    elif _type == "MAX":
        op = IteratedNumericExpression.MAX
    elif _type == "MIN":
        op = IteratedNumericExpression.MIN

    if len(t) > 7:
        if isinstance(t[8], Identifier):
          t[8] = ValuedNumericExpression(t[8])

        if isinstance(t[10], Identifier):
          t[10] = ValuedNumericExpression(t[10])

        t[0] = IteratedNumericExpression(op, t[10], t[4], t[8])
    else:
        if isinstance(t[6], Identifier):
          t[6] = ValuedNumericExpression(t[6])

        t[0] = IteratedNumericExpression(op, t[6], t[4])


def p_IteratedNumericExpression2(t):
    '''NumericExpression : COUNT LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | COUNT LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | COUNT LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | COUNT LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | COUNT LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | NUMBEROF Identifier IN LPAREN LLBRACE IndexingExpression RRBRACE Identifier RPAREN
                         | NUMBEROF Identifier IN LPAREN LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression RPAREN
                         | NUMBEROF NumericSymbolicExpression IN LPAREN LLBRACE IndexingExpression RRBRACE Identifier RPAREN
                         | NUMBEROF NumericSymbolicExpression IN LPAREN LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression RPAREN'''

    if t.slice[1].type == "NUMBEROF":

      if isinstance(t[2], Identifier):
        t[2] = ValuedNumericExpression(t[2])

      t[0] = IteratedNumericExpression2(IteratedNumericExpression2.NUMBEROF, t[8], t[6], t[2])      

    elif len(t) > 6:
        if isinstance(t[2], Identifier):
          t[2] = ValuedNumericExpression(t[2])

        op = None
        _type = t.slice[1].type
        if _type == "ATMOST":
          op = IteratedNumericExpression2.ATMOST

        elif _type == "ATLEAST":
          op = IteratedNumericExpression2.ATLEAST

        elif _type == "EXACTLY":
          op = IteratedNumericExpression2.EXACTLY

        t[0] = IteratedNumericExpression2(op, t[6], t[4], t[2])

    else:
        t[0] = IteratedNumericExpression2(IteratedNumericExpression2.COUNT, t[5], t[3])


def p_NumericExpression(t):
    '''NumericExpression : MINUS NumericSymbolicExpression %prec UMINUS
                         | MINUS Identifier %prec UMINUS
                         | PLUS NumericSymbolicExpression %prec UPLUS
                         | PLUS Identifier %prec UPLUS
                         | LPAREN Identifier RPAREN
                         | ConditionalNumericExpression
                         | NUMBER
                         | INFINITY'''

    if len(t) > 2 and isinstance(t[2], Identifier):
      t[2] = ValuedNumericExpression(t[2])

    if len(t) > 3:
      t[0] = NumericExpressionBetweenParenthesis(t[2])

    elif t.slice[1].type == "PLUS":
      t[0] = t[2]

    elif t.slice[1].type == "MINUS":
      t[0] = MinusNumericExpression(t[2])

    elif isinstance(t[1], ConditionalNumericExpression):
      t[0] = t[1]

    else:
      t[0] = ValuedNumericExpression(t[1])

def p_FractionalNumericExpression(t):
    '''NumericExpression : FRAC LBRACE Identifier RBRACE LBRACE Identifier RBRACE
                         | FRAC LBRACE Identifier RBRACE LBRACE NumericSymbolicExpression RBRACE
                         | FRAC LBRACE NumericSymbolicExpression RBRACE LBRACE Identifier RBRACE
                         | FRAC LBRACE NumericSymbolicExpression RBRACE LBRACE NumericSymbolicExpression RBRACE'''
    t[0] = FractionalNumericExpression(t[3], t[6])

def p_FunctionNumericExpression(t):
    '''NumericExpression : SQRT LBRACE NumericSymbolicExpression RBRACE
                         | SQRT LBRACE Identifier RBRACE
                         | LFLOOR NumericSymbolicExpression RFLOOR
                         | LFLOOR Identifier RFLOOR
                         | LCEIL NumericSymbolicExpression RCEIL
                         | LCEIL Identifier RCEIL
                         | PIPE NumericSymbolicExpression PIPE
                         | PIPE Identifier PIPE
                         | MAX LPAREN ValueList RPAREN
                         | MAX LPAREN NumericSymbolicExpression RPAREN
                         | MAX LPAREN Identifier RPAREN
                         | MIN LPAREN ValueList RPAREN
                         | MIN LPAREN NumericSymbolicExpression RPAREN
                         | MIN LPAREN Identifier RPAREN
                         | ASIN LPAREN NumericSymbolicExpression RPAREN
                         | ASIN LPAREN Identifier RPAREN
                         | SIN LPAREN NumericSymbolicExpression RPAREN
                         | SIN LPAREN Identifier RPAREN
                         | ASINH LPAREN NumericSymbolicExpression RPAREN
                         | ASINH LPAREN Identifier RPAREN
                         | SINH LPAREN NumericSymbolicExpression RPAREN
                         | SINH LPAREN Identifier RPAREN
                         | ACOS LPAREN NumericSymbolicExpression RPAREN
                         | ACOS LPAREN Identifier RPAREN
                         | COS LPAREN NumericSymbolicExpression RPAREN
                         | COS LPAREN Identifier RPAREN
                         | ACOSH LPAREN NumericSymbolicExpression RPAREN
                         | ACOSH LPAREN Identifier RPAREN
                         | COSH LPAREN NumericSymbolicExpression RPAREN
                         | COSH LPAREN Identifier RPAREN
                         | LOG LPAREN NumericSymbolicExpression RPAREN
                         | LOG LPAREN Identifier RPAREN
                         | LN LPAREN NumericSymbolicExpression RPAREN
                         | LN LPAREN Identifier RPAREN
                         | EXP LPAREN NumericSymbolicExpression RPAREN
                         | EXP LPAREN Identifier RPAREN
                         | TANH LPAREN NumericSymbolicExpression RPAREN
                         | TANH LPAREN Identifier RPAREN
                         | TAN LPAREN NumericSymbolicExpression RPAREN
                         | TAN LPAREN Identifier RPAREN
                         | ARCTANH LPAREN NumericSymbolicExpression RPAREN
                         | ARCTANH LPAREN Identifier RPAREN
                         | ARCTAN LPAREN NumericSymbolicExpression RPAREN
                         | ARCTAN LPAREN Identifier RPAREN
                         | ARCTAN LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | ARCTAN LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | ARCTAN LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | ARCTAN LPAREN Identifier COMMA Identifier RPAREN
                         | CARD LPAREN SetExpression RPAREN
                         | CARD LPAREN Range RPAREN
                         | CARD LPAREN Identifier RPAREN
                         | LENGTH LPAREN Identifier RPAREN
                         | ROUND LPAREN NumericSymbolicExpression RPAREN
                         | ROUND LPAREN Identifier RPAREN
                         | ROUND LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | ROUND LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | ROUND LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | ROUND LPAREN Identifier COMMA Identifier RPAREN
                         | PRECISION LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | PRECISION LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | PRECISION LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | PRECISION LPAREN Identifier COMMA Identifier RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression RPAREN
                         | TRUNC LPAREN Identifier RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | TRUNC LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | TRUNC LPAREN Identifier COMMA Identifier RPAREN
                         | NUM LPAREN SymbolicExpression RPAREN
                         | NUM LPAREN Identifier RPAREN
                         | NUM0 LPAREN SymbolicExpression RPAREN
                         | NUM0 LPAREN Identifier RPAREN
                         | ICHAR LPAREN SymbolicExpression RPAREN
                         | ICHAR LPAREN Identifier RPAREN
                         | MATCH LPAREN SymbolicExpression COMMA SymbolicExpression RPAREN
                         | MATCH LPAREN SymbolicExpression COMMA Identifier RPAREN
                         | MATCH LPAREN Identifier COMMA SymbolicExpression RPAREN
                         | MATCH LPAREN Identifier COMMA Identifier RPAREN
                         | UNIFORM LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | UNIFORM LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | UNIFORM LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | UNIFORM LPAREN Identifier COMMA Identifier RPAREN
                         | NORMAL LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | NORMAL LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | NORMAL LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | NORMAL LPAREN Identifier COMMA Identifier RPAREN
                         | BETA LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | BETA LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | BETA LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | BETA LPAREN Identifier COMMA Identifier RPAREN
                         | GAMMA LPAREN NumericSymbolicExpression RPAREN
                         | GAMMA LPAREN Identifier RPAREN
                         | POISSON LPAREN NumericSymbolicExpression RPAREN
                         | POISSON LPAREN Identifier RPAREN
                         | IRAND224 LPAREN RPAREN
                         | UNIFORM01 LPAREN RPAREN
                         | NORMAL01 LPAREN RPAREN
                         | CAUCHY LPAREN RPAREN
                         | EXPONENTIAL LPAREN RPAREN
                         | TIME LPAREN RPAREN
                         | ID LPAREN Identifier RPAREN
                         | ID LPAREN NumericSymbolicExpression RPAREN
                         | ID LPAREN ValueList RPAREN
                         | ID LPAREN RPAREN'''

    _type = t.slice[1].type
    if _type == "ID":
        op = ID(t[1])

    elif _type == "CARD":
        op = NumericExpressionWithFunction.CARD

        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

    elif _type == "LENGTH":
        op = NumericExpressionWithFunction.LENGTH

    elif _type == "ROUND":
        op = NumericExpressionWithFunction.ROUND

    elif _type == "PRECISION":
        op = NumericExpressionWithFunction.PRECISION

    elif _type == "TRUNC":
        op = NumericExpressionWithFunction.TRUNC

    elif _type == "SQRT":
        op = NumericExpressionWithFunction.SQRT

    elif _type == "LFLOOR":
        op = NumericExpressionWithFunction.FLOOR

    elif _type == "LCEIL":
        op = NumericExpressionWithFunction.CEIL

    elif _type == "PIPE":
        op = NumericExpressionWithFunction.ABS

    elif _type == "MAX":
        op = NumericExpressionWithFunction.MAX

    elif _type == "MIN":
        op = NumericExpressionWithFunction.MIN

    elif _type == "ASINH":
        op = NumericExpressionWithFunction.ASINH

    elif _type == "SINH":
        op = NumericExpressionWithFunction.SINH

    elif _type == "ASIN":
        op = NumericExpressionWithFunction.ASIN

    elif _type == "SIN":
        op = NumericExpressionWithFunction.SIN

    elif _type == "ACOSH":
        op = NumericExpressionWithFunction.ACOSH

    elif _type == "COSH":
        op = NumericExpressionWithFunction.COSH

    elif _type == "ACOS":
        op = NumericExpressionWithFunction.ACOS

    elif _type == "COS":
        op = NumericExpressionWithFunction.COS

    elif _type == "LOG":
        op = NumericExpressionWithFunction.LOG10

    elif _type == "LN":
        op = NumericExpressionWithFunction.LOG

    elif _type == "EXP":
        op = NumericExpressionWithFunction.EXP

    elif _type == "ARCTANH":
        op = NumericExpressionWithFunction.ATANH

    elif _type == "TANH":
        op = NumericExpressionWithFunction.TANH

    elif _type == "ARCTAN":
        if len(t) > 5:
          op = NumericExpressionWithFunction.ATAN2
        else:
          op = NumericExpressionWithFunction.ATAN

    elif _type == "TAN":
        op = NumericExpressionWithFunction.TAN

    elif _type == "UNIFORM01":
        op = NumericExpressionWithFunction.UNIFORM01

    elif _type == "UNIFORM":
        op = NumericExpressionWithFunction.UNIFORM

    elif _type == "NORMAL01":
        op = NumericExpressionWithFunction.NORMAL01

    elif _type == "NORMAL":
        op = NumericExpressionWithFunction.NORMAL

    elif _type == "CAUCHY":
        op = NumericExpressionWithFunction.CAUCHY

    elif _type == "EXPONENTIAL":
        op = NumericExpressionWithFunction.EXPONENTIAL

    elif _type == "BETA":
        op = NumericExpressionWithFunction.BETA

    elif _type == "GAMMA":
        op = NumericExpressionWithFunction.GAMMA

    elif _type == "POISSON":
        op = NumericExpressionWithFunction.POISSON

    elif _type == "GMTIME":
        op = NumericExpressionWithFunction.GMTIME

    elif _type == "TIME":
        op = NumericExpressionWithFunction.TIME

    elif _type == "IRAND224":
        op = NumericExpressionWithFunction.IRAND224

    elif _type == "STR2TIME":
        op = NumericExpressionWithFunction.STR2TIME

    elif _type == "NUM0":
        op = NumericExpressionWithFunction.NUM0

    elif _type == "NUM":
        op = NumericExpressionWithFunction.NUM

    elif _type == "ICHAR":
        op = NumericExpressionWithFunction.ICHAR

    elif _type == "MATCH":
        op = NumericExpressionWithFunction.MATCH

    if len(t) > 5:
        t[0] = NumericExpressionWithFunction(op, t[3], t[5])

    elif len(t) > 4:
        t[0] = NumericExpressionWithFunction(op, t[3])

    else:
        if isinstance(t[2], str) and t.slice[2].type == "LPAREN":
          t[0] = NumericExpressionWithFunction(op)
        else:
          t[0] = NumericExpressionWithFunction(op, t[2])

def p_ConditionalNumericExpression(t):
    '''ConditionalNumericExpression : IF Identifier THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF Identifier THEN NumericSymbolicExpression ELSE Identifier
                                    | IF Identifier THEN Identifier ELSE NumericSymbolicExpression
                                    | IF Identifier THEN Identifier ELSE Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF NumericSymbolicExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN Identifier ELSE Identifier
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF LogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF LogicalExpression THEN Identifier ELSE Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF ConnectedConstraintLogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF IteratedConstraintLogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF IteratedConstraintLogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF IteratedConstraintLogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF IteratedConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF AllDiffExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF AllDiffExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF AllDiffExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF AllDiffExpression THEN Identifier ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF Identifier THEN NumericSymbolicExpression
                                    | IF Identifier THEN Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN Identifier
                                    | IF LogicalExpression THEN NumericSymbolicExpression
                                    | IF LogicalExpression THEN Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN NumericSymbolicExpression
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier
                                    | IF IteratedConstraintLogicalExpression THEN NumericSymbolicExpression
                                    | IF IteratedConstraintLogicalExpression THEN Identifier
                                    | IF AllDiffExpression THEN NumericSymbolicExpression
                                    | IF AllDiffExpression THEN Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression
                                    | IF EntryConstraintLogicalExpression THEN Identifier'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
    
    if isinstance(t[4], Identifier):
      t[4] = ValuedNumericExpression(t[4])

    if len(t) > 5 and isinstance(t[6], Identifier):
      t[6] = ValuedNumericExpression(t[6])

    t[0] = ConditionalNumericExpression(t[2], t[4])

    if len(t) > 5:
      t[0].addElseExpression(t[6])

def p_Range(t):
    '''Range : NumericSymbolicExpression DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS NumericSymbolicExpression BY Identifier
             | NumericSymbolicExpression DOTS Identifier BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS Identifier BY Identifier
             | Identifier DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | Identifier DOTS NumericSymbolicExpression BY Identifier
             | Identifier DOTS Identifier BY NumericSymbolicExpression
             | Identifier DOTS Identifier BY Identifier
             | NumericSymbolicExpression DOTS NumericSymbolicExpression
             | NumericSymbolicExpression DOTS Identifier
             | Identifier DOTS NumericSymbolicExpression
             | Identifier DOTS Identifier'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

def p_Identifier(t):
    '''Identifier : ID UNDERLINE LBRACE ValueList RBRACE
                  | ID UNDERLINE LBRACE NumericSymbolicExpression RBRACE
                  | ID UNDERLINE LBRACE Identifier RBRACE
                  | ID LBRACKET ValueList RBRACKET
                  | ID LBRACKET NumericSymbolicExpression RBRACKET
                  | ID LBRACKET Identifier RBRACKET
                  | ID'''

    if len(t) > 5:
        if isinstance(t[4], ValueList):
          t[0] = Identifier(ID(t[1]), t[4].getValues())
        else:
          t[0] = Identifier(ID(t[1]), [t[4]])
    elif len(t) > 2:
        if isinstance(t[3], ValueList):
          t[0] = Identifier(ID(t[1]), t[3].getValues())
        else:
          t[0] = Identifier(ID(t[1]), [t[3]])
    else:
        t[0] = Identifier(ID(t[1]))

def p_ValueList(t):
    '''ValueList : ValueList COMMA NumericSymbolicExpression
                 | ValueList COMMA Identifier
                 | NumericSymbolicExpression COMMA NumericSymbolicExpression
                 | NumericSymbolicExpression COMMA Identifier
                 | Identifier COMMA NumericSymbolicExpression
                 | Identifier COMMA Identifier'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([t[1],t[3]])
    else:
        t[0] = t[1].add(t[3])

def p_Tuple(t):
    '''Tuple : LPAREN ValueList RPAREN'''

    if isinstance(t[2], ValueList):
      t[0] = Tuple(t[2].getValues())
    else:
      t[0] = Tuple([t[2]])

def p_TupleList(t):
    '''TupleList : TupleList COMMA Tuple
                 | Tuple'''

    if not isinstance(t[1], TupleList):
        t[0] = TupleList([t[1]])
    else:
        t[0] = t[1].add(t[3])

def p_error(t):
  if t:
    raise SyntaxException(t.lineno, t.lexpos, t.value, t)
  else:
    raise SyntaxException("EOF")
