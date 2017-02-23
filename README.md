Latex2MathProg
==============

This is an experimental tool that aims at converting a Linear Programming Model Latex Code to a <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">MathProg</a> Code (without the <b>data section</b>).

A MathProg Code can be solved using the <a href="https://www.gnu.org/software/glpk/" target="_glpk">GLPK (GNU Linear Programming Kit)</a>. Besides, the GLPK package offers commands/methods to convert a MathProg code to the following formats: <b>CPLEX LP</b>, <b>MPS fixed</b>, <b>MPS free</b> and <b>GLPK</b>.

- Use <b>\text{maximize}<b> or <b>\text{minimize}</b> to the Objective Function(s) in the <b>Objective section</b> and <b>\text{subject to}</b> to start the <b>Constraints and Declarations section</b>.
- A constraint can not end with COMMA "<b>,</b>", thus "<b>,\\\\</b>" means that the constraint continues in the next line.
- <b>Declarations</b> can be separated by SEMICOLON "<b>;</b>".
- <b>Variables</b> must belong to one of the following sets: <b>\mathbb{B}</b> or <b>\\{0,1\\}</b>, <b>\mathbb{R}</b>, <b>\mathbb{R}^{+}</b>, <b>\mathbb{Z}</b>, <b>\mathbb{Z}^{+}</b> and <b>\mathbb{N}</b>.
- A <b>Variable</b> can be defined by making it belong to one of the following sets: <b>\mathbb{V}</b>, <b>\mathbb{Var}</b>, <b>\mathbb{Vars}</b>, <b>\mathbb{Variable}</b> and <b>\mathbb{Variables}</b>.
- A <b>Parameter</b> can be defined by making it belong to one of the following sets: <b>\mathbb{P}</b>, <b>\mathbb{Param}</b>, <b>\mathbb{Params}</b> , <b>\mathbb{Parameter}</b> and <b>\mathbb{Parameters}</b>.
- A <b>Set</b> can be defined by making it belong to one of the following sets: <b>\mathbb{Set}</b> and <b>\mathbb{Sets}</b>.
- <b>Symbolic Parameters</b> must belong to <b>\mathbb{S}</b>.
- <b>Logical Parameters</b> must belong to <b>\mathbb{L}</b>.

Example o use in <a href='https://latex2mathprog.herokuapp.com' target='_blank'>https://latex2mathprog.herokuapp.com</a>

# Tokens

## Logic Notation

| Math      | Latex                         | Example      |
|-----------|-------------------------------|--------------|
| and       | <b>\land</b>, <b>\wedge</b> or <b>\text{and}</b> | a = 1 <b>\land</b> b = 1 |
| or        | <b>\lor</b>, <b>\vee</b> or <b>\text{or}</b> | a = 1 <b>\lor</b> b = 1 |
| not       | <b>\neg</b>, <b>!</b> or <b>\text{not}</b>       | <b>\neg</b> b | 
| exists    | <b>\exists</b> | <b>\exists</b> \\{i \in I\\} z[i] |
| not exists  | <b>\nexists</b> or <b>\not\exists</b> | <b>\nexists</b> \\{i \in I\\} z[i] |
| for all    | <b>\forall</b> | <b>\forall</b> \\{u \in unit\\} u \in mPos |
| not for all  | <b>\not\forall</b> | <b>\not\forall</b> \\{u \in unit\\} u \in mPos |

## Relation Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| less than | <       | a < b     |
| more than | >       | a > b     |
| less or equal than  | <b>\leq</b> | a <b>\leq</b> b |
| more or equal than  | <b>\geq</b> | a <b>\geq</b> b |
| equal to  | =       | a = b       |
| different from      | <b>\neq</b> | a <b>\neq</b> b |
