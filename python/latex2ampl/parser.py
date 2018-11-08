#!/usr/bin/python -tt

from lexer import tokens

from Main import *
from LinearProgram import *
from LinearEquations import *
from LinearExpression import *
from Objectives import *
from Constraints import *
from ConstraintExpression import *
from NodeExpression import *
from ArcExpression import *
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
    ('right', 'SLASHES', 'SEMICOLON'),
    ('right', 'FOR', 'WHERE', 'COLON'),
    ('right', 'PIPE'),
    ('right', 'DEFAULT', 'DIMEN', 'ASSIGN'),
    ('right', 'LPAREN', 'RPAREN', 'LLBRACE', 'RRBRACE', 'LBRACKET', 'RBRACKET'),
    ('right', 'LBRACE', 'RBRACE', 'UNDERLINE', 'FRAC'),
    ('left', 'MAXIMIZE', 'MINIMIZE'),
    ('right', 'IMPLIES', 'ISIMPLIEDBY', 'IFANDONLYIF'),
    ('right', 'IF', 'THEN', 'ELSE'),
    ('left', 'OR'),
    ('left', 'FORALL', 'EXISTS', 'NEXISTS'),
    ('left', 'AND'),
    ('right', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'SUBSET', 'NOTSUBSET'),
    ('left', 'NOT'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION'),
    ('left', 'INTER'),
    ('left', 'CROSS'),
    ('left', 'SETOF', 'COUNT', 'ATMOST', 'ATLEAST', 'EXACTLY', 'NUMBEROF', 'ALLDIFF', 'NODE', 'NETIN', 'NETOUT', 'ARC', 'FROM', 'TO', 'OBJ'),
    ('right', 'DOTS', 'BY'),
    ('right', 'AMPERSAND'),
    ('left', 'PLUS', 'MINUS', 'LESS'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'QUOTIENT'),
    ('left', 'UPLUS', 'UMINUS'),
    ('right', 'CARET'),
    ('left', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'ASIN', 'SINH', 'ASINH', 'COS', 'ACOS', 'COSH', 'ACOSH', 'ATAN', 'TAN', 'ATANH', 'TANH', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'INTEGERSET', 'INTEGERSETPOSITIVE', 'INTEGERSETNEGATIVE', 'INTEGERSETWITHONELIMIT', 'INTEGERSETWITHTWOLIMITS', 
      'REALSET', 'REALSETPOSITIVE', 'REALSETNEGATIVE', 'REALSETWITHONELIMIT', 'REALSETWITHTWOLIMITS', 
      'NATURALSET', 'NATURALSETWITHONELIMIT', 'NATURALSETWITHTWOLIMITS', 'BINARYSET', 'SYMBOLIC', 'LOGICAL', 'ORDERED', 'CIRCULAR')
)

def p_Main(t):
  '''MAIN : LinearEquations'''
  t[0] = Main(t[1])

def p_LinearEquations(t):
    '''LinearEquations : ConstraintList'''
    t[0] = LinearEquations(Constraints(t[1]))

