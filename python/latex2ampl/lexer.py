#!/usr/bin/python -tt

# List of token names.   This is always required

from Number import *
from String import *

from IntegerSet import *
from RealSet import *
from SymbolicSet import *
from LogicalSet import *
from BinarySet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *

import sys
import re
from SyntaxException import *

reserved = {
   'card' : 'CARD',
   'length' : 'LENGTH',
   'round' : 'ROUND',
   'precision' : 'PRECISION',
   'trunc' : 'TRUNC',
   'substr' : 'SUBSTR',
   'Irand224': 'IRAND224',
   'Uniform01': 'UNIFORM01',
   'Normal01': 'NORMAL01',
   'Uniform': 'UNIFORM',
   'Normal': 'NORMAL',
   'Beta': 'BETA',
   'Cauchy': 'CAUCHY',
   'Exponential': 'EXPONENTIAL',
   'Gamma': 'GAMMA',
   'Poisson': 'POISSON',
   'alias': 'ALIAS',
   'ctime': 'CTIME',
   'time': 'TIME',
   'num': 'NUM',
   'num0': 'NUM0',
   'ichar': 'ICHAR',
   'char': 'CHAR',
   'sprintf': 'SPRINTF',
   'match': 'MATCH',
   'sub': 'SUB',
   'gsub': 'GSUB'
}

tokens = [
   'OR',
   'AND',
   'NOT',
   'FORALL',
   'NFORALL',
   'EXISTS',
   'NEXISTS',
#   'QUESTION_MARK',
   'EMPTYSET',
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
   'NATURALSETWITHONELIMIT',
   'NATURALSETWITHTWOLIMITS',
   'FRAC',
   'DEFAULT',
   'SETOF',
   'DIMEN',
   'SUBSET',
   'NOTSUBSET',
   'NUMBER',
   'SYMBOLIC',
   'LOGICAL',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'QUOTIENT',
   'LESS',
   'MAXIMIZE',
   'MINIMIZE',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'LLBRACE',
   'RRBRACE',
   'LBRACKET',
   'RBRACKET',
   'LFLOOR',
   'RFLOOR',
   'LCEIL',
   'RCEIL',
   'SIN',
   'ASIN',
   'SINH',
   'ASINH',
   'COS',
   'ACOS',
   'COSH',
   'ACOSH',
   'TAN',
   'TANH',
   'ARCTAN',
   'ARCTANH',
   'SQRT',
   'LOG',
   'LN',
   'EXP',
   'MOD',
   'ASSIGN',
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
   'COMMA',
   'SEMICOLON',
   'COLON',
   'DOTS',
   'AMPERSAND',
   'FOR',
   'WHERE',
   'ID',
   'PIPE', 
   'DIFF',
   'SYMDIFF', 
   'UNION', 
   'INTER', 
   'CROSS',
   'STRING',
   'BY',
   'PARAMETERS',
   'SETS',
   'VARIABLES',
   'SLASHES',
   'INFINITY',
   'IF',
   'THEN',
   'ELSE'
] + list(reserved.values())

def _getBound(num, exp):
   bound = num
   if exp != None and exp != 0:
      bound += exp

   return Number(bound)

def _getOp(op):
   if op == "\\geq":
      op = ">="
   elif op == "\\leq":
      op = "<="

   return op

def t_IF(t):
   r'\\text\{\s*if\s*\}'
   return t

def t_THEN(t):
   r'\\text\{\s*then\s*\}'
   return t

def t_ELSE(t):
   r'\\text\{\s*else\s*\}'
   return t

def t_ASSIGN(t):
   r':='
   return t

def t_STRING(t):
   r'"(?:[^\\]|\\.)*?(?:"|$)|\'(?:[^\\]|\\.)*?(?:\'|$)'

   if t.value[0] != t.value[len(t.value)-1]:
      raise SyntaxException(t.lexer.lineno, t.lexer.lexpos, "unclosed string "+t.value)

   t.value = String(t.value)
   return t

def t_DOTS(t):
   r'\\cdots|\\ldots|\\dots|\.\.\.'
   return t

def t_EMPTYSET(t):
   r'\\emptyset|\\varnothing'
   return t

def t_INFINITY(t):
   r'\\infty'
   t.value = Number("Infinity")
   return t

def t_SLASHES(t):
   r'//'
   return t

def t_COMMENT(t):
    r'\%[^\n]*'
    pass

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'

def t_MOD(t):
   r'\\text\{\s*\%\s*\}|\\mod|\\bmod'
   return t

def t_BY(t):
   r'\\text\{\s*by\s*\}'
   return t

def t_QUOTIENT(t):
   r'\\big/|\\text\{\s*div\s*\}'
   return t

def t_TIMES(t):
   r'\*|\\cdot|\\ast'
   return t

def t_DIVIDE(t):
   r'/|\\div'
   return t

def t_LESS(t):
   r'\\text\{\s*less\s*\}'
   return t

