#!/usr/bin/python -tt

#import ply.lex as lex

# List of token names.   This is always required

from Number import *
from String import *
import sys
import re

reserved = {
   'card' : 'CARD',
   'length' : 'LENGTH',
   'round' : 'ROUND',
   'trunc' : 'TRUNC',
   'substr' : 'SUBSTR',
   'time2str': 'TIME2STR'
}

tokens = [
   'OR',
   'AND',
   'NOT',
   'FORALL',
   'EXISTS',
   'QUESTION_MARK',
   'INTEGERSET',
   'INTEGERSETPOSITIVE',
   'INTEGERSETNEGATIVE',
   'INTEGERSETWITHONELIMIT',
   'INTEGERSETWITHTWOLIMITS',
   'BINARYSET',
   'REALSET',
   'REALSETPOSITIVE',
   'REALSETNEGATIVE',
   'REALSETWITHONELIMIT',
   'REALSETWITHTWOLIMITS',
   'NATURALSET',
   'SUBSET',
   'NOTSUBSET',
   'NUMBER',
   'SYMBOLIC',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'QUOTIENT',
   'LESS',
   'MAXIMIZE',
   'MINIMIZE',
   'SUBJECTTO',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'LBRACKET',
   'RBRACKET',
   'LFLOOR',
   'RFLOOR',
   'LCEIL',
   'RCEIL',
   'SIN',
   'COS',
   'ARCTAN',
   'SQRT',
   'LOG',
   'LN',
   'EXP',
   'MOD',
   'EQ',
   'NEQ',
   'LE',
   'LT',
   'GE',
   'GT',
   'IN',
   'NOTIN',
   'UNDERLINE',
   'CARET',
   'SUM',
   'PROD',
   'MAX',
   'MIN',
   'LIMITS',
   'BEGIN',
   'END',
   'BEGIN_EQUATION',
   'END_EQUATION',
   'BEGIN_SPLIT',
   'END_SPLIT',
   'DISPLAYSTYLE',
   'TEXT',
   'COMMA',
   'COLON',
   'DOTS',
   'AMPERSAND',
   'AMP',
   'BACKSLASHES',
   'FOR',
   'ID',
   'QUAD',
   'MATHCLAP',
   'PIPE', 
   'DIFF',
   'SYMDIFF', 
   'UNION', 
   'INTER', 
   'CROSS',
   'STRING'
] + list(reserved.values())

def t_STRING(t):
   r'"(?:[^\\]|\\.)*?(?:"|$)|\'(?:[^\\]|\\.)*?(?:\'|$)'
   t.value = String(t.value)
   return t

def t_DOTS(t):
   r'\\cdots|\\ldots|\\dots|\.\.\.'
   t.value = "DOTS"
   return t

def t_COMMENT(t):
    r'\%[^\n]*'
    pass

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'

def t_MOD(t):
   r'\\text\{\%\}|\\mod|\\bmod'
   t.value = "\%"
   return t

def t_QUOTIENT(t):
   r'\\big/|\\text\{\s*div\s*\}|div'
   t.value = "quot"
   return t

def t_TIMES(t):
   r'\*|\\cdot|\\ast'
   t.value = "*"
   return t

def t_DIVIDE(t):
   r'/|\\div'
   t.value = "/"
   return t

def t_LESS(t):
   r'\\text\{\s*less\s*\}|less'
   t.value = "less"
   return t

def t_OR(t):
   r'\\vee|\\text\{or\}'
   t.value = "or"
   return t

def t_AND(t):
   r'\\wedge|\\text\{and\}'
   t.value = "and"
   return t

def t_NOT(t):
   r'!|not'
   t.value = "not"
   return t

def t_FORALL(t):
   r'\\forall'
   return t

def t_EXISTS(t):
   r'\\exists'
   return t

def t_BINARYSET(t):
   r'\\mathbb{B}'
   t.value = "binary"
   return t

def t_INTEGERSETWITHTWOLIMITS(t):
   r'\\mathbb{Z}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)

   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " , >="
      elif groups[0] == "\\leq":
         domain += " , <="
      else:
         domain += " , " + groups[0]+"="

      domain += " " + groups[1]

      if groups[2] != None and groups[2] != 0:
         domain += groups[2]

      if groups[3] == "\\geq":
         domain += ", >="
      elif groups[3] == "\\leq":
         domain += ", <="
      else:
         domain += ", " + groups[3]+"="
      
      domain += " " + groups[4]

      if groups[5] != None and groups[5] != 0:
         domain += groups[5]

   t.value = "integer" + domain

   return t