def p_Objective(t):
    '''Objective : MAXIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression
                 | MAXIMIZE Identifier FOR IndexingExpression
                 | MAXIMIZE Identifier WHERE IndexingExpression
                 | MAXIMIZE Identifier COLON IndexingExpression
                 | MAXIMIZE Identifier

                 | MINIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MINIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MINIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MINIMIZE NumericSymbolicExpression
                 | MINIMIZE Identifier FOR IndexingExpression
                 | MINIMIZE Identifier WHERE IndexingExpression
                 | MINIMIZE Identifier COLON IndexingExpression
                 | MINIMIZE Identifier'''

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
                      | ConstraintList NodeExpression SLASHES
                      | ConstraintList ArcExpression SLASHES
                      | ConstraintList Declarations SLASHES
                      | ConstraintList Objective
                      | ConstraintList Constraint
                      | ConstraintList NodeExpression
                      | ConstraintList ArcExpression
                      | ConstraintList Declarations
                      | Objective SLASHES
                      | Constraint SLASHES
                      | NodeExpression SLASHES
                      | ArcExpression SLASHES
                      | Declarations SLASHES
                      | Objective
                      | Constraint
                      | NodeExpression
                      | ArcExpression
                      | Declarations'''

    if len(t) > 2 and not isinstance(t[2], str):
        t[0] = t[1] + [t[2]]

    else:
        t[0] = [t[1]]

def p_NetExpression(t):
    '''NetExpression : NETIN
                     | NETOUT
                     | MINUS NetExpression %prec UMINUS
                     | PLUS NetExpression %prec UPLUS
                     | NETIN PLUS NumericSymbolicExpression
                     | NETIN MINUS NumericSymbolicExpression
                     | NETIN PLUS Identifier
                     | NETIN MINUS Identifier
                     | NETOUT PLUS NumericSymbolicExpression
                     | NETOUT MINUS NumericSymbolicExpression
                     | NETOUT PLUS Identifier
                     | NETOUT MINUS Identifier
                     | NumericSymbolicExpression PLUS NETIN
                     | NumericSymbolicExpression MINUS NETIN
                     | Identifier PLUS NETIN
                     | Identifier MINUS NETIN
                     | NumericSymbolicExpression PLUS NETOUT
                     | NumericSymbolicExpression MINUS NETOUT
                     | Identifier PLUS NETOUT
                     | Identifier MINUS NETOUT'''

    if len(t) == 2:
      if t.slice[1].type == "NETIN":
        t[0] = ValuedNumericExpression(NetInExpression())

      else:
        t[0] = ValuedNumericExpression(NetOutExpression())

    else:

      if t.slice[1].type == "MINUS":
        t[0] = MinusNumericExpression(t[2])

      elif t.slice[1].type == "PLUS":
        t[0] = ValuedNumericExpression(t[2])

      else:

        if t.slice[1].type == "NETIN":
          t[1] = ValuedNumericExpression(NetInExpression())

        elif t.slice[1].type == "NETOUT":
          t[1] = ValuedNumericExpression(NetOutExpression())

        elif isinstance(t[1], Identifier):
          t[1] = ValuedNumericExpression(t[1])

        if t.slice[3].type == "NETIN":
          t[3] = ValuedNumericExpression(NetInExpression())

        elif t.slice[3].type == "NETOUT":
          t[3] = ValuedNumericExpression(NetOutExpression())

        elif isinstance(t[3], Identifier):
          t[3] = ValuedNumericExpression(t[3])

        op = None
        if t.slice[2].type == "PLUS":
          op = NumericExpressionWithArithmeticOperation.PLUS
        else:
          op = NumericExpressionWithArithmeticOperation.MINUS

        t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

def p_NodeExpression(t):
    '''NodeExpression : NODE Identifier NetExpression EQ NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier NetExpression EQ NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier NetExpression EQ NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier NetExpression EQ NumericSymbolicExpression

                      | NODE Identifier NetExpression EQ Identifier FOR IndexingExpression
                      | NODE Identifier NetExpression EQ Identifier WHERE IndexingExpression
                      | NODE Identifier NetExpression EQ Identifier COLON IndexingExpression
                      | NODE Identifier NetExpression EQ Identifier

                      | NODE Identifier NetExpression LE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier NetExpression LE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier NetExpression LE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier NetExpression LE NumericSymbolicExpression

                      | NODE Identifier NetExpression LE Identifier FOR IndexingExpression
                      | NODE Identifier NetExpression LE Identifier WHERE IndexingExpression
                      | NODE Identifier NetExpression LE Identifier COLON IndexingExpression
                      | NODE Identifier NetExpression LE Identifier

                      | NODE Identifier NetExpression GE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier NetExpression GE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier NetExpression GE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier NetExpression GE NumericSymbolicExpression

                      | NODE Identifier NetExpression GE Identifier FOR IndexingExpression
                      | NODE Identifier NetExpression GE Identifier WHERE IndexingExpression
                      | NODE Identifier NetExpression GE Identifier COLON IndexingExpression
                      | NODE Identifier NetExpression GE Identifier
                      
                      
                      | NODE Identifier NumericSymbolicExpression EQ NetExpression FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression EQ NetExpression WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression EQ NetExpression COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression EQ NetExpression

                      | NODE Identifier Identifier EQ NetExpression FOR IndexingExpression
                      | NODE Identifier Identifier EQ NetExpression WHERE IndexingExpression
                      | NODE Identifier Identifier EQ NetExpression COLON IndexingExpression
                      | NODE Identifier Identifier EQ NetExpression

                      | NODE Identifier NumericSymbolicExpression LE NetExpression FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression

                      | NODE Identifier Identifier LE NetExpression FOR IndexingExpression
                      | NODE Identifier Identifier LE NetExpression WHERE IndexingExpression
                      | NODE Identifier Identifier LE NetExpression COLON IndexingExpression
                      | NODE Identifier Identifier LE NetExpression

                      | NODE Identifier NumericSymbolicExpression GE NetExpression FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression

                      | NODE Identifier Identifier GE NetExpression FOR IndexingExpression
                      | NODE Identifier Identifier GE NetExpression WHERE IndexingExpression
                      | NODE Identifier Identifier GE NetExpression COLON IndexingExpression
                      | NODE Identifier Identifier GE NetExpression

                      | NODE Identifier Identifier GE NetExpression GE Identifier FOR IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE Identifier WHERE IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE Identifier COLON IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE Identifier

                      | NODE Identifier Identifier GE NetExpression GE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier Identifier GE NetExpression GE NumericSymbolicExpression

                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE Identifier FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE Identifier WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE Identifier COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE Identifier

                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression GE NetExpression GE NumericSymbolicExpression

                      | NODE Identifier Identifier LE NetExpression LE Identifier FOR IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE Identifier WHERE IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE Identifier COLON IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE Identifier

                      | NODE Identifier Identifier LE NetExpression LE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier Identifier LE NetExpression LE NumericSymbolicExpression

                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE Identifier FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE Identifier WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE Identifier COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE Identifier

                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE NumericSymbolicExpression FOR IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE NumericSymbolicExpression WHERE IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE NumericSymbolicExpression COLON IndexingExpression
                      | NODE Identifier NumericSymbolicExpression LE NetExpression LE NumericSymbolicExpression'''

    op = None
    if t.slice[4].type == "LE":
      op = NodeExpression.LE

    elif t.slice[4].type == "GE":
      op = NodeExpression.GE

    else:
      op = NodeExpression.EQ

    if len(t) > 6 and (t.slice[6].type == "LE" or t.slice[6].type == "GE"):
      if len(t) > 9:
          t[9].setStmtIndexing(True)
          t[0] = NodeExpression(t[2], op, t[3], t[5], t[7], t[9])

      else:
          t[0] = NodeExpression(t[2], op, t[3], t[5], t[7])

    else:

      if len(t) > 7:
          t[7].setStmtIndexing(True)
          t[0] = NodeExpression(t[2], op, t[3], t[5], None, t[7])

      else:
          t[0] = NodeExpression(t[2], op, t[3], t[5])

def p_IdentifierList(t):
    '''IdentifierList : IdentifierList COMMA Identifier LPAREN NumericSymbolicExpression RPAREN
                      | IdentifierList COMMA Identifier
                      | Identifier LPAREN NumericSymbolicExpression RPAREN COMMA Identifier LPAREN NumericSymbolicExpression RPAREN
                      | Identifier LPAREN NumericSymbolicExpression RPAREN COMMA Identifier
                      | Identifier COMMA Identifier LPAREN NumericSymbolicExpression RPAREN
                      | Identifier COMMA Identifier'''

    if t.slice[1].type == "IdentifierList":
      if len(t) > 4:
        t[0] = t[1] + [ArcItem(t[3], t[5])]
      else:
        t[0] = t[1] + [ArcItem(t[3])]

    else:

      if len(t) > 9:
        t[0] = [ArcItem(t[1], t[3]), ArcItem(t[6], t[8])]
      
      elif len(t) > 6:
        if t.slice[2].type == "LPAREN":
          t[0] = [ArcItem(t[1], t[3]), ArcItem(t[6])]
        else:
          t[0] = [ArcItem(t[1]), ArcItem(t[3], t[5])]

      else:
        t[0] = [ArcItem(t[1]), ArcItem(t[3])]

def p_FromList(t):
    '''FromList : FROM Identifier
                | FROM Identifier LPAREN NumericSymbolicExpression RPAREN
                | FROM IdentifierList'''

    if len(t) > 3:
      t[0] = [ArcItem(t[2], t[4])]

    else:

      if t.slice[2].type == "IdentifierList":
        t[0] = t[2]

      else:
        t[0] = [ArcItem(t[2])]

def p_ToList(t):
    '''ToList : TO Identifier
              | TO Identifier LPAREN NumericSymbolicExpression RPAREN
              | TO IdentifierList'''
    if len(t) > 3:
      t[0] = [ArcItem(t[2], t[4])]

    else:

      if t.slice[2].type == "IdentifierList":
        t[0] = t[2]

      else:
        t[0] = [ArcItem(t[2])]

def p_ArcObj(t):
    '''ArcObj : OBJ ID Identifier'''
    t[0] = [ID(t[2]), t[3]]

def p_ArcExpression(t):
    '''ArcExpression : ARC Identifier DeclarationAttributeList FromList ToList ArcObj
                     | ARC Identifier DeclarationAttributeList FromList ToList
                     | ARC Identifier DeclarationAttributeList FromList ArcObj
                     | ARC Identifier DeclarationAttributeList FromList
                     | ARC Identifier DeclarationAttributeList ToList ArcObj
                     | ARC Identifier DeclarationAttributeList ToList
                     | ARC Identifier DeclarationAttributeList ArcObj
                     | ARC Identifier DeclarationAttributeList
                     | ARC Identifier FromList ToList ArcObj
                     | ARC Identifier FromList ToList
                     | ARC Identifier FromList ArcObj
                     | ARC Identifier FromList
                     | ARC Identifier ToList ArcObj
                     | ARC Identifier ToList
                     | ARC Identifier ArcObj
                     | ARC Identifier

                     | ARC Identifier DeclarationAttributeList FromList ToList ArcObj FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ToList FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ArcObj FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList ArcObj FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList ArcObj FOR IndexingExpression
                     | ARC Identifier DeclarationAttributeList FOR IndexingExpression
                     | ARC Identifier FromList ToList ArcObj FOR IndexingExpression
                     | ARC Identifier FromList ToList FOR IndexingExpression
                     | ARC Identifier FromList ArcObj FOR IndexingExpression
                     | ARC Identifier FromList FOR IndexingExpression
                     | ARC Identifier ToList ArcObj FOR IndexingExpression
                     | ARC Identifier ToList FOR IndexingExpression
                     | ARC Identifier ArcObj FOR IndexingExpression
                     | ARC Identifier FOR IndexingExpression
                    
                     | ARC Identifier DeclarationAttributeList FromList ToList ArcObj WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ToList WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ArcObj WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList ArcObj WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList ArcObj WHERE IndexingExpression
                     | ARC Identifier DeclarationAttributeList WHERE IndexingExpression
                     | ARC Identifier FromList ToList ArcObj WHERE IndexingExpression
                     | ARC Identifier FromList ToList WHERE IndexingExpression
                     | ARC Identifier FromList ArcObj WHERE IndexingExpression
                     | ARC Identifier FromList WHERE IndexingExpression
                     | ARC Identifier ToList ArcObj WHERE IndexingExpression
                     | ARC Identifier ToList WHERE IndexingExpression
                     | ARC Identifier ArcObj WHERE IndexingExpression
                     | ARC Identifier WHERE IndexingExpression

                     | ARC Identifier DeclarationAttributeList FromList ToList ArcObj COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ToList COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList ArcObj COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList FromList COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList ArcObj COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList ToList COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList ArcObj COLON IndexingExpression
                     | ARC Identifier DeclarationAttributeList COLON IndexingExpression
                     | ARC Identifier FromList ToList ArcObj COLON IndexingExpression
                     | ARC Identifier FromList ToList COLON IndexingExpression
                     | ARC Identifier FromList ArcObj COLON IndexingExpression
                     | ARC Identifier FromList COLON IndexingExpression
                     | ARC Identifier ToList ArcObj COLON IndexingExpression
                     | ARC Identifier ToList COLON IndexingExpression
                     | ARC Identifier ArcObj COLON IndexingExpression
                     | ARC Identifier COLON IndexingExpression'''

    _types = map(lambda el: el.type, t.slice)
    
    if "DeclarationAttributeList" in _types:
      attributes = t[_types.index("DeclarationAttributeList")]
    else:
      attributes = None

    if "FromList" in _types:
      _from = t[_types.index("FromList")]
    else:
      _from = None

    if "ToList" in _types:
      _to = t[_types.index("ToList")]
    else:
      _to = None

    if "ArcObj" in _types:
      _obj = t[_types.index("ArcObj")]
      objName = _obj[0]
      objValue = _obj[1]
    else:
      objName = None
      objValue = None

    if "IndexingExpression" in _types:
      indexing = t[_types.index("IndexingExpression")]
      indexing.setStmtIndexing(True)
    else:
      indexing = None

    t[0] = ArcExpression(t[2], attributes, _from, _to, objName, objValue, indexing)


def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression WHERE IndexingExpression
                  | ConstraintExpression COLON IndexingExpression
                  | ConstraintExpression

                  | ValueListInExpression FOR IndexingExpression
                  | ValueListInExpression WHERE IndexingExpression
                  | ValueListInExpression COLON IndexingExpression
                  | ValueListInExpression

                  | EntryConstraintLogicalExpression FOR IndexingExpression
                  | EntryConstraintLogicalExpression WHERE IndexingExpression
                  | EntryConstraintLogicalExpression COLON IndexingExpression
                  | EntryConstraintLogicalExpression'''
    
    if not isinstance(t[1], ConstraintExpression) and not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])


