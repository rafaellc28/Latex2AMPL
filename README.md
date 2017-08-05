Latex2MathProg
==============

This tool converts a Linear Programming Model written in LaTeX to a <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">MathProg</a> code.

A MathProg code describes either a Linear Program or a System of Linear Equations. It can be solved using the <a href="https://www.gnu.org/software/glpk/" target="_glpk">GLPK (GNU Linear Programming Kit)</a>. Besides, the GLPK package offers commands/methods to convert a MathProg code to the following formats: <b>CPLEX LP</b>, <b>MPS fixed</b>, <b>MPS free</b> and <b>GLPK</b>.

Check <a href='https://latex2mathprog.herokuapp.com' target='_blank'>https://latex2mathprog.herokuapp.com</a> to see <b>latex2mathprog</b> working.

Consider as an example the following LaTex code

```latex
\begin{equation}
\begin{split}
  \text{minimize} & \displaystyle\sum\limits_{i \in I,j \in J}C_{i,j} * x_{i,j}\\
  \text{subject to} & \displaystyle\sum\limits_{j \in J}x_{i,j} \leq A_{i} \text{ for } i \in I\\
  & \displaystyle\sum\limits_{i \in I}x_{i,j} \geq B_{j} \text{ for } j \in J,\\
  & x_{i,j} \in \mathbb{N}
\end{split}
\end{equation}
```

<b>latex2mathprog</b> converts it to the following MathProg code

```ampl
set I;

set J;

param A{i in I};

param C{i in I, j in J};

param B{j in J};


var x{i in I, j in J} integer >= 0;


minimize obj: sum{i in I, j in J}C[i,j] * x[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j], <= A[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j], >= B[j];


solve;


data;

set I :=;

set J :=;

param A :=;

param C :=;

param B :=;


end;
```

The Inference Mechanism is what defines if an identifier is a set, parameter or variable. This mechanism is explained in the <b>Inference Mechanism</b> section below.


> In the rest of this article, it is used terms that are not fully explained here, like Indexing Expression, Numeric Expression and others. Please, refer to <a href="https://www3.nd.edu/~jeff/mathprog/glpk-4.47/doc/gmpl.pdf" target="_mathProgTutorial">Modeling Language GNU MathProg</a> to see their meanings.


# Objectives section

A Linear Program written in LaTex code can have one or more objectives. The <b>Objectives</b> section corresponds to the first statements, where each statement must begin with `\text{maximize}` or `\text{minimize}`. The first objective statement is the main objective in a MathProg code, i.e., it is the one to be optmized, the others are secundaries.

For instance, <b>latex2mathprog</b> converts

```latex
\text{minimize} \sum_{i \in I,j \in J}C_{i,j} * x_{i,j}
```

to 

```ampl
minimize obj: sum{i in I, j in J}C[i,j] * x[i,j];
```

A more formal definition of the Objective Statement is given in <b>Statements and Expressions</b> section.


# Constraints and Declarations section

The <b>Constraints and Declarations</b> section must start with `\text{subject to}`. It must have at least one Constraint or one Declaration, up to many of both, interchangeably.

If the LaTeX code is a <b>System of Linear Equations</b>, then `\text{subject to}` must not be used, because it is used only to separate the <b>Objectives</b> section from the <b>Constraints and Declarations</b> section.

For instance, <b>latex2mathprog</b> converts

```latex
\text{subject to} \sum_{j \in J}x_{i,j} \leq A_{i}: i \in I\\
\sum_{i \in I}x_{i,j} \geq B_{j}: j \in J\\
```

to 

```ampl
s.t. C1 {i in I} :
	sum{j in J}x[i,j], <= A[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j], >= B[j];
```

## Constraints

The LaTex code below illustrates how Constraints can be expressed

```latex
\sum_{j \in J}x_{i,j} \leq A_{i}: i \in I\\
\sum_{i \in I}x_{i,j} \geq B_{j}: j \in J\\
0 \leq \sum_{j \in J}x_{i,j} \leq 100: i \in I\\
1000 \geq \sum_{i \in I}x_{i,j} \geq 0: j \in J\\
C_{i} = 1: i \in I\\
```

It is converted to

```ampl
s.t. C1 {i in I} :
	sum{j in J}x[i,j], <= A[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j], >= B[j];

s.t. C3 {i in I} :
	0, <= sum{j in J}x[i,j], <= 100;

s.t. C4 {j in J} :
	1000, >= sum{i in I}x[i,j], >= 0;

s.t. C5 {i in I} :
	C[i], = 1;
```

