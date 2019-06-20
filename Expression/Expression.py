class Expression:
    def __init__(self):
        self.value = []

    def addSubExpr(self,sub):
        self.value.append(sub)

    def __str__(self):
        s = ""
        for i in range(len(self.value)):
            if i is not len(self.value) - 1:
                s += str(self.value[i]) + " "
            else:
                s += str(self.value[i])
        return s

###ATOMICS

##OPERANDS

#Class for numerical constants
class Constant:
    def __init__(self,value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

#Class for symbolic constants 
class Variable:
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

##OPERATORS
class Addition:
    def __init__(self):
        self.value = "+"
    
    def __str__(self):
        return str(self.value)

class Subtraction:
    def __init__(self):
        self.value = "-"

    def __str__(self):
        return str(self.value)

###STRUCTURES

class Fraction:
    def __init__(self):
        self.numerator = None
        self.denominator = None
    
    def setnumerator(self,num):
        self.numerator = num

    def setdenominator(self,denom):
        self.denominator = denom

    def __str__(self):
        return "(" + str(self.numerator) + ")/(" + str(self.denominator) + ")"

class Multiplication:
    def __init__(self):
        self.first = None
        self.second = None

    def setfirst(self,f):
        self.first = f

    def setsecond(self,s):
        self.second = s

    def __str__(self):
        return "(" + str(self.first) + ")(" + str(self.second) + ")"

class Exponent:
    def __init__(self):
        self.base = None
        self.power = None

    def setbase(self,b):
        self.base = b

    def setpower(self,p):
        self.power = p

    def __str__(self):
        return str(self.base) + "^(" + str(self.power) + ")"

