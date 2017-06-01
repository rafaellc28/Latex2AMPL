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
    ('left', 'ID'),
    ('left', 'COMMA', 'DOTS', 'FOR', 'WHERE', 'BACKSLASHES'),
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
    ('right', 'AMPERSAND'),
    ('right', 'PLUS', 'MINUS'),
    ('right', 'TIMES', 'DIVIDE', 'MOD', 'QUOTIENT', 'LESS'),
    ('right', 'UPLUS', 'UMINUS'),
    ('right', 'IN', 'NOTIN'),
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
                 | MAXIMIZE NumericExpression
                 | MAXIMIZE Variable
                 | MINIMIZE LinearExpression
                 | MINIMIZE NumericExpression
                 | MINIMIZE Variable
                 | MAXIMIZE LinearExpression FOR IndexingExpression
                 | MAXIMIZE NumericExpression FOR IndexingExpression
                 | MAXIMIZE Variable FOR IndexingExpression
                 | MINIMIZE LinearExpression FOR IndexingExpression
                 | MINIMIZE NumericExpression FOR IndexingExpression
                 | MINIMIZE Variable FOR IndexingExpression
                 | MAXIMIZE LinearExpression WHERE IndexingExpression
                 | MAXIMIZE NumericExpression WHERE IndexingExpression
                 | MAXIMIZE Variable WHERE IndexingExpression
                 | MINIMIZE LinearExpression WHERE IndexingExpression
                 | MINIMIZE NumericExpression WHERE IndexingExpression
                 | MINIMIZE Variable WHERE IndexingExpression
                 | MAXIMIZE LinearExpression COLON IndexingExpression
                 | MAXIMIZE NumericExpression COLON IndexingExpression
                 | MAXIMIZE Variable COLON IndexingExpression
                 | MINIMIZE LinearExpression COLON IndexingExpression
                 | MINIMIZE NumericExpression COLON IndexingExpression
                 | MINIMIZE Variable COLON IndexingExpression'''

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
    '''Constraint : ConstraintExpression FOR BACKSLASHES IndexingExpression
                  | ConstraintExpression WHERE BACKSLASHES IndexingExpression
                  | ConstraintExpression COLON BACKSLASHES IndexingExpression
                  | ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression WHERE IndexingExpression
                  | ConstraintExpression COLON IndexingExpression
                  | ConstraintExpression'''
    
    if len(t) > 4:
        t[4].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[4])
    elif len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])

def p_ConstraintExpression(t):
    '''ConstraintExpression : LinearExpression EQ LinearExpression
                            | NumericExpression EQ LinearExpression
                            | Variable EQ LinearExpression
                            | LinearExpression EQ NumericExpression
                            | LinearExpression EQ Variable
                            | NumericExpression EQ NumericExpression
                            | NumericExpression EQ Variable
                            | Variable EQ NumericExpression
                            | Variable EQ Variable
                            | LinearExpression LE LinearExpression
                            | NumericExpression LE LinearExpression
                            | Variable LE LinearExpression
                            | LinearExpression LE NumericExpression
                            | LinearExpression LE Variable
                            | NumericExpression LE NumericExpression
                            | NumericExpression LE Variable
                            | Variable LE NumericExpression
                            | Variable LE Variable
                            | LinearExpression GE LinearExpression
                            | NumericExpression GE LinearExpression
                            | Variable GE LinearExpression
                            | LinearExpression GE NumericExpression
                            | LinearExpression GE Variable
                            | NumericExpression GE NumericExpression
                            | NumericExpression GE Variable
                            | Variable GE NumericExpression
                            | Variable GE Variable
                            | LinearExpression LE LinearExpression LE LinearExpression
                            | LinearExpression LE LinearExpression LE NumericExpression
                            | LinearExpression LE LinearExpression LE Variable
                            | LinearExpression LE NumericExpression LE LinearExpression
                            | LinearExpression LE Variable LE LinearExpression
                            | LinearExpression LE NumericExpression LE NumericExpression
                            | LinearExpression LE NumericExpression LE Variable
                            | LinearExpression LE Variable LE NumericExpression
                            | LinearExpression LE Variable LE Variable
                            | NumericExpression LE LinearExpression LE LinearExpression
                            | Variable LE LinearExpression LE LinearExpression
                            | NumericExpression LE LinearExpression LE NumericExpression
                            | NumericExpression LE LinearExpression LE Variable
                            | Variable LE LinearExpression LE NumericExpression
                            | Variable LE LinearExpression LE Variable
                            | NumericExpression LE NumericExpression LE LinearExpression
                            | NumericExpression LE Variable LE LinearExpression
                            | Variable LE NumericExpression LE LinearExpression
                            | Variable LE Variable LE LinearExpression
                            | NumericExpression LE NumericExpression LE NumericExpression
                            | NumericExpression LE NumericExpression LE Variable
                            | NumericExpression LE Variable LE NumericExpression
                            | Variable LE NumericExpression LE NumericExpression
                            | Variable LE NumericExpression LE Variable
                            | Variable LE Variable LE NumericExpression
                            | Variable LE Variable LE Variable
                            | LinearExpression GE LinearExpression GE LinearExpression
                            | LinearExpression GE LinearExpression GE NumericExpression
                            | LinearExpression GE LinearExpression GE Variable
                            | LinearExpression GE NumericExpression GE LinearExpression
                            | LinearExpression GE Variable GE LinearExpression
                            | LinearExpression GE NumericExpression GE NumericExpression
                            | LinearExpression GE NumericExpression GE Variable
                            | LinearExpression GE Variable GE NumericExpression
                            | LinearExpression GE Variable GE Variable
                            | NumericExpression GE LinearExpression GE LinearExpression
                            | Variable GE LinearExpression GE LinearExpression
                            | NumericExpression GE LinearExpression GE NumericExpression
                            | NumericExpression GE LinearExpression GE Variable
                            | Variable GE LinearExpression GE NumericExpression
                            | Variable GE LinearExpression GE Variable
                            | NumericExpression GE NumericExpression GE LinearExpression
                            | NumericExpression GE Variable GE LinearExpression
                            | Variable GE NumericExpression GE LinearExpression
                            | Variable GE Variable GE LinearExpression
                            | NumericExpression GE NumericExpression GE NumericExpression
                            | NumericExpression GE NumericExpression GE Variable
                            | NumericExpression GE Variable GE NumericExpression
                            | NumericExpression GE Variable GE Variable
                            | Variable GE NumericExpression GE NumericExpression
                            | Variable GE NumericExpression GE Variable
                            | Variable GE Variable GE NumericExpression
                            | Variable GE Variable GE Variable'''
    
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
                  | DeclarationList WHERE IndexingExpression
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
                   | DeclarationExpression WHERE IndexingExpression
                   | DeclarationExpression COLON IndexingExpression
                   | DeclarationExpression FOR BACKSLASHES IndexingExpression
                   | DeclarationExpression WHERE BACKSLASHES IndexingExpression
                   | DeclarationExpression COLON BACKSLASHES IndexingExpression
                   | ValueList FOR BACKSLASHES IndexingExpression
                   | NumericExpression FOR BACKSLASHES IndexingExpression
                   | Variable FOR BACKSLASHES IndexingExpression
                   | SymbolicExpression FOR BACKSLASHES IndexingExpression
                   | ValueList FOR IndexingExpression
                   | NumericExpression FOR IndexingExpression
                   | Variable FOR IndexingExpression
                   | SymbolicExpression FOR IndexingExpression
                   | ValueList WHERE BACKSLASHES IndexingExpression
                   | NumericExpression WHERE BACKSLASHES IndexingExpression
                   | Variable WHERE BACKSLASHES IndexingExpression
                   | SymbolicExpression WHERE BACKSLASHES IndexingExpression
                   | ValueList WHERE IndexingExpression
                   | NumericExpression WHERE IndexingExpression
                   | Variable WHERE IndexingExpression
                   | SymbolicExpression WHERE IndexingExpression
                   | ValueList COLON BACKSLASHES IndexingExpression
                   | NumericExpression COLON BACKSLASHES IndexingExpression
                   | Variable COLON BACKSLASHES IndexingExpression
                   | SymbolicExpression COLON BACKSLASHES IndexingExpression
                   | ValueList COLON IndexingExpression
                   | NumericExpression COLON IndexingExpression
                   | Variable COLON IndexingExpression
                   | SymbolicExpression COLON IndexingExpression
                   | DeclarationExpression'''
    if len(t) > 3:
        t[3].setStmtIndexing(True)
        if isinstance(t[1], ValueList):
          t[1] = DeclarationExpression(t[1], [])
        elif isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Variable):
          t[1] = DeclarationExpression(ValueList([t[1]]), [])

        t[0] = Declaration(t[1], t[3])
    else:
        t[0] = Declaration(t[1])

