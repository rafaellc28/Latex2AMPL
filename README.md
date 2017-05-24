Latex2MathProg
==============

This is an experimental tool that aims at converting a Linear Programming Model Latex Code to a <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">MathProg</a> Code (without the <b>data section</b>).

A MathProg Code can be solved using the <a href="https://www.gnu.org/software/glpk/" target="_glpk">GLPK (GNU Linear Programming Kit)</a>. Besides, the GLPK package offers commands/methods to convert a MathProg code to the following formats: <b>CPLEX LP</b>, <b>MPS fixed</b>, <b>MPS free</b> and <b>GLPK</b>.

- Use <b>\text{maximize}</b> or <b>\text{minimize}</b> to the Objective Function(s) in the <b>Objective section</b> and <b>\text{subject to}</b> to start the <b>Constraints and Declarations section</b>.
- A constraint can not end with COMMA "<b>,</b>", thus "<b>,\\\\</b>" means that the constraint continues in the next line.
- <b>Declarations</b> can be separated by SEMICOLON "<b>;</b>".
- <b>Variables</b> must be members of one of the following sets: <b>\mathbb{B}</b> or <b>\\{0,1\\}</b>, <b>\mathbb{R}</b>, <b>\mathbb{R}^{+}</b>, <b>\mathbb{Z}</b>, <b>\mathbb{Z}^{+}</b> and <b>\mathbb{N}</b>.
- A <b>Variable</b> can be defined by making it be member of one of the following sets: <b>\mathbb{V}</b>, <b>\mathbb{Var}</b>, <b>\mathbb{Vars}</b>, <b>\mathbb{Variable}</b> and <b>\mathbb{Variables}</b>.
- A <b>Parameter</b> can be defined by making it be member of one of the following sets: <b>\mathbb{P}</b>, <b>\mathbb{Param}</b>, <b>\mathbb{Params}</b> , <b>\mathbb{Parameter}</b> and <b>\mathbb{Parameters}</b>.
- A <b>Set</b> can be defined by making it be member of one of the following sets: <b>\mathbb{Set}</b> and <b>\mathbb{Sets}</b>.
- <b>Symbolic Parameters</b> must be member of <b>\mathbb{S}</b>.
- <b>Logical Parameters</b> must be member of <b>\mathbb{L}</b>.

Example o use in <a href='https://latex2mathprog.herokuapp.com' target='_blank'>https://latex2mathprog.herokuapp.com</a>


# Tokens

## Arithmetic Notation

| Math      | Latex                         | Example      |
|-----------|-------------------------------|--------------|
| addition  | <b>+</b>  | 2 <b>+</b> 3 |
| subtraction  | <b>-</b>  | 2 <b>-</b> 3 |
| less (positive difference) | <b>\text{less}</b>  | 2 <b>\text{less}</b> 3 = 0 |
| multiplication  | <b>*</b>, <b>\cdot</b> or <b>\ast</b> | 2 <b>*</b> 3 |
| division  | <b>/</b> or <b>\div</b> | 4 <b>/</b> 2 = 2 |
| exact quotient | <b>\big/</b>, <b>\text{div}</b> | 5 <b>\text{div}</b> 3 = 1 |
| remainder | <b>\text\{%}</b>, <b>\mod</b> or <b>\bmod</b> | 5 <b>\mod</b> 3 = 2 |


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


## Set Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| Natural set | <b>\mathbb{N}</b> | a \in <b>\mathbb{N}</b> |
| Integer set | <b>\mathbb{Z}</b> | a \in <b>\mathbb{Z}</b> |
| Binary set | <b>\mathbb{B}</b> or <b>\\{0,1\\}</b> | a \in <b>\mathbb{B}</b> |
| Real set | <b>\mathbb{R}</b> | a \in <b>\mathbb{R}</b> |
| Variable | <b>\mathbb{V}</b>, <b>\mathbb{Var}</b>, <b>\mathbb{Vars}</b>, <b>\mathbb{Variable}</b> or <b>\mathbb{Variables}</b> | a \in <b>\mathbb{V}</b> |
| Parameter | <b>\mathbb{P}</b>, <b>\mathbb{Param}</b>, <b>\mathbb{Params}</b>, <b>\mathbb{Parameter}</b> or <b>\mathbb{Parameters}</b> | a \in <b>\mathbb{P}</b> |
| Set | <b>\mathbb{Set}</b> or <b>\mathbb{Sets}</b> | a \in <b>\mathbb{Set}</b> |
| Symbolic Parameter | <b>\mathbb{S}</b> | a \in <b>\mathbb{S}</b> |
| Logical Parameter | <b>\mathbb{L}</b> | a \in <b>\mathbb{L}</b> |
| is member of | <b>\in</b> | a <b>\in</b> \mathbb{B} |
| is not member of | <b>\notin</b> | a <b>\notin</b> \mathbb{B} |
| is (proper) subset of | <b>\subset</b> or <b>\subseteq</b>  | A <b>\subseteq</b> B |
| union | <b>\cup</b>  | A <b>\cup</b> B |
| intersection | <b>\cap</b>  | A <b>\cap</b> B |
| Cartesian product | <b>\cross</b>  | A <b>\cross</b> B |
| difference | <b>\setminus</b>  | A <b>\setminus</b> B |
| symetric difference | <b>\triangle</b>, <b>\ominus</b> or <b>\oplus</b>  | A <b>\oplus</b> B |


