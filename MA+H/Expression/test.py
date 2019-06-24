from Expression import *

E = Expression()

#Relevant Constants
a = Variable("x")
b = Variable("y")

#Multiply the constants 
m = Multiplication()
m.setfirst(a)
m.setsecond(b)

#Making a fractional exponenet
one = Constant(1)
two = Constant(2)
power = Fraction()
power.setnumerator(one)
power.setdenominator(two)

e = Exponent()
e.setbase(a)
e.setpower(power)

#Create a fraction
f = Fraction()
f.setnumerator(m)
f.setdenominator(e)

#Add the pieces 
plus = Addition()
minus = Subtraction()

#Define the second part of the expression
ea = Exponent()
ea.setbase(a)
ea.setpower(two)

eb = Exponent()
eb.setbase(b)
eb.setpower(two)

E.addSubExpr(f)
E.addSubExpr(plus)
E.addSubExpr(ea)
E.addSubExpr(minus)
E.addSubExpr(eb)

print(E)