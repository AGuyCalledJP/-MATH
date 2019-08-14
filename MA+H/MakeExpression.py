from Expression import *

# take second element for sort
def xcoord(elem):
    return elem[1]

def ycoord(elem):
    return elem[2]

#prediction -> class_id, x, y, w, h
def OrderInputs(predictions):
    predictions = sorted(predictions, key=xcoord)
    for prediction in predictions:
        print("Found " + str(prediction[0]) + " `centered at (" + str(prediction[1]) + "," + str(prediction[2]) + ")" )
    return predictions

#Takes what is presumed to be one unified chunk of math
def CreateExpression(predictions):
    E = Expression()
    last = None
    for prediction in predictions:
        label = prediction[0]
        e = None
        if ord(label) >= 48 and ord(label) <= 57:
            if type(last) is Constant:
                last.addVal(label)
                e = last
                continue
            else:
                e = Constant(label)
        elif ord(label) == 42 or ord(label) == 120:
            e = Multiplication()
        elif ord(label) == 43 or ord(label) == 116:
            e = Addition()
        elif ord(label) == 45:
            e = Subtraction()
        elif ord(label) == 47:
            e = Division()
        elif (ord(label) >= 65 and ord(label) <= 90) or (ord(label) >= 97 and ord(label) <= 122):
            e = Variable(label)
        else:
            print("Unrecognized input")
        last = e
        E.addSubExpr(e)
    return E