## Functions

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| sqrt        | <b>\sqrt</b> | <b>\sqrt</b>{2} |
| floor       | <b>\lfloor</b> and <b>\rfloor</b> | <b>\lfloor</b> 2.567 <b>\rfloor</b> |
| ceil        | <b>\lceil</b> and <b>\rceil</b> | <b>\lceil</b> 2.567 <b>\rceil</b> |
| absolute    | <b>\mid</b>, <b>\vert</b> or <b>\|</b>| <ringb>\mid</b> -2.567 <b>\mid</b> |
| round       | <b>round</b>    | <b>round</b>(2.567) and <b>round</b>(2.567,2) |
| trunc       | <b>trunc</b>    | <b>trunc</b>(2.567) and <b>trunc</b>(2.567,2) |
| sine        | <b>\sin</b> | <b>\sin</b>(2.567) |
| cosine      | <b>\cos</b> | <b>\cos</b>(2.567) |
| arctangent  | <b>\arctan</b> | <b>\arctan</b>(a) and <b>\arctan</b>(y,x) |
| natural logarithm    | <b>\ln</b> | <b>\ln</b>(a) |
| decimal logarithm    | <b>\log</b> | <b>\log</b>(a) |
| base-e exponential   | <b>\exp</b> | <b>\exp</b>(a) |
| maximum   | <b>\max</b> | <b>\max</b>(3,6,4,7) |
| minimum   | <b>\min</b> | <b>\min</b>(3,6,5,7,18,25) |
| length of string   | <b>length</b> | <b>length</b>("string") |
| cardinality of set   | <b>card</b> | <b>card</b>(B) |
| string to calendar time | <b>str2time</b> | <b>str2time</b>("2017-02-03","%Y-%m-%d") |
| calendar time to string | <b>time2str</b> | <b>time2str</b>(gmtime(),"%Y-%m-%d") |
| substring | <b>substr</b> | <b>substr</b>(string,start) and <b>substr</b>(string,start,end) |
| seconds since 00:00:00 Jan 1, 1970 (UTC) | <b>gmtime</b>  | <b>gmtime</b>() |
| pseudo-random integer in [0,2^24) |  <b>Irand224</b>  | <b>Irand224</b>() |
| pseudo-random number in [0,1) |  <b>Uniform01</b>  | <b>Uniform01</b>() |
| pseudo-random number in [0,1) |  <b>Uniform01</b>  | <b>Uniform01</b>() |
| pseudo-random number in [a,b) |  <b>Uniform</b>  | <b>Uniform</b>(a,b) |
| Gaussian pseudo-random variable |  <b>Normal01</b>  | <b>Normal01</b>() |
| Gaussian pseudo-random variable |  <b>Normal</b>  | <b>Normal</b>(mu,sigma) |


## String Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| string    | <b>"</b> | "Hello, wold!" |
| string concatenator   | <b>\&</b> | "Hello, " <b>\&</b> "wold!" |


# Statements and Expressions

## Objective Statement

<b>\text{maximize}</b> || <b>\text{minimize}</b> LinearExpression


## Constraints/Declarations Statement

<b>\text{subject to}</b> Constraint \|\| Declaration [<b>\\\\</b> Constraint \|\| Declaration ... ]


## Constraint Statement

ConstraintExpression [ SEPARATOR IndexingExpression ], where SEPARATOR is is <b>COLON</b> or <b>\text{where}</b> or <b>\text{for}</b>, and COLON is <b>:</b>


## Declaration Statement

DeclarationExpression [ SEPARATOR IndexingExpression ], where SEPARATOR is <b>COLON</b> or <b>\text{where}</b> or <b>\text{for}</b>, and COLON is <b>:</b>


## Conditional Statement

<b>(</b> LogicalExpression <b>)</b> <b>?</b> Expression when LogicalExpression is True <b>:</b> Expression when LogicalExpression is False


## Indexing Expression

EntryIndexingExpression [, EntryIndexingExpression [, EntryIndexingExpression ... ] ] [SUCH_THAT LogicalExpression ], where SUCH_THAT is <b>|</b> or <b>\vert</b> or <b>\mid</b>


## Declaration Expression
Parameter | Set | Variable [ [SEPARATOR] DeclarationAttribute [, DeclarationAttribute ... ] ] [<b>;</b>], where SEPARATOR is <b>COLON</b> or <b>\text{where}</b> or <b>\text{for}</b>, and COLON is <b>:</b>


## Declaration Attributes

| Math      | Latex   | Example   |
|-----------|---------|-----------
| assign    | <b>:=</b> | A <b>:=</b> 1 |
| default   | <b>default</b> | A <b>\text{default}</b> 1 |
| less than | <       | a < b     |
| more than | >       | a > b     |
| less or equal than  | <b>\leq</b> | a <b>\leq</b> b |
| more or equal than  | <b>\geq</b> | a <b>\geq</b> b |
| equal to  | <b>=</b> | a <b>=</b> 1 |
| different from  | <b>\neq</b> | a <b>\neq</b> 1 |
| is member of | <b>\in</b> | a <b>\in</b> \mathbb{B} |
| is (proper) subset of | <b>\subset</b> or <b>\subseteq</b>  | A <b>\subseteq</b> B |
| dimen | <b>dimen</b>  | A <b>dimen</b> 2 |
