#!/usr/bin/python -tt

import sys

# Abstract Syntax Tree (AST) for Latex (Mixed) Linear Progamming formulation (MLP)

Sets = {}
Vars = {}
Params = {}
Indices = {}
Types = {}
Tuples = {}

constraintNumber = 0;
SetsNumber = 0;
VarsNumber = 0;
ParamsNumber = 0;

class LinearProgram:
    """
    Class representing the root node in the AST of a MLP
    """

    @staticmethod
    def _getVarDomain(varDomain):
        """
        Generate the MathProg code for the declaration of the domain of a variable
        """
        global Indices

        if varDomain["var"] in Indices:
            if ".." in Indices[varDomain["var"]]:
                return Indices[varDomain["var"]]
            else:
                return varDomain["var"] + " in " + Indices[varDomain["var"]]
        elif varDomain["min"] < float('inf'):
            return str(varDomain["min"]) + ".." + str(varDomain["max"])
        else:
            return ""

    @staticmethod
    def _getSetDomain(setDomain):
        """
        Generate the MathProg code for the declaration of the domain of a set
        """
        global Indices

        if setDomain["var"] in Indices:
            if ".." in Indices[setDomain["var"]]:
                return Indices[setDomain["var"]]
            else:
                return setDomain["var"] + " in " + Indices[setDomain["var"]]
        elif setDomain["min"] < float('inf'):
            return setDomain["var"] + " in " + str(setDomain["min"]) + ".." + str(setDomain["max"])
        else:
            return ""

    @staticmethod
    def _getParamDomain(paramDomain):
        """
        Generate the MathProg code for the declaration of the domain of a parameter
        """
        global Indices

        if paramDomain["var"] in Indices:
            if ".." in Indices[paramDomain["var"]]:
                return Indices[paramDomain["var"]]
            else:
                return paramDomain["var"] + " in " + Indices[paramDomain["var"]]
        elif paramDomain["min"] < float('inf'):
            return str(paramDomain["min"]) + ".." + str(paramDomain["max"])
        else:
            return ""
        
    @staticmethod
    def _declareVars():
        """
        Generate the MathProg code for the declaration of variables
        """
        global Types, Indices

        if len(Vars) > 0:

            varStr = ""
            for var in Vars:
                if not var in Params and not var in Sets:
                    if len(Vars[var]["sub-indices"]) == 0:
                        varStr += "var " + var
                    else:
                        domain = ", ".join(map(LinearProgram._getVarDomain, Vars[var]["sub-indices"]))
                        if domain:
                            varStr += "var " + var + "{" + domain + "}"
                        else:
                            varStr += "var " + var

                    if var in Types and Types[var]:
                        varStr += " " + Types[var]

                    varStr += ";\n"

            return varStr
        else:
            return ""

    @staticmethod
    def _declareSets():
        """
        Generate the MathProg code for the declaration of sets
        """

        if len(Sets) > 0:
            setStr = ""
            for setIn in Sets:
                if not setIn in Params:
                    if len(Sets[setIn]["sub-indices"]) == 0:
                        setStr += "set " + setIn + ";\n"
                    else:
                        domain = ", ".join(map(LinearProgram._getSetDomain, Sets[setIn]["sub-indices"]))

                        if domain:
                            setStr += "set " + setIn + "{" + domain + "};\n"
                        else:
                            setStr += "set " + setIn + ";\n"

            return setStr
        else:
            return ""

    @staticmethod
    def _getTuple(sub_indices):
        """
        Get a tuple with sub-indices
        """

        global Tuples

        subIndices = set(map(lambda var: var["var"], sub_indices))

        for key in Tuples:
            if subIndices == set(Tuples[key]["tuple"]):
                return key

        return None

    @staticmethod
    def _declareParams():
        """
        Generate the MathProg code for the declaration of params
        """
        global Types
        global Tuples

        if len(Params) > 0:
            paramStr = ""
            for paramIn in Params:
                if len(Params[paramIn]["sub-indices"]) == 0:
                    paramStr += "param " + paramIn
                else:
                    tupleVal = LinearProgram._getTuple(Params[paramIn]["sub-indices"])

                    if tupleVal != None:
                        domain = "("+",".join(Tuples[tupleVal]["tuple"]) + ") " + Tuples[tupleVal]["op"] + " " + tupleVal
                    else:
                        domain = ", ".join(map(LinearProgram._getParamDomain, Params[paramIn]["sub-indices"]))

                    if domain:
                        paramStr += "param " + paramIn + "{" + domain + "}"
                    else:
                        paramStr += "param " + paramIn

                if paramIn in Types and Types[paramIn]:
                    paramStr += " " + Types[paramIn]

                #if Params[paramIn]["type"] != "":
                #    paramStr += " " + Params[paramIn]["type"]

                paramStr += ";\n"

            return paramStr
        else:
            return ""

    def __init__(self, objective, constraints):
        """
        Set the objective and the constraints
        
        :param objective: Objective
        :param constraints: Constraints
        """
        
        self.objective = objective
        self.constraints = constraints
    
    def __str__(self):
        """
        to string
        """
        
        if self.constraints:
            return "\nLP:\n" + str(self.objective) + "\n" + str(self.constraints) + "\n"
        else:
            return "\nLP:\n" + str(self.objective) + "\n"
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the Set, Parameter and Variable statements
        """

        self.objective.setupEnvironment()
        if self.constraints:
            self.constraints.setupEnvironment()

        return LinearProgram._declareSets() + "\n" + LinearProgram._declareParams() + "\n" + LinearProgram._declareVars() + "\n"

    def postModel(self):
        return "\nsolve;\n\nend;\n"
    
    def generateCode(self):
        """
        Generate the code in MathProg for this Linear Program
        """
        
        if self.constraints:
            return self.setupEnvironment() + "\n" + self.objective.generateCode() + "\n" + self.constraints.generateCode() + "\n" + self.postModel() + "\n"
        else:
            return self.setupEnvironment() + "\n" + self.objective.generateCode() + "\n" + self.postModel() + "\n"
        #return SupportGenCode.emitLinearProgram(self.setupEnvironment(), self.objective.generateCode(), self.constraints.generateCode())
    
class Objective:
    """
    Class representing the node of the objective function in the AST of a MLP
    """
    
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"
    
    def __init__(self, linearExpression, type = MAXIMIZE, domain = None):
        """
        Set the objective type (maximize/minimize) and the expression being maximized/minimized
        
        :param linearExpression : LinearExpression
        :param type             : (MAXIMIZE,MINIMIZE)
        :param domain           : optional indexing expression
        """
        
        self.linearExpression = linearExpression
        self.type = type
        self.domain = domain
    
    def __str__(self):
        """
        to string
        """
        
        return "\nObj:\n" + str(self.type) + ": " + str(self.linearExpression) + "\n"
    
    def setDomain(domain):
        """
        Set the domain
        """

        self.domain = domain

    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this objective function
        """

        self.linearExpression.setupEnvironment()

        if self.domain:
            self.domain.setupEnvironment()

    def generateCode(self):
        """
        Generate the code in MathProg for this Objective
        """
        
        if self.domain:
            domain_str = " {" + self.domain.generateCode() + "}"
        else:
            domain_str = ""

        return self.type + " obj" + domain_str + ": " + self.linearExpression.generateCode() + ";"
        #return SupportGenCode.emitObjective(self.type, self.domain, self.linearExpression.generateCode())