def p_ConstraintExpressionLogical(t):
    '''ConstraintExpression : ConstraintExpression AND ConstraintExpression
                            | ConstraintExpression AND ValueListInExpression
                            | ConstraintExpression AND EntryConstraintLogicalExpression

                            | ValueListInExpression AND ConstraintExpression
                            | EntryConstraintLogicalExpression AND ConstraintExpression

                            | ConstraintExpression OR ConstraintExpression
                            | ConstraintExpression OR ValueListInExpression
                            | ConstraintExpression OR EntryConstraintLogicalExpression

                            | ValueListInExpression OR ConstraintExpression
                            | EntryConstraintLogicalExpression OR ConstraintExpression

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

        if not isinstance(t[1], LogicalExpression):
          entry = LogicalExpression([t[1]])
        else:
          entry = t[1]

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

                            | Identifier IMPLIES ConstraintExpression ELSE Identifier
                            | Identifier IMPLIES Identifier ELSE Identifier
                            | Identifier IMPLIES Identifier ELSE ValueListInExpression
                            | Identifier IMPLIES Identifier ELSE ConstraintExpression
                            | Identifier IMPLIES Identifier ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES Identifier ELSE NumericSymbolicExpression

                            | Identifier IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | Identifier IMPLIES ValueListInExpression ELSE Identifier
                            | Identifier IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | Identifier IMPLIES ValueListInExpression ELSE ConstraintExpression
                            | Identifier IMPLIES ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES ValueListInExpression ELSE NumericSymbolicExpression

                            | Identifier IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE Identifier
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | Identifier IMPLIES ConstraintExpression ELSE NumericSymbolicExpression
                            | Identifier IMPLIES NumericSymbolicExpression ELSE Identifier
                            | Identifier IMPLIES NumericSymbolicExpression ELSE ValueListInExpression
                            | Identifier IMPLIES NumericSymbolicExpression ELSE ConstraintExpression
                            | Identifier IMPLIES NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | Identifier IMPLIES NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES Identifier ELSE Identifier
                            | NumericSymbolicExpression IMPLIES Identifier ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES Identifier ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES Identifier ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES Identifier ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE NumericSymbolicExpression
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE Identifier
                            | ConstraintExpression IMPLIES Identifier ELSE Identifier
                            | ConstraintExpression IMPLIES Identifier ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES Identifier ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES Identifier ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES Identifier ELSE NumericSymbolicExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE Identifier
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE Identifier
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE NumericSymbolicExpression
                            | ConstraintExpression IMPLIES NumericSymbolicExpression ELSE Identifier
                            | ConstraintExpression IMPLIES NumericSymbolicExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES NumericSymbolicExpression ELSE ConstraintExpression
                            | ConstraintExpression IMPLIES NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE Identifier
                            | ValueListInExpression IMPLIES Identifier ELSE Identifier
                            | ValueListInExpression IMPLIES Identifier ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES Identifier ELSE ConstraintExpression
                            | ValueListInExpression IMPLIES Identifier ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES Identifier ELSE NumericSymbolicExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE Identifier
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE ConstraintExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression ELSE Identifier
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE NumericSymbolicExpression
                            | ValueListInExpression IMPLIES NumericSymbolicExpression ELSE Identifier
                            | ValueListInExpression IMPLIES NumericSymbolicExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES NumericSymbolicExpression ELSE ConstraintExpression
                            | ValueListInExpression IMPLIES NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE Identifier
                            | EntryConstraintLogicalExpression IMPLIES Identifier ELSE Identifier
                            | EntryConstraintLogicalExpression IMPLIES Identifier ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES Identifier ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES Identifier ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES Identifier ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression ELSE Identifier
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE Identifier
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression ELSE NumericSymbolicExpression
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression ELSE Identifier
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression ELSE NumericSymbolicExpression


                            
                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY Identifier ELSE Identifier
                            | Identifier ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY Identifier ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY Identifier ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY Identifier ELSE NumericSymbolicExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE NumericSymbolicExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE NumericSymbolicExpression
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression ELSE ConstraintExpression
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE NumericSymbolicExpression
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE NumericSymbolicExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE NumericSymbolicExpression
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE NumericSymbolicExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE NumericSymbolicExpression
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression ELSE NumericSymbolicExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression ELSE NumericSymbolicExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression ELSE Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression ELSE ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression ELSE EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression ELSE NumericSymbolicExpression



                            | Identifier IMPLIES ConstraintExpression
                            | Identifier IMPLIES Identifier
                            | Identifier IMPLIES ValueListInExpression
                            | Identifier IMPLIES EntryConstraintLogicalExpression
                            | Identifier IMPLIES NumericSymbolicExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression
                            | NumericSymbolicExpression IMPLIES Identifier
                            | NumericSymbolicExpression IMPLIES ValueListInExpression
                            | NumericSymbolicExpression IMPLIES EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IMPLIES NumericSymbolicExpression

                            | ConstraintExpression IMPLIES ConstraintExpression
                            | ConstraintExpression IMPLIES Identifier
                            | ConstraintExpression IMPLIES ValueListInExpression
                            | ConstraintExpression IMPLIES EntryConstraintLogicalExpression
                            | ConstraintExpression IMPLIES NumericSymbolicExpression

                            | ValueListInExpression IMPLIES ConstraintExpression
                            | ValueListInExpression IMPLIES Identifier
                            | ValueListInExpression IMPLIES ValueListInExpression
                            | ValueListInExpression IMPLIES EntryConstraintLogicalExpression
                            | ValueListInExpression IMPLIES NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IMPLIES ConstraintExpression
                            | EntryConstraintLogicalExpression IMPLIES Identifier
                            | EntryConstraintLogicalExpression IMPLIES ValueListInExpression
                            | EntryConstraintLogicalExpression IMPLIES EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IMPLIES NumericSymbolicExpression



                            | Identifier ISIMPLIEDBY ConstraintExpression
                            | Identifier ISIMPLIEDBY Identifier
                            | Identifier ISIMPLIEDBY ValueListInExpression
                            | Identifier ISIMPLIEDBY EntryConstraintLogicalExpression
                            | Identifier ISIMPLIEDBY NumericSymbolicExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY NumericSymbolicExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | ConstraintExpression ISIMPLIEDBY NumericSymbolicExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | ValueListInExpression ISIMPLIEDBY NumericSymbolicExpression

                            | EntryConstraintLogicalExpression ISIMPLIEDBY ConstraintExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY Identifier
                            | EntryConstraintLogicalExpression ISIMPLIEDBY ValueListInExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression ISIMPLIEDBY NumericSymbolicExpression



                            | Identifier IFANDONLYIF ConstraintExpression
                            | Identifier IFANDONLYIF Identifier
                            | Identifier IFANDONLYIF ValueListInExpression
                            | Identifier IFANDONLYIF EntryConstraintLogicalExpression
                            | Identifier IFANDONLYIF NumericSymbolicExpression

                            | NumericSymbolicExpression IFANDONLYIF ConstraintExpression
                            | NumericSymbolicExpression IFANDONLYIF Identifier
                            | NumericSymbolicExpression IFANDONLYIF ValueListInExpression
                            | NumericSymbolicExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | NumericSymbolicExpression IFANDONLYIF NumericSymbolicExpression

                            | ConstraintExpression IFANDONLYIF ConstraintExpression
                            | ConstraintExpression IFANDONLYIF Identifier
                            | ConstraintExpression IFANDONLYIF ValueListInExpression
                            | ConstraintExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | ConstraintExpression IFANDONLYIF NumericSymbolicExpression

                            | ValueListInExpression IFANDONLYIF ConstraintExpression
                            | ValueListInExpression IFANDONLYIF Identifier
                            | ValueListInExpression IFANDONLYIF ValueListInExpression
                            | ValueListInExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | ValueListInExpression IFANDONLYIF NumericSymbolicExpression

                            | EntryConstraintLogicalExpression IFANDONLYIF ConstraintExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF Identifier
                            | EntryConstraintLogicalExpression IFANDONLYIF ValueListInExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF EntryConstraintLogicalExpression
                            | EntryConstraintLogicalExpression IFANDONLYIF NumericSymbolicExpression'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

    if len(t) > 5 and (isinstance(t[5], NumericExpression) or isinstance(t[5], SymbolicExpression) or isinstance(t[5], Identifier)):
      t[5] = EntryLogicalExpressionNumericOrSymbolic(t[5])

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
    '''ConstraintExpression : Identifier LE Identifier LE Identifier
                            | Identifier LE Identifier LE NumericSymbolicExpression
                            | Identifier LE NumericSymbolicExpression LE Identifier
                            | Identifier LE NumericSymbolicExpression LE NumericSymbolicExpression
                            | Identifier GE Identifier GE Identifier
                            | Identifier GE Identifier GE NumericSymbolicExpression
                            | Identifier GE NumericSymbolicExpression GE Identifier
                            | Identifier GE NumericSymbolicExpression GE NumericSymbolicExpression

                            | NumericSymbolicExpression LE Identifier LE Identifier
                            | NumericSymbolicExpression LE Identifier LE NumericSymbolicExpression
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE Identifier
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE NumericSymbolicExpression
                            | NumericSymbolicExpression GE Identifier GE Identifier
                            | NumericSymbolicExpression GE Identifier GE NumericSymbolicExpression
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE Identifier
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE NumericSymbolicExpression'''

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

                                        | NumericSymbolicExpression IN SetExpression
                                        | NumericSymbolicExpression IN Identifier
                                        | NumericSymbolicExpression SUBSET SetExpression
                                        | NumericSymbolicExpression SUBSET Identifier

                                        | Identifier IN SetExpression
                                        | Identifier IN Identifier
                                        | Identifier SUBSET SetExpression
                                        | Identifier SUBSET Identifier

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

      elif _type == "IN":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])

      elif _type == "SUBSET":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        if t.slice[2].type == "SUBSET" and not isinstance(t[1], SetExpression):
          t[1] = SetExpressionWithValue(t[1])

        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])


def p_IteratedConstraintLogicalExpression(t):
    '''IteratedConstraintLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | NFORALL LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | EXISTS LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression
                                           | NEXISTS LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression'''

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
                                            | EntryConstraintLogicalExpression OR EntryConstraintLogicalExpression'''

    if not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    if t.slice[2].type == "AND":
      t[0] = t[1].addAnd(t[3])
    else:
      t[0] = t[1].addOr(t[3])