def t_INTEGERSETWITHONELIMIT(t):
   r'\\mathbb{Z}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)

   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " >="
      elif groups[0] == "\\leq":
         domain += " <="
      else:
         domain += " " + groups[0]+"="

      domain += " " + groups[1]

      if groups[2] != None and groups[2] != 0:
         domain += groups[2]

   t.value = "integer" + domain

   return t

def t_INTEGERSETPOSITIVE(t):
   r'\\mathbb{Z}[_\^]{\+}'
   t.value = "integer >= 0"
   return t

def t_INTEGERSETNEGATIVE(t):
   r'\\mathbb{Z}[_\^]{-}'
   t.value = "integer <= 0"
   return t

def t_INTEGERSET(t):
   r'\\mathbb{Z}'
   t.value = "integer"
   return t

def t_REALSETWITHTWOLIMITS(t):
   r'\\mathbb{R}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)

   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " , >="
      elif groups[0] == "\\leq":
         domain += " , <="
      else:
         domain += " , " + groups[0]+"="

      domain += " " + groups[1]

      if groups[2] != None and groups[2] != 0:
         domain += groups[2]

      if groups[3] == "\\geq":
         domain += ", >="
      elif groups[3] == "\\leq":
         domain += ", <="
      else:
         domain += ", " + groups[3]+"="
      
      domain += " " + groups[4]

      if groups[5] != None and groups[5] != 0:
         domain += groups[5]

   t.value = "realset" + domain

   return t

def t_REALSETWITHONELIMIT(t):
   r'\\mathbb{R}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)

   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " >="
      elif groups[0] == "\\leq":
         domain += " <="
      else:
         domain += " " + groups[0]+"="

      domain += " " + groups[1]

      if groups[2] != None and groups[2] != 0:
         domain += groups[2]

   t.value = "realset" + domain
   return t

def t_REALSETPOSITIVE(t):
   r'\\mathbb{R}[_\^]{\+}'
   t.value = "realset >= 0"
   return t

def t_REALSETNEGATIVE(t):
   r'\\mathbb{R}[_\^]{-}'
   t.value = "realset <= 0"
   return t

def t_REALSET(t):
   r'\\mathbb{R}'
   t.value = "realset"
   return t

def t_NATURALSETWITHTWOLIMITS(t):
   r'\\mathbb{N}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?\s*,\s*([><]|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)
   
   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " , >="
      elif groups[0] == "\\leq":
         domain += " , <="
      else:
         domain += " , " + groups[0]+"="

      limit = float(groups[1])
      if limit < 0:
         limit = 0

      domain += " " + str(limit)

      if limit > 0:
         if groups[2] != None and groups[2] != 0:
            domain += groups[2]

      if groups[3] == "\\geq":
         domain += ", >="
      elif groups[3] == "\\leq":
         domain += ", <="
      else:
         domain += ", " + groups[3]+"="
      
      limit = float(groups[4])
      if limit < 0:
         limit = 0

      domain += " " + str(limit)

      if limit > 0:
         if groups[5] != None and groups[5] != 0:
            domain += groups[5]

   t.value = "realset" + domain

   return t

def t_NATURALSETWITHONELIMIT(t):
   r'\\mathbb{N}[_\^]{([><]|\\geq|\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}'
   m = re.search('[_\^]{(>|<|\\\\geq|\\\\leq)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?}', t.value)

   domain = ""
   if m:
      groups = m.groups(0)
      if groups[0] == "\\geq":
         domain += " >="
      elif groups[0] == "\\leq":
         domain += " <="
      else:
         domain += " " + groups[0]+"="

      limit = float(groups[1])
      if limit < 0:
         limit = 0

      domain += " " + str(limit)

      if limit > 0:
         if groups[2] != None and groups[2] != 0:
            domain += groups[2]

   t.value = "realset" + domain
   return t

def t_NATURALSET(t):
   r'\\mathbb{N}'
   t.value = "integer >= 0"
   return t

def t_SUBSET(t):
   r'\\subseteq|\\subset'
   t.value = "subset"
   return t

def t_NOTSUBSET(t):
   r'\\not\\subseteq|\\not\\subset'
   t.value = "notsubset"
   return t

def t_SYMBOLIC(t):
   r'\\mathbb{S}'
   t.value = "symbolic"
   return t

#t_DOT = r'\\cdot'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_MAXIMIZE(t):
   r'\\text\{\s*maximize\s*\}|maximize|\\text\{\s*maximize:\s*\}|maximize:'
   t.value = "maximize"
   return t

def t_MINIMIZE(t):
   r'\\text\{\s*minimize\s*\}|minimize|\\text\{\s*minimize:\s*\}|minimize:'
   t.value = "minimize"
   return t

