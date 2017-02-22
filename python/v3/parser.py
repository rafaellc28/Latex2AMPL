#!/usr/bin/python -tt

import sys
import re

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
from SyntaxException import *
from Declarations import *
from DeclarationExpression import *

precedence = (
    ('left', 'COMMA', 'DOTS', 'FOR', 'BACKSLASHES'),
    ('left', 'ID'),
    ('left', 'NUMBER'),
    ('left', 'LBRACE', 'RBRACE'),
    ('right', 'LPAREN', 'RPAREN', 'LLBRACE', 'RRBRACE', 'LBRACKET', 'RBRACKET'),
    ('left', 'OR', 'AND', 'NOT'),
    ('left', 'FORALL', 'EXISTS', 'NEXISTS'),
    ('right', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ', 'COLON', 'DEFAULT', 'DIMEN', 'SETOF'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION', 'INTER', 'CROSS', 'BY'),
    ('left', 'UNDERLINE', 'CARET'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'PIPE', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'COS', 'ARCTAN', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'QUOTIENT', 'LESS'),
    ('left', 'UPLUS', 'UMINUS'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'INTEGERSET', 'INTEGERSETPOSITIVE', 'INTEGERSETNEGATIVE', 'INTEGERSETWITHONELIMIT', 
      'REALSET', 'REALSETPOSITIVE', 'REALSETNEGATIVE', 'REALSETWITHONELIMIT', 'NATURALSET', 'BINARYSET', 'SYMBOLIC', 'LOGICAL')
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

    if isinstance(t[1], LinearProgram):
      t[1].setDeclarations(t[2])
      t[0] = t[1]

    else:
      if len(t) > 3:
          t[0] = LinearProgram(t[1], t[3])
      elif len(t) > 2:
          t[0] = LinearProgram(t[1], t[2])
      else:
          t[0] = LinearProgram(t[1], None)

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
        if re.search(r"\\text\{\s*maximize\s*\}|maximize|\\text\{\s*maximize:\s*\}|maximize:", t[1]):
            obj = Objective.MAXIMIZE

        t[0] = Objective(t[2], obj, t[4])
    else:
        if re.search(r"\\text\{\s*minimize\s*\}|minimize|\\text\{\s*minimize:\s*\}|minimize:", t[1]):
            t[0] = Objective(t[2])
        else:
            t[0] = Objective(t[2], Objective.MAXIMIZE)

def p_Constraints(t):
    '''Constraints : SUBJECTTO ConstraintList'''
    t[0] = Constraints(t[2])

def p_ConstraintList(t):
    '''ConstraintList : ConstraintList BACKSLASHES Constraint
                      | ConstraintList BACKSLASHES Declarations
                      | ConstraintList BACKSLASHES
                      | Declarations
                      | Constraint'''
    if len(t) > 3:
      if isinstance(t[3], Declarations):
        t[0] = t[1] + t[3].declarations
      else:
        t[0] = t[1] + [t[3]]

    elif isinstance(t[1], Declarations):
        t[0] = t[1].declarations
    elif len(t) > 2:
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression COMMA IndexingExpression
                  | ConstraintExpression COLON IndexingExpression
                  | ConstraintExpression FOR BACKSLASHES IndexingExpression
                  | ConstraintExpression COMMA BACKSLASHES IndexingExpression
                  | ConstraintExpression COLON BACKSLASHES IndexingExpression
                  | ConstraintExpression'''
    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])

def p_ConstraintExpression(t):
    '''ConstraintExpression : LinearExpression EQ LinearExpression
                           |  LinearExpression LE LinearExpression
                           |  LinearExpression GE LinearExpression
                           |  LinearExpression LE LinearExpression LE LinearExpression
                           |  LinearExpression GE LinearExpression GE LinearExpression'''
    
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

def p_Declarations(t):
  '''Declarations : DeclarationList
                  | DeclarationList FOR IndexingExpression
                  | DeclarationList COLON IndexingExpression'''

  if len(t) > 3:
    for decl in t[1]:
      if decl.indexingExpression == None:
        decl.setIndexingExpression(t[3])
  else:
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
    '''DeclarationList : Declaration
                       | DeclarationList SEMICOLON Declaration
                       | DeclarationList SEMICOLON BACKSLASHES Declaration
                       | DeclarationList SEMICOLON BACKSLASHES
                       | DeclarationList SEMICOLON'''
    if len(t) > 4:
      t[0] = t[1] + [t[4]]
    elif len(t) > 3:
      if isinstance(t[3], Declaration):
        t[0] = t[1] + [t[3]]
      else:
        t[0] = t[1]
    elif len(t) > 2:
      t[0] = t[1]
    else:
      t[0] = [t[1]]

def p_Declaration(t):
    '''Declaration : DeclarationExpression FOR IndexingExpression
                   | DeclarationExpression COMMA IndexingExpression
                   | DeclarationExpression COLON IndexingExpression
                   | DeclarationExpression FOR BACKSLASHES IndexingExpression
                   | DeclarationExpression COMMA BACKSLASHES IndexingExpression
                   | DeclarationExpression COLON BACKSLASHES IndexingExpression
                   | ValueList FOR BACKSLASHES IndexingExpression
                   | ValueList FOR IndexingExpression
                   | ValueList COLON BACKSLASHES IndexingExpression
                   | ValueList COLON IndexingExpression
                   | DeclarationExpression'''
    if len(t) > 3:
        t[3].setStmtIndexing(True)
        if isinstance(t[1], ValueList):
          t[1] = DeclarationExpression(t[1], [])

        t[0] = Declaration(t[1], t[3])
    else:
        t[0] = Declaration(t[1])

def p_DeclarationExpression(t):
    '''DeclarationExpression : ValueList IN SetExpression
                             | ValueList SUBSET SetExpression
                             | ValueList DEFAULT NumericOrSymbolicExpression
                             | ValueList DEFAULT SetExpression
                             | ValueList DIMEN NumericOrSymbolicExpression
                             | ValueList COLON EQ NumericOrSymbolicExpression
                             | ValueList COLON EQ SetExpression
                             | ValueList LT NumericOrSymbolicExpression
                             | ValueList GT NumericOrSymbolicExpression
                             | ValueList NEQ NumericOrSymbolicExpression
                             | ValueList COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList
                             | DeclarationExpression DeclarationAttributeList'''

    if isinstance(t[1], DeclarationExpression):
      if t[2] == ",":
        t[1].addAttribute(t[3])
      else:
        t[1].addAttribute(t[2])

      t[0] = t[1]

    else:
      attr = None
      if t[2] == ",":
        attr = t[3]
      elif t[2] == "\\in":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.IN)
      elif re.search(r"\\subseteq|\\subset", t[2]):
        attr = DeclarationAttribute(t[3], DeclarationAttribute.WT)
      elif re.search(r"\\text\{\s*default\s*\}", t[2]):
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DF)
      elif re.search(r"\\text\{\s*dimen\s*\}", t[2]):
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DM)
      elif t[2] == ":":
        attr = DeclarationAttribute(t[4], DeclarationAttribute.ST)
      elif t[2] == "<":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LT)
      elif t[2] == "\\leq":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LE)
      elif t[2] == ">":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GT)
      elif t[2] == "\\geq":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GE)
      elif t[2] == "\\neq":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.NEQ)

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
                          | SUBSET SetExpression
                          | DEFAULT NumericOrSymbolicExpression
                          | DEFAULT SetExpression
                          | DIMEN NumericOrSymbolicExpression
                          | COLON EQ NumericOrSymbolicExpression
                          | COLON EQ SetExpression
                          | LT NumericOrSymbolicExpression
                          | LE NumericOrSymbolicExpression
                          | EQ NumericOrSymbolicExpression
                          | GT NumericOrSymbolicExpression
                          | GE NumericOrSymbolicExpression
                          | NEQ NumericOrSymbolicExpression'''

  if t[1] == "\\in":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.IN)
  elif re.search(r"\\subseteq|\\subset", t[1]):
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.WT)
  elif re.search(r"\\text\{\s*default\s*\}", t[1]):
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DF)
  elif re.search(r"\\text\{\s*dimen\s*\}", t[1]):
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DM)
  elif t[1] == ":":
    t[0] = DeclarationAttribute(t[3], DeclarationAttribute.ST)
  elif t[1] == "<":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LT)
  elif t[1] == "\\leq":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LE)
  elif t[1] == ">":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GT)
  elif t[1] == "\\geq":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GE)
  elif t[1] == "\\neq":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.NEQ)