def _getDeclarationExpression(entryConstraintLogicalExpression):

    attr = None
    numNot = 0
    putNot = False

    while isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionBetweenParenthesis) or \
          isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionNot):

          if isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionNot):
            numNot += 1

          entryConstraintLogicalExpression = entryConstraintLogicalExpression.logicalExpression

    # discard not expressions because it is not allowed in declaration attributes
    if numNot % 2 != 0:
      putNot = True

    op = entryConstraintLogicalExpression.op

    if isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionRelational):
      expr1 = entryConstraintLogicalExpression.numericExpression1
      expr2 = entryConstraintLogicalExpression.numericExpression2

    elif isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionWithSet):
      expr1 = entryConstraintLogicalExpression.identifier
      expr2 = entryConstraintLogicalExpression.setExpression

    elif isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionWithSetOperation):
      expr1 = entryConstraintLogicalExpression.setExpression1
      expr2 = entryConstraintLogicalExpression.setExpression2

    if putNot:
      expr2 = EntryLogicalExpressionNot(expr2)

    if op == EntryLogicalExpressionWithSet.IN:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.IN)

    if op == EntryLogicalExpressionWithSetOperation.SUBSET:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.WT)

    elif op == EntryLogicalExpressionRelational.LT:
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

    if not isinstance(expr1, ValueList):
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
                       | DeclarationList SEMICOLON ValueListInExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression

                       | DeclarationList SEMICOLON ValueListInExpression FOR IndexingExpression
                       | DeclarationList SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | DeclarationList SEMICOLON ValueListInExpression COLON IndexingExpression

                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression SEMICOLON Declaration
                       | ValueListInExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression

                       | ValueListInExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON Declaration
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON Declaration
                       | ValueListInExpression COLON IndexingExpression SEMICOLON Declaration
                        
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression

                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON Declaration

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | Declaration'''

    if len(t) > 7:

      t[3].setStmtIndexing(True)

      if isinstance(t[1], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[1])
        t[1] = Declaration(declaration, t[3]) # turn into Declaration
        t[1] = [t[1]] # turn into DeclarationList


      t[7].setStmtIndexing(True)

      if isinstance(t[5], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[5])
        t[5] = Declaration(declaration, t[7]) # turn into Declaration

      t[0] = t[1] + [t[5]]

    elif len(t) > 5:

      if t.slice[2].type == "SEMICOLON":

        t[5].setStmtIndexing(True)

        if isinstance(t[1], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[1])
          t[1] = Declaration(declaration) # turn into Declaration
          t[1] = [t[1]] # turn into DeclarationList

        if isinstance(t[3], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[3])
          t[3] = Declaration(declaration, t[5]) # turn into Declaration

        t[0] = t[1] + [t[3]]

      else:

        t[3].setStmtIndexing(True)

        if isinstance(t[1], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[1])
          t[1] = Declaration(declaration, t[3]) # turn into Declaration
          t[1] = [t[1]] # turn into DeclarationList

        if isinstance(t[5], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[5])
          t[5] = Declaration(declaration) # turn into Declaration

        t[0] = t[1] + [t[5]]

    elif len(t) > 3:

      if isinstance(t[1], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[1])
        t[1] = Declaration(declaration) # turn into Declaration
        t[1] = [t[1]] # turn into DeclarationList

      if isinstance(t[3], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[3])
        t[3] = Declaration(declaration) # turn into Declaration

      t[0] = t[1] + [t[3]]

    else:
      t[0] = [t[1]]

def p_Declaration(t):
    '''Declaration : DeclarationExpression FOR IndexingExpression
                   | DeclarationExpression WHERE IndexingExpression
                   | DeclarationExpression COLON IndexingExpression

                   | ValueList FOR IndexingExpression
                   | ValueList WHERE IndexingExpression
                   | ValueList COLON IndexingExpression

                   | Identifier FOR IndexingExpression
                   | Identifier WHERE IndexingExpression
                   | Identifier COLON IndexingExpression

                   | NumericSymbolicExpression FOR IndexingExpression
                   | NumericSymbolicExpression WHERE IndexingExpression
                   | NumericSymbolicExpression COLON IndexingExpression

                   | DeclarationExpression'''

    if isinstance(t[1], EntryLogicalExpression):
      t[1] = _getDeclarationExpression(t[1])

    if len(t) > 4:
      t[0] = Declaration(t[1])

    elif len(t) > 3:
        t[3].setStmtIndexing(True)

        if isinstance(t[1], ValueList):
          t[1] = DeclarationExpression(t[1], [])

        elif isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
          t[1] = DeclarationExpression(ValueList([t[1]]), [])

        t[0] = Declaration(t[1], t[3])

    else:
        t[0] = Declaration(t[1])

def p_DeclarationExpression(t):
    '''DeclarationExpression : ValueList SUBSET SetExpression
                             | ValueList SUBSET Identifier
                             | ValueList DEFAULT SetExpression
                             | ValueList DEFAULT Identifier
                             | ValueList DEFAULT NumericSymbolicExpression
                             | ValueList DIMEN Identifier
                             | ValueList DIMEN NumericSymbolicExpression
                             | ValueList ASSIGN SetExpression
                             | ValueList ASSIGN Identifier
                             | ValueList ASSIGN NumericSymbolicExpression
                             | ValueList LE Identifier
                             | ValueList LE NumericSymbolicExpression
                             | ValueList GE Identifier
                             | ValueList GE NumericSymbolicExpression
                             | ValueList EQ Identifier
                             | ValueList EQ NumericSymbolicExpression
                             | ValueList LT Identifier
                             | ValueList LT NumericSymbolicExpression
                             | ValueList GT Identifier
                             | ValueList GT NumericSymbolicExpression
                             | ValueList NEQ Identifier
                             | ValueList NEQ NumericSymbolicExpression
                             | ValueList COMMA DeclarationAttributeList

                             | NumericSymbolicExpression DEFAULT SetExpression
                             | NumericSymbolicExpression DEFAULT Identifier
                             | NumericSymbolicExpression DEFAULT NumericSymbolicExpression
                             | NumericSymbolicExpression DIMEN Identifier
                             | NumericSymbolicExpression DIMEN NumericSymbolicExpression
                             | NumericSymbolicExpression ASSIGN SetExpression
                             | NumericSymbolicExpression ASSIGN Identifier
                             | NumericSymbolicExpression ASSIGN NumericSymbolicExpression
                             | NumericSymbolicExpression COMMA DeclarationAttributeList

                             | Identifier DEFAULT SetExpression
                             | Identifier DEFAULT Identifier
                             | Identifier DEFAULT NumericSymbolicExpression
                             | Identifier DIMEN Identifier
                             | Identifier DIMEN NumericSymbolicExpression
                             | Identifier ASSIGN SetExpression
                             | Identifier ASSIGN Identifier
                             | Identifier ASSIGN NumericSymbolicExpression
                             | Identifier COMMA DeclarationAttributeList

                             | EntryConstraintLogicalExpression COMMA DeclarationAttributeList
                             | ValueListInExpression COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList'''

    
    if isinstance(t[1], DeclarationExpression):
      if t.slice[2].type == "COMMA":
        t[1].addAttribute(t[3])
      else:
        t[1].addAttribute(t[2])

      t[0] = t[1]

    elif t.slice[1].type == "ValueListInExpression" or t.slice[1].type == "EntryConstraintLogicalExpression":
      t[0] = _getDeclarationExpression(t[1])
      t[0].addAttribute(t[3])

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
  '''DeclarationAttributeList : DeclarationAttributeList COMMA DeclarationAttribute
                              | DeclarationAttribute'''
  if len(t) > 3:
    t[0] = t[1] + [t[3]]
  else:
    t[0] = [t[1]]

def p_DeclarationAttribute(t):
  '''DeclarationAttribute : IN SetExpression
                          | IN Identifier

                          | SUBSET SetExpression
                          | SUBSET Identifier

                          | DEFAULT SetExpression
                          | DEFAULT Identifier
                          | DEFAULT NumericSymbolicExpression

                          | DIMEN Identifier
                          | DIMEN NumericSymbolicExpression

                          | ASSIGN SetExpression
                          | ASSIGN Identifier
                          | ASSIGN NumericSymbolicExpression

                          | LT Identifier
                          | LT NumericSymbolicExpression
                          | LE Identifier
                          | LE NumericSymbolicExpression
                          | EQ Identifier
                          | EQ NumericSymbolicExpression
                          | GT Identifier
                          | GT NumericSymbolicExpression
                          | GE Identifier
                          | GE NumericSymbolicExpression
                          | NEQ Identifier
                          | NEQ NumericSymbolicExpression'''

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


def p_ValueListInExpression(t):
    '''ValueListInExpression : ValueList IN SetExpression
                             | ValueList IN Identifier

                             | LPAREN ValueListInExpression RPAREN
                             | NOT ValueListInExpression'''

    if t.slice[1].type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif t.slice[1].type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      if not isinstance(t[3], SetExpression):
        t[3] = SetExpressionWithValue(t[3])

      t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])


def p_LogicalExpression(t):
    '''ConstraintExpression : EntryLogicalExpression

                            | AllDiffExpression
                            | IteratedConstraintLogicalExpression
                            | ConnectedConstraintLogicalExpression

                            | ConstraintExpression OR NumericSymbolicExpression
                            | ConstraintExpression OR Identifier
                            
                            | ValueListInExpression OR ValueListInExpression
                            | ValueListInExpression OR EntryConstraintLogicalExpression
                            | ValueListInExpression OR NumericSymbolicExpression
                            | ValueListInExpression OR Identifier

                            | EntryConstraintLogicalExpression OR ValueListInExpression
                            | EntryConstraintLogicalExpression OR NumericSymbolicExpression
                            | EntryConstraintLogicalExpression OR Identifier

                            | NumericSymbolicExpression OR ConstraintExpression
                            | NumericSymbolicExpression OR ValueListInExpression
                            | NumericSymbolicExpression OR EntryConstraintLogicalExpression
                            | NumericSymbolicExpression OR NumericSymbolicExpression
                            | NumericSymbolicExpression OR Identifier

                            | Identifier OR ConstraintExpression
                            | Identifier OR ValueListInExpression
                            | Identifier OR EntryConstraintLogicalExpression
                            | Identifier OR NumericSymbolicExpression
                            | Identifier OR Identifier

                            | ConstraintExpression AND NumericSymbolicExpression
                            | ConstraintExpression AND Identifier
                            
                            | ValueListInExpression AND ValueListInExpression
                            | ValueListInExpression AND EntryConstraintLogicalExpression
                            | ValueListInExpression AND NumericSymbolicExpression
                            | ValueListInExpression AND Identifier

                            | EntryConstraintLogicalExpression AND ValueListInExpression
                            | EntryConstraintLogicalExpression AND NumericSymbolicExpression
                            | EntryConstraintLogicalExpression AND Identifier
                            
                            | NumericSymbolicExpression AND ConstraintExpression
                            | NumericSymbolicExpression AND ValueListInExpression
                            | NumericSymbolicExpression AND EntryConstraintLogicalExpression
                            | NumericSymbolicExpression AND NumericSymbolicExpression
                            | NumericSymbolicExpression AND Identifier

                            | Identifier AND ConstraintExpression
                            | Identifier AND ValueListInExpression
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
                              | NOT Identifier'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    _type = t.slice[1].type
    if _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    elif _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    else:
      t[0] = t[2]