## Declarations

Declarations are used to define the attributes of an identifier. For instance

```latex
m, n \in \mathbb{Z}, \in \mathbb{P}, > 0; J := 1 \ldots n; M := 1 \ldots m\\
```

is converted to

```ampl
param m integer, > 0;

param n integer, > 0;

set J, := 1..n;

set M, := 1..m;
```

Note that Declarations inside a statement can be separated by `;`. Each Declaration can have its own Indexing Expression. For those declarations separated by `;` within a statement, the last Indexing Expression is used to infer the domains of identifiers that do not have its own Indexing Expression declared. For instance, consider the example below

```latex
x_{i} \in \mathbb{Z}; A_{i} \text{default} 0: i \in I
```

It is converted to

```ampl
param A{i in I}, default 0;

var x{i in I} integer;
```

Here, the Indexing Expression `i in I` is used for the identifiers `A` and `x`.

Note also the expression `\in \mathbb{P}`. It defines the identifiers `m` and `n` as parameters. When there is no such attribute (and at most cases it is indeed not necessary), <b>latex2mathprog</b> uses its Inference Mechanism to define what an identifier is: set, parameter or variable.

More formal definitions of <b>Constraint Statement</b> and <b>Declaration Statement</b> are given in <b>Statements and Expressions</b> section. The attributes that can be defined for an identifier are given in <b>Declaration Attributes</b> section.

# Variables, Parameters and Sets

A variable must be member of one of the following sets: `\mathbb{B}` or `\{0,1\}` for binary numbers, `\mathbb{R}` or `\mathbb{R}^{+}` for real numbers, `\mathbb{Z}` or `\mathbb{Z}^{+}` for integer numbers and `\mathbb{N}` for natural numbers. Additionally, a variable can be defined by making an identifier member of one of the following sets: `\mathbb{V}`, `\mathbb{Var}`, `\mathbb{Vars}`, `\mathbb{Variable}` or `\mathbb{Variables}`. Ex.: `x \in \mathbb{V}`.

A parameter can be defined by making an identifier member of one of the following sets: `\mathbb{P}`, `\mathbb{Param}`, `\mathbb{Params}`, `\mathbb{Parameter}` and `\mathbb{Parameters}`. Ex.: `D \in \mathbb{P}`. At most cases, the Inference Mechanism is capable of defining correctly that an identifier is a parameter. This explicit definition is useful when defining that a parameter is an integer, natural or real number, like in `P \in \mathbb{Z}`. In this example, the rules in previous paragraph are applied and `P` is considered a variable, unless explicitly stated that it is a parameter, for instance `P \in \mathbb{Z}, P \in \mathbb{Param}`.
 
A set can be defined by making an identifier member of one of the following sets: `\mathbb{Set}` and `\mathbb{Sets}`. Ex.: `A \in \mathbb{Set}`. At most cases, the Inference Mechanism is capable of defining correctly that an identifier is a set.


A Symbolic Parameter is used for parameters that are Symbolic Expressions. For instance, strings. It must be member of `\mathbb{S}`. Ex.: `sym \in \mathbb{S}`.

Below, an example of a symbolic parameter.

```latex
sym \in \mathbb{S}, := "test"
```

It is converted to

```ampl
param sym symbolic, := "test";
```

A Logical Parameter is used for parameters that are Logical Expressions. It must be member of `\mathbb{L}`. Ex.: `logic \in \mathbb{L}`. 

Logical parameters are useful to use in conditional expressions. For instance, 

```latex
L \in \mathbb{S}\\
P := (L)? 1 : 0\\
```

is converted to

```ampl
param L logical;
param P := if L then 1 else 0;
```

If `L` was not of the type `param logical`, the second line in the MathProg code above would result in an error thrown by a MathProg solver.


# Notation

> Any lexer inside a `\text{ }` can have several whitespaces between the braces, to the left or to the right of the word. For instance, `\text{default}` can also be `\text{ default }`, `\text{ default}`, `\text{default }`, and so on.

## Arithmetic Notation

