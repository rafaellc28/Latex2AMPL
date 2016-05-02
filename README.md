Latex2MathProg
==============

This is an experimental tool that aims at converting a Linear Programming Model Latex Code to a <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">MathProg</a> Code (without the <b>data section</b>). It is still being developed and needs more tests.

A MathProg Code can be solved using the <a href="https://www.gnu.org/software/glpk/" target="_glpk">GLPK (GNU Linear Programming Kit)</a> tool.

- The Linear Programming Model must be inside the <i>equation > split environments</i>
- Use <b>\text{maximize}/\text{minimize}</b> to the Objective Function and <b>\text{subject to}</b> to start the Constraints
- The last constraint can not end with BACKSLASHES "<b>\\\\</b>"
- A constraint can not end with COMMA "<b>,</b>", thus "<b>,\\\\</b>" means that the constraint continues in the next line
- Parameters must start with an upper case letter

Example o use in <a href='https://latex2mathprog.herokuapp.com' target='_blank'>https://latex2mathprog.herokuapp.com</a>