class Constraints:
    """
    Class that encapsulate a list of all nodes in the AST that represent a contraint in a MLP
    """

    # Get the MathProg code for a given constraint
    @staticmethod
    def _getCodeConstraint(constraint):
        global constraintNumber

        constraintNumber += 1
        return "s.t. C" + str(constraintNumber) + " " + constraint.generateCode()
    #def _getCodeConstraint(constraint): return SupportGenCode.emitConstraint(constraint.generateCode())

    # Get the MathProg code for a given constraint
    @staticmethod
    def _setupConstraint(constraint):
        constraint.setupEnvironment()
    #def _getCode(constraint): return SupportGenCode.emitConstraint(constraint.generateCode())
    
    def __init__(self, constraints):
        """
        Set the list of constraints
        
        :param constraints: [Constraint]
        """
        
        self.constraints = constraints
    
    def __str__(self):
        """
        to string
        """
        
        return "\nCnts:\n" + "\n".join(map(lambda i: str(i), self.constraints))
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in these constraints
        """

        map(Constraints._setupConstraint, self.constraints)

    def generateCode(self):
        """
        Generate the code in MathProg for these Constraints
        """
        
        # Get the MathProg code for each constraint in constraints and concatenates with '\n'
        return "\n".join(map(Constraints._getCodeConstraint, self.constraints))
    
class Constraint:
    """
    Class representing a constraint node in the AST of a MLP
    """
    
    # Get the MathProg code for a given IndexingExpression
    @staticmethod
    def _getCodeIndexingExpression(indexingExpression): return indexingExpression.generateCode()
    #def _getCodeIndexingExpression(indexingExpression): return SupportGenCode.emitIndexingExpression(indexingExpression.generateCode())

    def __init__(self, constraintExpression, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of an constraint
        
        :param constraintExpression: ConstraintExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.constraintExpression = constraintExpression
        self.indexingExpression   = indexingExpression
    
    def __str__(self):
        """
        to string
        """
        
        res = str(self.constraintExpression)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Cnt:" + res

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets in this constraint
        """
        
        self.constraintExpression.setupEnvironment()

        if self.indexingExpression:
            self.indexingExpression.setupEnvironment()
    
    def generateCode(self):
        """
        Generate the MathProg code for this constraint
        """

        res = ""

        if self.indexingExpression:
            # Get the MathProg code for each constraint expression in for clause and concatenates with \n
            res += "{" + self.indexingExpression.generateCode() + "} :\n\t"
        else:
            res += " : "

        res += self.constraintExpression.generateCode() + ";"
        #res += SupportGenCode.emitConstraintExpression(self.constraintExpression.generateCode())

        return res

class Expression:
    """
    Class representing a expression node in the AST of a MLP
    """

