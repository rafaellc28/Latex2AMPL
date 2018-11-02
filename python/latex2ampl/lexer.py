#!/usr/bin/python -tt

# List of token names.   This is always required

from Number import *
from String import *

from IntegerSet import *
from RealSet import *
from SymbolicSet import *
from LogicalSet import *
from OrderedSet import *
from CircularSet import *
from BinarySet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *

import sys
import re
from SyntaxException import *

reserved = {
}

tokens = [
   'CARD',
   'LENGTH',
   'ROUND',
   'PRECISION',
   'TRUNC',
   'SUBSTR',
   'IRAND224',
   'UNIFORM01',
   'NORMAL01',
   'UNIFORM',
   'NORMAL',
   'BETA',
   'CAUCHY',
   'EXPONENTIAL',
   'GAMMA',
   'POISSON',
   'ALIAS',
   'CTIME',
   'TIME',
   'NUM',
   'NUM0',
   'ICHAR',
   'CHAR',
   'SPRINTF',
   'MATCH',
   'SUB',
   'GSUB',
   'OR',
   'AND',
   'NOT',
   'FORALL',
   'NFORALL',
   'EXISTS',
   'NEXISTS',
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
   'COUNT',
   'ATMOST',
   'ATLEAST',
   'EXACTLY',
   'NUMBEROF',
   'ALLDIFF',
   'DIMEN',
   'SUBSET',
   'NOTSUBSET',
   'NUMBER',
   'SYMBOLIC',
   'LOGICAL',
   'ORDERED',
   'CIRCULAR',
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
   'ATAN',
   'ATANH',
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
   'ELSE',
   'IMPLIES',
   'ISIMPLIEDBY',
   'IFANDONLYIF',
   'NODE',
   'NETIN',
   'NETOUT',
   'ARC',
   'FROM',
   'TO',
   'OBJ'
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

# Define a rule so we can track line numbers
def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r'

def t_CARD(t):
   r'\\text\{\s*card\s*\}|\s*card(?!\\_|[a-zA-Z0-9])'
   return t

def t_LENGTH(t):
   r'\\text\{\s*length\s*\}|\s*length(?!\\_|[a-zA-Z0-9])'
   return t

def t_ROUND(t):
   r'\\text\{\s*round\s*\}|\s*round(?!\\_|[a-zA-Z0-9])'
   return t

def t_PRECISION(t):
   r'\\text\{\s*precision\s*\}|\s*precision(?!\\_|[a-zA-Z0-9])'
   return t

def t_TRUNC(t):
   r'\\text\{\s*trunc\s*\}|\s*trunc(?!\\_|[a-zA-Z0-9])'
   return t

def t_SUBSTR(t):
   r'\\text\{\s*substr\s*\}|\s*substr(?!\\_|[a-zA-Z0-9])'
   return t

def t_IRAND224(t):
   r'\\text\{\s*Irand224\s*\}|\s*Irand224(?!\\_|[a-zA-Z0-9])'
   return t

def t_UNIFORM01(t):
   r'\\text\{\s*Uniform01\s*\}|\s*Uniform01(?!\\_|[a-zA-Z0-9])'
   return t

def t_NORMAL01(t):
   r'\\text\{\s*Normal01\s*\}|\s*Normal01(?!\\_|[a-zA-Z0-9])'
   return t

def t_UNIFORM(t):
   r'\\text\{\s*Uniform\s*\}|\s*Uniform(?!\\_|[a-zA-Z0-9])'
   return t

def t_NORMAL(t):
   r'\\text\{\s*Normal\s*\}|\s*Normal(?!\\_|[a-zA-Z0-9])'
   return t

def t_BETA(t):
   r'\\text\{\s*Beta\s*\}|\s*Beta(?!\\_|[a-zA-Z0-9])'
   return t

def t_CAUCHY(t):
   r'\\text\{\s*Cauchy\s*\}|\s*Cauchy(?!\\_|[a-zA-Z0-9])'
   return t

def t_EXPONENTIAL(t):
   r'\\text\{\s*Exponential\s*\}|\s*Exponential(?!\\_|[a-zA-Z0-9])'
   return t

def t_GAMMA(t):
   r'\\text\{\s*Gamma\s*\}|\s*Gamma(?!\\_|[a-zA-Z0-9])'
   return t

def t_POISSON(t):
   r'\\text\{\s*Poisson\s*\}|\s*Poisson(?!\\_|[a-zA-Z0-9])'
   return t

def t_ALIAS(t):
   r'\\text\{\s*alias\s*\}|\s*alias(?!\\_|[a-zA-Z0-9])'
   return t

def t_NODE(t):
   r'\\text\{\s*node\s*\}|\s*node(?!\\_|[a-zA-Z0-9])'
   return t

def t_NETIN(t):
   r'\\text\{\s*net_in\s*\}|\s*net\\_in(?!\\_|[a-zA-Z0-9])'
   return t

def t_NETOUT(t):
   r'\\text\{\s*net_out\s*\}|\s*net\\_out(?!\\_|[a-zA-Z0-9])'
   return t

def t_ARC(t):
   r'\\text\{\s*arc\s*\}|\s*arc(?!\\_|[a-zA-Z0-9])'
   return t

def t_FROM(t):
   r'\\text\{\s*from\s*\}|\s*from(?!\\_|[a-zA-Z0-9])'
   return t

def t_TO(t):
   r'\\text\{\s*to\s*\}|\s*to(?!\\_|[a-zA-Z0-9])'
   return t

def t_OBJ(t):
   r'\\text\{\s*obj\s*\}|\s*obj(?!\\_|[a-zA-Z0-9])'
   return t


def t_CTIME(t):
   r'\\text\{\s*ctime\s*\}|\s*ctime(?!\\_|[a-zA-Z0-9])'
   return t

def t_TIME(t):
   r'\\text\{\s*time\s*\}|\s*time(?!\\_|[a-zA-Z0-9])'
   return t

def t_NUM0(t):
   r'\\text\{\s*num0\s*\}|\s*num0(?!\\_|[a-zA-Z0-9])'
   return t

def t_NUM(t):
   r'\\text\{\s*num\s*\}|\s*num(?!\\_|[a-zA-Z0-9])'
   return t

def t_ICHAR(t):
   r'\\text\{\s*ichar\s*\}|\s*ichar(?!\\_|[a-zA-Z0-9])'
   return t

def t_CHAR(t):
   r'\\text\{\s*char\s*\}|\s*char(?!\\_|[a-zA-Z0-9])'
   return t

def t_SPRINTF(t):
   r'\\text\{\s*sprintf\s*\}|\s*sprintf(?!\\_|[a-zA-Z0-9])'
   return t

def t_MATCH(t):
   r'\\text\{\s*match\s*\}|\s*match(?!\\_|[a-zA-Z0-9])'
   return t

def t_GSUB(t):
   r'\\text\{\s*gsub\s*\}|\s*gsub(?!\\_|[a-zA-Z0-9])'
   return t

def t_SUB(t):
   r'\\text\{\s*sub\s*\}|\s*sub(?!\\_|[a-zA-Z0-9])'
   return t

def t_IF(t):
   r'\\text\{\s*if\s*\}|\s*if(?!\\_|[a-zA-Z0-9])'
   return t

def t_THEN(t):
   r'\\text\{\s*then\s*\}|\s*then(?!\\_|[a-zA-Z0-9])'
   return t

def t_ELSE(t):
   r'\\text\{\s*else\s*\}|\s*else(?!\\_|[a-zA-Z0-9])'
   return t

def t_IMPLIES(t):
   r'\\implies|\\Rightarrow|\\Longrightarrow'
   return t

def t_ISIMPLIEDBY(t):
   r'\\Leftarrow|\\Longleftarrow|\\impliedby'
   return t

def t_IFANDONLYIF(t):
   r'\\iff|\\Leftrightarrow'
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
   r'\\text\{\s*by\s*\}|\s*by(?!\\_|[a-zA-Z0-9])'
   return t

def t_QUOTIENT(t):
   r'\\big/|\\text\{\s*div\s*\}|\s*div(?!\\_|[a-zA-Z0-9])'
   return t

def t_TIMES(t):
   r'\*|\\cdot|\\ast'
   return t

def t_DIVIDE(t):
   r'/|\\div'
   return t

def t_LESS(t):
   r'\\text\{\s*less\s*\}|\s*less(?!\\_|[a-zA-Z0-9])'
   return t

def t_FOR(t):
   r'\\text\{\s*for\s*\}|\s*for(?!\\_|[a-zA-Z0-9])'
   return t

def t_WHERE(t):
   r'\\text\{\s*where\s*\}|\s*where(?!\\_|[a-zA-Z0-9])'
   return t

def t_OR(t):
   r'\\lor|\\vee|\\text\{\s*or\s*\}|\s*or(?!\\_|[a-zA-Z0-9])'
   return t

def t_AND(t):
   r'\\land|\\wedge|\\text\{\s*and\s*\}|\s*and(?!\\_|[a-zA-Z0-9])'
   return t

def t_NOT(t):
   r'\\neg|!|\\text\{\s*not\s*}|\s*not(?!\\_|[a-zA-Z0-9])'
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
   r'\\text\{\s*default\s*\}|\s*default(?!\\_|[a-zA-Z0-9])'
   return t

def t_DIMEN(t):
   r'\\text\{\s*dimen\s*\}|\s*dimen(?!\\_|[a-zA-Z0-9])'
   return t

def t_SETOF(t):
   r'\\text\{\s*setof\s*\}|\s*setof(?!\\_|[a-zA-Z0-9])'
   return t

def t_COUNT(t):
   r'\\text\{\s*count\s*\}|\s*count(?!\\_|[a-zA-Z0-9])'
   return t

def t_ATMOST(t):
   r'\\text\{\s*atmost\s*\}|\s*atmost(?!\\_|[a-zA-Z0-9])'
   return t

def t_ATLEAST(t):
   r'\\text\{\s*atleast\s*\}|\s*atleast(?!\\_|[a-zA-Z0-9])'
   return t

def t_EXACTLY(t):
   r'\\text\{\s*exactly\s*\}|\s*exactly(?!\\_|[a-zA-Z0-9])'
   return t

def t_NUMBEROF(t):
   r'\\text\{\s*numberof\s*\}|\s*numberof(?!\\_|[a-zA-Z0-9])'
   return t

def t_ALLDIFF(t):
   r'\\text\{\s*alldiff\s*\}|\s*alldiff(?!\\_|[a-zA-Z0-9])'
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

def t_ORDERED(t):
   r'\\mathbb{O}'
   t.value2 = OrderedSet()
   return t

def t_CIRCULAR(t):
   r'\\mathbb{C}'
   t.value2 = CircularSet()
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
   r'\\text\{\s*maximize\s*:\s*\}|\s*maximize\s*:|\\text\{\s*maximize\s*\}|\s*maximize(?!\\_|[a-zA-Z0-9])'
   return t

def t_MINIMIZE(t):
   r'\\text\{\s*minimize\s*:\s*\}|\s*minimize\s*:|\\text\{\s*minimize\s*\}|\s*minimize(?!\\_|[a-zA-Z0-9])'
   return t

def t_ignore_SUBJECTTO(t):
   r'\\text\{\s*subject\s+to\s*:\s*\}|\\text\{\s*subj\s*\.\s*to\s*:\s*\}|\\text\{\s*s\s*\.\s*t\s*\.\s*:\s*\}|\s*subject\s+to\s*:|\s*subj\s*\.\s*to\s*:|\s*s\s*\.\s*t\s*\.\s*:|\\text\{\s*subject\s+to\s*\}|\\text\{\s*subj\s*\.\s*to\s*\}|\\text\{\s*s\s*\.\s*t\s*\.\s*\}|\s*subject\s+to(?!\\_|[a-zA-Z0-9])|\s*subj\s*\.\s*to(?!\\_|[a-zA-Z0-9])|\s*s\s*\.\s*t\s*\.'
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
t_ATANH = r'\\tanh\^\{-1\}'
t_TANH = r'\\tanh'
t_TAN = r'\\tan'
t_ATAN = r'\\tan\^\{-1\}|\\arctan'
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
   r'\\text\{\s*(\\_)*[a-zA-Z]((\\_)*[a-zA-Z0-9]*)*\s*\}|(\\_)*[a-zA-Z]((\\_)*[a-zA-Z0-9]*)*'
   t.type = reserved.get(t.value, 'ID') # Check for reserved words

   m = re.search(r"\\text\{\s*(.+)\s*\}", t.value)

   if m:
      t.value = m.groups(0)[0]

   return t

# A regular expression rule with some action code
def t_NUMBER(t):
   r'[0-9]*\.?[0-9]+([dDeE][-+]?[0-9]+)?'
   t.value = Number(t.value)
   return t

def t_ignore_TEXT(t):
    r'\\text\{.*\}|\\text'
    pass

# Error handling rule
def t_error(t):
   sys.stderr.write( "Illegal character '%s'" % t.value[0] )
   t.lexer.skip(1)