def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList NOTIN SetExpression
                              | ValueList NOTIN Identifier

                              | Tuple IN SetExpression
                              | Tuple IN Identifier
                              | Tuple NOTIN SetExpression
                              | Tuple NOTIN Identifier

                              | NumericSymbolicExpression NOTIN SetExpression
                              | NumericSymbolicExpression NOTIN Identifier

                              | Identifier NOTIN SetExpression
                              | Identifier NOTIN Identifier
                              | Identifier NOTSUBSET SetExpression
                              | Identifier NOTSUBSET Identifier

                              | SetExpression SUBSET SetExpression
                              | SetExpression SUBSET Identifier
                              | SetExpression NOTSUBSET SetExpression
                              | SetExpression NOTSUBSET Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if (t.slice[2].type == "SUBSET" or t.slice[2].type == "NOTSUBSET") and not isinstance(t[1], SetExpression):
      t[1] = SetExpressionWithValue(t[1])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
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
    '''EntryLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | FORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | NFORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | EXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | NEXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression'''

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


def p_AllDiffExpression(t):
    '''AllDiffExpression : ALLDIFF LLBRACE IndexingExpression RRBRACE Identifier
                         | ALLDIFF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:
      t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.ALLDIFF, t[3], t[5])


def p_SetExpressionWithOperation(t):
    '''SetExpression : SetExpression DIFF SetExpression
                     | SetExpression DIFF Identifier
                     | SetExpression SYMDIFF SetExpression
                     | SetExpression SYMDIFF Identifier
                     | SetExpression UNION SetExpression
                     | SetExpression UNION Identifier
                     | SetExpression INTER SetExpression
                     | SetExpression INTER Identifier
                     | SetExpression CROSS SetExpression
                     | SetExpression CROSS Identifier

                     | Identifier DIFF SetExpression
                     | Identifier DIFF Identifier
                     | Identifier SYMDIFF SetExpression
                     | Identifier SYMDIFF Identifier
                     | Identifier UNION SetExpression
                     | Identifier UNION Identifier
                     | Identifier INTER SetExpression
                     | Identifier INTER Identifier
                     | Identifier CROSS SetExpression
                     | Identifier CROSS Identifier'''

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
                     | LLBRACE TupleList RRBRACE
                     | LLBRACE SetExpression RRBRACE
                     | LLBRACE Identifier RRBRACE
                     | LLBRACE NumericSymbolicExpression RRBRACE
                     | LLBRACE IndexingExpression RRBRACE
                     | LLBRACE RRBRACE

                     | LPAREN SetExpression RPAREN

                     | Range
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
                     | ORDERED
                     | CIRCULAR

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

          t[0] = t[2]

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
                     | Identifier LBRACKET Identifier RBRACKET
                     | Identifier LBRACKET NumericSymbolicExpression RBRACKET'''

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = ValueList([t[3]])

    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE Tuple
                     | SETOF LLBRACE IndexingExpression RRBRACE Identifier
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression

                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                     | UNION UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression

                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Tuple
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE SetExpression
                     | INTER UNDERLINE LBRACE IndexingExpression RBRACE Identifier
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
    '''ConditionalSetExpression : IF ConstraintExpression THEN SetExpression ELSE SetExpression
                                | IF ConstraintExpression THEN SetExpression ELSE Identifier
                                | IF ConstraintExpression THEN Identifier ELSE SetExpression
                                | IF ConstraintExpression THEN SetExpression

                                | IF ValueListInExpression THEN SetExpression ELSE SetExpression
                                | IF ValueListInExpression THEN SetExpression ELSE Identifier
                                | IF ValueListInExpression THEN Identifier ELSE SetExpression
                                | IF ValueListInExpression THEN SetExpression

                                | IF EntryConstraintLogicalExpression THEN SetExpression ELSE SetExpression
                                | IF EntryConstraintLogicalExpression THEN SetExpression ELSE Identifier
                                | IF EntryConstraintLogicalExpression THEN Identifier ELSE SetExpression
                                | IF EntryConstraintLogicalExpression THEN SetExpression

                                | IF Identifier THEN SetExpression ELSE SetExpression
                                | IF Identifier THEN SetExpression ELSE Identifier
                                | IF Identifier THEN Identifier ELSE SetExpression
                                | IF Identifier THEN SetExpression

                                | IF NumericSymbolicExpression THEN SetExpression ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression ELSE Identifier
                                | IF NumericSymbolicExpression THEN Identifier ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression'''

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

                          | IndexingExpression PIPE ConstraintExpression
                          | IndexingExpression PIPE ValueListInExpression
                          | IndexingExpression PIPE EntryConstraintLogicalExpression
                          | IndexingExpression PIPE Identifier
                          | IndexingExpression PIPE NumericSymbolicExpression

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
    '''LogicalIndexExpression : IF ConstraintExpression
                              | IF ValueListInExpression
                              | IF EntryConstraintLogicalExpression
                              | IF Identifier
                              | IF NumericSymbolicExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])

    t[0] = ConditionalLinearExpression(t[2])

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | ValueList IN Identifier
                               
                               | Tuple IN SetExpression
                               | Tuple IN Identifier
                               
                               | Identifier IN SetExpression
                               | Identifier IN Identifier
                               
                               | NumericSymbolicExpression IN SetExpression
                               | NumericSymbolicExpression IN Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])

    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Identifier LE Identifier
                               | Identifier LE NumericSymbolicExpression
                               | Identifier GE Identifier
                               | Identifier GE NumericSymbolicExpression
                               | Identifier EQ SetExpression
                               | Identifier EQ Identifier
                               | Identifier EQ NumericSymbolicExpression
                               | Identifier LT Identifier
                               | Identifier LT NumericSymbolicExpression
                               | Identifier GT Identifier
                               | Identifier GT NumericSymbolicExpression
                               | Identifier NEQ Identifier
                               | Identifier NEQ NumericSymbolicExpression'''

    if t.slice[3].type == "Range":
      t[3] = SetExpressionWithValue(t[3])

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


