#!/usr/bin/python -tt

import re
import logging

from SyntaxException import *
from CodeSetup import *
from CodeGenerator import *
from Identifier import *

from objects import *

class Compiler:

    def __init__(self, DEBUG = False):
        self.DEBUG = DEBUG

        # Set up a logging object
        logging.basicConfig(
            level = logging.DEBUG,
            filename = "parselog.txt",
            filemode = "w",
            format = "%(filename)10s:%(lineno)4d:%(message)s"
        )
        self.log = logging.getLogger()

    def compile(self, doc):

        res = ""
        lines = doc.split("\n")
        result = None
        parsing = True
        msg = None
        new_comma = []

        # Parser parses 'Identifier GE|LE|EQ Expression' as a Constraint, but sometimes it is part of a Declaration, like in 'Identifier GE Number, := 1 ...'.
        # This kind of Declaration causes a syntax error to be thrown. If, instead, this kind of Declaration is declared as in 
        # 'Identifier, GE Number, := 1 ...' (with a COMMA after Identifier), then no error occur. 
        # This loop tries to recover from a parser error thrown by such situation: 
        # first check whether this is the cause of the error, if so, then automatically insert a COMMA after the Identifier and rerun the parser.
        while parsing:
            parsing = False
            lexer.lineno = 1
            
            try:
                result = parser.parse(doc, debug=self.log)

            except SyntaxException as msg:
                stack = parser.symstack # stack of the parser when the error was thrown
                
                for i in range(len(stack)-1, 0, -1):
                    if (isinstance(stack[i-1], Identifier) or str(stack[i-1]) == "Identifier") and isinstance(stack[i], lex.LexToken) and stack[i].type in ['EQ', 'GE', 'LE', 'NEQ', 'GT', 'LT']:
                        pos = stack[i].lexpos
                        data = doc[:pos]
                        data += "," + doc[pos:]
                        new_comma.append(pos)

                        doc = data
                        parsing = True

                        break

                    elif stack[i].type == "EntryConstraintLogicalExpression":
                        pos = msg[1]
                        data = doc[:pos]

                        # get last match
                        match = None
                        for match in re.finditer(r"(?<![{:])\s*(=|>|<|\\neq|\\geq|\\leq|\\in|\\subseteq|\\subset)", data):
                            pass
                        
                        if match:
                            pos = match.start(0)

                            data = doc[:pos]
                            data += "," + doc[pos:]
                            new_comma.append(pos)

                            doc = data
                            parsing = True

                            break


                
                lex_token = msg[-1] # the token that caused the error
                
                if isinstance(lex_token, lex.LexToken):
                    if lex_token.type in ['EQ', 'GE', 'LE', 'NEQ', 'GT', 'LT'] and (isinstance(stack[-1], Identifier) or str(stack[-1]) == "Identifier"):
                        pos = lex_token.lexpos
                        data = doc[:pos]
                        data += "," + doc[pos:]
                        new_comma.append(pos)

                        doc = data
                        parsing = True

                    elif lex_token.type == "EntryConstraintLogicalExpression":
                        pos = msg[1]
                        data = doc[:pos]

                        # get last match
                        match = None
                        for match in re.finditer(r"(?<![{:])\s*(=|>|<|\\neq|\\geq|\\leq|\\in|\\subseteq|\\subset)", data):
                            pass
                    
                        if match:
                            pos = match.start(0)

                            data = doc[:pos]
                            data += "," + doc[pos:]
                            new_comma.append(pos)

                            doc = data
                            parsing = True


        if not result:

            if msg[0] == "EOF":
                res += "Syntax error at EOF."
            else:
                line, lineNum, pos = _getPositionToken(msg, lines, new_comma)

                res += "Syntax error at line %d, position %d: '%s'.\nContext: %s." % (msg[0], pos, msg[2], line)

        else:
            if not self.DEBUG:

                try:
                    codeGenerator = CodeGenerator()
                    result.setupEnvironment(CodeSetup(codeGenerator))
                    response = result.generateCode(codeGenerator)
                    res += response

                except CodeGenerationException as msg:
                    
                    if isinstance(msg[0], str):
                        res += msg[0]

                    else:
                        print(msg)
                        lineNum = msg[0]-1
                        linesaux = filter(lambda el: len(el) == 0 or el[0] != "%", lines)
                        line = linesaux[lineNum]
                        
                        res += "Invalid indexing expression at statement %d: '%s'. %s.\nContext: %s." % (msg[0], msg[1], msg[2], line)

                except:
                    res += "Error while generating AMPL code. Please, check your Latex code!"

            else:
                if self.DEBUG:
                    res += str(result)

                codeGenerator = CodeGenerator()
                result.setupEnvironment(CodeSetup(codeGenerator))
                response = result.generateCode(codeGenerator)
                res += response

        return res


def _getPositionToken(msg, lines, new_comma):
    lineNum = msg[0]-1
    line = lines[lineNum]

    totalCharLinesAbove = 0
    lineNum -= 1
    while lineNum >= 0:
        totalCharLinesAbove += len(lines[lineNum])+1
        lineNum -= 1
    
    # If a COMMA was inserted after an Identifier (see above), 
    # then the real position of the character that caused the error must be discounted by this COMMA
    # (the original document has not this automatically inserted COMMA)
    pos_aux = msg[1]
    less_pos = 0
    for p in new_comma:
        if pos_aux > p:
            less_pos += 1

    pos = pos_aux-less_pos-totalCharLinesAbove
    if totalCharLinesAbove > 0:
        pos += 1

    return line, lineNum, pos