def p_DeclarationExpression(t):
    '''DeclarationExpression : ValueList IN SetExpression
                             | NumericExpression IN SetExpression
                             | Variable IN SetExpression
                             | SymbolicExpression IN SetExpression
                             | ValueList IN Variable
                             | NumericExpression IN Variable
                             | Variable IN Variable
                             | SymbolicExpression IN Variable
                             | ValueList SUBSET SetExpression
                             | NumericExpression SUBSET SetExpression
                             | Variable SUBSET SetExpression
                             | SymbolicExpression SUBSET SetExpression
                             | ValueList SUBSET Variable
                             | NumericExpression SUBSET Variable
                             | Variable SUBSET Variable
                             | SymbolicExpression SUBSET Variable
                             | ValueList DEFAULT NumericExpression
                             | ValueList DEFAULT Variable
                             | NumericExpression DEFAULT NumericExpression
                             | NumericExpression DEFAULT Variable
                             | Variable DEFAULT NumericExpression
                             | Variable DEFAULT Variable
                             | SymbolicExpression DEFAULT NumericExpression
                             | SymbolicExpression DEFAULT Variable
                             | ValueList DEFAULT SymbolicExpression
                             | NumericExpression DEFAULT SymbolicExpression
                             | Variable DEFAULT SymbolicExpression
                             | SymbolicExpression DEFAULT SymbolicExpression
                             | ValueList DEFAULT SetExpression
                             | NumericExpression DEFAULT SetExpression
                             | Variable DEFAULT SetExpression
                             | SymbolicExpression DEFAULT SetExpression
                             | ValueList DIMEN NumericExpression
                             | ValueList DIMEN Variable
                             | NumericExpression DIMEN NumericExpression
                             | NumericExpression DIMEN Variable
                             | Variable DIMEN NumericExpression
                             | Variable DIMEN Variable
                             | SymbolicExpression DIMEN NumericExpression
                             | SymbolicExpression DIMEN Variable
                             | ValueList DIMEN SymbolicExpression
                             | NumericExpression DIMEN SymbolicExpression
                             | Variable DIMEN SymbolicExpression
                             | SymbolicExpression DIMEN SymbolicExpression
                             | ValueList COLON EQ NumericExpression
                             | ValueList COLON EQ Variable
                             | NumericExpression COLON EQ NumericExpression
                             | NumericExpression COLON EQ Variable
                             | Variable COLON EQ NumericExpression
                             | Variable COLON EQ Variable
                             | SymbolicExpression COLON EQ NumericExpression
                             | SymbolicExpression COLON EQ Variable
                             | ValueList COLON EQ SymbolicExpression
                             | NumericExpression COLON EQ SymbolicExpression
                             | Variable COLON EQ SymbolicExpression
                             | SymbolicExpression COLON EQ SymbolicExpression
                             | ValueList COLON EQ SetExpression
                             | NumericExpression COLON EQ SetExpression
                             | Variable COLON EQ SetExpression
                             | SymbolicExpression COLON EQ SetExpression
                             | ValueList LT NumericExpression
                             | ValueList LT Variable
                             | NumericExpression LT NumericExpression
                             | NumericExpression LT Variable
                             | Variable LT NumericExpression
                             | Variable LT Variable
                             | SymbolicExpression LT NumericExpression
                             | SymbolicExpression LT Variable
                             | ValueList LT SymbolicExpression
                             | NumericExpression LT SymbolicExpression
                             | Variable LT SymbolicExpression
                             | SymbolicExpression LT SymbolicExpression
                             | ValueList GT NumericExpression
                             | ValueList GT Variable
                             | NumericExpression GT NumericExpression
                             | NumericExpression GT Variable
                             | Variable GT NumericExpression
                             | Variable GT Variable
                             | SymbolicExpression GT NumericExpression
                             | SymbolicExpression GT Variable
                             | ValueList GT SymbolicExpression
                             | NumericExpression GT SymbolicExpression
                             | Variable GT SymbolicExpression
                             | SymbolicExpression GT SymbolicExpression
                             | ValueList NEQ NumericExpression
                             | ValueList NEQ Variable
                             | NumericExpression NEQ NumericExpression
                             | NumericExpression NEQ Variable
                             | Variable NEQ NumericExpression
                             | Variable NEQ Variable
                             | SymbolicExpression NEQ NumericExpression
                             | SymbolicExpression NEQ Variable
                             | ValueList NEQ SymbolicExpression
                             | NumericExpression NEQ SymbolicExpression
                             | Variable NEQ SymbolicExpression
                             | SymbolicExpression NEQ SymbolicExpression
                             | ValueList COMMA DeclarationAttributeList
                             | NumericExpression COMMA DeclarationAttributeList
                             | Variable COMMA DeclarationAttributeList
                             | SymbolicExpression COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList
                             | DeclarationExpression DeclarationAttributeList'''

    if len(t) > 3 and isinstance(t[3], Variable):
      t[3] = SetExpressionWithValue(t[3])    

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

      if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Variable):
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
                          | IN Variable
                          | SUBSET SetExpression
                          | SUBSET Variable
                          | DEFAULT NumericExpression
                          | DEFAULT Variable
                          | DEFAULT SymbolicExpression
                          | DEFAULT SetExpression
                          | DIMEN NumericExpression
                          | DIMEN Variable
                          | DIMEN SymbolicExpression
                          | COLON EQ NumericExpression
                          | COLON EQ Variable
                          | COLON EQ SymbolicExpression
                          | COLON EQ SetExpression
                          | LT NumericExpression
                          | LT Variable
                          | LT SymbolicExpression
                          | LE NumericExpression
                          | LE Variable
                          | LE SymbolicExpression
                          | EQ NumericExpression
                          | EQ Variable
                          | EQ SymbolicExpression
                          | GT NumericExpression
                          | GT Variable
                          | GT SymbolicExpression
                          | GE NumericExpression
                          | GE Variable
                          | GE SymbolicExpression
                          | NEQ NumericExpression
                          | NEQ Variable
                          | NEQ SymbolicExpression'''
  if isinstance(t[2], Variable):
    t[2] = SetExpressionWithValue(t[2])    

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
    '''LinearExpression : SymbolicExpression
                        | LPAREN LinearExpression RPAREN
                        | ConditionalLinearExpression'''

    if len(t) > 3:
        t[0] = LinearExpressionBetweenParenthesis(t[2])
    elif isinstance(t[1], ConditionalLinearExpression):
        t[0] = t[1]
    else:
        t[0] = ValuedLinearExpression(t[1])

def p_LinearExpression_binop(t):
    '''LinearExpression : LinearExpression PLUS LinearExpression
                        | LinearExpression PLUS NumericExpression
                        | LinearExpression PLUS Variable
                        | NumericExpression PLUS LinearExpression
                        | Variable PLUS LinearExpression
                        | LinearExpression MINUS LinearExpression
                        | LinearExpression MINUS NumericExpression
                        | LinearExpression MINUS Variable
                        | NumericExpression MINUS LinearExpression
                        | Variable MINUS LinearExpression
                        | LinearExpression TIMES NumericExpression
                        | LinearExpression TIMES Variable
                        | LinearExpression DIVIDE NumericExpression
                        | LinearExpression DIVIDE Variable'''

    if t[2] == "+":
        op = LinearExpressionWithArithmeticOperation.PLUS
    elif t[2] == "-":
        op = LinearExpressionWithArithmeticOperation.MINUS
    elif re.search(r"\*|\\cdot|\\ast", t[2]):
        op = LinearExpressionWithArithmeticOperation.TIMES
    elif re.search(r"/|\\div", t[2]):
        op = LinearExpressionWithArithmeticOperation.DIV

    t[0] = LinearExpressionWithArithmeticOperation(op, t[1], t[3])

#def p_IteratedLinearExpression(t):
#    '''LinearExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE LinearExpression
#                        | SUM UNDERLINE LBRACE IndexingExpression RBRACE LinearExpression'''
#    if len(t) > 7:
#        t[0] = IteratedLinearExpression(t[10], t[4], t[8])
#    else:
#        t[0] = IteratedLinearExpression(t[6], t[4])