def p_LinearExpression(t):
    '''LinearExpression : NumericExpression
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

def p_LinearExpression_binop(t):
    '''LinearExpression : LinearExpression PLUS LinearExpression
                        | LinearExpression MINUS LinearExpression
                        | LinearExpression TIMES NumericExpression
                        | LinearExpression DIVIDE NumericExpression'''

    if t[2] == "+":
        op = LinearExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = LinearExpressionWithArithmeticOperation.MINUS
    elif re.search(r"\*|\\cdot|\\ast", t[2]):
        op = LinearExpressionWithArithmeticOperation.TIMES
    elif re.search(r"/|\\div", t[2]):
        op = LinearExpressionWithArithmeticOperation.DIV

    t[0] = LinearExpressionWithArithmeticOperation(op, t[1], t[3])

def p_IteratedLinearExpression(t):
    '''LinearExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE LinearExpression
                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE LinearExpression'''
    if len(t) > 7:
        t[0] = IteratedLinearExpression(t[10], t[4], t[8])
    else:
        t[0] = IteratedLinearExpression(t[6], t[4])

def p_ConditionalLinearExpression(t):
    '''ConditionalLinearExpression : LPAREN SetExpression RPAREN QUESTION_MARK LinearExpression
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK LinearExpression
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
      if re.search(r"\\wedge|\\text\{\s*and\s*\}", t[2]):
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])
    else:
        t[0] = LogicalExpression([t[1]])

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NumericOrSymbolicExpression
                              | NOT EntryLogicalExpression
                              | LPAREN LogicalExpression RPAREN'''

    if isinstance(t[1], str) and re.search(r"!|\\text\{\s*not\s*}", t[1]):
      t[0] = EntryLogicalExpressionNot(t[2])
    elif t[1] == "(":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])
    else:
      t[0] = EntryLogicalExpressionNumericOrSymbolic(t[1])

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
    elif re.search(r"\\subseteq|\\subset", t[2]):
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])
    elif re.search(r"\\not\\subseteq|\\not\\subset", t[2]):
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.NOTSUBSET, t[1], t[3])

def p_EntryIteratedLogicalExpression(t):
    '''EntryLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression'''

    if t[1] == "\\forall":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])
    elif t[1] == "\\not\\forall":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])
    elif t[1] == "\\exists":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])
    elif t[1] == "\\nexists" or t[1] == "\\not\\exists":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])

def p_SetExpressionWithOperation(t):
    '''SetExpression : SetExpression DIFF SetExpression
                     | SetExpression SYMDIFF SetExpression
                     | SetExpression UNION SetExpression
                     | SetExpression INTER SetExpression
                     | SetExpression CROSS SetExpression'''

    if re.search(r"\\setminus", t[2]):
        op = SetExpressionWithOperation.DIFF
    elif re.search(r"\\triangle|\\ominus", t[2]):
        op = SetExpressionWithOperation.SYMDIFF
    elif re.search(r"\\cup", t[2]):
        op = SetExpressionWithOperation.UNION
    elif re.search(r"\\cap", t[2]):
        op = SetExpressionWithOperation.INTER
    elif re.search(r"\\times", t[2]):
        op = SetExpressionWithOperation.CROSS

    t[0] = SetExpressionWithOperation(op, t[1], t[3])

def p_SetExpressionWithValue(t):
    '''SetExpression : LLBRACE ValueList RRBRACE
                     | LLBRACE Range RRBRACE
                     | LLBRACE SetExpression RRBRACE
                     | LLBRACE TupleList RRBRACE
                     | LLBRACE IndexingExpression RRBRACE
                     | LLBRACE RRBRACE
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
                     | SYMBOLIC
                     | LOGICAL
                     | PARAMETERS
                     | SETS
                     | VARIABLES'''

    if len(t) > 2:
        if isinstance(t[1], str) and re.search(r"\\\{", t[1]):
          if not (isinstance(t[2], str) and re.search(r"\\\}", t[2])):
            t[0] = SetExpressionBetweenBraces(SetExpressionWithValue(t[2]))
          else:
            t[0] = SetExpressionBetweenBraces(None)
        elif t[1] == "(":
            t[0] = SetExpressionBetweenParenthesis(t[2])
        else:
            t[0] = SetExpressionWithValue(t[2])
    else:
        value = t[1]
        if hasattr(t.slice[1], 'value2'):
          value = t.slice[1].value2
        
        t[0] = SetExpressionWithValue(value)

def p_SetExpressionWithIndices(t):
    '''SetExpression : Variable LPAREN ValueList RPAREN
                     | Variable LBRACKET ValueList RBRACKET
                     | Variable LPAREN NumericExpression RPAREN
                     | Variable LBRACKET NumericExpression RBRACKET'''
    
    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE NumericOrSymbolicExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE LPAREN ValueList RPAREN'''
    
    if t[5] == "(":
      t[0] = IteratedSetExpression(t[3], t[6])
    else:
      t[0] = IteratedSetExpression(t[3], [t[5]])