class ConstraintExpression(Expression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """
    EQ = "="
    LE = "<="
    GE = ">="

class ConstraintExpression2(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression1, linearExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression1: LinearExpression
        :param linearExpression2: LinearExpression
        """
        
        self.linearExpression1 = linearExpression1
        self.linearExpression2 = linearExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExpr:" + str(self.linearExpression1) + " " + self.op + " " + str(self.linearExpression2)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets in this constraint
        """

        self.linearExpression1.setupEnvironment()
        self.linearExpression2.setupEnvironment()
    
    def generateCode(self):
        """
        Generate the MathProg code for this constraint expression
        """
        
        return self.linearExpression1.generateCode() + ", " + self.op + " " + self.linearExpression2.generateCode()
        # return SupportGenCode.emitConstraintExpression(self.linearExpression1.generateCode(), self.linearExpression2.generateCode(), self.op)

class ConstraintExpression3(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression, numericExpression1, numericExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression   : LinearExpression
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """
        
        self.linearExpression   = linearExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExpr:" + str(self.numericExpression1) + " " + self.op + " " + str(self.linearExpression) + " " + self.op + " " + str(self.numericExpression2)
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets in this constraint
        """

        self.linearExpression.setupEnvironment()
        self.numericExpression1.setupEnvironment()
        self.numericExpression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this constraint expression
        """
        
        return self.linearExpression.generateCode() + ", " + self.op + " " + self.numericExpression1.generateCode() + ", " + self.op + " " + self.numericExpression2.generateCode()
        # return SupportGenCode.emitConstraintExpression(self.linearExpression.generateCode(), self.numericExpression1.generateCode(), self.numericExpression2.generateCode(), self.op)

class LinearExpression(Expression):
    """
    Class representing a linear expression node in the AST of a MLP
    """

class ValuedLinearExpression(LinearExpression):
    """
    Class representing a valued linear expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this linear expression

        :param value : Variable | Number
        """

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "ValuedExpr:" + str(self.value)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """

        self.value.setupEnvironment()
    
    def generateCode(self):
        """
        Generate the MathProg code for this valued linear expression
        """
        
        return self.value.generateCode()
        # return SupportGenCode.emitValuedLinearExpression(self.value.generateCode())

class LinearExpressionBetweenParenthesis(LinearExpression):
    """
    Class representing a linear expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, linearExpression):
        """
        Set the linear expression

        :param linearExpression : LinearExpression
        """

        self.linearExpression = linearExpression

    def __str__(self):
        """
        to string
        """
        
        return "LE: (" + str(self.linearExpression) + ")"

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """

        self.linearExpression.setupEnvironment()
    
    def generateCode(self):
        """
        Generate the MathProg code for this linear expression
        """
        
        return "(" + self.linearExpression.generateCode() + ")"
        # return SupportGenCode.emitLinearExpressionBetweenParenthesis(self.linearExpression.generateCode())

class LinearExpressionWithArithmeticOperation(LinearExpression):
    """
    Class representing a linear expression with arithmetic operation node in the AST of a MLP
    """
    
    PLUS  = "+"
    MINUS = "-"
    TIMES = "*"
    DIV   = "/"

    def __init__(self, op, expression1, expression2):
        """
        Set the expressions participating in the arithmetic operation
        
        :param op          : (PLUS, MINUS, TIMES, DIV)
        :param expression1 : LinearExpression | NumericExpression
        :param expression2 : LinearExpression | NumericExpression
        """
        
        self.op          = op
        self.expression1 = expression1
        self.expression2 = expression2
    
    def __str__(self):
        """
        to string
        """
        
        return "OpLE:" + str(self.expression1) + " " + self.op + " " + str(self.expression2)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """

        self.expression1.setupEnvironment()
        self.expression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this linear expression with arithmetic pperation
        """
        
        return self.expression1.generateCode() + " " + self.op + " " + self.expression2.generateCode()
        # return SupportGenCode.emitLinearExpressionWithArithmeticOperation(self.expression1.generateCode(), self.expression2.generateCode().self.op)

class MinusLinearExpression(LinearExpression):
    """
    Class representing a minus linear expression node in the AST of a MLP
    """
    
    def __init__(self, linearExpression):
        """
        Set the expressions being negated
        
        :param linearExpression: LinearExpression
        """
        
        self.linearExpression = linearExpression
    
    def __str__(self):
        """
        to string
        """
        
        return "MinusLE:" + "-(" + str(self.linearExpression) + ")"
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """

        self.linearExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this minus linear expression
        """
        
        return "-" + self.linearExpression.generateCode()
        # return SupportGenCode.emitMinusLinearExpression(self.linearExpression.generateCode())

class IteratedLinearExpression(LinearExpression):
    """
    Class representing a iterated linear expression node in the AST of a MLP
    """

    SUM = "sum"

    def __init__(self, linearExpression, indexingExpression, numericExpression = None):
        """
        Set the components of the iterated linear expression

        :param linearExpression   : LinearExpression
        :param indexingExpression : IndexingExpression
        :param numericExpression  : NumericExpression
        """
        
        self.linearExpression   = linearExpression
        self.indexingExpression = indexingExpression
        self.numericExpression  = numericExpression

    def __str__(self):
        """
        to string
        """
        
        res = IteratedLinearExpression.SUM + "(" + str(self.indexingExpression) + ")"

        if self.numericExpression:
            res += "^(" + str(self.numericExpression) + ")"

        res += "(" + str(self.linearExpression) + ")"

        return "ItLE:" + res
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """

        if self.numericExpression:
            self.numericExpression.setupEnvironment()
            self.indexingExpression.setHasSup(True)
        
        self.linearExpression.setupEnvironment()
        self.indexingExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this iterated linear expression
        """

        if self.numericExpression:
            res = IteratedLinearExpression.SUM + "{" + self.indexingExpression.generateCode() + "..(" + self.numericExpression.generateCode() + ")}"
        else:
            res = IteratedLinearExpression.SUM + "{" + self.indexingExpression.generateCode() + "}"

        #if self.numericExpression:
        #    res += "^{" + self.numericExpression.generateCode() + "}"
        
        res += "(" + self.linearExpression.generateCode() + ")"

        return res

        #if self.numericExpression:
        #   return SupportGenCode.emitIteratedLinearExpression(self.linearExpression.generateCode(), self.indexingExpression.generateCode(), self.numericExpression.generateCode())
        #else:
        #   return SupportGenCode.emitIteratedLinearExpression(self.linearExpression.generateCode(), self.indexingExpression.generateCode())

class NumericExpression:
    """
    Class representing a numeric expression node in the AST of a MLP
    """

class NumericExpressionWithFunction(NumericExpression):
    """
    Class representing a numeric expression with function node in the AST of a MLP
    """

    ABS    = "abs"
    ATAN   = "atan"
    CARD   = "card"
    CEIL   = "ceil"
    COS    = "cos"
    FLOOR  = "floor"
    EXP    = "exp"
    LENGTH = "length"
    LOG    = "log"
    LOG10  = "log10"
    ROUND  = "round"
    SIN    = "sin"
    SQRT   = "sqrt"
    TRUNC  = "trunc"

    def __init__(self, function, numericExpression):
        """
        Set the numeric expression and the function

        :param function          : (abs | atan | card | ceil | cos | floor | exp | length | log | log10 | round | sin | sqrt | trunc)
        :param numericExpression : NumericExpression
        """

        self.function = function
        self.numericExpression = numericExpression

    def __str__(self):
        """
        to string
        """

        return str(self.function) + "(" + str(self.numericExpression) + ")"

    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """

        self.numericExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this numeric expression with function
        """

        return str(self.function) + "(" + self.numericExpression.generateCode() + ")"

class ValuedNumericExpression(NumericExpression):
    """
    Class representing a valued numeric expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this numeric expression

        :param value : Variable | Number
        """

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "ValuedExpr:" + str(self.value)
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        self.value.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this valued linear expression
        """
        
        return self.value.generateCode()
        # return SupportGenCode.emitValuedNumericExpression(self.value.generateCode())

class NumericExpressionBetweenParenthesis(NumericExpression):
    """
    Class representing a numeric expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, numericExpression):
        """
        Set the numeric expression

        :param numericExpression : NumericExpression
        """

        self.numericExpression = numericExpression

    def __str__(self):
        """
        to string
        """
        
        return "NE: (" + str(self.numericExpression) + ")"
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        self.numericExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this valued linear expression
        """
        
        return "(" + self.numericExpression.generateCode() + ")"
        # return SupportGenCode.emitNumericExpressionBetweenParenthesis(self.numericExpression.generateCode())