def p_ConditionalLinearExpression(t):
    '''ConditionalLinearExpression : LPAREN Variable RPAREN QUESTION_MARK LinearExpression COLON LinearExpression
                                   | LPAREN Variable RPAREN QUESTION_MARK LinearExpression COLON NumericExpression
                                   | LPAREN Variable RPAREN QUESTION_MARK LinearExpression COLON Variable
                                   | LPAREN Variable RPAREN QUESTION_MARK NumericExpression COLON LinearExpression
                                   | LPAREN Variable RPAREN QUESTION_MARK Variable COLON LinearExpression
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK LinearExpression COLON LinearExpression
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK LinearExpression COLON NumericExpression
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK LinearExpression COLON Variable
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK NumericExpression COLON LinearExpression
                                   | LPAREN LogicalExpression RPAREN QUESTION_MARK Variable COLON LinearExpression'''
    t[0] = ConditionalLinearExpression(t[2], t[5])
    t[0].addElseExpression(t[7])

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
    '''EntryLogicalExpression : NumericExpression
                              | Variable
                              | NOT EntryLogicalExpression
                              | LPAREN LogicalExpression RPAREN'''

    if isinstance(t[1], str) and re.search(r"!|\\text\{\s*not\s*}", t[1]):
      t[0] = EntryLogicalExpressionNot(t[2])
    elif t[1] == "(":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])
    else:
      t[0] = EntryLogicalExpressionNumericOrSymbolic(t[1])

