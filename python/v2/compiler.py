#!/usr/bin/python -tt

import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys
import re

from SyntaxException import *
from CodeSetup import *
from CodeGenerator import *

DEBUG = False

lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=parser)
parser.defaulted_states = {}

for arg in sys.argv:
	if arg == "-d":
		DEBUG = True

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

doc = re.sub(',\s*\\\\\\\\', ', ', doc)

lines = doc.split("\n")

try:
	result = parser.parse(doc, debug=log)
except SyntaxException, msg:
	lineNum = msg[0]-1
	line = lines[lineNum]

	totalCharLinesAbove = 0
	lineNum -= 1
	while lineNum >= 0:
		totalCharLinesAbove += len(lines[lineNum])+1
		lineNum -= 1

	print("Syntax error at line %d, position %d: '%s'.\nContext: %s." % (msg[0], msg[1]-totalCharLinesAbove+1, msg[2], line))
	exit()


if DEBUG:
	sys.stderr.write(str(result) + "\n")

if result:
	if not DEBUG:
		try:
			codeGenerator = CodeGenerator()
			result.setupEnvironment(CodeSetup(codeGenerator))
			response = result.generateCode(codeGenerator)
			print(response)
		except CodeGenerationException, msg:
			print(msg)
		except:
			print("Error while generating MathProg code. Please, check your Latex code!")
	else:
		codeGenerator = CodeGenerator()
		result.setupEnvironment(CodeSetup(codeGenerator))
		response = result.generateCode(codeGenerator)
		print(response)