class NumericExpressionWithArithmeticOperation(NumericExpression):
    """
    Class representing a numeric expression with arithmetic operation node in the AST of a MLP
    """
    
    PLUS  = "+"
    MINUS = "-"
    TIMES = "*"
    DIV   = "/"
    MOD   = "%"
    POW   = "^"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the expressions participating in the arithmetic operation
        
        :param op                 : (PLUS, MINUS, TIMES, MOD, POW)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """
        
        self.op                 = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
    
    def __str__(self):
        """
        to string
        """
        
        return "OpArthNE:" + str(self.numericExpression1) + " " + self.op + " " + str(self.numericExpression2)
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        self.numericExpression1.setupEnvironment()
        self.numericExpression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this numeric expression with arithmetic operation
        """
        
        return self.numericExpression1.generateCode() + " " + self.op + " " + self.numericExpression2.generateCode()
        # return SupportGenCode.emitNumericExpressionWithArithmeticOperation(self.numericExpression1.generateCode(), self.numericExpression2.generateCode().self.op)

class MinusNumericExpression(NumericExpression):
    """
    Class representing a minus numeric expression node in the AST of a MLP
    """
    
    def __init__(self, numericExpression):
        """
        Set the numeric expression being negated
        
        :param numericExpression: NumericExpression
        """
        
        self.numericExpression = numericExpression
    
    def __str__(self):
        """
        to string
        """
        
        return "MinusNE:" + "-(" + str(self.numericExpression) + ")"
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        self.numericExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this minus numeric expression
        """
        
        return "-" + self.numericExpression.generateCode()
        # return SupportGenCode.emitMinusNumericExpression(self.numericExpression.generateCode())

class IteratedNumericExpression(NumericExpression):
    """
    Class representing a iterated numeric expression node in the AST of a MLP
    """

    SUM  = "sum"
    PROD = "prod"
    MAX  = "max"
    MIN  = "min"

    def __init__(self, op, numericExpression, indexingExpression, supNumericExpression = None):
        """
        Set the components of the iterated linear expression

        :param op                   : op
        :param numericExpression    : NumericExpression
        :param indexingExpression   : IndexingExpression
        :param supNumericExpression : NumericExpression
        """
        
        self.op                   = op
        self.numericExpression    = numericExpression
        self.indexingExpression   = indexingExpression
        self.supNumericExpression = supNumericExpression

    def __str__(self):
        """
        to string
        """
        
        res = str(self.op) + "(" + str(self.indexingExpression) + ")"

        if self.supNumericExpression:
            res += "^(" + str(self.supNumericExpression) + ")"

        res += str(self.numericExpression)

        return "ItLE:" + res
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """

        if self.supNumericExpression:
            self.supNumericExpression.setupEnvironment()
            self.indexingExpression.setHasSup(True)
        
        self.numericExpression.setupEnvironment()
        self.indexingExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this iterated numeric expression
        """

        if self.supNumericExpression:
            res = str(self.op) + "{" + self.indexingExpression.generateCode() + "..(" + self.supNumericExpression.generateCode() + ")}"
        else:
            res = str(self.op) + "{" + self.indexingExpression.generateCode() + "}"

        #if self.supNumericExpression:
        #    res += "^{" + self.supNumericExpression.generateCode() + "}"
        
        res += self.numericExpression.generateCode()

        return res

        #if self.supNumericExpression:
        #   return SupportGenCode.emitIteratedNumericExpression(self.op, self.numericExpression.generateCode(), self.indexingExpression.generateCode(), self.supNumericExpression.generateCode())
        #else:
        #   return SupportGenCode.emitIteratedNumericExpression(self.op, self.numericExpression.generateCode(), self.indexingExpression.generateCode())

class IndexingExpression(Expression):
    """
    Class representing an indexing expression in the AST of the MLP
    """

    @staticmethod
    def _deleteEmpty(str):
        return str != ""

    # Get the MathProg code for a given constraint
    @staticmethod
    def _setupEntry(entry): return entry.setupEnvironment()
    #def _getCodeEntry(entry): return SupportGenCode.emitEntryIndexingExpression(entry.generateCode())

    # Get the MathProg code for a given constraint
    @staticmethod
    def _getCodeEntry(entry): return entry.generateCode()
    #def _getCodeEntry(entry): return SupportGenCode.emitEntryIndexingExpression(entry.generateCode())

    # Get the MathProg code for a given constraint
    @staticmethod
    def _getCodePredicateEntry(entry): return entry.generatePredicateCode()
    #def _getCodePredicateEntry(entry): return SupportGenCode.emitEntryIndexingExpression(entry.generateCode())

    def __init__(self, entriesIndexingExpression, logicalExpression = None):
        """
        Set the entries for the indexing expression
        """

        self.entriesIndexingExpression = entriesIndexingExpression
        self.logicalExpression = logicalExpression
        self.hasSup = False

    def __str__(self):
        """
        to string
        """

        res = "\nIE:\n"
        res += "\n".join(filter(IndexingExpression._deleteEmpty, map(lambda i: str(i), self.entriesIndexingExpression)))

        if self.logicalExpression:
            res += str(self.logicalExpression)

        return res


    def __len__(self):
        """
        length method
        """

        return len(self.entriesIndexingExpression)

    def add(self, entry):
        """
        Add an entry to the indexing expression
        """

        self.entriesIndexingExpression += [entry]
        return self

    def setLogicalExpression(self, logicalExpression):
        """
        Set the logical expression
        """

        self.logicalExpression = logicalExpression
        return self

    def setHasSup(self, hasSup):
        self.hasSup = hasSup

    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        if self.hasSup:
            if len(self.entriesIndexingExpression) > 1:
                raise Exception('If iterated expression has a superior expression, then is must have only a single entry!')
            elif not isinstance(self.entriesIndexingExpression[0], EntryIndexingExpressionEq):
                raise Exception('If iterated expression has a superior expression, then its single entry must be of type EntryIndexingExpressionEq!')
            else:
                self.entriesIndexingExpression[0].setHasSup(True)

        map(IndexingExpression._setupEntry, self.entriesIndexingExpression)

        if self.logicalExpression:
            self.logicalExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this indexing expression
        """

        indexing = filter(IndexingExpression._deleteEmpty, map(IndexingExpression._getCodeEntry, self.entriesIndexingExpression))
        res = ", ".join(indexing)

        if self.logicalExpression:
            res += " : " + self.logicalExpression.generateCode()

        return res