def p_EntryRelationalLogicalExpression(t):
    '''EntryLogicalExpression : NumericExpression LT NumericExpression
                              | NumericExpression LT Variable
                              | Variable LT NumericExpression
                              | Variable LT Variable
                              | NumericExpression LT SymbolicExpression
                              | Variable LT SymbolicExpression
                              | SymbolicExpression LT NumericExpression
                              | SymbolicExpression LT Variable
                              | SymbolicExpression LT SymbolicExpression
                              | NumericExpression LE NumericExpression
                              | NumericExpression LE Variable
                              | Variable LE NumericExpression
                              | Variable LE Variable
                              | NumericExpression LE SymbolicExpression
                              | Variable LE SymbolicExpression
                              | SymbolicExpression LE NumericExpression
                              | SymbolicExpression LE Variable
                              | SymbolicExpression LE SymbolicExpression
                              | NumericExpression EQ NumericExpression
                              | NumericExpression EQ Variable
                              | Variable EQ NumericExpression
                              | Variable EQ Variable
                              | NumericExpression EQ SymbolicExpression
                              | Variable EQ SymbolicExpression
                              | SymbolicExpression EQ NumericExpression
                              | SymbolicExpression EQ Variable
                              | SymbolicExpression EQ SymbolicExpression
                              | NumericExpression GT NumericExpression
                              | NumericExpression GT Variable
                              | Variable GT NumericExpression
                              | Variable GT Variable
                              | NumericExpression GT SymbolicExpression
                              | Variable GT SymbolicExpression
                              | SymbolicExpression GT NumericExpression
                              | SymbolicExpression GT Variable
                              | SymbolicExpression GT SymbolicExpression
                              | NumericExpression GE NumericExpression
                              | NumericExpression GE Variable
                              | Variable GE NumericExpression
                              | Variable GE Variable
                              | NumericExpression GE SymbolicExpression
                              | Variable GE SymbolicExpression
                              | SymbolicExpression GE NumericExpression
                              | SymbolicExpression GE Variable
                              | SymbolicExpression GE SymbolicExpression
                              | NumericExpression NEQ NumericExpression
                              | NumericExpression NEQ Variable
                              | Variable NEQ NumericExpression
                              | Variable NEQ Variable
                              | NumericExpression NEQ SymbolicExpression
                              | Variable NEQ SymbolicExpression
                              | SymbolicExpression NEQ NumericExpression
                              | SymbolicExpression NEQ Variable
                              | SymbolicExpression NEQ SymbolicExpression'''

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
                              | NumericExpression IN SetExpression
                              | Variable IN SetExpression
                              | SymbolicExpression IN SetExpression
                              | ValueList IN Variable
                              | NumericExpression IN Variable
                              | Variable IN Variable
                              | SymbolicExpression IN Variable
                              | Tuple IN SetExpression
                              | Tuple IN Variable
                              | ValueList NOTIN SetExpression
                              | NumericExpression NOTIN SetExpression
                              | Variable NOTIN SetExpression
                              | SymbolicExpression NOTIN SetExpression
                              | ValueList NOTIN Variable
                              | NumericExpression NOTIN Variable
                              | Variable NOTIN Variable
                              | SymbolicExpression NOTIN Variable
                              | Tuple NOTIN SetExpression
                              | Tuple NOTIN Variable
                              | SetExpression SUBSET SetExpression
                              | Variable SUBSET SetExpression
                              | SetExpression SUBSET Variable
                              | SetExpression NOTSUBSET SetExpression
                              | Variable NOTSUBSET SetExpression
                              | SetExpression NOTSUBSET Variable'''
    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], ValueList):
      t[1] = ValueList([t[1]])

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
    '''SetExpression : Variable DIFF Variable
                     | SetExpression DIFF SetExpression
                     | Variable DIFF SetExpression
                     | SetExpression DIFF Variable
                     | SetExpression SYMDIFF SetExpression
                     | Variable SYMDIFF Variable
                     | Variable SYMDIFF SetExpression
                     | SetExpression SYMDIFF Variable
                     | SetExpression UNION SetExpression
                     | Variable UNION Variable
                     | Variable UNION SetExpression
                     | SetExpression UNION Variable
                     | SetExpression INTER SetExpression
                     | Variable INTER Variable
                     | Variable INTER SetExpression
                     | SetExpression INTER Variable
                     | SetExpression CROSS SetExpression
                     | Variable CROSS Variable
                     | Variable CROSS SetExpression
                     | SetExpression CROSS Variable'''

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

    if not isinstance(t[1], SetExpression):
      t[1] = SetExpressionWithValue(t[1])

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    t[0] = SetExpressionWithOperation(op, t[1], t[3])

def p_SetExpressionWithValue(t):
    '''SetExpression : LLBRACE ValueList RRBRACE
                     | LLBRACE NumericExpression RRBRACE
                     | LLBRACE Variable RRBRACE
                     | LLBRACE SymbolicExpression RRBRACE
                     | LLBRACE Range RRBRACE
                     | LLBRACE SetExpression RRBRACE
                     | LLBRACE TupleList RRBRACE
                     | LLBRACE IndexingExpression RRBRACE
                     | LLBRACE RRBRACE
                     | LPAREN SetExpression RPAREN
                     | Range
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
            if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Variable):
              t[2] = ValueList([t[2]])

            t[0] = SetExpressionBetweenBraces(SetExpressionWithValue(t[2]))
          else:
            t[0] = SetExpressionBetweenBraces(None)
        elif t[1] == "(":
          t[0] = SetExpressionBetweenParenthesis(t[2])
        else:
          if not isinstance(t[2], SetExpression):
            t[2] = SetExpressionWithValue(t[2])

          t[0] = SetExpressionWithValue(t[2])
    else:
        value = t[1]
        if hasattr(t.slice[1], 'value2'):
          value = t.slice[1].value2
        
        t[0] = SetExpressionWithValue(value)

