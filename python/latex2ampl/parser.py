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
    '''Objective : MAXIMIZE LinearExpression
                 | MAXIMIZE SymbolicExpression
                 | MAXIMIZE NumericExpression
                 | MAXIMIZE Identifier
                 | MINIMIZE LinearExpression
                 | MINIMIZE SymbolicExpression
                 | MINIMIZE NumericExpression
                 | MINIMIZE Identifier
                 | MAXIMIZE LinearExpression FOR IndexingExpression
                 | MAXIMIZE SymbolicExpression FOR IndexingExpression
                 | MAXIMIZE NumericExpression FOR IndexingExpression
                 | MAXIMIZE Identifier FOR IndexingExpression
                 | MINIMIZE LinearExpression FOR IndexingExpression
                 | MINIMIZE SymbolicExpression FOR IndexingExpression
                 | MINIMIZE NumericExpression FOR IndexingExpression
                 | MINIMIZE Identifier FOR IndexingExpression
                 | MAXIMIZE LinearExpression WHERE IndexingExpression
                 | MAXIMIZE SymbolicExpression WHERE IndexingExpression
                 | MAXIMIZE NumericExpression WHERE IndexingExpression
                 | MAXIMIZE Identifier WHERE IndexingExpression
                 | MINIMIZE LinearExpression WHERE IndexingExpression
                 | MINIMIZE SymbolicExpression WHERE IndexingExpression
                 | MINIMIZE NumericExpression WHERE IndexingExpression
                 | MINIMIZE Identifier WHERE IndexingExpression
                 | MAXIMIZE LinearExpression COLON IndexingExpression
                 | MAXIMIZE SymbolicExpression COLON IndexingExpression
                 | MAXIMIZE NumericExpression COLON IndexingExpression
                 | MAXIMIZE Identifier COLON IndexingExpression
                 | MINIMIZE LinearExpression COLON IndexingExpression
                 | MINIMIZE SymbolicExpression COLON IndexingExpression
                 | MINIMIZE NumericExpression COLON IndexingExpression
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

                            | NumericExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | NumericExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | NumericExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | NumericExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

                            | SymbolicExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | SymbolicExpression IMPLIES ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression IMPLIES ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression IMPLIES ConstraintExpression ELSE AllDiffExpression
                            | SymbolicExpression IMPLIES AllDiffExpression ELSE ConstraintExpression
                            | SymbolicExpression IMPLIES AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES AllDiffExpression ELSE AllDiffExpression

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

                            | NumericExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | NumericExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | NumericExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE AllDiffExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE AllDiffExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE ConstraintExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression ELSE AllDiffExpression

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

                            | NumericExpression IMPLIES ConstraintExpression
                            | NumericExpression IMPLIES ConnectedConstraintLogicalExpression
                            | NumericExpression IMPLIES IteratedConstraintLogicalExpression
                            | NumericExpression IMPLIES EntryConstraintLogicalExpression
                            | NumericExpression IMPLIES AllDiffExpression

                            | SymbolicExpression IMPLIES ConstraintExpression
                            | SymbolicExpression IMPLIES ConnectedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES IteratedConstraintLogicalExpression
                            | SymbolicExpression IMPLIES EntryConstraintLogicalExpression
                            | SymbolicExpression IMPLIES AllDiffExpression

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

                            | NumericExpression ISIMPLIEDBY ConstraintExpression
                            | NumericExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | NumericExpression ISIMPLIEDBY AllDiffExpression

                            | SymbolicExpression ISIMPLIEDBY ConstraintExpression
                            | SymbolicExpression ISIMPLIEDBY ConnectedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY IteratedConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | SymbolicExpression ISIMPLIEDBY AllDiffExpression

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

                            | NumericExpression IFANDONLYIF ConstraintExpression
                            | NumericExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | NumericExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | NumericExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | NumericExpression IFANDONLYIF AllDiffExpression

                            | SymbolicExpression IFANDONLYIF ConstraintExpression
                            | SymbolicExpression IFANDONLYIF ConnectedConstraintLogicalExpression
                            | SymbolicExpression IFANDONLYIF IteratedConstraintLogicalExpression
                            | SymbolicExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | SymbolicExpression IFANDONLYIF AllDiffExpression

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
    '''ConstraintExpression : LinearExpression EQ LinearExpression
                            | LinearExpression EQ NumericExpression
                            | LinearExpression EQ Identifier
                            | LinearExpression LE LinearExpression
                            | LinearExpression LE NumericExpression
                            | LinearExpression LE Identifier
                            | LinearExpression GE LinearExpression
                            | LinearExpression GE NumericExpression
                            | LinearExpression GE Identifier
                            | NumericExpression EQ LinearExpression
                            | NumericExpression LE LinearExpression
                            | NumericExpression GE LinearExpression
                            | Identifier EQ LinearExpression
                            | Identifier LE LinearExpression
                            | Identifier GE LinearExpression
                            | LinearExpression LE LinearExpression LE LinearExpression
                            | SymbolicExpression LE SymbolicExpression LE SymbolicExpression
                            | LinearExpression LE LinearExpression LE NumericExpression
                            | SymbolicExpression LE SymbolicExpression LE NumericExpression
                            | LinearExpression LE LinearExpression LE Identifier
                            | SymbolicExpression LE SymbolicExpression LE Identifier
                            | LinearExpression LE NumericExpression LE LinearExpression
                            | SymbolicExpression LE NumericExpression LE SymbolicExpression
                            | LinearExpression LE Identifier LE LinearExpression
                            | SymbolicExpression LE Identifier LE SymbolicExpression
                            | LinearExpression LE NumericExpression LE NumericExpression
                            | SymbolicExpression LE NumericExpression LE NumericExpression
                            | LinearExpression LE NumericExpression LE Identifier
                            | SymbolicExpression LE NumericExpression LE Identifier
                            | LinearExpression LE Identifier LE NumericExpression
                            | SymbolicExpression LE Identifier LE NumericExpression
                            | LinearExpression LE Identifier LE Identifier
                            | SymbolicExpression LE Identifier LE Identifier
                            | NumericExpression LE LinearExpression LE LinearExpression
                            | NumericExpression LE SymbolicExpression LE SymbolicExpression
                            | Identifier LE LinearExpression LE LinearExpression
                            | Identifier LE SymbolicExpression LE SymbolicExpression
                            | NumericExpression LE LinearExpression LE NumericExpression
                            | NumericExpression LE SymbolicExpression LE NumericExpression
                            | NumericExpression LE LinearExpression LE Identifier
                            | NumericExpression LE SymbolicExpression LE Identifier
                            | Identifier LE LinearExpression LE NumericExpression
                            | Identifier LE SymbolicExpression LE NumericExpression
                            | Identifier LE LinearExpression LE Identifier
                            | Identifier LE SymbolicExpression LE Identifier
                            | NumericExpression LE NumericExpression LE LinearExpression
                            | NumericExpression LE NumericExpression LE SymbolicExpression
                            | NumericExpression LE Identifier LE LinearExpression
                            | NumericExpression LE Identifier LE SymbolicExpression
                            | Identifier LE NumericExpression LE LinearExpression
                            | Identifier LE NumericExpression LE SymbolicExpression
                            | Identifier LE Identifier LE LinearExpression
                            | Identifier LE Identifier LE SymbolicExpression
                            | NumericExpression LE NumericExpression LE NumericExpression
                            | NumericExpression LE NumericExpression LE Identifier
                            | NumericExpression LE Identifier LE NumericExpression
                            | Identifier LE NumericExpression LE NumericExpression
                            | Identifier LE NumericExpression LE Identifier
                            | Identifier LE Identifier LE NumericExpression
                            | Identifier LE Identifier LE Identifier
                            | LinearExpression GE LinearExpression GE LinearExpression
                            | SymbolicExpression GE SymbolicExpression GE SymbolicExpression
                            | LinearExpression GE LinearExpression GE NumericExpression
                            | SymbolicExpression GE SymbolicExpression GE NumericExpression
                            | LinearExpression GE LinearExpression GE Identifier
                            | SymbolicExpression GE SymbolicExpression GE Identifier
                            | LinearExpression GE NumericExpression GE LinearExpression
                            | SymbolicExpression GE NumericExpression GE SymbolicExpression
                            | LinearExpression GE Identifier GE LinearExpression
                            | SymbolicExpression GE Identifier GE SymbolicExpression
                            | LinearExpression GE NumericExpression GE NumericExpression
                            | SymbolicExpression GE NumericExpression GE NumericExpression
                            | LinearExpression GE NumericExpression GE Identifier
                            | SymbolicExpression GE NumericExpression GE Identifier
                            | LinearExpression GE Identifier GE NumericExpression
                            | SymbolicExpression GE Identifier GE NumericExpression
                            | LinearExpression GE Identifier GE Identifier
                            | SymbolicExpression GE Identifier GE Identifier
                            | NumericExpression GE LinearExpression GE LinearExpression
                            | NumericExpression GE SymbolicExpression GE SymbolicExpression
                            | Identifier GE LinearExpression GE LinearExpression
                            | Identifier GE SymbolicExpression GE SymbolicExpression
                            | NumericExpression GE LinearExpression GE NumericExpression
                            | NumericExpression GE SymbolicExpression GE NumericExpression
                            | NumericExpression GE LinearExpression GE Identifier
                            | NumericExpression GE SymbolicExpression GE Identifier
                            | Identifier GE LinearExpression GE NumericExpression
                            | Identifier GE SymbolicExpression GE NumericExpression
                            | Identifier GE LinearExpression GE Identifier
                            | Identifier GE SymbolicExpression GE Identifier
                            | NumericExpression GE NumericExpression GE LinearExpression
                            | NumericExpression GE NumericExpression GE SymbolicExpression
                            | NumericExpression GE Identifier GE LinearExpression
                            | NumericExpression GE Identifier GE SymbolicExpression
                            | Identifier GE NumericExpression GE LinearExpression
                            | Identifier GE NumericExpression GE SymbolicExpression
                            | Identifier GE Identifier GE LinearExpression
                            | Identifier GE Identifier GE SymbolicExpression
                            | NumericExpression GE NumericExpression GE NumericExpression
                            | NumericExpression GE NumericExpression GE Identifier
                            | NumericExpression GE Identifier GE NumericExpression
                            | NumericExpression GE Identifier GE Identifier
                            | Identifier GE NumericExpression GE NumericExpression
                            | Identifier GE NumericExpression GE Identifier
                            | Identifier GE Identifier GE NumericExpression
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
    '''EntryConstraintLogicalExpression : NumericExpression LE NumericExpression
                                        | NumericExpression LE Identifier
                                        | NumericExpression LE SymbolicExpression
                                        | NumericExpression EQ NumericExpression
                                        | NumericExpression EQ Identifier
                                        | NumericExpression EQ SymbolicExpression
                                        | NumericExpression GE NumericExpression
                                        | NumericExpression GE Identifier
                                        | NumericExpression GE SymbolicExpression
                                        | Identifier LE NumericExpression
                                        | Identifier LE Identifier
                                        | Identifier LE SymbolicExpression
                                        | Identifier EQ NumericExpression
                                        | Identifier EQ Identifier
                                        | Identifier EQ SymbolicExpression
                                        | Identifier GE NumericExpression
                                        | Identifier GE Identifier
                                        | Identifier GE SymbolicExpression
                                        | SymbolicExpression LE NumericExpression
                                        | SymbolicExpression LE Identifier
                                        | SymbolicExpression LE SymbolicExpression
                                        | SymbolicExpression EQ NumericExpression
                                        | SymbolicExpression EQ Identifier
                                        | SymbolicExpression EQ SymbolicExpression
                                        | SymbolicExpression GE NumericExpression
                                        | SymbolicExpression GE Identifier
                                        | SymbolicExpression GE SymbolicExpression
                                        | NumericExpression LT NumericExpression
                                        | NumericExpression LT Identifier
                                        | NumericExpression LT SymbolicExpression
                                        | NumericExpression GT NumericExpression
                                        | NumericExpression GT Identifier
                                        | NumericExpression GT SymbolicExpression
                                        | NumericExpression NEQ NumericExpression
                                        | NumericExpression NEQ Identifier
                                        | NumericExpression NEQ SymbolicExpression
                                        | Identifier LT NumericExpression
                                        | Identifier LT Identifier
                                        | Identifier LT SymbolicExpression
                                        | Identifier GT NumericExpression
                                        | Identifier GT Identifier
                                        | Identifier GT SymbolicExpression
                                        | Identifier NEQ NumericExpression
                                        | Identifier NEQ Identifier
                                        | Identifier NEQ SymbolicExpression
                                        | SymbolicExpression LT NumericExpression
                                        | SymbolicExpression LT Identifier
                                        | SymbolicExpression LT SymbolicExpression
                                        | SymbolicExpression GT NumericExpression
                                        | SymbolicExpression GT Identifier
                                        | SymbolicExpression GT SymbolicExpression
                                        | SymbolicExpression NEQ NumericExpression
                                        | SymbolicExpression NEQ Identifier
                                        | SymbolicExpression NEQ SymbolicExpression
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
                   | NumericExpression FOR IndexingExpression
                   | NumericExpression WHERE IndexingExpression
                   | NumericExpression COLON IndexingExpression
                   | Identifier FOR IndexingExpression
                   | Identifier WHERE IndexingExpression
                   | Identifier COLON IndexingExpression
                   | SymbolicExpression FOR IndexingExpression
                   | SymbolicExpression WHERE IndexingExpression
                   | SymbolicExpression COLON IndexingExpression
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
                             | NumericExpression IN SetExpression
                             | NumericExpression IN Range
                             | Identifier IN SetExpression
                             | Identifier IN Range
                             | SymbolicExpression IN SetExpression
                             | SymbolicExpression IN Range
                             | ValueList IN Identifier
                             | NumericExpression IN Identifier
                             | Identifier IN Identifier
                             | SymbolicExpression IN Identifier
                             | ValueList SUBSET SetExpression
                             | ValueList SUBSET Range
                             | NumericExpression SUBSET SetExpression
                             | NumericExpression SUBSET Range
                             | Identifier SUBSET SetExpression
                             | Identifier SUBSET Range
                             | SymbolicExpression SUBSET SetExpression
                             | SymbolicExpression SUBSET Range
                             | ValueList SUBSET Identifier
                             | NumericExpression SUBSET Identifier
                             | Identifier SUBSET Identifier
                             | SymbolicExpression SUBSET Identifier
                             | ValueList DEFAULT NumericExpression
                             | ValueList DEFAULT Identifier
                             | NumericExpression DEFAULT NumericExpression
                             | NumericExpression DEFAULT Identifier
                             | Identifier DEFAULT NumericExpression
                             | Identifier DEFAULT Identifier
                             | SymbolicExpression DEFAULT NumericExpression
                             | SymbolicExpression DEFAULT Identifier
                             | ValueList DEFAULT SymbolicExpression
                             | NumericExpression DEFAULT SymbolicExpression
                             | Identifier DEFAULT SymbolicExpression
                             | SymbolicExpression DEFAULT SymbolicExpression
                             | ValueList DEFAULT SetExpression
                             | ValueList DEFAULT Range
                             | NumericExpression DEFAULT SetExpression
                             | NumericExpression DEFAULT Range
                             | Identifier DEFAULT SetExpression
                             | Identifier DEFAULT Range
                             | SymbolicExpression DEFAULT SetExpression
                             | SymbolicExpression DEFAULT Range
                             | ValueList DIMEN NumericExpression
                             | ValueList DIMEN Identifier
                             | NumericExpression DIMEN NumericExpression
                             | NumericExpression DIMEN Identifier
                             | Identifier DIMEN NumericExpression
                             | Identifier DIMEN Identifier
                             | SymbolicExpression DIMEN NumericExpression
                             | SymbolicExpression DIMEN Identifier
                             | ValueList DIMEN SymbolicExpression
                             | NumericExpression DIMEN SymbolicExpression
                             | Identifier DIMEN SymbolicExpression
                             | SymbolicExpression DIMEN SymbolicExpression
                             | ValueList ASSIGN NumericExpression
                             | ValueList ASSIGN Identifier
                             | NumericExpression ASSIGN NumericExpression
                             | NumericExpression ASSIGN Identifier
                             | Identifier ASSIGN NumericExpression
                             | Identifier ASSIGN Identifier
                             | SymbolicExpression ASSIGN NumericExpression
                             | SymbolicExpression ASSIGN Identifier
                             | ValueList ASSIGN SymbolicExpression
                             | NumericExpression ASSIGN SymbolicExpression
                             | Identifier ASSIGN SymbolicExpression
                             | SymbolicExpression ASSIGN SymbolicExpression
                             | ValueList ASSIGN SetExpression
                             | ValueList ASSIGN Range
                             | NumericExpression ASSIGN SetExpression
                             | NumericExpression ASSIGN Range
                             | Identifier ASSIGN SetExpression
                             | Identifier ASSIGN Range
                             | SymbolicExpression ASSIGN SetExpression
                             | SymbolicExpression ASSIGN Range
                             | ValueList LE NumericExpression
                             | ValueList LE Identifier
                             | ValueList LE SymbolicExpression
                             | ValueList GE NumericExpression
                             | ValueList GE Identifier
                             | ValueList GE SymbolicExpression
                             | ValueList EQ NumericExpression
                             | ValueList EQ Identifier
                             | ValueList EQ SymbolicExpression
                             | ValueList LT NumericExpression
                             | ValueList LT Identifier
                             | ValueList LT SymbolicExpression
                             | ValueList GT NumericExpression
                             | ValueList GT Identifier
                             | ValueList GT SymbolicExpression
                             | ValueList NEQ NumericExpression
                             | ValueList NEQ Identifier
                             | ValueList NEQ SymbolicExpression
                             | ValueList COMMA DeclarationAttributeList
                             | NumericExpression COMMA DeclarationAttributeList
                             | Identifier COMMA DeclarationAttributeList
                             | SymbolicExpression COMMA DeclarationAttributeList
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
                          | DEFAULT NumericExpression
                          | DEFAULT Identifier
                          | DEFAULT SymbolicExpression
                          | DEFAULT SetExpression
                          | DEFAULT Range
                          | DIMEN NumericExpression
                          | DIMEN Identifier
                          | DIMEN SymbolicExpression
                          | ASSIGN NumericExpression
                          | ASSIGN Identifier
                          | ASSIGN SymbolicExpression
                          | ASSIGN SetExpression
                          | ASSIGN Range
                          | LT NumericExpression
                          | LT Identifier
                          | LT SymbolicExpression
                          | LE NumericExpression
                          | LE Identifier
                          | LE SymbolicExpression
                          | EQ NumericExpression
                          | EQ Identifier
                          | EQ SymbolicExpression
                          | GT NumericExpression
                          | GT Identifier
                          | GT SymbolicExpression
                          | GE NumericExpression
                          | GE Identifier
                          | GE SymbolicExpression
                          | NEQ NumericExpression
                          | NEQ Identifier
                          | NEQ SymbolicExpression'''

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

