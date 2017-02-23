Latex2MathProg
==============

This is an experimental tool that aims at converting a Linear Programming Model Latex Code to a <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">MathProg</a> Code (without the <b>data section</b>).

A MathProg Code can be solved using the <a href="https://www.gnu.org/software/glpk/" target="_glpk">GLPK (GNU Linear Programming Kit)</a>. Besides, the GLPK package offers commands/methods to convert a MathProg code to the following formats: <b>CPLEX LP</b>, <b>MPS fixed</b>, <b>MPS free</b> and <b>GLPK</b>.

- Use <b>\text{maximize}/\text{minimize}</b> to the Objective Function(s) in the Objective section and <b>\text{subject to}</b> to start the Constraints and Declarations section.
- A constraint can not end with COMMA "<b>,</b>", thus "<b>,\\\\</b>" means that the constraint continues in the next line.
- Declarations can be separated by SEMICOLON "<b>;</b>".
- <b>Variables</b> must belong to one of the following sets: $\\mathbb{B}$ or $\\{0,1\\}$, $\\mathbb{R}$, $\\mathbb{R}^{+}$, $\\mathbb{Z}$, $\\mathbb{Z}^{+}$ and $\\mathbb{N}$.
- A <b>Variable</b> can be defined by making it belong to one of the following sets: $\\mathbb{V}$, $\\mathbb{Var}$, $\\mathbb{Vars}$, , $\\mathbb{Variable}$ and $\\mathbb{Variables}$.
- A <b>Parameter</b> can be defined by making it belong to one of the following sets: $\\mathbb{P}$, $\\mathbb{Param}$, $\\mathbb{Params}$, , $\\mathbb{Parameter}$ and $\\mathbb{Parameters}$.
- A <b>Set</b> can be defined by making it belong to one of the following sets: $\\mathbb{Set}$ and $\\mathbb{Sets}$.
- <b>Symbolic Parameters</b> must belong to $\\mathbb{S}$.
- <b>Logical Parameters</b> must belong to $\\mathbb{L}$.

Example o use in <a href='https://latex2mathprog.herokuapp.com' target='_blank'>https://latex2mathprog.herokuapp.com</a>