def p_SetExpressionWithIndices(t):
    '''SetExpression : Variable LPAREN ValueList RPAREN
                     | Variable LPAREN NumericExpression RPAREN
                     | Variable LPAREN Variable RPAREN
                     | Variable LPAREN SymbolicExpression RPAREN
                     | Variable LBRACKET ValueList RBRACKET
                     | Variable LBRACKET NumericExpression RBRACKET
                     | Variable LBRACKET Variable RBRACKET
                     | Variable LBRACKET SymbolicExpression RBRACKET'''
    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Variable):
      t[3] = ValueList([t[3]])

    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE ValueList
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE Variable
                     | SETOF LLBRACE IndexingExpression RRBRACE SymbolicExpression
                     | SETOF LLBRACE IndexingExpression RRBRACE LPAREN ValueList RPAREN'''
    
    if t[5] == "(":
      t[0] = IteratedSetExpression(t[3], t[6])
    else:
      if isinstance(t[5], NumericExpression) or isinstance(t[5], SymbolicExpression) or isinstance(t[5], Variable):
        t[5] = ValueList([t[5]])

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
                               | NumericExpression IN SetExpression
                               | Variable IN SetExpression
                               | SymbolicExpression IN SetExpression
                               | ValueList IN Variable
                               | NumericExpression IN Variable
                               | Variable IN Variable
                               | SymbolicExpression IN Variable
                               | Tuple IN SetExpression
                               | Tuple IN Variable'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Variable):
      t[1] = ValueList([t[1]])

    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Variable EQ NUMBER
                               | Variable EQ Variable
                               | Variable EQ Range
                               | Variable NEQ NumericExpression
                               | Variable NEQ Variable
                               | Variable LE NumericExpression
                               | Variable LE Variable
                               | Variable GE NumericExpression
                               | Variable GE Variable
                               | Variable LT NumericExpression
                               | Variable LT Variable
                               | Variable GT NumericExpression
                               | Variable GT Variable'''
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
    '''SymbolicExpression : NumericExpression AMPERSAND NumericExpression
                          | NumericExpression AMPERSAND Variable
                          | Variable AMPERSAND NumericExpression
                          | Variable AMPERSAND Variable
                          | NumericExpression AMPERSAND SymbolicExpression
                          | Variable AMPERSAND SymbolicExpression
                          | SymbolicExpression AMPERSAND NumericExpression
                          | SymbolicExpression AMPERSAND Variable
                          | SymbolicExpression AMPERSAND SymbolicExpression'''
    if re.search(r"\\&", t[2]):
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])