class EntryIndexingExpression(Expression):
    """
    Class representing an entry of indexing expression in the AST of the MLP
    """

class EntryIndexingExpressionWithSet(EntryIndexingExpression):
    """
    Class representing an entry with set of indexing expression in the AST of the MLP
    """

    IN = "in"
    NOTIN = "not in"

    def __init__(self, variable, setExpression, op = IN):
        """
        Set the variable(s) and the set

        :param variable      : Variable | [Value]
        :param setExpression : SetExpression
        :param op            : (IN | NOTIN)
        """

        self.variable      = variable
        self.setExpression = setExpression
        self.op = op
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isReal = False

    def __str__(self):
        """
        to string
        """

        if isinstance(self.variable, ValueList):
            return "EIE_S: ValueList: " + ", ".join(map(lambda var: str(var) + " " + self.op + " " + str(self.setExpression), self.variable))
        else:
            return "EIE_S: " + str(self.variable) + " " + self.op + " " + str(self.setExpression)



    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """

        global Types
        global Tuples

        if isinstance(self.variable, TupleList):
            Tuples[self.setExpression.generateCode()] = {}
            Tuples[self.setExpression.generateCode()]["tuple"] = map(lambda val: val.generateCode(), self.variable.getValues())
            Tuples[self.setExpression.generateCode()]["op"] = self.op

        else:
            if isinstance(self.variable, Variable) and len(self.variable.sub_indices) > 0:
                self.variable.setupEnvironment()

            setCode = self.setExpression.generateCode()

            if setCode == "{0,1}":
                self.isBinary = True
                Types[self.variable.generateCodeWithoutIndices()] = "binary"
            elif setCode == "integer":
                self.isInteger = True
                Types[self.variable.generateCodeWithoutIndices()] = "integer"
            elif setCode == "natural":
                self.isNatural = True
                Types[self.variable.generateCodeWithoutIndices()] = "integer, >= 0"
            elif setCode == "real":
                self.isReal = True
                Types[self.variable.generateCodeWithoutIndices()] = ""

            ind = self.variable.generateCode()
            if ind in Indices:
                Indices[ind] = self.setExpression.generateCode()

        self.setExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry with Set of Indexing Expression
        """

        if self.isBinary or self.isInteger or self.isNatural or self.isReal:
            return ""
        else:
            if isinstance(self.variable, ValueList):
                return ", ".join(map(lambda var: var.generateCode() + " " + self.op + " " + self.setExpression.generateCode(), self.variable))
            else:
                return self.variable.generateCode() + " " + self.op + " " + self.setExpression.generateCode()

# This type of comparison is used only as a predicate of an entry in an indexing expression
class EntryIndexingExpressionCmp(EntryIndexingExpression):
    """
    Class representing an entry with comparison operator of indexing expression in the AST of the MLP
    """

    NEQ = "<>"
    LE  = "<="
    GE  = ">="
    LT  = "<"
    GT  = ">"

    def __init__(self, op, variable, numericExpression):
        """
        Set the variable and the numeric expression being compared, and the comparison operator

        :param op                : op
        :param variable          : Variable
        :param numericExpression : NumericExpression
        """

        self.op                = op
        self.variable          = variable
        self.numericExpression = numericExpression
        self.internalSet       = 0

    def __str__(self):
        """
        to string
        """

        return "EIE_C: " + str(self.variable) + " " + self.op + " " + str(self.numericExpression)

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """

        #self.variable.setupEnvironment()
        self.numericExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry with Comparison of Indexing Expression
        """

        #SetsNumber += 1
        #self.internalSet = SetsNumber
        #Set["EntryIndexingExpressionCmp" + str(self.internalSet)] = "Set" + str(self.internalSet)
        return self.variable.generateCode() + " " + self.op + " " + self.numericExpression.generateCode()

class EntryIndexingExpressionEq(EntryIndexingExpression):
    """
    Class representing an entry with equality operator of indexing expression in the AST of the MLP
    """

    EQ = "="
    NEQ = "!=" # delete this constant, make no sense a indexing expression with inequality instead of equality

    @staticmethod
    def _getInt(val):
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    def __init__(self, op, variable, value):
        """
        Set the variable and the numeric expression being compared, and the comparison operator

        :param          : op
        :param variable : Variable
        :param value    : Value | Range
        """

        self.op       = op
        self.variable = variable
        self.value    = value
        self.internalSet = 0
        self.hasSup = False

    def __str__(self):
        """
        to string
        """

        return "EIE_E: " + str(self.variable) + " " + self.op + " " + str(self.value)

    def setHasSup(self, value):
        """
        Set if the entry expression has a sup value
        """
        self.hasSup = value

    def setInternalSet(internalSet):
        self.internalSet = internalSet

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """

        global Indices

        #self.variable.setupEnvironment()
        ind = self.variable.generateCode()
        if ind in Indices:
            Indices[ind] = self.value.generateCode()

        self.value.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry with Equality of Indexing Expression
        """
        global SetsNumber, Sets

        if self.hasSup:
            return self.variable.generateCode() + " in " + EntryIndexingExpressionEq._getInt(self.value.generateCode())
        else:
            SetsNumber += 1
            self.internalSet = SetsNumber
            Sets["Set" + str(self.internalSet)] = self.value.generateCode()
            return self.variable.generateCode() + " in " + Sets["Set" + str(self.internalSet)]