| Math      | Latex                         | Example      |
|-----------|-------------------------------|--------------|
| addition  | `+`  | `2 + 3` |
| subtraction  | `-`  | `2 - 3` |
| less (positive difference) | `\text{less}`  | `2 \text{less} 3 = 0` |
| multiplication  | `*`, `\cdot` or `\ast` | `2 * 3` |
| division  | `/` or `\div` | `4/2 = 2` |
| exact quotient | `\big/`, `\text{div}` | `5 \text{div} 3 = 1` |
| remainder | `\text\{%}`, `\mod` or `\bmod` | `5 \mod 3 = 2` |


## Logic Notation

| Math      | Latex                         | Example      |
|-----------|-------------------------------|--------------|
| and       | `\land`, `\wedge` or `\text{and}` | `a = 1 \land b = 1` |
| or        | `\lor`, `\vee` or `\text{or}` | `a = 1 \lor b = 1` |
| not       | `\neg`, `!` or `\text{not}`       | `\neg b` | 
| exists    | `\exists` | `\exists \{i \in I\} z[i]` |
| not exists  | `\nexists` or `\not\exists` | `\nexists \{i \in I\} z[i]` |
| for all    | `\forall` | `\forall \{u \in unit\} u \in mPos` |
| not for all  | `\not\forall` | `\not\forall \{u \in unit\} u \in mPos` |


## Relation Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| less than | `<`     | `a < b`   |
| more than | `>`     | `a > b`   |
| less or equal than  | `\leq` | `a \leq b` |
| more or equal than  | `\geq` | `a \geq b` |
| equal to  | `=`     | `a = b`       |
| different from      | `\neq` | `a \neq b` |


## Set Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| Natural set | `\mathbb{N}` | `a \in \mathbb{N}` |
| Integer set | `\mathbb{Z}` | `a \in \mathbb{Z}` |
| Binary set | `\mathbb{B}` or `\{0,1\}` | `a \in \mathbb{B}` |
| Real set | `\mathbb{R}` | `a \in \mathbb{R}` |
| Variable | `\mathbb{V}`, `\mathbb{Var}`, `\mathbb{Vars}`, `\mathbb{Variable}` or `\mathbb{Variables}` | `a \in \mathbb{V}` |
| Parameter | `\mathbb{P}`, `\mathbb{Param}`, `\mathbb{Params}`, `\mathbb{Parameter}` or `\mathbb{Parameters}` | `a \in \mathbb{P}` |
| Set | `\mathbb{Set}` or `\mathbb{Sets}` | `a \in \mathbb{Set}` |
| Symbolic Parameter | `\mathbb{S}` | `a \in \mathbb{S}` |
| Logical Parameter | `\mathbb{L}` | `a \in \mathbb{L}` |
| is member of | `\in` | `a \in \mathbb{B}` |
| is not member of | `\notin` | `a \notin \mathbb{B}` |
| is (proper) subset of | `\subset` or `\subseteq` | `A \subseteq B` |
| union | `\cup`  | `A \cup B` |
| intersection | `\cap`  | `A \cap B` |
| Cartesian product | `\cross`  | `A \cross B` |
| difference | `\setminus`  | `A \setminus B` |
| symetric difference | `\triangle`, `\ominus` or `\oplus`  | `A \oplus B` |


## Functions

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| sqrt        | `\sqrt` | `\sqrt</b>{2}` |
| floor       | `\lfloor` and `\rfloor` | `\lfloor 2.567 \rfloor` |
| ceil        | `\lceil` and `\rceil` | `\lceil 2.567 \rceil` |
| absolute    | `\mid`, `\vert` or `\|` | `\mid -2.567 \mid` |
| round       | `round`    | `round(2.567)` and `round(2.567,2)` |
| trunc       | `trunc`    | `trunc(2.567)` and `trunc(2.567,2)` |
| sine        | `\sin` | `\sin(2.567)` |
| cosine      | `\cos` | `\cos(2.567)` |
| arctangent  | `\arctan` | `\arctan(a)` and `\arctan(y,x)` |
| natural logarithm    | `\ln` | `\ln(a)` |
| decimal logarithm    | `\log` | `\log(a)` |
| base-e exponential   | `\exp` | `\exp(a)` |
| maximum   | `\max` | `\max(3,6,4,7)` |
| minimum   | `\min` | `\min(3,6,5,7,18,25)` |
| length of string   | `length` | `length("string")` |
| cardinality of set   | `card` | `card(B)` |
| string to calendar time | `str2time` | `str2time("2017-02-03","%Y-%m-%d")` |
| calendar time to string | `time2str` | `time2str(gmtime(),"%Y-%m-%d")` |
| substring | `substr` | `substr(string,start)` and `substr(string,start,end)` |
| seconds since 00:00:00 Jan 1, 1970 (UTC) | `gmtime`  | `gmtime()` |
| pseudo-random integer in [0,2^24) |  `Irand224`  | `Irand224()` |
| pseudo-random number in [0,1) |  `Uniform01`  | `Uniform01()` |
| pseudo-random number in [a,b) |  `Uniform`  | `Uniform(a,b)` |
| Gaussian pseudo-random variable with mean 0 and deviation 1 |  `Normal01`  | `Normal01</b>` |
| Gaussian pseudo-random variable with mean mu and deviation sigma |  `Normal`  | `Normal(mu,sigma)` |