def p_LinearExpression(t):
    '''LinearExpression : LPAREN LinearExpression RPAREN
                        | ConditionalLinearExpression'''

    if len(t) > 3:
        t[0] = LinearExpressionBetweenParenthesis(t[2])
    elif isinstance(t[1], ConditionalLinearExpression):
        t[0] = t[1]
    else:
        t[0] = ValuedLinearExpression(t[1])

def p_LinearExpression_binop(t):
    '''LinearExpression : LinearExpression PLUS LinearExpression
                        | SymbolicExpression PLUS SymbolicExpression
                        | LinearExpression PLUS NumericExpression
                        | SymbolicExpression PLUS NumericExpression
                        | LinearExpression PLUS Identifier
                        | SymbolicExpression PLUS Identifier
                        | NumericExpression PLUS LinearExpression
                        | NumericExpression PLUS SymbolicExpression
                        | Identifier PLUS LinearExpression
                        | Identifier PLUS SymbolicExpression
                        | LinearExpression MINUS LinearExpression
                        | SymbolicExpression MINUS SymbolicExpression
                        | LinearExpression MINUS NumericExpression
                        | SymbolicExpression MINUS NumericExpression
                        | LinearExpression MINUS Identifier
                        | SymbolicExpression MINUS Identifier
                        | NumericExpression MINUS LinearExpression
                        | NumericExpression MINUS SymbolicExpression
                        | Identifier MINUS LinearExpression
                        | Identifier MINUS SymbolicExpression
                        | LinearExpression TIMES NumericExpression
                        | SymbolicExpression TIMES NumericExpression
                        | LinearExpression TIMES Identifier
                        | SymbolicExpression TIMES Identifier
                        | LinearExpression DIVIDE NumericExpression
                        | SymbolicExpression DIVIDE NumericExpression
                        | LinearExpression DIVIDE Identifier
                        | SymbolicExpression DIVIDE Identifier'''

    _type = t.slice[2].type
    if _type == "PLUS":
        op = LinearExpressionWithArithmeticOperation.PLUS

    elif _type == "MINUS":
        op = LinearExpressionWithArithmeticOperation.MINUS

    elif _type == "TIMES":
        op = LinearExpressionWithArithmeticOperation.TIMES

    elif _type == "DIVIDE":
        op = LinearExpressionWithArithmeticOperation.DIV

    t[0] = LinearExpressionWithArithmeticOperation(op, t[1], t[3])

