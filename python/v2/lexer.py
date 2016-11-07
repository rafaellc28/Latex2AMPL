#!/usr/bin/python -tt

#import ply.lex as lex

# List of token names.   This is always required

from Number import *
import sys

reserved = {
   'card' : 'CARD',
   'length' : 'LENGTH',
   'round' : 'ROUND',
   'trunc' : 'TRUNC'
}

tokens = [
   'OR',
   'AND',
   'NOT',
   'FORALL',
   'EXISTS',
   'INTEGERSET',
   'BINARYSET',
   'REALSET',
   'REALSETPOSITIVE',
   'NATURALSET',
   'SUBSET',
   'NOTSUBSET',
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
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
   'CROSS'
] + list(reserved.values())

def t_DOTS(t):
   r'\\cdots|\\ldots|\\dots|\.\.\.'
   t.value = "DOTS"
   return t

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'

def t_TIMES(t):
   r'\*|\\cdot|\\ast'
   t.value = "*"
   return t

def t_DIVIDE(t):
   r'/|\\div'
   t.value = "/"
   return t

def t_OR(t):
   r'\|\||or'
   t.value = "or"
   return t

def t_AND(t):
   r'&&|and'
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

def t_INTEGERSET(t):
   r'\\mathbb{Z}'
   t.value = "integer"
   return t

def t_BINARYSET(t):
   r'\\mathbb{B}'
   t.value = "binary"
   return t

def t_REALSETPOSITIVE(t):
   r'\\mathbb{R}\^{\+}'
   t.value = "realpositive"
   return t

def t_REALSET(t):
   r'\\mathbb{R}'
   t.value = "real"
   return t

def t_NATURALSET(t):
   r'\\mathbb{N}'
   t.value = "natural"
   return t

def t_SUBSET(t):
   r'\\subseteq|\\subset'
   t.value = "subset"
   return t

def t_NOTSUBSET(t):
   r'\\not\\subseteq|\\not\\subset'
   t.value = "notsubset"
   return t

#t_DOT = r'\\cdot'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_MAXIMIZE(t):
   r'\\text\{maximize\}|\\text\{max\}|\\max|maximize|max|\\text\{maximize:\}|\\text\{max:\}|\\max:|maximize:|max:'
   t.value = "maximize"
   return t

def t_MINIMIZE(t):
   r'\\text\{minimize\}|\\text\{min\}|\\min|minimize|min|\\text\{minimize:\}|\\text\{min:\}|\\min:|minimize:|min:'
   t.value = "minimize"
   return t

def t_SUBJECTTO(t):
   r'\\text\{subject\sto\}|\\text\{subj\.to\}|\\text\{s\.t\.\}|subject\sto|subj\.to| s\.t\.|\\text\{subject\sto:\}|\\text\{subj\.to:\}|\\text\{s\.t\.:\}|subject\sto:|subj\.to:| s\.t\.:'
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
t_MOD = r'%'

def t_PIPE(t):
   r'\\vert|\|'
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
    r'\\text'
    pass

t_COMMA = r','

def t_COLON(t):
   r':'
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
   r'\\times|\\wedge'
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
   r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
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