def p_IndexingExpression(t):
    '''IndexingExpression : EntryIndexingExpression
                          | IndexingExpression PIPE LogicalExpression
                          | IndexingExpression COMMA EntryIndexingExpression
                          | IndexingExpression COMMA BACKSLASHES EntryIndexingExpression'''

    if len(t) > 4:
        t[0] = t[1].add(t[4])
    elif len(t) > 3:
        if re.search(r"\\mid|\\vert|\|", t[2]):
            t[0] = t[1].setLogicalExpression(t[3])
        else:
            t[0] = t[1].add(t[3])
    else:
        t[0] = IndexingExpression([t[1]])

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | Tuple IN SetExpression
                               | Variable IN SetExpression'''
    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

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

def p_StringSymbolicExpression(t):
    '''SymbolicExpression : LPAREN SymbolicExpression RPAREN
                          | STRING'''

    if len(t) > 2:
        t[0] = SymbolicExpressionBetweenParenthesis(t[2])
    else:
        t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : NumericOrSymbolicExpression AMPERSAND NumericOrSymbolicExpression'''
    if re.search(r"\\&", t[2]):
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

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

def p_NumericExpression_binop(t):
    '''NumericExpression : NumericExpression PLUS NumericExpression
                         | NumericExpression MINUS NumericExpression
                         | NumericExpression TIMES NumericExpression
                         | NumericExpression DIVIDE NumericExpression
                         | NumericExpression MOD NumericExpression
                         | NumericExpression QUOTIENT NumericExpression
                         | NumericExpression LESS NumericExpression
                         | NumericExpression CARET LBRACE NumericExpression RBRACE'''

    if t[2] == "+":
        op = NumericExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = NumericExpressionWithArithmeticOperation.MINUS
    elif re.search(r"\*|\\cdot|\\ast", t[2]):
        op = NumericExpressionWithArithmeticOperation.TIMES
    elif re.search(r"/|\\div", t[2]):
        op = NumericExpressionWithArithmeticOperation.DIV
    elif re.search(r"\\text\{\s*\%\s*\}|\\mod|\\bmod", t[2]):
        op = NumericExpressionWithArithmeticOperation.MOD
    elif t[2] == "^":
        op = NumericExpressionWithArithmeticOperation.POW
    elif re.search(r"\\big/|\\text\{\s*div\s*\}", t[2]):
        op = NumericExpressionWithArithmeticOperation.QUOT
    elif re.search(r"\\text\{\s*less\s*\}", t[2]):
        op = NumericExpressionWithArithmeticOperation.LESS

    if t[2] == "^":
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[4])
    else:
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

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
                         | STR2TIME LPAREN NumericOrSymbolicExpression COMMA NumericOrSymbolicExpression RPAREN
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
    elif re.search(r"\\mid|\\vert|\|", t[1]):
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
    elif t[1] == "Uniform01":
        op = NumericExpressionWithFunction.UNIFORM01
    elif t[1] == "Uniform":
        op = NumericExpressionWithFunction.UNIFORM
    elif t[1] == "Normal01":
        op = NumericExpressionWithFunction.NORMAL01
    elif t[1] == "Normal":
        op = NumericExpressionWithFunction.NORMAL
    elif t[1] == "gmtime":
        op = NumericExpressionWithFunction.GMTIME
    elif t[1] == "Irand224":
        op = NumericExpressionWithFunction.IRAND224
    elif t[1] == "str2time":
        op = NumericExpressionWithFunction.STR2TIME

    if len(t) > 5:
        t[0] = NumericExpressionWithFunction(op, t[3], t[5])
    elif len(t) > 4:
        t[0] = NumericExpressionWithFunction(op, t[3])
    else:
        if t[2] == "(":
          t[0] = NumericExpressionWithFunction(op)
        else:
          t[0] = NumericExpressionWithFunction(op, t[2])

