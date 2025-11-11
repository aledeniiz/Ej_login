#Excepciones personalizadas


class MiExcepcionTest(BaseException):
    def __init__(self, mensaje, detalles):
        self.mensaje = mensaje
        self.detalles = detalles

#raise MiExcepcionTest("Estoy lanzando una excepción personalizada")

try:
    raise MiExcepcionTest("Lanzo MiExcepcion", "Esta es la información detallada de mi excepción")
except MiExcepcionTest as e:
    print(type(e)) #Nos indica el origen de la excepción
    print(e.mensaje)
    print(e.detalles)


class MiExcepcionTest2(BaseException):
    pass

try:
    raise MiExcepcionTest2({"mensaje" : "Lanzo MiExcepcion", "detalles" : "Esta es la información detallada de mi excepción"})
except MiExcepcionTest2 as e:
    print(type(e)) #Nos indica el origen de la excepción
    dataerror = e.args[0]
    print(dataerror["mensaje"])
    print(dataerror["detalles"])


#Tratar excepciones: try - except

try:
    num1 = 5 / 0
    num2 = 2 + "3"
except ZeroDivisionError as e: 
    print("No se puede dividir por 0")
except TypeError as e:
    print("No se pueden sumar los tipos")
except Exception as e:
    print("Ha habido una excepción", type(e))
else: 
    print("No ha habido excepciones, todo bien")
finally:
    print("Hemos llegado al final del bloque")


#Assert

#assert(1==2)

def calcpromedio(list):
    return sum(list) / len(list)

assert(calcpromedio([1,2,3,4,5])==3)
#assert(calcpromedio([1,2,3,4,5])==400)


# Funcion para sumar enteros
def suma(a, b):
    assert(type(a) == int)
    assert(type(b) == int)
    return a+b

suma(3, 5)
#suma(3.0, 5.0)

class AnimalDomestico:
    pass

class AnimalSalvaje:
    pass

iguana1 = AnimalDomestico()
iguana2 = AnimalSalvaje()

assert(isinstance(iguana1, AnimalDomestico))
assert(isinstance(iguana2, AnimalSalvaje))
assert(isinstance(iguana2, AnimalDomestico))
assert(isinstance(iguana1, AnimalSalvaje))