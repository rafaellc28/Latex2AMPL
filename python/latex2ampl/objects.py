import ply.lex as lex
import ply.yacc as yacc
import lexer as lexer_mod
import parser as parser_mod

lexer = lex.lex(module=lexer_mod, debug=False, optimize=True)
parser = yacc.yacc(module=parser_mod, debug=False, optimize=True)
parser.defaulted_states = {}