def p_ConditionalNumericExpression(t):
    '''ConditionalNumericExpression : LPAREN SetExpression RPAREN QUESTION_MARK NumericExpression
                                    | LPAREN LogicalExpression RPAREN QUESTION_MARK NumericExpression
                                    | ConditionalNumericExpression COLON NumericExpression'''
    if len(t) > 4:
        t[0] = ConditionalNumericExpression(t[2], t[5])
    else:
        t[1].addElseExpression(t[3])
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

def p_Variable(t):
    '''Variable : ID UNDERLINE LBRACE ValueList RBRACE
                | ID UNDERLINE LBRACE NumericOrSymbolicExpression RBRACE
                | ID LBRACKET ValueList RBRACKET
                | ID LBRACKET NumericOrSymbolicExpression RBRACKET
                | ID'''

    if len(t) > 5:
        if isinstance(t[4], ValueList):
          t[0] = Variable(ID(t[1]), t[4].getValues())
        else:
          t[0] = Variable(ID(t[1]), t[4])
    elif len(t) > 2:
        if isinstance(t[3], ValueList):
          t[0] = Variable(ID(t[1]), t[3].getValues())
        else:
          t[0] = Variable(ID(t[1]), t[3])
    else:
        t[0] = Variable(ID(t[1]))

def p_ValueList(t):
    '''ValueList : ValueList COMMA NumericOrSymbolicExpression
                 | NumericOrSymbolicExpression'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([t[1]])
    else:
        t[0] = t[1].add(t[3])

def p_Tuple(t):
    '''Tuple : LPAREN ValueList RPAREN'''
    t[0] = Tuple(t[2].getValues())

def p_TupleList(t):
    '''TupleList : TupleList COMMA Tuple
                 | Tuple'''

    if not isinstance(t[1], TupleList):
        t[0] = TupleList([t[1]])
    else:
        t[0] = t[1].add(t[3])

def p_error(t):
  if t:
    raise SyntaxException(t.lineno, t.lexpos, t.value)
  else:
    raise SyntaxException("EOF")