def t_SUBJECTTO(t):
   r'\\text\{\s*subject\sto\s*\}|\\text\{\s*subj\.to\s*\}|\\text\{\s*s\.t\.\s*\}|subject\sto\s*|subj\.to\s*|s\.t\.\s*|\\text\{\s*subject\sto:\s*\}|\\text\{\s*subj\.to:\s*\}|\\text\{\s*s\.t\.:\s*\}|subject\sto:\s*|subj\.to:\s*|s\.t\.:\s*'
   t.value = "subjectto"
   return t

def t_LBRACE(t):
   r'\{|\\\{'
   t.value = "{"
   return t

def t_RBRACE(t):
   r'\}|\\\}'
   t.value = "}"
   return t

def t_LBRACKET(t):
   r'\[|\\\['
   t.value = "["
   return t

def t_RBRACKET(t):
   r'\]|\\\]'
   t.value = "]"
   return t

t_QUESTION_MARK = r'\?'
t_EQ = r'='
t_NEQ = r'\\neq'
t_LE = r'\\leq'
t_LT = r'<'
t_GE = r'\\geq'
t_GT = r'>'
t_IN = r'\\in'
t_NOTIN = r'\\notin'
t_UNDERLINE = r'_'
t_CARET = r'\^'
t_SUM = r'\\sum'
t_PROD = r'\\prod'
t_MAX = r'\\max'
t_MIN = r'\\min'
t_LFLOOR = r'\\lfloor'
t_RFLOOR = r'\\rfloor'
t_LCEIL = r'\\lceil'
t_RCEIL = r'\\rceil'
t_SIN = r'\\sin'
t_COS = r'\\cos'
t_ARCTAN = r'\\arctan'
t_SQRT = r'\\sqrt'
t_LOG = r'\\log'
t_LN = r'\\ln'
t_EXP = r'\\exp'

def t_PIPE(t):
   r'\\mid|\\vert|\|'
   t.value = "\\vert"
   return t

def t_ignore_LIMITS(t):
   r'\\limits'
   pass

def t_ignore_BEGIN(t):
   r'\\begin\{[a-zA-Z][a-zA-Z0-9]*[\*]?\}[\{\[][a-zA-Z0-9][a-zA-Z0-9]*[\*]?[\}\]]|\\begin\{[a-zA-Z][a-zA-Z0-9]*[\*]?\}'
   pass

def t_ignore_END(t):
   r'\\end\{[a-zA-Z][a-zA-Z0-9]*[\*]?\}[\{\[][a-zA-Z0-9][a-zA-Z0-9]*[\*]?[\}\]]|\\end\{[a-zA-Z][a-zA-Z0-9]*[\*]?\}'
   pass

def t_ignore_BEGIN_EQUATION(t):
   r'\\begin\{equation\}'
   pass

def t_ignore_END_EQUATION(t):
   r'\\end\{equation\}'
   pass

def t_ignore_BEGIN_SPLIT(t):
   r'\\begin\{split\}'
   pass

def t_ignore_END_SPLIT(t):
   r'\\end\{split\}'
   pass

def t_ignore_DISPLAYSTYLE(t):
   r'\\displaystyle'
   pass

def t_ignore_QUAD(t):
   r'\\quad'
   pass

def t_ignore_MATHCLAP(t):
   r'\\mathclap'
   pass

def t_ignore_TEXT(t):
    r'\\text\{\s*\}|\\text'
    pass

t_COMMA = r','

def t_COLON(t):
   r':'
   return t

def t_AMPERSAND(t):
   r'\\&'
   t.value = "AMP"
   return t

def t_ignore_AMP(t):
   r'&'
   pass

def t_BACKSLASHES(t):
   r'\\\\.*\n'
   t.lexer.lineno += 1
   t.value = "BACKSLASHES"
   return t

def t_DIFF(t):
   r'\\setminus'
   t.value = "DIFF"
   return t

def t_SYMDIFF(t):
   r'\\triangle|\\ominus'
   t.value = "SYMDIFF"
   return t

def t_UNION(t):
   r'\\cup'
   t.value = "UNION"
   return t

def t_INTER(t):
   r'\\cap'
   t.value = "INTER"
   return t

def t_CROSS(t):
   r'\\times'
   t.value = "CROSS"
   return t

def t_FOR(t):
   r'for'
   return t

def t_ID(t):
   r'[a-zA-Z][a-zA-Z0-9]*'
   t.type = reserved.get(t.value, 'ID') # Check for reserved words
   return t

# A regular expression rule with some action code
def t_NUMBER(t):
   r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
   t.value = Number(float(t.value))
   return t

# Define a rule so we can track line numbers
def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
   sys.stderr.write( "Illegal character '%s'" % t.value[0] )
   t.lexer.skip(1)