class LogicalExpression(Expression):
    """
    Class representing an logical expression in the AST of the MLP
    """

    @staticmethod
    def _deleteEmpty(str):
        return str != ""

    # Get the MathProg code for a given entry
    @staticmethod
    def _setupEntry(entry):
        for key in entry:
            return entry[key].setupEnvironment()
    #def _setupEntry(entry): return SupportGenCode.emitEntryLogicalExpression(entry.generateCode())

    # Get the MathProg code for a given entry
    @staticmethod
    def _getCodeEntry(entry):
        for key in entry:
            return key, entry[key].generateCode()
    #def _getCodeEntry(entry): return SupportGenCode.emitEntryLogicalExpression(entry.generateCode())

    def __init__(self, entriesLogicalExpression):
        """
        Set the entries for the logical expression
        """

        self.entriesLogicalExpression = map(lambda e: {"and": e}, entriesLogicalExpression)

    def __str__(self):
        """
        to string
        """
        res = "\nLE:\n"
        resAux = ""
        first = True

        for i in range(len(self.entriesLogicalExpression)):
            for conj in self.entriesLogicalExpression[i]:
                code = str(self.entriesLogicalExpression[i][conj])

                if code != 0:
                    if first:
                        first = False
                        res += code
                    else:
                        res += " " + conj + " " + code

        return res + resAux

    def __len__(self):
        """
        length method
        """

        return len(self.entriesLogicalExpression)

    def addAnd(self, entry):
        """
        Add an entry to the logical expression with and conjunctor
        """

        self.entriesLogicalExpression.append({"and": entry})
        return self

    def addOr(self, entry):
        """
        Add an entry to the logical expression with or conjunctor
        """

        self.entriesLogicalExpression.append({"or": entry})
        return self

    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        
        map(LogicalExpression._setupEntry, self.entriesLogicalExpression)

    def generateCode(self):
        """
        Generate the MathProg code for this logical expression
        """

        res = ""
        first = True

        for i in range(len(self.entriesLogicalExpression)):
            conj, code = LogicalExpression._getCodeEntry(self.entriesLogicalExpression[i])

            if code != 0:
                if first:
                    first = False
                    res += code
                else:
                    res += " " + conj + " " + code

        return res

class EntryLogicalExpression(Expression):
    """
    Class representing an entry of logical expression in the AST of the MLP
    """

class EntryLogicalExpressionRelational(EntryLogicalExpression):
    """
    Class representing an entry of relational logical expression in the AST of the MLP
    """

    LT = "<"
    LE = "<="
    EQ = "="
    GE = ">="
    NEQ = "<>"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the operator and the numeric expressions

        :param op : (LT, LE, EQ, GE, NEQ)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        self.op = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """

        return str(self.numericExpression1) + " " + self.op + " " + str(self.numericExpression2)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """

        self.numericExpression1.setupEnvironment()
        self.numericExpression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry of Relational Logical Expression
        """

        return self.numericExpression1.generateCode() + " " + self.op + " " + self.numericExpression2.generateCode()

class EntryLogicalExpressionWithSet(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    IN = "in"
    NOTIN = "not in"

    def __init__(self, op, value, setExpression):
        """
        Set the operator, the value and the set expression

        :param op : op
        :param value : ValueList, Variable
        :param setExpression : setExpression
        """

        self.op = op
        self.value = value
        self.setExpression = setExpression
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isReal = False

    def __str__(self):
        """
        to string
        """

        return str(self.value) + " " + self.op + " " + str(self.setExpression)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """

        global Types
        
        if isinstance(self.value, Variable) and len(self.value.sub_indices) > 0:
            self.value.setupEnvironment()

        setCode = self.setExpression.generateCode()

        if setCode == "{0,1}":
            self.isBinary = True
            Types[self.variable.generateCodeWithoutIndices()] = "binary"
        elif setCode == "integer":
            self.isInteger = True
            Types[self.variable.generateCodeWithoutIndices()] = "integer"
        elif setCode == "natural":
            self.isNatural = True
            Types[self.variable.generateCodeWithoutIndices()] = "integer, >= 0"
        elif setCode == "real":
            self.isReal = True
            Types[self.variable.generateCodeWithoutIndices()] = ""

        ind = self.value.generateCode()
        if ind in Indices:
            Indices[ind] = self.setExpression.generateCode()

        self.setExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry of Logical Expression with Set
        """

        if self.isBinary or self.isInteger or self.isNatural or self.isReal:
            return ""
        else:
            return self.value.generateCode() + " " + self.op + " " + self.setExpression.generateCode()

class EntryLogicalExpressionWithSetOperation(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    SUBSET = "within"
    NOTSUBSET = "not within"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the set expressions

        :param op : (SUBSET, NOTSUBSET)
        :param setExpression1 : SetExpression
        :param setExpression2 : SetExpression
        """

        self.op = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """

        self.setExpression1.setupEnvironment()
        self.setExpression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry of Logical Expression with Set
        """

        return self.setExpression1.generateCode() + " " + self.op + " " + self.setExpression2.generateCode()

class EntryLogicalExpressionIterated(EntryLogicalExpression):
    """
    Class representing an entry of iterated logical expression in the AST of the MLP
    """

    FORALL = "forall"
    EXISTS = "exists"

    def __init__(self, op, indexingExpression, logicalExpression):
        """
        Set the operator and the numeric expressions

        :param op : (FORALL, EXISTS)
        :param indexingExpression : IndexingExpression
        :param logicalExpression  : LogicalExpression
        """

        self.op = op
        self.indexingExpression = indexingExpression
        self.logicalExpression  = logicalExpression

    def __str__(self):
        """
        to string
        """

        return self.op + "{" + str(self.indexingExpression) + "} " +  str(self.logicalExpression)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """

        self.indexingExpression.setupEnvironment()
        self.logicalExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for Entry of Iterated Logical Expression
        """

        return self.op + "{" + self.indexingExpression.generateCode() + "} " +  self.logicalExpression.generateCode()

class EntryLogicalExpressionBetweenParenthesis(NumericExpression):
    """
    Class representing a logical expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, logicalExpression):
        """
        Set the logical expression

        :param logicalExpression : LogicalExpression
        """

        self.logicalExpression = logicalExpression

    def __str__(self):
        """
        to string
        """
        
        return "LE: (" + str(self.logicalExpression) + ")"
    
    def setupEnvironment(self):
        """
        Generate the MathProg code for the variables and sets used in this logical expression
        """
        
        self.logicalExpression.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this logical expression
        """
        
        return "(" + self.logicalExpression.generateCode() + ")"
        # return SupportGenCode.emitLogicalExpressionBetweenParenthesis(self.logicalExpression.generateCode())

class SetExpression(Expression):
    """
    Class representing a set in the AST of the MLP
    """