def p_FunctionSymbolicExpression(t):
    '''SymbolicExpression : SUBSTR LPAREN NumericExpression COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA NumericExpression COMMA Variable RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Variable COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Variable COMMA Variable RPAREN
                          | SUBSTR LPAREN Variable COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Variable COMMA NumericExpression COMMA Variable RPAREN
                          | SUBSTR LPAREN Variable COMMA Variable COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Variable COMMA Variable COMMA Variable RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression COMMA Variable RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Variable COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Variable COMMA Variable RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN NumericExpression COMMA Variable RPAREN
                          | SUBSTR LPAREN Variable COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN Variable COMMA Variable RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA NumericExpression RPAREN
                          | SUBSTR LPAREN SymbolicExpression COMMA Variable RPAREN
                          | TIME2STR LPAREN NumericExpression COMMA NumericExpression RPAREN
                          | TIME2STR LPAREN NumericExpression COMMA Variable RPAREN
                          | TIME2STR LPAREN Variable COMMA NumericExpression RPAREN
                          | TIME2STR LPAREN Variable COMMA Variable RPAREN
                          | TIME2STR LPAREN NumericExpression COMMA SymbolicExpression RPAREN
                          | TIME2STR LPAREN Variable COMMA SymbolicExpression RPAREN'''

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
                         | NumericExpression PLUS Variable
                         | Variable PLUS NumericExpression
                         | Variable PLUS Variable
                         | NumericExpression MINUS NumericExpression
                         | NumericExpression MINUS Variable
                         | Variable MINUS NumericExpression
                         | Variable MINUS Variable
                         | NumericExpression TIMES NumericExpression
                         | NumericExpression TIMES Variable
                         | Variable TIMES NumericExpression
                         | Variable TIMES Variable
                         | NumericExpression DIVIDE NumericExpression
                         | NumericExpression DIVIDE Variable
                         | Variable DIVIDE NumericExpression
                         | Variable DIVIDE Variable
                         | NumericExpression MOD NumericExpression
                         | NumericExpression MOD Variable
                         | Variable MOD NumericExpression
                         | Variable MOD Variable
                         | NumericExpression QUOTIENT NumericExpression
                         | NumericExpression QUOTIENT Variable
                         | Variable QUOTIENT NumericExpression
                         | Variable QUOTIENT Variable
                         | NumericExpression LESS NumericExpression
                         | NumericExpression LESS Variable
                         | Variable LESS NumericExpression
                         | Variable LESS Variable
                         | NumericExpression CARET LBRACE NumericExpression RBRACE
                         | NumericExpression CARET LBRACE Variable RBRACE
                         | Variable CARET LBRACE NumericExpression RBRACE
                         | Variable CARET LBRACE Variable RBRACE'''

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

    if len(t) > 4 and isinstance(t[4], Variable):
      t[4] = ValuedNumericExpression(t[4])
    elif len(t) > 3 and isinstance(t[3], Variable):
      t[3] = ValuedNumericExpression(t[3])
    elif isinstance(t[1], Variable):
      t[1] = ValuedNumericExpression(t[1])

    if t[2] == "^":
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[4])
    else:
      t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

def p_IteratedNumericExpression(t):
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Variable
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE Variable
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE Variable
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Variable
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE Variable
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Variable
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Variable
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE Variable
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Variable
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericExpression RBRACE Variable
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Variable RBRACE Variable
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE Variable'''

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
                         | MINUS Variable %prec UMINUS
                         | PLUS NumericExpression %prec UPLUS
                         | PLUS Variable %prec UPLUS
                         | LPAREN NumericExpression RPAREN
                         | LPAREN Variable RPAREN
                         | ConditionalNumericExpression
                         | NUMBER'''

    if len(t) > 2 and isinstance(t[2], Variable):
      t[2] = ValuedNumericExpression(t[2])

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
                         | SQRT LBRACE Variable RBRACE
                         | LFLOOR NumericExpression RFLOOR
                         | LFLOOR Variable RFLOOR
                         | LCEIL NumericExpression RCEIL
                         | LCEIL Variable RCEIL
                         | PIPE NumericExpression PIPE
                         | PIPE Variable PIPE
                         | MAX LPAREN ValueList RPAREN
                         | MAX LPAREN NumericExpression RPAREN
                         | MAX LPAREN Variable RPAREN
                         | MAX LPAREN SymbolicExpression RPAREN
                         | MIN LPAREN ValueList RPAREN
                         | MIN LPAREN NumericExpression RPAREN
                         | MIN LPAREN Variable RPAREN
                         | MIN LPAREN SymbolicExpression RPAREN
                         | SIN LPAREN NumericExpression RPAREN
                         | SIN LPAREN Variable RPAREN
                         | COS LPAREN NumericExpression RPAREN
                         | COS LPAREN Variable RPAREN
                         | LOG LPAREN NumericExpression RPAREN
                         | LOG LPAREN Variable RPAREN
                         | LN LPAREN NumericExpression RPAREN
                         | LN LPAREN Variable RPAREN
                         | EXP LPAREN NumericExpression RPAREN
                         | EXP LPAREN Variable RPAREN
                         | ARCTAN LPAREN NumericExpression RPAREN
                         | ARCTAN LPAREN Variable RPAREN
                         | ARCTAN LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | ARCTAN LPAREN NumericExpression COMMA Variable RPAREN
                         | ARCTAN LPAREN Variable COMMA NumericExpression RPAREN
                         | ARCTAN LPAREN Variable COMMA Variable RPAREN
                         | CARD LPAREN SetExpression RPAREN
                         | CARD LPAREN Variable RPAREN
                         | LENGTH LPAREN NumericExpression RPAREN
                         | LENGTH LPAREN Variable RPAREN
                         | LENGTH LPAREN SymbolicExpression RPAREN
                         | ROUND LPAREN NumericExpression RPAREN
                         | ROUND LPAREN Variable RPAREN
                         | ROUND LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | ROUND LPAREN NumericExpression COMMA Variable RPAREN
                         | ROUND LPAREN Variable COMMA NumericExpression RPAREN
                         | ROUND LPAREN Variable COMMA Variable RPAREN
                         | STR2TIME LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | STR2TIME LPAREN NumericExpression COMMA Variable RPAREN
                         | STR2TIME LPAREN Variable COMMA NumericExpression RPAREN
                         | STR2TIME LPAREN Variable COMMA Variable RPAREN
                         | STR2TIME LPAREN NumericExpression COMMA SymbolicExpression RPAREN
                         | STR2TIME LPAREN Variable COMMA SymbolicExpression RPAREN
                         | STR2TIME LPAREN SymbolicExpression COMMA NumericExpression RPAREN
                         | STR2TIME LPAREN SymbolicExpression COMMA Variable RPAREN
                         | STR2TIME LPAREN SymbolicExpression COMMA SymbolicExpression RPAREN
                         | TRUNC LPAREN NumericExpression RPAREN
                         | TRUNC LPAREN Variable RPAREN
                         | TRUNC LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | TRUNC LPAREN NumericExpression COMMA Variable RPAREN
                         | TRUNC LPAREN Variable COMMA NumericExpression RPAREN
                         | TRUNC LPAREN Variable COMMA Variable RPAREN
                         | UNIFORM LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | UNIFORM LPAREN NumericExpression COMMA Variable RPAREN
                         | UNIFORM LPAREN Variable COMMA NumericExpression RPAREN
                         | UNIFORM LPAREN Variable COMMA Variable RPAREN
                         | NORMAL LPAREN NumericExpression COMMA NumericExpression RPAREN
                         | NORMAL LPAREN NumericExpression COMMA Variable RPAREN
                         | NORMAL LPAREN Variable COMMA NumericExpression RPAREN
                         | NORMAL LPAREN Variable COMMA Variable RPAREN
                         | GMTIME LPAREN RPAREN
                         | IRAND224 LPAREN RPAREN
                         | UNIFORM01 LPAREN RPAREN
                         | NORMAL01 LPAREN RPAREN'''

    if t[1] == "card":
        op = NumericExpressionWithFunction.CARD

        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

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
        if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Variable):
          t[3] = ValueList([t[3]])

        t[0] = NumericExpressionWithFunction(op, t[3], t[5])
    elif len(t) > 4:
        if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Variable):
          t[3] = ValueList([t[3]])

        t[0] = NumericExpressionWithFunction(op, t[3])
    else:
        if t[2] == "(":
          t[0] = NumericExpressionWithFunction(op)
        else:
          t[0] = NumericExpressionWithFunction(op, t[2])