def t_FOR(t):
   r'\\text\{\s*[fF][oO][rR]\s*\}'
   return t

def t_WHERE(t):
   r'\\text\{\s*[wW][hH][eE][rR][eE]\s*\}'
   return t

def t_OR(t):
   r'\\lor|\\vee|\\text\{\s*or\s*\}'
   return t

def t_AND(t):
   r'\\land|\\wedge|\\text\{\s*and\s*\}'
   return t

def t_NOT(t):
   r'\\neg|!|\\text\{\s*not\s*}'
   return t

def t_FORALL(t):
   r'\\forall'
   return t

def t_NFORALL(t):
   r'\\not\\forall'
   return t

def t_EXISTS(t):
   r'\\exists'
   return t

def t_NEXISTS(t):
   r'\\nexists|\\not\\exists'
   return t

def t_FRAC(t):
   r'\\frac'
   return t

def t_DEFAULT(t):
   r'\\text\{\s*default\s*\}'
   return t

def t_DIMEN(t):
   r'\\text\{\s*dimen\s*\}'
   return t

def t_SETOF(t):
   r'\\text\{\s*setof\s*\}'
   return t

def t_PARAMETERS(t):
   r'\\mathbb{P}|\\mathbb{Param}|\\mathbb{Params}|\\mathbb{Parameter}|\\mathbb{Parameters}'
   t.value2 = ParameterSet()
   return t

def t_SETS(t):
   r'\\mathbb{Set}|\\mathbb{Sets}'
   t.value2 = SetSet()
   return t

def t_VARIABLES(t):
   r'\\mathbb{V}|\\mathbb{Var}|\\mathbb{Variable}|\\mathbb{Vars}|\\mathbb{Variables}'
   t.value2 = VariableSet()
   return t

def t_BINARYSET(t):
   r'\\mathbb{B}'
   t.value2 = BinarySet()
   return t

def t_INTEGERSETWITHTWOLIMITS(t):
   r'\\mathbb{Z}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)

   if m:

      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound  = _getBound(groups[1], groups[2])
      secondBound = _getBound(groups[4], groups[5])

      firstOp  = _getOp(groups[0])
      secondOp = _getOp(groups[3])

      t.value2 = IntegerSet(firstBound, firstOp, secondBound, secondOp)

   return t

def t_INTEGERSETWITHONELIMIT(t):
   r'\\mathbb{Z}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)

   if m:
      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound = _getBound(groups[1], groups[2])
      firstOp = _getOp(groups[0])

      t.value2 = IntegerSet(firstBound, firstOp, secondBound, None)

   return t

def t_INTEGERSETPOSITIVE(t):
   r'\\mathbb{Z}[_\^]{\+}'
   t.value2 = IntegerSet(Number("0"), ">=", Number("Infinity"), "<=")

   return t

def t_INTEGERSETNEGATIVE(t):
   r'\\mathbb{Z}[_\^]{-}'
   t.value2 = IntegerSet(Number("-Infinity"), ">=", Number("0"), "<=")
   return t

def t_INTEGERSET(t):
   r'\\mathbb{Z}'
   t.value2 = IntegerSet(Number("-Infinity"), ">=", Number("Infinity"), "<=")
   return t

def t_REALSETWITHTWOLIMITS(t):
   r'\\mathbb{R}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)

   if m:

      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound  = _getBound(groups[1], groups[2])
      secondBound = _getBound(groups[4], groups[5])

      firstOp  = _getOp(groups[0])
      secondOp = _getOp(groups[3])

      t.value2 = RealSet(firstBound, firstOp, secondBound, secondOp)

   return t

def t_REALSETWITHONELIMIT(t):
   r'\\mathbb{R}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)

   if m:
      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound = _getBound(groups[1], groups[2])
      firstOp = _getOp(groups[0])

      t.value2 = RealSet(firstBound, firstOp, secondBound, None)

   return t

def t_REALSETPOSITIVE(t):
   r'\\mathbb{R}[_\^]{\+}'
   t.value2 = RealSet(Number("0"), ">=", Number("Infinity"), "<=")
   return t

def t_REALSETNEGATIVE(t):
   r'\\mathbb{R}[_\^]{-}'
   t.value2 = RealSet(Number("-Infinity"), ">=", Number("0"), "<=")
   return t

def t_REALSET(t):
   r'\\mathbb{R}'
   t.value2 = RealSet(Number("-Infinity"), ">=", Number("Infinity"), "<=")
   return t

def t_NATURALSETWITHTWOLIMITS(t):
   r'\\mathbb{N}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?\s*,\s*([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)
   
   if m:

      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound  = _getBound(groups[1], groups[2])
      secondBound = _getBound(groups[4], groups[5])

      firstOp  = _getOp(groups[0])
      secondOp = _getOp(groups[3])

      t.value2 = IntegerSet(Number("0") if firstBound.lessThanZero() else firstBound, firstOp, secondBound, secondOp)

   return t