def p_NumericSymbolicExpression(t):
    '''NumericSymbolicExpression : NumericExpression
                                 | SymbolicExpression
                                 | LPAREN NumericSymbolicExpression RPAREN'''

    if len(t) > 2:
        t[0] = NumericExpressionBetweenParenthesis(t[2])

    else:
        t[0] = t[1]


def p_StringSymbolicExpression(t):
    '''SymbolicExpression : STRING'''
    t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : Identifier AMPERSAND Identifier
                          | Identifier AMPERSAND NumericSymbolicExpression
                          | NumericSymbolicExpression AMPERSAND Identifier
                          | NumericSymbolicExpression AMPERSAND NumericSymbolicExpression'''

    if t.slice[2].type == "AMPERSAND":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

def p_FunctionSymbolicExpression(t):
    '''SymbolicExpression : SUBSTR LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression COMMA Identifier RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericSymbolicExpression RPAREN

                          | CHAR LPAREN Identifier RPAREN
                          | CHAR LPAREN NumericSymbolicExpression RPAREN

                          | SPRINTF LPAREN Identifier COMMA ValueList RPAREN
                          | SPRINTF LPAREN Identifier COMMA Identifier RPAREN
                          | SPRINTF LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA ValueList RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA Identifier RPAREN
                          | SPRINTF LPAREN SymbolicExpression COMMA NumericSymbolicExpression RPAREN

                          | SUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | SUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | SUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN

                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN SymbolicExpression COMMA SymbolicExpression COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA Identifier COMMA SymbolicExpression RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA Identifier RPAREN
                          | GSUB LPAREN Identifier COMMA SymbolicExpression COMMA SymbolicExpression RPAREN

                          | ALIAS LPAREN Identifier RPAREN

                          | CTIME LPAREN Identifier RPAREN
                          | CTIME LPAREN NumericSymbolicExpression RPAREN
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
    '''NumericExpression : Identifier PLUS Identifier
                         | Identifier PLUS NumericSymbolicExpression
                         | Identifier MINUS Identifier
                         | Identifier MINUS NumericSymbolicExpression
                         | Identifier TIMES Identifier
                         | Identifier TIMES NumericSymbolicExpression
                         | Identifier DIVIDE Identifier
                         | Identifier DIVIDE NumericSymbolicExpression
                         | Identifier MOD Identifier
                         | Identifier MOD NumericSymbolicExpression
                         | Identifier QUOTIENT Identifier
                         | Identifier QUOTIENT NumericSymbolicExpression
                         | Identifier LESS Identifier
                         | Identifier LESS NumericSymbolicExpression
                         | Identifier CARET LBRACE Identifier RBRACE
                         | Identifier CARET LBRACE NumericSymbolicExpression RBRACE

                         | NumericSymbolicExpression PLUS Identifier
                         | NumericSymbolicExpression PLUS NumericSymbolicExpression
                         | NumericSymbolicExpression MINUS Identifier
                         | NumericSymbolicExpression MINUS NumericSymbolicExpression
                         | NumericSymbolicExpression TIMES Identifier
                         | NumericSymbolicExpression TIMES NumericSymbolicExpression
                         | NumericSymbolicExpression DIVIDE Identifier
                         | NumericSymbolicExpression DIVIDE NumericSymbolicExpression
                         | NumericSymbolicExpression MOD Identifier
                         | NumericSymbolicExpression MOD NumericSymbolicExpression
                         | NumericSymbolicExpression QUOTIENT Identifier
                         | NumericSymbolicExpression QUOTIENT NumericSymbolicExpression
                         | NumericSymbolicExpression LESS Identifier
                         | NumericSymbolicExpression LESS NumericSymbolicExpression
                         | NumericSymbolicExpression CARET LBRACE Identifier RBRACE
                         | NumericSymbolicExpression CARET LBRACE NumericSymbolicExpression RBRACE'''

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
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression

                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression

                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression

                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression'''

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
                         | COUNT LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | COUNT LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | ATMOST Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | ATMOST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | ATLEAST Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | ATLEAST NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | EXACTLY Identifier LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ConstraintExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE ValueListInExpression
                         | EXACTLY NumericSymbolicExpression LLBRACE IndexingExpression RRBRACE EntryConstraintLogicalExpression

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
    '''NumericExpression : MINUS Identifier %prec UMINUS
                         | MINUS NumericSymbolicExpression %prec UMINUS
                         | PLUS Identifier %prec UPLUS
                         | PLUS NumericSymbolicExpression %prec UPLUS
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
    '''NumericExpression : SQRT LBRACE Identifier RBRACE
                         | SQRT LBRACE NumericSymbolicExpression RBRACE

                         | LFLOOR Identifier RFLOOR
                         | LFLOOR NumericSymbolicExpression RFLOOR

                         | LCEIL Identifier RCEIL
                         | LCEIL NumericSymbolicExpression RCEIL

                         | PIPE Identifier PIPE
                         | PIPE NumericSymbolicExpression PIPE

                         | MAX LPAREN ValueList RPAREN
                         | MAX LPAREN Identifier RPAREN
                         | MAX LPAREN NumericSymbolicExpression RPAREN

                         | MIN LPAREN ValueList RPAREN
                         | MIN LPAREN Identifier RPAREN
                         | MIN LPAREN NumericSymbolicExpression RPAREN

                         | ASIN LPAREN Identifier RPAREN
                         | ASIN LPAREN NumericSymbolicExpression RPAREN

                         | SIN LPAREN Identifier RPAREN
                         | SIN LPAREN NumericSymbolicExpression RPAREN

                         | ASINH LPAREN Identifier RPAREN
                         | ASINH LPAREN NumericSymbolicExpression RPAREN

                         | SINH LPAREN Identifier RPAREN
                         | SINH LPAREN NumericSymbolicExpression RPAREN

                         | ACOS LPAREN Identifier RPAREN
                         | ACOS LPAREN NumericSymbolicExpression RPAREN

                         | COS LPAREN Identifier RPAREN
                         | COS LPAREN NumericSymbolicExpression RPAREN

                         | ACOSH LPAREN Identifier RPAREN
                         | ACOSH LPAREN NumericSymbolicExpression RPAREN

                         | COSH LPAREN Identifier RPAREN
                         | COSH LPAREN NumericSymbolicExpression RPAREN

                         | LOG LPAREN Identifier RPAREN
                         | LOG LPAREN NumericSymbolicExpression RPAREN

                         | LN LPAREN Identifier RPAREN
                         | LN LPAREN NumericSymbolicExpression RPAREN

                         | EXP LPAREN Identifier RPAREN
                         | EXP LPAREN NumericSymbolicExpression RPAREN

                         | TANH LPAREN Identifier RPAREN
                         | TANH LPAREN NumericSymbolicExpression RPAREN

                         | TAN LPAREN Identifier RPAREN
                         | TAN LPAREN NumericSymbolicExpression RPAREN

                         | ATANH LPAREN Identifier RPAREN
                         | ATANH LPAREN NumericSymbolicExpression RPAREN

                         | ATAN LPAREN Identifier COMMA Identifier RPAREN
                         | ATAN LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | ATAN LPAREN Identifier RPAREN
                         | ATAN LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | ATAN LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | ATAN LPAREN NumericSymbolicExpression RPAREN

                         | CARD LPAREN SetExpression RPAREN
                         | CARD LPAREN Identifier RPAREN

                         | LENGTH LPAREN Identifier RPAREN

                         | ROUND LPAREN Identifier COMMA Identifier RPAREN
                         | ROUND LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | ROUND LPAREN Identifier RPAREN
                         | ROUND LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | ROUND LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | ROUND LPAREN NumericSymbolicExpression RPAREN

                         | PRECISION LPAREN Identifier COMMA Identifier RPAREN
                         | PRECISION LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | PRECISION LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | PRECISION LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN

                         | TRUNC LPAREN Identifier COMMA Identifier RPAREN
                         | TRUNC LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | TRUNC LPAREN Identifier RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | TRUNC LPAREN NumericSymbolicExpression RPAREN

                         | NUM LPAREN Identifier RPAREN
                         | NUM LPAREN SymbolicExpression RPAREN

                         | NUM0 LPAREN Identifier RPAREN
                         | NUM0 LPAREN SymbolicExpression RPAREN

                         | ICHAR LPAREN Identifier RPAREN
                         | ICHAR LPAREN SymbolicExpression RPAREN

                         | MATCH LPAREN Identifier COMMA Identifier RPAREN
                         | MATCH LPAREN Identifier COMMA SymbolicExpression RPAREN
                         | MATCH LPAREN SymbolicExpression COMMA Identifier RPAREN
                         | MATCH LPAREN SymbolicExpression COMMA SymbolicExpression RPAREN

                         | UNIFORM LPAREN Identifier COMMA Identifier RPAREN
                         | UNIFORM LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | UNIFORM LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | UNIFORM LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN

                         | NORMAL LPAREN Identifier COMMA Identifier RPAREN
                         | NORMAL LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | NORMAL LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | NORMAL LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN

                         | BETA LPAREN Identifier COMMA Identifier RPAREN
                         | BETA LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | BETA LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | BETA LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN

                         | GAMMA LPAREN Identifier RPAREN
                         | GAMMA LPAREN NumericSymbolicExpression RPAREN

                         | POISSON LPAREN Identifier RPAREN
                         | POISSON LPAREN NumericSymbolicExpression RPAREN

                         | IRAND224 LPAREN RPAREN

                         | UNIFORM01 LPAREN RPAREN

                         | NORMAL01 LPAREN RPAREN

                         | CAUCHY LPAREN RPAREN

                         | EXPONENTIAL LPAREN RPAREN

                         | TIME LPAREN RPAREN

                         | ID LPAREN ValueList RPAREN
                         | ID LPAREN SetExpression RPAREN
                         | ID LPAREN Identifier RPAREN
                         | ID LPAREN NumericSymbolicExpression RPAREN
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

    elif _type == "ATANH":
        op = NumericExpressionWithFunction.ATANH

    elif _type == "TANH":
        op = NumericExpressionWithFunction.TANH

    elif _type == "ATAN":
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
    '''ConditionalNumericExpression : IF ConstraintExpression THEN Identifier ELSE Identifier
                                    | IF ConstraintExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF ConstraintExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF ConstraintExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF ConstraintExpression THEN Identifier
                                    | IF ConstraintExpression THEN NumericSymbolicExpression

                                    | IF ValueListInExpression THEN Identifier ELSE Identifier
                                    | IF ValueListInExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF ValueListInExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF ValueListInExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF ValueListInExpression THEN Identifier
                                    | IF ValueListInExpression THEN NumericSymbolicExpression

                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF EntryConstraintLogicalExpression THEN Identifier
                                    | IF EntryConstraintLogicalExpression THEN NumericSymbolicExpression

                                    | IF Identifier THEN Identifier ELSE Identifier
                                    | IF Identifier THEN Identifier ELSE NumericSymbolicExpression
                                    | IF Identifier THEN NumericSymbolicExpression ELSE Identifier
                                    | IF Identifier THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF Identifier THEN Identifier
                                    | IF Identifier THEN NumericSymbolicExpression

                                    | IF NumericSymbolicExpression THEN Identifier ELSE Identifier
                                    | IF NumericSymbolicExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression'''

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
    '''Range : Identifier DOTS Identifier BY Identifier
             | Identifier DOTS Identifier BY NumericSymbolicExpression
             | Identifier DOTS NumericSymbolicExpression BY Identifier
             | Identifier DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | Identifier DOTS Identifier
             | Identifier DOTS NumericSymbolicExpression

             | NumericSymbolicExpression DOTS Identifier BY Identifier
             | NumericSymbolicExpression DOTS Identifier BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS NumericSymbolicExpression BY Identifier
             | NumericSymbolicExpression DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS Identifier
             | NumericSymbolicExpression DOTS NumericSymbolicExpression'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

def p_Identifier(t):
    '''Identifier : ID UNDERLINE LBRACE ValueList RBRACE
                  | ID UNDERLINE LBRACE Identifier RBRACE
                  | ID UNDERLINE LBRACE NumericSymbolicExpression RBRACE
                  
                  | ID LBRACKET ValueList RBRACKET
                  | ID LBRACKET Identifier RBRACKET
                  | ID LBRACKET NumericSymbolicExpression RBRACKET
                  
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
    '''ValueList : ValueList COMMA SetExpression
                 | ValueList COMMA Identifier
                 | ValueList COMMA NumericSymbolicExpression
                 
                 | SetExpression COMMA SetExpression
                 | SetExpression COMMA Identifier
                 | SetExpression COMMA NumericSymbolicExpression
                 
                 | Identifier COMMA SetExpression
                 | Identifier COMMA Identifier
                 | Identifier COMMA NumericSymbolicExpression
                 
                 | NumericSymbolicExpression COMMA SetExpression
                 | NumericSymbolicExpression COMMA Identifier
                 | NumericSymbolicExpression COMMA NumericSymbolicExpression'''

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