def p_IteratedLinearExpression(t):
    '''LinearExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE LinearExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE LinearExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE SymbolicExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE SymbolicExpression'''
    if len(t) > 7:
        t[0] = IteratedLinearExpression(t[10], t[4], t[8])
    else:
        t[0] = IteratedLinearExpression(t[6], t[4])

def p_ConditionalLinearExpression(t):
    '''ConditionalLinearExpression : IF Identifier THEN LinearExpression ELSE LinearExpression
                                   | IF Identifier THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF Identifier THEN LinearExpression ELSE NumericExpression
                                   | IF Identifier THEN SymbolicExpression ELSE NumericExpression
                                   | IF Identifier THEN LinearExpression ELSE Identifier
                                   | IF Identifier THEN SymbolicExpression ELSE Identifier
                                   | IF Identifier THEN NumericExpression ELSE LinearExpression
                                   | IF Identifier THEN NumericExpression ELSE SymbolicExpression
                                   | IF Identifier THEN Identifier ELSE LinearExpression
                                   | IF Identifier THEN Identifier ELSE SymbolicExpression
                                   | IF NumericExpression THEN LinearExpression ELSE LinearExpression
                                   | IF NumericExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF NumericExpression THEN LinearExpression ELSE NumericExpression
                                   | IF NumericExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF NumericExpression THEN LinearExpression ELSE Identifier
                                   | IF NumericExpression THEN SymbolicExpression ELSE Identifier
                                   | IF NumericExpression THEN NumericExpression ELSE LinearExpression
                                   | IF NumericExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF NumericExpression THEN Identifier ELSE LinearExpression
                                   | IF NumericExpression THEN Identifier ELSE SymbolicExpression
                                   | IF SymbolicExpression THEN LinearExpression ELSE LinearExpression
                                   | IF SymbolicExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF SymbolicExpression THEN LinearExpression ELSE NumericExpression
                                   | IF SymbolicExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF SymbolicExpression THEN LinearExpression ELSE Identifier
                                   | IF SymbolicExpression THEN SymbolicExpression ELSE Identifier
                                   | IF SymbolicExpression THEN NumericExpression ELSE LinearExpression
                                   | IF SymbolicExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF SymbolicExpression THEN Identifier ELSE LinearExpression
                                   | IF SymbolicExpression THEN Identifier ELSE SymbolicExpression
                                   | IF LogicalExpression THEN LinearExpression ELSE LinearExpression
                                   | IF LogicalExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF LogicalExpression THEN LinearExpression ELSE NumericExpression
                                   | IF LogicalExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF LogicalExpression THEN LinearExpression ELSE Identifier
                                   | IF LogicalExpression THEN SymbolicExpression ELSE Identifier
                                   | IF LogicalExpression THEN NumericExpression ELSE LinearExpression
                                   | IF LogicalExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF LogicalExpression THEN Identifier ELSE LinearExpression
                                   | IF LogicalExpression THEN Identifier ELSE SymbolicExpression
                                   | IF ConnectedConstraintLogicalExpression THEN LinearExpression ELSE LinearExpression
                                   | IF ConnectedConstraintLogicalExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF ConnectedConstraintLogicalExpression THEN LinearExpression ELSE NumericExpression
                                   | IF ConnectedConstraintLogicalExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF ConnectedConstraintLogicalExpression THEN LinearExpression ELSE Identifier
                                   | IF ConnectedConstraintLogicalExpression THEN SymbolicExpression ELSE Identifier
                                   | IF ConnectedConstraintLogicalExpression THEN NumericExpression ELSE LinearExpression
                                   | IF ConnectedConstraintLogicalExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE LinearExpression
                                   | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE SymbolicExpression
                                   | IF IteratedConstraintLogicalExpression THEN LinearExpression ELSE LinearExpression
                                   | IF IteratedConstraintLogicalExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF IteratedConstraintLogicalExpression THEN LinearExpression ELSE NumericExpression
                                   | IF IteratedConstraintLogicalExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF IteratedConstraintLogicalExpression THEN LinearExpression ELSE Identifier
                                   | IF IteratedConstraintLogicalExpression THEN SymbolicExpression ELSE Identifier
                                   | IF IteratedConstraintLogicalExpression THEN NumericExpression ELSE LinearExpression
                                   | IF IteratedConstraintLogicalExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF IteratedConstraintLogicalExpression THEN Identifier ELSE LinearExpression
                                   | IF IteratedConstraintLogicalExpression THEN Identifier ELSE SymbolicExpression
                                   | IF AllDiffExpression THEN LinearExpression ELSE LinearExpression
                                   | IF AllDiffExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF AllDiffExpression THEN LinearExpression ELSE NumericExpression
                                   | IF AllDiffExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF AllDiffExpression THEN LinearExpression ELSE Identifier
                                   | IF AllDiffExpression THEN SymbolicExpression ELSE Identifier
                                   | IF AllDiffExpression THEN NumericExpression ELSE LinearExpression
                                   | IF AllDiffExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF AllDiffExpression THEN Identifier ELSE LinearExpression
                                   | IF AllDiffExpression THEN Identifier ELSE SymbolicExpression
                                   | IF EntryConstraintLogicalExpression THEN LinearExpression ELSE LinearExpression
                                   | IF EntryConstraintLogicalExpression THEN SymbolicExpression ELSE SymbolicExpression
                                   | IF EntryConstraintLogicalExpression THEN LinearExpression ELSE NumericExpression
                                   | IF EntryConstraintLogicalExpression THEN SymbolicExpression ELSE NumericExpression
                                   | IF EntryConstraintLogicalExpression THEN LinearExpression ELSE Identifier
                                   | IF EntryConstraintLogicalExpression THEN SymbolicExpression ELSE Identifier
                                   | IF EntryConstraintLogicalExpression THEN NumericExpression ELSE LinearExpression
                                   | IF EntryConstraintLogicalExpression THEN NumericExpression ELSE SymbolicExpression
                                   | IF EntryConstraintLogicalExpression THEN Identifier ELSE LinearExpression
                                   | IF EntryConstraintLogicalExpression THEN Identifier ELSE SymbolicExpression
                                   | IF Identifier THEN LinearExpression
                                   | IF Identifier THEN SymbolicExpression
                                   | IF NumericExpression THEN LinearExpression
                                   | IF NumericExpression THEN SymbolicExpression
                                   | IF SymbolicExpression THEN LinearExpression
                                   | IF SymbolicExpression THEN SymbolicExpression
                                   | IF LogicalExpression THEN LinearExpression
                                   | IF LogicalExpression THEN SymbolicExpression
                                   | IF ConnectedConstraintLogicalExpression THEN LinearExpression
                                   | IF ConnectedConstraintLogicalExpression THEN SymbolicExpression
                                   | IF IteratedConstraintLogicalExpression THEN LinearExpression
                                   | IF IteratedConstraintLogicalExpression THEN SymbolicExpression
                                   | IF AllDiffExpression THEN LinearExpression
                                   | IF AllDiffExpression THEN SymbolicExpression
                                   | IF EntryConstraintLogicalExpression THEN LinearExpression
                                   | IF EntryConstraintLogicalExpression THEN SymbolicExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])

    t[0] = ConditionalLinearExpression(t[2], t[4])

    if len(t) > 5:
      t[0].addElseExpression(t[6])

def p_LogicalExpression(t):
    '''LogicalExpression : EntryLogicalExpression
                         | LogicalExpression OR EntryLogicalExpression
                         | LogicalExpression OR ConnectedConstraintLogicalExpression
                         | LogicalExpression OR IteratedConstraintLogicalExpression
                         | LogicalExpression OR AllDiffExpression
                         | LogicalExpression OR EntryConstraintLogicalExpression
                         | LogicalExpression OR NumericExpression
                         | LogicalExpression OR SymbolicExpression
                         | LogicalExpression OR Identifier
                         | ConnectedConstraintLogicalExpression OR LogicalExpression
                         | ConnectedConstraintLogicalExpression OR NumericExpression
                         | ConnectedConstraintLogicalExpression OR SymbolicExpression
                         | ConnectedConstraintLogicalExpression OR Identifier
                         | IteratedConstraintLogicalExpression OR LogicalExpression
                         | IteratedConstraintLogicalExpression OR NumericExpression
                         | IteratedConstraintLogicalExpression OR SymbolicExpression
                         | IteratedConstraintLogicalExpression OR Identifier
                         | AllDiffExpression OR LogicalExpression
                         | AllDiffExpression OR NumericExpression
                         | AllDiffExpression OR SymbolicExpression
                         | AllDiffExpression OR Identifier
                         | EntryConstraintLogicalExpression OR LogicalExpression
                         | EntryConstraintLogicalExpression OR NumericExpression
                         | EntryConstraintLogicalExpression OR SymbolicExpression
                         | EntryConstraintLogicalExpression OR Identifier
                         | NumericExpression OR LogicalExpression
                         | NumericExpression OR ConnectedConstraintLogicalExpression
                         | NumericExpression OR IteratedConstraintLogicalExpression
                         | NumericExpression OR AllDiffExpression
                         | NumericExpression OR EntryConstraintLogicalExpression
                         | NumericExpression OR NumericExpression
                         | NumericExpression OR SymbolicExpression
                         | NumericExpression OR Identifier
                         | SymbolicExpression OR LogicalExpression
                         | SymbolicExpression OR ConnectedConstraintLogicalExpression
                         | SymbolicExpression OR IteratedConstraintLogicalExpression
                         | SymbolicExpression OR AllDiffExpression
                         | SymbolicExpression OR EntryConstraintLogicalExpression
                         | SymbolicExpression OR NumericExpression
                         | SymbolicExpression OR SymbolicExpression
                         | SymbolicExpression OR Identifier
                         | Identifier OR LogicalExpression
                         | Identifier OR ConnectedConstraintLogicalExpression
                         | Identifier OR IteratedConstraintLogicalExpression
                         | Identifier OR AllDiffExpression
                         | Identifier OR EntryConstraintLogicalExpression
                         | Identifier OR NumericExpression
                         | Identifier OR SymbolicExpression
                         | Identifier OR Identifier
                         | LogicalExpression AND EntryLogicalExpression
                         | LogicalExpression AND ConnectedConstraintLogicalExpression
                         | LogicalExpression AND IteratedConstraintLogicalExpression
                         | LogicalExpression AND AllDiffExpression
                         | LogicalExpression AND EntryConstraintLogicalExpression
                         | LogicalExpression AND NumericExpression
                         | LogicalExpression AND SymbolicExpression
                         | LogicalExpression AND Identifier
                         | ConnectedConstraintLogicalExpression AND LogicalExpression
                         | ConnectedConstraintLogicalExpression AND NumericExpression
                         | ConnectedConstraintLogicalExpression AND SymbolicExpression
                         | ConnectedConstraintLogicalExpression AND Identifier
                         | IteratedConstraintLogicalExpression AND LogicalExpression
                         | IteratedConstraintLogicalExpression AND NumericExpression
                         | IteratedConstraintLogicalExpression AND SymbolicExpression
                         | IteratedConstraintLogicalExpression AND Identifier
                         | AllDiffExpression AND LogicalExpression
                         | AllDiffExpression AND NumericExpression
                         | AllDiffExpression AND SymbolicExpression
                         | AllDiffExpression AND Identifier
                         | EntryConstraintLogicalExpression AND LogicalExpression
                         | EntryConstraintLogicalExpression AND NumericExpression
                         | EntryConstraintLogicalExpression AND SymbolicExpression
                         | EntryConstraintLogicalExpression AND Identifier
                         | NumericExpression AND LogicalExpression
                         | NumericExpression AND ConnectedConstraintLogicalExpression
                         | NumericExpression AND IteratedConstraintLogicalExpression
                         | NumericExpression AND AllDiffExpression
                         | NumericExpression AND EntryConstraintLogicalExpression
                         | NumericExpression AND NumericExpression
                         | NumericExpression AND SymbolicExpression
                         | NumericExpression AND Identifier
                         | SymbolicExpression AND LogicalExpression
                         | SymbolicExpression AND ConnectedConstraintLogicalExpression
                         | SymbolicExpression AND IteratedConstraintLogicalExpression
                         | SymbolicExpression AND AllDiffExpression
                         | SymbolicExpression AND EntryConstraintLogicalExpression
                         | SymbolicExpression AND NumericExpression
                         | SymbolicExpression AND SymbolicExpression
                         | SymbolicExpression AND Identifier
                         | Identifier AND LogicalExpression
                         | Identifier AND ConnectedConstraintLogicalExpression
                         | Identifier AND IteratedConstraintLogicalExpression
                         | Identifier AND AllDiffExpression
                         | Identifier AND EntryConstraintLogicalExpression
                         | Identifier AND NumericExpression
                         | Identifier AND SymbolicExpression
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
    '''EntryLogicalExpression : NOT NumericExpression
                              | NOT SymbolicExpression
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
                         | ALLDIFF LLBRACE IndexingExpression RRBRACE NumericExpression
                         | ALLDIFF LLBRACE IndexingExpression RRBRACE SymbolicExpression
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
                              | NumericExpression IN SetExpression
                              | NumericExpression IN Range
                              | Identifier IN SetExpression
                              | Identifier IN Range
                              | SymbolicExpression IN SetExpression
                              | SymbolicExpression IN Range
                              | ValueList IN Identifier
                              | NumericExpression IN Identifier
                              | Identifier IN Identifier
                              | SymbolicExpression IN Identifier
                              | Tuple IN SetExpression
                              | Tuple IN Range
                              | Tuple IN Identifier
                              | ValueList NOTIN SetExpression
                              | ValueList NOTIN Range
                              | NumericExpression NOTIN SetExpression
                              | NumericExpression NOTIN Range
                              | Identifier NOTIN SetExpression
                              | Identifier NOTIN Range
                              | SymbolicExpression NOTIN SetExpression
                              | SymbolicExpression NOTIN Range
                              | ValueList NOTIN Identifier
                              | NumericExpression NOTIN Identifier
                              | Identifier NOTIN Identifier
                              | SymbolicExpression NOTIN Identifier
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
                              | FORALL LLBRACE IndexingExpression RRBRACE NumericExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE SymbolicExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | NFORALL LLBRACE IndexingExpression RRBRACE NumericExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE SymbolicExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | EXISTS LLBRACE IndexingExpression RRBRACE NumericExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE SymbolicExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | NEXISTS LLBRACE IndexingExpression RRBRACE NumericExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE SymbolicExpression
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
                     | LLBRACE NumericExpression RRBRACE
                     | LLBRACE Identifier RRBRACE
                     | LLBRACE SymbolicExpression RRBRACE
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
                     | Identifier LBRACKET NumericExpression RBRACKET
                     | Identifier LBRACKET Identifier RBRACKET
                     | Identifier LBRACKET SymbolicExpression RBRACKET'''
    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = ValueList([t[3]])

    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE Identifier
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE SymbolicExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE SymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE SymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE SymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE SymbolicExpression'''
    
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
                                | IF NumericExpression THEN SetExpression ELSE SetExpression
                                | IF NumericExpression THEN SetExpression ELSE Identifier
                                | IF NumericExpression THEN Identifier ELSE SetExpression
                                | IF SymbolicExpression THEN SetExpression ELSE SetExpression
                                | IF SymbolicExpression THEN SetExpression ELSE Identifier
                                | IF SymbolicExpression THEN Identifier ELSE SetExpression
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
                                | IF NumericExpression THEN SetExpression
                                | IF SymbolicExpression THEN SetExpression
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
                          | IndexingExpression PIPE NumericExpression
                          | IndexingExpression PIPE SymbolicExpression
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
                              | IF NumericExpression
                              | IF SymbolicExpression
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
                               | NumericExpression IN SetExpression
                               | NumericExpression IN Range
                               | Identifier IN SetExpression
                               | Identifier IN Range
                               | SymbolicExpression IN SetExpression
                               | SymbolicExpression IN Range
                               | ValueList IN Identifier
                               | NumericExpression IN Identifier
                               | Identifier IN Identifier
                               | SymbolicExpression IN Identifier
                               | Tuple IN SetExpression
                               | Tuple IN Range
                               | Tuple IN Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])

    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Identifier EQ NumericExpression
                               | Identifier EQ Identifier
                               | Identifier EQ Range
                               | Identifier NEQ NumericExpression
                               | Identifier NEQ Identifier
                               | Identifier LE NumericExpression
                               | Identifier LE Identifier
                               | Identifier GE NumericExpression
                               | Identifier GE Identifier
                               | Identifier LT NumericExpression
                               | Identifier LT Identifier
                               | Identifier GT NumericExpression
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
    '''SymbolicExpression : LPAREN SymbolicExpression RPAREN
                          | STRING'''

    if len(t) > 2:
        t[0] = SymbolicExpressionBetweenParenthesis(t[2])
    else:
        t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : NumericExpression AMPERSAND NumericExpression
                          | NumericExpression AMPERSAND Identifier
                          | Identifier AMPERSAND NumericExpression
                          | Identifier AMPERSAND Identifier
                          | NumericExpression AMPERSAND SymbolicExpression
                          | Identifier AMPERSAND SymbolicExpression
                          | SymbolicExpression AMPERSAND NumericExpression
                          | SymbolicExpression AMPERSAND Identifier
                          | SymbolicExpression AMPERSAND SymbolicExpression'''

    if t.slice[2].type == "AMPERSAND":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