## String Notation

| Math      | Latex   | Example   |
|-----------|---------|-----------|
| string    | `""` | `"Hello, wold!"` |
| string concatenator   | `\&` | `"Hello, " \& "wold!"` |


## Range Notation

Consider that

`DOTS` is `\cdots` or `\ldots` or `\dots` or `...`

`BOUND` is \<NumericExpression\> or \<Identifier\>


Then a range is expressed as 

`BOUND DOTS BOUND` [`\text{by}` `BOUND`]

For instance, the folowing LaTex code

```latex
A_{i} \in \mathbb{R}^{+}, \in \mathbb{P}: i \in 1 \cdots N \text{ by } 2
```

is converted to

```ampl
param N;
param A{i in 1..N by 2} >= 0;
```


## Tuple Notation

A tuple is expressed as

`(`\<Indice1\>`, `\<Indice2\>[`,` ...]`)`

For instance, the folowing LaTex code

```latex
x_{i,j} \in \mathbb{R}: (i,j) \in E
```

is converted to

```ampl
set E dimen 2;
var x{(i,j) in E};
```


## Comments

`%` is the line comment delimiter. However, `%` has no effect as a comment delimiter when inside a string, like in `"%"`, or inside a `\text`, like in `\text{%}`.


## Ignored Lexers

The following LaTeX environments and lexers can be used to format the Linear Programming Model. They are ignored by the compiler.

| | | | |
|---------|--------|--------|-----------|
| `\begin{array}`  | `\end{array}` | `\begin{equation}` | `\end{equation}` |
| `\begin{split}` | `\end{split}` | `\displaystyle` | `\quad` |
| `\limits` | `\mathclap` | `\text{ }` | `&` |
| `\n` | `\t` | `\r` | `\\` |


# Statements and Expressions

For the statements and expressions below, we have that

`SEPARATOR` is `:` or `\text{where}` or `\text{for}`;

`SUCH_THAT` is `|` or `\vert` or `\mid`.

\<Expression\> is \<NumericExpression\> or \<LinearExpression\>.


## Objective Statement

`\text{maximize}` \<LinearExpression\> [`SEPARATOR` \<IndexingExpression\> ]

or

`\text{minimize}` \<LinearExpression\> [`SEPARATOR` \<IndexingExpression\> ]

A Linear Program can have more than one objective.


## Constraints and Declarations Statements

`\text{subject to}` \<Constraint \|\| Declaration\> [\<Constraint \|\| Declaration\> ... ]


## Constraint Statement

\<ConstraintExpression\> [`SEPARATOR` \<IndexingExpression\> ]


## Declaration Statement

\<DeclarationExpression\> [`SEPARATOR` \<IndexingExpression\> ] [`;` Declaration]


## Conditional Statement

`(` \<LogicalExpression\> `)?` \<Expression when LogicalExpression is True\> `:` \<Expression when LogicalExpression is False\>


## Constraint Expression

\<NumericExpression\> `\leq` \<LinearExpression\> `\leq` \<NumericExpression\>

or

\<NumericExpression\> `\qeq` \<LinearExpression\> `\qeq` \<NumericExpression\>

or

\<LinearExpression\> `\leq` \<Expression\>

or

\<LinearExpression\> `\qeq` \<Expression\>

or

\<LinearExpression\> `=` \<Expression\>.


## Indexing Expression

\<EntryIndexingExpression\> [`,` \<EntryIndexingExpression\> ...] [`SUCH_THAT` LogicalExpression ]