class SetExpressionWithValue(SetExpression):
    """
    Class representing a set with value in the AST of the MLP
    """

    def __init__(self, value):
        """
        Set the value that correspond to the Set expression

        :param value : Variable | ValueList | Range
        """

        self.value = value

    def __str__(self):
        """
        to string
        """

        return "SEV: "+str(self.value)

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """

        if isinstance(self.value, Variable):
            self.value.setIsSet(True)

        if not isinstance(self.value, str):
            self.value.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this Set expression
        """
        if not isinstance(self.value, str):
            return self.value.generateCode()
        else:
            return self.value

class SetExpressionWithIndices(SetExpression):
    """
    Class representing a set with indices in the AST of the MLP
    """

    def __init__(self, variable, indices):
        """
        Set the value that correspond to the Set expression

        :param variable : Variable
        :param indices: ValueList | Variable
        """

        self.variable = variable
        self.indices = indices

    def __str__(self):
        """
        to string
        """

        if isinstance(self.indices, Variable):
            return "SEI: " + str(self.variable) + "[" + str(self.indices) + "]"
        else:
            return "SEI: " + str(self.variable) + "[" + ",".join(map(lambda ind: str(ind), self.indices)) + "]"

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """

        if isinstance(self.variable, Variable):
            self.variable.setIsSet(True)

        if not isinstance(self.variable, str):
            self.variable.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this Set expression
        """

        if not isinstance(self.variable, str):
            if isinstance(self.indices, Variable):
                return self.variable.generateCode() + "[" + self.indices.generateCode() + "]"
            else:
                return self.variable.generateCode() + "[" + ",".join(map(lambda ind: ind.generateCode(), self.indices.getValues())) + "]"
        else:
            if isinstance(self.indices, Variable):
                return self.variable + "[" + self.indices.generateCode() + "]"
            else:
                return self.variable + "[" + ",".join(map(lambda ind: ind.generateCode(), self.indices.getValues())) + "]"

class SetExpressionWithOperation(SetExpression):
    """
    Class representing a set with operation in the AST of the MLP
    """

    DIFF    = "diff"
    SYMDIFF = "symdiff"
    UNION   = "union"
    INTER   = "inter"
    CROSS   = "cross"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the expressions
        """
        
        self.op             = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def setupEnvironment(self):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        
        self.setExpression1.setupEnvironment()
        self.setExpression2.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this Set expression
        """

        return self.setExpression1.generateCode() + " " + self.op + " " + self.setExpression2.generateCode()

class Range(Expression):
    """
    Class representing a range in the AST of the MLP
    """

    @staticmethod
    def _getInt(val):
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    def __init__(self, rangeInit, rangeEnd):
        """
        Set the range init and end
        
        :param rangeInit : Variable | Number
        :param rangeEnd  : Variable | Number
        """
        
        self.rangeInit = rangeInit
        self.rangeEnd  = rangeEnd

    def __str__(self):
        """
        to string
        """
        
        return "Var: [" + str(self.rangeInit) + ".." + str(self.rangeEnd) + "]"

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """

        if isinstance(self.rangeInit, Variable):
            self.rangeInit.setIsParam(True)

        if isinstance(self.rangeEnd, Variable):
            self.rangeEnd.setIsParam(True)

        self.rangeInit.setupEnvironment()
        self.rangeEnd.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this Range
        """
        
        initValue = self.rangeInit.generateCode()
        initValue = Range._getInt(initValue)

        endValue = self.rangeEnd.generateCode()
        endValue = Range._getInt(endValue)

        return initValue + ".." + endValue

class ValueList(Expression):
    """
    Class representing a list of values in the AST of the MLP
    """

    @staticmethod
    def _setupValue(value):
        value.setupEnvironment()

    # Get the MathProg code for a given relational expression
    @staticmethod
    def _getCodeValue(value):
        val = value.generateCode()
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val
    #def _getCodeValue(value): return SupportGenCode.emitValue(value.generateCode())

    def __init__(self, values):
        """
        Set the values
        
        :param values : [Variable|Number]
        :param setExpression : SetExpression
        """
        
        self.values = values
        self.i = -1

    def __str__(self):
        """
        to string
        """
        
        return "ValueList: " + ",".join(map(lambda i: str(i), self.values))

    def __len__(self):
        """
        length method
        """

        return len(self.values)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.values)-1:
            self.i += 1         
            return self.values[self.i]
        else:
            self.i = -1
            raise StopIteration


    def getValues(self):
        """
        get the values in this ValueList
        """

        return self.values

    def add(self, value):
        """
        Add a value to the list
        """

        self.values += [value]
        return self

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        
        map(ValueList._setupValue, self.values)

    def generateCode(self):
        """
        Generate the MathProg code for this Range
        """
        
        return ",".join(map(ValueList._getCodeValue, self.values))


class TupleList(Expression):
    """
    Class representing a tuple of values in the AST of the MLP
    """

    global Tuples

    @staticmethod
    def _setupValue(value):
        value.setupEnvironment()

    # Get the MathProg code for a given relational expression
    @staticmethod
    def _getCodeValue(value):
        val = value.generateCode()
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val
    #def _getCodeValue(value): return SupportGenCode.emitValue(value.generateCode())

    def __init__(self, values):
        """
        Set the values
        
        :param values : [Variable|Number]
        """
        
        self.values = values
        self.i = -1

    def __str__(self):
        """
        to string
        """
        
        return "TupleList: (" + ",".join(map(lambda i: str(i), self.values)) + ")"

    def __len__(self):
        """
        length method
        """

        return len(self.values)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.values)-1:
            self.i += 1         
            return self.values[self.i]
        else:
            self.i = -1
            raise StopIteration

    def getValues(self):
        """
        get the values in this TupleList
        """

        return self.values

    def add(self, value):
        """
        Add a value to the tuple
        """

        self.values += [value]
        return self

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        
        map(TupleList._setupValue, self.values)


    def generateCode(self):
        """
        Generate the MathProg code for this TupleList
        """
        
        return "(" + ",".join(map(TupleList._getCodeValue, self.values)) + ")"

