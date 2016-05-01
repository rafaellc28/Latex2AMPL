#!/usr/bin/python -tt

import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys

lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=parser)

doc = sys.stdin.read()

# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

result = parser.parse(doc, debug=log)

response = result.generateCode()

print(response)