## Logical Expression

\<EntryLogicalExpression\> [`,` \<EntryLogicalExpression\> ...]


## Declaration Expression
\<Identifier\> [[`,`] \<DeclarationAttribute\> [`,` \<DeclarationAttribute\> ... ]]


## Declaration Attributes

| Math      | Latex   | Example   |
|-----------|---------|-----------
| assign    | `:=` | `A := 1` |
| default   | `\text{default}` | `A \text{default} 1` |
| less than | `<`       | `a < b`     |
| more than | `>`       | `a > b`     |
| less or equal than  | `\leq` | `a \leq b` |
| more or equal than  | `\geq` | `a \geq b` |
| equal to  | `=` | `a = 1` |
| different from  | `\neq` | `a \neq 1` |
| is member of | `\in` | `a \in \mathbb{B}` |
| is (proper) subset of | `\subset` or `\subseteq`  | `A \subseteq B` |
| dimen | `dimen`  | `A dimen 2` |


### Note

\<Identifier\> `\leq` \<Expression\>

or 

\<Identifier\> `\geq` \<Expression\>

are considered constraints. If you want these to be declarations, they must be written as 

\<Identifier\>`, \leq` \<Expression\>

or

\<Identifier\>`, \geq` \<Expression\>.


# Inference Mechanism

Inference Mechanism is the mechanism used to infer types (variable, parameter or set) and domains of identifiers. Types and domains are inferred in different ways. 

When inferring domains, Declaration statements have higher priority and are examined first. After looking in the Declarations of an identifier, if the mechanism has not yet inferred the identifier's domain, then it basically scan the LaTex code from bottom to top statements, right to left, aiming at inferring the domain based on the last identifier's position where it is possible to extract this information.

Attributes of an identifier are accumulated through the Declarations that define it.


## Inference Rules for Types

### Variables, Parameters and Sets

The explicit declaration of an identifier as variable, parameter or set has higher priority. The last declaration associated to an identifier is considered the corret. Explicit declarations use the "is A" token `\in` to associate an identifier to its type:

- Variables: `id \in \mathbb{V}`, `id \in \mathbb{Var}`, `id \in \mathbb{Vars}`, `id \in \mathbb{Variable}`, `id \in \mathbb{Variables}`
 
- Parameters: `id \in \mathbb{P}`, `id \in \mathbb{Param}`, `id \in \mathbb{Params}`, `id \in \mathbb{Parameter}`, `id \in \mathbb{Parameters}`
 
- Sets: `id \in \mathbb{Set}`, `id \in \mathbb{Sets}`

The inference of the type of an identifier (Variable, Parameter or Set) is done as follow:

- Variables: identifier `id` is defined as a variable when it belongs to the set of real, integer or binary numbers. Ex.: `id \in \mathbb{R}`, `id \in \mathbb{Z}`, `id \in \mathbb{B}` or `id \in \{0,1\}`.

- Sets: identifier `id` is inferred as a set when it is in an expression of the form `id1 \in id`, or when it is in an expression of the form `id1 \in \{P,id\}`.

- Parameters: identifier `id` is inferred as a parameter when it is not inferred neither as a variable nor as a set, and also it is not an index. Furthermore, if an identifier `id` is defined as symbolic `id \in \mathbb{S}` or logical `id \in \mathbb{L}`, then it is as a parameter, because only a parameter can be symbolic or logical. When `id` is in an expression of the form `i \in 1 \dots id`, then `id` must be a parameter, even if there are other expressions where `id` would be considered a set, like `id1 \in id` or `id1 \in \{P,id\}`.

### Some minor flaws (to be corrected)

There is a minor flaw in the inference mechanism that makes it define a set as a parameter. It occurs in Declaration statements when a set is defined with another set as its default or initial value, but the mechanism does not know yet that the default or assigned value is a set. For instance, consider the following LaTex code.

```latex
SAFE := PETS\\
PETS := DOGS \cup CATS \cup FISH\\
```

It is converted to

```ampl
set FISH;
set CATS;
set DOGS;
set PETS, := DOGS union CATS union FISH;

param SAFE, := PETS;
```

Here, `SAFE` is declared as a parameter, even though the set `PETS` is assigned to it. Certainly, `SAFE` must also be a set. It occurs because the inference is done in a single pass, in the AST (Abstract Syntax Tree), that implements the rules above. When the identifier `SAFE` is processed, `PETS` was not defined yet, so the inference mechanism does not know that `PETS` is a set. It can be corrected by changing the order of the statements in the LaTex code above.