class Value(Expression):
    """
    Class representing an Value in the AST of the MLP
    """

    def __init__(self, value):
        """
        Set the value

        :param value: float|Variable
        """

        if isinstance(value, float):
            self.value = Number(value)
        else:
            self.value = value

    def __str__(self):
        """
        to string
        """

        return "Value: "  + str(self.value)

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of the variable of this value
        """

        self.value.setupEnvironment()

    def generateCode(self):
        """
        Generate the MathProg code for this Value
        """

        return self.value.generateCode()

class Variable(Expression):
    """
    Class representing an Variable in the AST of the MLP
    """

    # Get the MathProg code for a given sub-indice
    @staticmethod
    def _getCodeID(id_):
        val = id_.generateCode()
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val
        #return id_.generateCode()
    #def _getCodeID(id_): return SupportGenCode.emitID(id_.generateCode())

    def __init__(self, variable, sub_indices = []):
        """
        Set the variable and the sub indices (if there are)
        
        :param variable: ID
        :param sub_indices: [ID|Number]
        """
        
        self.variable = variable
        self.sub_indices = sub_indices
        self.inSets = []
        self.isSet = False
        self.isParam = False

    def __str__(self):
        """
        to string
        """
        
        if len(self.sub_indices) > 0:
            if isinstance(self.sub_indices, Variable) or isinstance(self.sub_indices, ID) or isinstance(self.sub_indices, Number):
                res = str(self.variable) + "[" + str(self.sub_indices) + "]"
            else:
                res = str(self.variable) + "[" + ",".join(map(lambda i: str(i), self.sub_indices)) + "]"
        else:
            res = str(self.variable)
        
        return "Var:" + res

    def __len__(self):
        """
        length method
        """

        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]

    def _checkSubIndices(self, varKey, Stm):
        #if len(self.inSets) > 0 and len(self.sub_indices) > 0:
        #    for i in range(len(self.sub_indices)):
        #        Stm[varKey]["sub-indices"][i]["set"] = self.inSets[i]

        if len(self.sub_indices) > 0:
            if isinstance(self.sub_indices, Number):
                num = int(Variable._getCodeID(self.sub_indices))
                
                if num < Stm[varKey]["sub-indices"][0]["min"]:
                    Stm[varKey]["sub-indices"][0]["min"] = num
                elif num > Stm[varKey]["sub-indices"][0]["max"]:
                    Stm[varKey]["sub-indices"][0]["max"] = num

            elif isinstance(self.sub_indices, Variable) or isinstance(self.sub_indices, ID):
                ind = self.sub_indices.generateCode()

                Stm[varKey]["sub-indices"][0]["var"] = ind

                if not ind in Indices:
                    Indices[ind] = ""

            elif isinstance(self.sub_indices, list):
                for i in range(len(self.sub_indices)):
                    if isinstance(self.sub_indices[i], Number):
                        num = int(Variable._getCodeID(self.sub_indices[i]))

                        if num < Stm[varKey]["sub-indices"][i]["min"]:
                            Stm[varKey]["sub-indices"][i]["min"] = num
                        elif num > Stm[varKey]["sub-indices"][i]["max"]:
                            Stm[varKey]["sub-indices"][i]["max"] = num
                    elif isinstance(self.sub_indices[i], Variable) or isinstance(self.sub_indices[i], ID):
                        ind = self.sub_indices[i].generateCode()
                        
                        Stm[varKey]["sub-indices"][i]["var"] = ind
                        
                        if not ind in Indices:
                            Indices[ind] = ""

    def addSet(self, inSet):
        self.inSets += [inSet]

    def setIsSet(self, isSet):
        self.isSet = isSet

    def setIsParam(self, isParam):
        self.isParam = isParam

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of this variable
        """
        global Vars
        global Sets
        global Params
        global Indices

        varKey = self.variable.generateCode()

        if varKey[0].isupper():
            self.setIsParam(True)

        if self.isSet:
            if not varKey in Sets: # check if this set was not seen yet
                Sets[varKey] = {}
                Sets[varKey]["sub-indices"] = []

                if len(self.sub_indices) > 0:
                    for i in range(len(self.sub_indices)):
                        Sets[varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1})

            self._checkSubIndices(varKey, Sets)

        elif self.isParam:
            if not varKey in Params and not varKey in Sets: # check if this param was not seen yet
                Params[varKey] = {}
                Params[varKey]["type"] = ""
                Params[varKey]["sub-indices"] = []

                if len(self.sub_indices) > 0:
                    for i in range(len(self.sub_indices)):
                        Params[varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

            self._checkSubIndices(varKey, Params)

        else:
            if not varKey in Vars and not varKey in Params and not varKey in Sets: # check if this variable was not seen yet
                Vars[varKey] = {}
                Vars[varKey]["type"] = ""
                Vars[varKey]["sub-indices"] = []

                if len(self.sub_indices) > 0:
                    for i in range(len(self.sub_indices)):
                        Vars[varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

            self._checkSubIndices(varKey, Vars)

    def generateCode(self):
        """
        Generate the MathProg code for this Variable
        """
        
        if len(self.sub_indices) > 0:
            if isinstance(self.sub_indices, Variable) or isinstance(self.sub_indices, ID) or isinstance(self.sub_indices, Number):
                res = str(self.variable) + "[" + Variable._getCodeID(self.sub_indices) + "]"
            else:
                 res = self.variable.generateCode() + "[" + ",".join(map(Variable._getCodeID, self.sub_indices)) + "]"
        else:
            res = self.variable.generateCode()
        
        return res

    def generateCodeWithoutIndices(self):
        """
        Generate the MathProg code for this Variable without the Indexing, if there are 
        """

        return self.variable.generateCode()

class ID:
    """
    Class representing a variable node in the AST of the MLP
    """
    
    def __init__(self, variable):
        """
        Set the string that represents the variable
        
        :param variable: String
        """
        
        self.variable = variable
    
    def __str__(self):
        """
        to string
        """
        
        return self.variable

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]

    def setupEnvironment(self):
        """
        Generate the MathProg code for the declaration of this ID
        """

        pass

    def generateCode(self):
        """
        Generate the MathProg code for this Variable
        """
        
        return self.variable
        # return SupportGenCode.emitVariable(self.variable)

class Number(Expression):
    """
    Class representing a number node in the AST of the MLP
    """

    def __init__(self, number):
        """
        Set the number
        
        :param number: float
        """
        
        self.number = number
    
    def __str__(self):
        """
        to string
        """
        
        return str(self.number)

    def __len__(self):
        """
        length method
        """

        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]

    def setupEnvironment(self):
        """
        Do nothing
        """

        pass

    def generateCode(self):
        """
        Generate the MathProg code for this Number
        """
        
        return str(self.number)
        # return SupportGenCode.emitNumber(self.number)