def p_ConditionalNumericExpression(t):
    '''ConditionalNumericExpression : LPAREN Variable RPAREN QUESTION_MARK NumericExpression COLON NumericExpression
                                    | LPAREN Variable RPAREN QUESTION_MARK NumericExpression COLON Variable
                                    | LPAREN Variable RPAREN QUESTION_MARK Variable COLON NumericExpression
                                    | LPAREN Variable RPAREN QUESTION_MARK Variable COLON Variable
                                    | LPAREN LogicalExpression RPAREN QUESTION_MARK NumericExpression COLON NumericExpression
                                    | LPAREN LogicalExpression RPAREN QUESTION_MARK NumericExpression COLON Variable
                                    | LPAREN LogicalExpression RPAREN QUESTION_MARK Variable COLON NumericExpression
                                    | LPAREN LogicalExpression RPAREN QUESTION_MARK Variable COLON Variable'''
    t[0] = ConditionalNumericExpression(t[2], t[5])
    t[0].addElseExpression(t[7])

#def p_NumericOrSymbolicExpression(t):
#    '''NumericOrSymbolicExpression : NumericExpression
#                                   | SymbolicExpression'''
#    t[0] = t[1]


def p_Range(t):
    '''Range : NumericExpression DOTS NumericExpression BY NumericExpression
             | NumericExpression DOTS NumericExpression BY Variable
             | NumericExpression DOTS Variable BY NumericExpression
             | NumericExpression DOTS Variable BY Variable
             | Variable DOTS NumericExpression BY NumericExpression
             | Variable DOTS NumericExpression BY Variable
             | Variable DOTS Variable BY NumericExpression
             | Variable DOTS Variable BY Variable
             | NumericExpression DOTS NumericExpression
             | NumericExpression DOTS Variable
             | Variable DOTS NumericExpression
             | Variable DOTS Variable'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

def p_Variable(t):
    '''Variable : ID UNDERLINE LBRACE ValueList RBRACE
                | ID UNDERLINE LBRACE NumericExpression RBRACE
                | ID UNDERLINE LBRACE Variable RBRACE
                | ID UNDERLINE LBRACE SymbolicExpression RBRACE
                | ID LBRACKET ValueList RBRACKET
                | ID LBRACKET NumericExpression RBRACKET
                | ID LBRACKET Variable RBRACKET
                | ID LBRACKET SymbolicExpression RBRACKET
                | ID'''

    if len(t) > 5:
        if isinstance(t[4], ValueList):
          t[0] = Variable(ID(t[1]), t[4].getValues())
        else:
          t[0] = Variable(ID(t[1]), [t[4]])
    elif len(t) > 2:
        if isinstance(t[3], ValueList):
          t[0] = Variable(ID(t[1]), t[3].getValues())
        else:
          t[0] = Variable(ID(t[1]), [t[3]])
    else:
        t[0] = Variable(ID(t[1]))

def p_ValueList(t):
    '''ValueList : ValueList COMMA NumericExpression
                 | ValueList COMMA Variable
                 | ValueList COMMA SymbolicExpression
                 | NumericExpression COMMA NumericExpression
                 | NumericExpression COMMA Variable
                 | Variable COMMA NumericExpression
                 | Variable COMMA Variable
                 | NumericExpression COMMA SymbolicExpression
                 | Variable COMMA SymbolicExpression
                 | SymbolicExpression COMMA NumericExpression
                 | SymbolicExpression COMMA Variable
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
    raise SyntaxException(t.lineno, t.lexpos, t.value)
  else:
    raise SyntaxException("EOF")