def t_NATURALSETWITHONELIMIT(t):
   r'\\mathbb{N}[_\^]{([><]|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}'
   m = re.search(r"[_\^]{(>|<|\\geq|\\leq)\s*([-+]?[0-9]*\.?[0-9]+)([dDeE][-+]?[0-9]+)?}", t.value)

   if m:
      firstBound  = Number("-Infinity")
      secondBound = Number("Infinity")

      groups = m.groups(0)
      firstBound = _getBound(groups[1], groups[2])
      firstOp = _getOp(groups[0])

      t.value2 = IntegerSet(Number("0") if firstBound.lessThanZero() else firstBound, firstOp, secondBound, None)

   return t

def t_NATURALSET(t):
   r'\\mathbb{N}'
   t.value2 = IntegerSet(Number("0"), ">=", Number("Infinity"), "<=")
   return t

def t_SYMBOLIC(t):
   r'\\mathbb{S}'
   t.value2 = SymbolicSet()
   return t

def t_LOGICAL(t):
   r'\\mathbb{L}'
   t.value2 = LogicalSet()
   return t

def t_SUBSET(t):
   r'\\subseteq|\\subset'
   return t

def t_NOTSUBSET(t):
   r'\\not\\subseteq|\\not\\subset'
   return t

t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_MAXIMIZE(t):
   r'\\text\{\s*maximize:\s*\}|maximize:|\\text\{\s*maximize\s*\}|maximize'
   return t

def t_MINIMIZE(t):
   r'\\text\{\s*minimize:\s*\}|minimize:|\\text\{\s*minimize\s*\}|minimize'
   return t

def t_ignore_SUBJECTTO(t):
   r'\\text\{\s*subject\sto:\s*\}|\\text\{\s*subj\.to:\s*\}|\\text\{\s*s\.t\.:\s*\}|subject\sto:\s*|subj\.to:\s*|s\.t\.:\s*|\\text\{\s*subject\sto\s*\}|\\text\{\s*subj\.to\s*\}|\\text\{\s*s\.t\.\s*\}|subject\sto\s*|subj\.to\s*|s\.t\.\s*'
   pass

def t_LLBRACE(t):
   r'\\\{'
   return t

def t_RRBRACE(t):
   r'\\\}'
   return t

def t_LBRACE(t):
   r'\{'
   return t

def t_RBRACE(t):
   r'\}'
   return t

def t_LBRACKET(t):
   r'\[|\\\['
   return t

def t_RBRACKET(t):
   r'\]|\\\]'
   return t

#t_QUESTION_MARK = r'\?'
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
t_ASINH = r'\\sinh\^\{-1\}'
t_SINH = r'\\sinh'
t_ASIN = r'\\sin\^\{-1\}|\\arcsin'
t_SIN = r'\\sin'
t_ACOSH = r'\\cosh\^\{-1\}'
t_COSH = r'\\cosh'
t_ACOS = r'\\cos\^\{-1\}|\\arccos'
t_COS = r'\\cos'
t_ARCTANH = r'\\tanh\^\{-1\}'
t_TANH = r'\\tanh'
t_TAN = r'\\tan'
t_ARCTAN = r'\\tan\^\{-1\}|\\arctan'
t_SQRT = r'\\sqrt'
t_LOG = r'\\log'
t_LN = r'\\ln'
t_EXP = r'\\exp'

def t_PIPE(t):
   r'\\mid|\\vert|\|'
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

def t_ignored_LEFT(t):
   r'\\left'
   pass

def t_ignored_RIGHT(t):
   r'\\right'
   pass

t_COMMA = r','

t_SEMICOLON = r';'

def t_COLON(t):
   r':'
   return t

def t_AMPERSAND(t):
   r'\\&'
   return t

def t_ignore_AMP(t):
   r'&'
   pass

def t_ignore_BACKSLASHES(t):
   r'\\\\'
   pass

def t_ignore_N(t):
   r'\n'
   t.lexer.lineno += 1
   pass

def t_ignore_R(t):
   r'\r'
   pass

def t_DIFF(t):
   r'\\setminus'
   return t

def t_SYMDIFF(t):
   r'\\triangle|\\ominus|\\oplus'
   return t

def t_UNION(t):
   r'\\cup|\\bigcup'
   return t

def t_INTER(t):
   r'\\cap|\\bigcap'
   return t

def t_CROSS(t):
   r'\\times'
   return t

def t_ID(t):
   r'(\\_)*[a-zA-Z]((\\_)*[a-zA-Z0-9]*)*'
   t.type = reserved.get(t.value, 'ID') # Check for reserved words
   return t

# A regular expression rule with some action code
def t_NUMBER(t):
   r'[0-9]*\.?[0-9]+([dDeE][-+]?[0-9]+)?'
   t.value = Number(t.value)
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