Another solution is explicitly defines `SAFE` as a set. For instance,

```latex
SAFE := PETS, \in \mathbb{Set}\\
PETS := DOGS \cup CATS \cup FISH\\
```

is converted to

```ampl
set CATS;
set DOGS;
set PETS, := DOGS union CATS union FISH;
set SAFE, := PETS;
```

> Tip: use the explicit definition for a type, like in `P \in \mathbb{Set}`, to solve this kind of problem. Also, two good practices are: put Declarations after Constraints; declare dependencies before the identifier that depends on them. For instance,

```latex
PETS := DOGS \cup CATS \cup FISH\\
SAFE := PETS\\
```

is converted correctly to

```ampl
set CATS;
set DOGS;
set PETS, := DOGS union CATS union FISH;
set SAFE, := PETS;
```


## Inference Rules for Domains

### Scopes

The inference mechanism considers each statement as a different scope. There is no global scope. Each statement has a root scope that contains its Indexing Expression (when an Indexing Expression is declared). Besides, other expressions that create scopes inside a statement are: Iterated Expressions (`\sum`, `\prod`, `\max` and `\min`), expressions between parenthesis, `\forall` and `\exists`, both blocks of a conditional ternary expression `(condition)? block1:block2` (each block creates one scope). Each scope (except the root scope) points to a parent scope that contains it. 

The root scope has higher priority. If the identifier is not resolved in the root scope of a statement, then the search is continued from each leaf scope (scopes that do not have another scope pointing to it) up to the root scope, from the last leaf scope inside a statement until the first one. It is necessary to walk from leaf to root scope because some indices can be defined in diferent scopes through the path. For instance, consider the following constraint written in LaTex

```latex
\sum_{j \in J}x_{i,j} \leq B_{i}: i \in I, j \in J1\\
x_{i,j} \in \mathbb{R}
```

It is converted to

```ampl
set I;
set J;
set J1;

param B{i in I};

var x{i in I, j in J};

s.t. C1 {i in I, j in J1} :
	sum{j in J}x[i,j], <= B[i];
```

Note that the index `j` is defined in the scope created by the `\sum_{j \in J}` expression (whose parent is the root scope), and index `i` is defined in the root scope, where the Indexing Expression `i \in I, j \in J1` is present. The mechanism is capable of finding the sets associated to `i` and `j` because the scan is done from the leaf up to the root scope.

Note also that, in the above code, the identifier `x` is not resolved in the root scope (higher priority) because it is not declared there. In this example, the root scope contains the identifiers `j`, `J1`, `B`, `i` and `I`.

If `x` were resolved in the root scope, then its domain would be `{i in I, j in J1}`. For instance,

```latex
\sum_{j \in J}x_{i,j} \leq B_{i}: i \in I, j \in J1, x_{i,j} \in \mathbb{R}
```

is converted to

```ampl
set I;
set J;
set J1;

param B{i in I};

var x{i in I, j in J1};

s.t. C1 {i in I, j in J1} :
	sum{j in J}x[i,j], <= B[i];
```

Here, the root scope contains the identifiers `x`, `j`, `J1`, `B`, `i` and `I`.

> It is important to state that <b>latex2mathprog</b> does not do semantic analysis. A MathProg solver will throw an error to the above code because the definition of index `j` is duplicated inside the constraint `C1`.


### Domains 

In order to infer the domain of an identifier `id`, the mechanism looks if `id` is present in an expression of the type `id \in A`, if so then it is defined that the domain of `id` is `A`.

The inference of indices's domains follows basically the same logic. However, the mechanism first search for tuples that correspond to some sub-sequence of the indices. For instance, for the identifier `id[p,a,aloc,b,bloc]`, the mechanism looks for tuples of the kind: `(p,a,aloc,b,blob) \in T`, `(p,a,aloc,b) \in T`, `(p,a,aloc) \in T`, ..., `(a,aloc,b,blob) \in T`, `(a,aloc,b) \in T`, `(a,aloc) \in T`, and so on. It is important that a tuple corresponds to a sub-sequence of the indices in order to be used in the domain of an identifier, because it can only be used like in `id{p in P, (a,aloc) in T1, (b,bloc) in T2}`.