def p_FunctionSymbolicExpression(t):
    '''SymbolicExpression : SUBSTR LPAREN NumericExpression COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA NumericExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Identifier COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | ALIAS LPAREN Identifier RPAREN
                          | CHAR LPAREN NumericExpression RPAREN
                          | CHAR LPAREN Identifier RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA ValueList RPAREN
                          | SPRINTF LPAREN Identifier COMMA ValueList RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | SPRINTF LPAREN Identifier COMMA Identifier RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SPRINTF LPAREN Identifier COMMA SymbolicExpression RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA NumericExpression RPAREN
                          | SPRINTF LPAREN Identifier COMMA NumericExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | CTIME LPAREN Identifier RPAREN
                          | CTIME LPAREN NumericExpression RPAREN
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


def p_NumericExpression_binop(t):
    '''NumericExpression : NumericExpression PLUS NumericExpression
                         | NumericExpression PLUS Identifier
                         | Identifier PLUS NumericExpression
                         | Identifier PLUS Identifier
                         | NumericExpression MINUS NumericExpression
                         | NumericExpression MINUS Identifier
                         | Identifier MINUS NumericExpression
                         | Identifier MINUS Identifier
                         | NumericExpression TIMES NumericExpression
                         | NumericExpression TIMES Identifier
                         | Identifier TIMES NumericExpression
                         | Identifier TIMES Identifier
                         | NumericExpression DIVIDE NumericExpression
                         | NumericExpression DIVIDE Identifier
                         | Identifier DIVIDE NumericExpression
                         | Identifier DIVIDE Identifier
                         | NumericExpression MOD NumericExpression
                         | NumericExpression MOD Identifier
                         | Identifier MOD NumericExpression
                         | Identifier MOD Identifier
                         | NumericExpression QUOTIENT NumericExpression
                         | NumericExpression QUOTIENT Identifier
                         | Identifier QUOTIENT NumericExpression
                         | Identifier QUOTIENT Identifier
                         | NumericExpression LESS NumericExpression
                         | NumericExpression LESS Identifier
                         | Identifier LESS NumericExpression
                         | Identifier LESS Identifier
                         | NumericExpression CARET LBRACE NumericExpression RBRACE
                         | NumericExpression CARET LBRACE Identifier RBRACE
                         | Identifier CARET LBRACE NumericExpression RBRACE
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
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
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

                         | ATMOST NumericExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATMOST NumericExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATMOST NumericExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATMOST NumericExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATMOST NumericExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | ATLEAST NumericExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST NumericExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | ATLEAST NumericExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | ATLEAST NumericExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | ATLEAST NumericExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | EXACTLY NumericExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY NumericExpression LLBRACE IndexingExpression RRBRACE ConnectedConstraintLogicalExpression
                         | EXACTLY NumericExpression LLBRACE IndexingExpression RRBRACE IteratedConstraintLogicalExpression
                         | EXACTLY NumericExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                         | EXACTLY NumericExpression LLBRACE IndexingExpression RRBRACE AllDiffExpression

                         | NUMBEROF Identifier IN LPAREN LLBRACE IndexingExpression RRBRACE Identifier RPAREN
                         | NUMBEROF NumericExpression IN LPAREN LLBRACE IndexingExpression RRBRACE Identifier RPAREN
                         | NUMBEROF SymbolicExpression IN LPAREN LLBRACE IndexingExpression RRBRACE Identifier RPAREN
                         | NUMBEROF Identifier IN LPAREN LLBRACE IndexingExpression RRBRACE NumericExpression RPAREN
                         | NUMBEROF NumericExpression IN LPAREN LLBRACE IndexingExpression RRBRACE NumericExpression RPAREN
                         | NUMBEROF SymbolicExpression IN LPAREN LLBRACE IndexingExpression RRBRACE NumericExpression RPAREN
                         | NUMBEROF Identifier IN LPAREN LLBRACE IndexingExpression RRBRACE SymbolicExpression RPAREN
                         | NUMBEROF NumericExpression IN LPAREN LLBRACE IndexingExpression RRBRACE SymbolicExpression RPAREN
                         | NUMBEROF SymbolicExpression IN LPAREN LLBRACE IndexingExpression RRBRACE SymbolicExpression RPAREN'''

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
    '''NumericExpression : MINUS NumericExpression %prec UMINUS
                         | MINUS Identifier %prec UMINUS
                         | PLUS NumericExpression %prec UPLUS
                         | PLUS Identifier %prec UPLUS
                         | LPAREN NumericExpression RPAREN
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
                         | FRAC LBRACE Identifier RBRACE LBRACE NumericExpression RBRACE
                         | FRAC LBRACE NumericExpression RBRACE LBRACE Identifier RBRACE
                         | FRAC LBRACE NumericExpression RBRACE LBRACE NumericExpression RBRACE'''
    t[0] = FractionalNumericExpression(t[3], t[6])

def p_FunctionNumericExpression(t):
    '''NumericExpression : SQRT LBRACE NumericExpression RBRACE
                         | SQRT LBRACE Identifier RBRACE
                         | LFLOOR NumericExpression RFLOOR
                         | LFLOOR Identifier RFLOOR
                         | LCEIL NumericExpression RCEIL
                         | LCEIL Identifier RCEIL
                         | PIPE NumericExpression PIPE
                         | PIPE Identifier PIPE
                         | MAX LPAREN ValueList RPAREN
                         | MAX LPAREN NumericExpression RPAREN
                         | MAX LPAREN Identifier RPAREN
                         | MAX LPAREN SymbolicExpression RPAREN
                         | MIN LPAREN ValueList RPAREN
                         | MIN LPAREN NumericExpression RPAREN
                         | MIN LPAREN Identifier RPAREN
                         | MIN LPAREN SymbolicExpression RPAREN
                         | ASIN LPAREN NumericExpression RPAREN
                         | ASIN LPAREN Identifier RPAREN
                         | SIN LPAREN NumericExpression RPAREN
                         | SIN LPAREN Identifier RPAREN
                         | ASINH LPAREN NumericExpression RPAREN
                         | ASINH LPAREN Identifier RPAREN
                         | SINH LPAREN NumericExpression RPAREN
                         | SINH LPAREN Identifier RPAREN
                         | ACOS LPAREN NumericExpression RPAREN
                         | ACOS LPAREN Identifier RPAREN
                         | COS LPAREN NumericExpression RPAREN
                         | COS LPAREN Identifier RPAREN
                         | ACOSH LPAREN NumericExpression RPAREN
                         | ACOSH LPAREN Identifier RPAREN
                         | COSH LPAREN NumericExpression RPAREN
                         | COSH LPAREN Identifier RPAREN
                         | LOG LPAREN NumericExpression RPAREN
                         | LOG LPAREN Identifier RPAREN
                         | LN LPAREN NumericExpression RPAREN
                         | LN LPAREN Identifier RPAREN
                         | EXP LPAREN NumericExpression RPAREN
                         | EXP LPAREN Identifier RPAREN
                         | TANH LPAREN NumericExpression RPAREN
                         | TANH LPAREN Identifier RPAREN
                         | TAN LPAREN NumericExpression RPAREN
                         | TAN LPAREN Identifier RPAREN
                         | ARCTANH LPAREN NumericExpression RPAREN
                         | ARCTANH LPAREN Identifier RPAREN
                         | ARCTAN LPAREN NumericExpression RPAREN
                         | ARCTAN LPAREN Identifier RPAREN
                         | ARCTAN LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | ARCTAN LPAREN NumericExpression COMMA Identifier RPAREN
                         | ARCTAN LPAREN Identifier COMMA NumericExpression RPAREN
                         | ARCTAN LPAREN Identifier COMMA Identifier RPAREN
                         | CARD LPAREN SetExpression RPAREN
                         | CARD LPAREN Range RPAREN
                         | CARD LPAREN Identifier RPAREN
                         | LENGTH LPAREN Identifier RPAREN
                         | LENGTH LPAREN SymbolicExpression RPAREN
                         | ROUND LPAREN NumericExpression RPAREN
                         | ROUND LPAREN Identifier RPAREN
                         | ROUND LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | ROUND LPAREN NumericExpression COMMA Identifier RPAREN
                         | ROUND LPAREN Identifier COMMA NumericExpression RPAREN
                         | ROUND LPAREN Identifier COMMA Identifier RPAREN
                         | PRECISION LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | PRECISION LPAREN NumericExpression COMMA Identifier RPAREN
                         | PRECISION LPAREN Identifier COMMA NumericExpression RPAREN
                         | PRECISION LPAREN Identifier COMMA Identifier RPAREN
                         | TRUNC LPAREN NumericExpression RPAREN
                         | TRUNC LPAREN Identifier RPAREN
                         | TRUNC LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | TRUNC LPAREN NumericExpression COMMA Identifier RPAREN
                         | TRUNC LPAREN Identifier COMMA NumericExpression RPAREN
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
                         | UNIFORM LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | UNIFORM LPAREN NumericExpression COMMA Identifier RPAREN
                         | UNIFORM LPAREN Identifier COMMA NumericExpression RPAREN
                         | UNIFORM LPAREN Identifier COMMA Identifier RPAREN
                         | NORMAL LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | NORMAL LPAREN NumericExpression COMMA Identifier RPAREN
                         | NORMAL LPAREN Identifier COMMA NumericExpression RPAREN
                         | NORMAL LPAREN Identifier COMMA Identifier RPAREN
                         | BETA LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | BETA LPAREN NumericExpression COMMA Identifier RPAREN
                         | BETA LPAREN Identifier COMMA NumericExpression RPAREN
                         | BETA LPAREN Identifier COMMA Identifier RPAREN
                         | GAMMA LPAREN NumericExpression RPAREN
                         | GAMMA LPAREN Identifier RPAREN
                         | POISSON LPAREN NumericExpression RPAREN
                         | POISSON LPAREN Identifier RPAREN
                         | IRAND224 LPAREN RPAREN
                         | UNIFORM01 LPAREN RPAREN
                         | NORMAL01 LPAREN RPAREN
                         | CAUCHY LPAREN RPAREN
                         | EXPONENTIAL LPAREN RPAREN
                         | TIME LPAREN RPAREN
                         | ID LPAREN Identifier RPAREN
                         | ID LPAREN SymbolicExpression RPAREN
                         | ID LPAREN NumericExpression RPAREN
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
    '''ConditionalNumericExpression : IF Identifier THEN NumericExpression ELSE NumericExpression
                                    | IF Identifier THEN NumericExpression ELSE Identifier
                                    | IF Identifier THEN Identifier ELSE NumericExpression
                                    | IF Identifier THEN Identifier ELSE Identifier
                                    | IF NumericExpression THEN NumericExpression ELSE NumericExpression
                                    | IF NumericExpression THEN NumericExpression ELSE Identifier
                                    | IF NumericExpression THEN Identifier ELSE NumericExpression
                                    | IF NumericExpression THEN Identifier ELSE Identifier
                                    | IF SymbolicExpression THEN NumericExpression ELSE NumericExpression
                                    | IF SymbolicExpression THEN NumericExpression ELSE Identifier
                                    | IF SymbolicExpression THEN Identifier ELSE NumericExpression
                                    | IF SymbolicExpression THEN Identifier ELSE Identifier
                                    | IF LogicalExpression THEN NumericExpression ELSE NumericExpression
                                    | IF LogicalExpression THEN NumericExpression ELSE Identifier
                                    | IF LogicalExpression THEN Identifier ELSE NumericExpression
                                    | IF LogicalExpression THEN Identifier ELSE Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN NumericExpression ELSE NumericExpression
                                    | IF ConnectedConstraintLogicalExpression THEN NumericExpression ELSE Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE NumericExpression
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF IteratedConstraintLogicalExpression THEN NumericExpression ELSE NumericExpression
                                    | IF IteratedConstraintLogicalExpression THEN NumericExpression ELSE Identifier
                                    | IF IteratedConstraintLogicalExpression THEN Identifier ELSE NumericExpression
                                    | IF IteratedConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF AllDiffExpression THEN NumericExpression ELSE NumericExpression
                                    | IF AllDiffExpression THEN NumericExpression ELSE Identifier
                                    | IF AllDiffExpression THEN Identifier ELSE NumericExpression
                                    | IF AllDiffExpression THEN Identifier ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericExpression ELSE NumericExpression
                                    | IF EntryConstraintLogicalExpression THEN NumericExpression ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE NumericExpression
                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF Identifier THEN NumericExpression
                                    | IF Identifier THEN Identifier
                                    | IF NumericExpression THEN NumericExpression
                                    | IF NumericExpression THEN Identifier
                                    | IF SymbolicExpression THEN NumericExpression
                                    | IF SymbolicExpression THEN Identifier
                                    | IF LogicalExpression THEN NumericExpression
                                    | IF LogicalExpression THEN Identifier
                                    | IF ConnectedConstraintLogicalExpression THEN NumericExpression
                                    | IF ConnectedConstraintLogicalExpression THEN Identifier
                                    | IF IteratedConstraintLogicalExpression THEN NumericExpression
                                    | IF IteratedConstraintLogicalExpression THEN Identifier
                                    | IF AllDiffExpression THEN NumericExpression
                                    | IF AllDiffExpression THEN Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericExpression
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
    '''Range : NumericExpression DOTS NumericExpression BY NumericExpression
             | NumericExpression DOTS NumericExpression BY Identifier
             | NumericExpression DOTS Identifier BY NumericExpression
             | NumericExpression DOTS Identifier BY Identifier
             | Identifier DOTS NumericExpression BY NumericExpression
             | Identifier DOTS NumericExpression BY Identifier
             | Identifier DOTS Identifier BY NumericExpression
             | Identifier DOTS Identifier BY Identifier
             | NumericExpression DOTS NumericExpression
             | NumericExpression DOTS Identifier
             | Identifier DOTS NumericExpression
             | Identifier DOTS Identifier'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

def p_Identifier(t):
    '''Identifier : ID UNDERLINE LBRACE ValueList RBRACE
                  | ID UNDERLINE LBRACE NumericExpression RBRACE
                  | ID UNDERLINE LBRACE Identifier RBRACE
                  | ID UNDERLINE LBRACE SymbolicExpression RBRACE
                  | ID LBRACKET ValueList RBRACKET
                  | ID LBRACKET NumericExpression RBRACKET
                  | ID LBRACKET Identifier RBRACKET
                  | ID LBRACKET SymbolicExpression RBRACKET
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
    '''ValueList : ValueList COMMA NumericExpression
                 | ValueList COMMA Identifier
                 | ValueList COMMA SymbolicExpression
                 | NumericExpression COMMA NumericExpression
                 | NumericExpression COMMA Identifier
                 | NumericExpression COMMA SymbolicExpression
                 | Identifier COMMA NumericExpression
                 | Identifier COMMA Identifier
                 | Identifier COMMA SymbolicExpression
                 | SymbolicExpression COMMA NumericExpression
                 | SymbolicExpression COMMA Identifier
                 | SymbolicExpression COMMA SymbolicExpression'''

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
