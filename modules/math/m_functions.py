import math
import cmath


def is_complex(* args):
    for item in args:
        if isinstance(item, complex):
            return True
    return False


def sqrt(x):
    if is_complex(x):
        return cmath.sqrt(x)
    try:
        return math.sqrt(x)
    except ValueError:
        return cmath.sqrt(x)


def sin(x):
    if is_complex(x):
        return cmath.sin(x)
    return math.sin(x)


def cos(x):
    if is_complex(x):
        return cmath.cos(x)
    return math.cos(x)


def tan(x):
    if is_complex(x):
        return cmath.tan(x)
    return math.tan(x)


def asin(x):
    if is_complex(x):
        return cmath.asin(x)
    return math.asin(x)


def acos(x):
    if is_complex(x):
        return cmath.acos(x)
    return math.acos(x)


def atan(x):
    if is_complex(x):
        return cmath.atan(x)
    return math.atan(x)


def real(x):
    if is_complex(x):
        return x.real
    raise Exception({'type': 'runtime', 'message': 'Real function only works on complex numbers.'})


def imaginary(x):
    if is_complex(x):
        return x.imag
    raise Exception({'type': 'runtime', 'message': 'Imaginary function only works on complex numbers.'})


def sinh(x):
    if is_complex(x):
        return cmath.sinh(x)
    return math.sinh(x)


def cosh(x):
    if is_complex(x):
        return cmath.cosh(x)
    return math.cosh(x)


def tanh(x):
    if is_complex(x):
        return cmath.tanh(x)
    return math.tanh(x)


def asinh(x):
    if is_complex(x):
        return cmath.asinh(x)
    return math.asinh(x)


def acosh(x):
    if is_complex(x):
        return cmath.acosh(x)
    return math.acosh(x)


def atanh(x):
    if is_complex(x):
        return cmath.atanh(x)
    return math.atanh(x)


def log(x, base=10):
    if is_complex(x):
        return cmath.log(x, base)
    return math.log(x, base)


def ln(x):
    if is_complex(x):
        return cmath.log(x, math.e)
    return math.log(x, math.e)


def intf(x):
    if is_complex(x):
        raise Exception({'type': 'runtime', 'message': 'Complex numbers cannot be used with the int function.'})
    else:
        return float(math.floor(x))


def roundf(x, pos=None):
    if is_complex(x):
        raise Exception({'type': 'runtime', 'message': 'Complex numbers cannot be used with the round function.'})
    else:
        if pos:
            if pos.is_integer():
                if pos < 0:
                    raise Exception({'type': 'runtime', 'message': 'The digit place rounded to must be non-negative.'})
                return float(round(x, int(pos)))
            else:
                raise Exception({'type': 'runtime', 'message': 'The digit place rounded to must be an integer.'})
        return float(round(x))


def lcm(a, b):
    if not a.is_integer() or not b.is_integer():
        raise Exception({'type': 'runtime', 'message': 'The LCM function only accepts integers.'})
    return a * b / float(math.gcd(int(a), int(b)))


def gcd(a, b):
    if not a.is_integer() or not b.is_integer():
        raise Exception({'type': 'runtime', 'message': 'The LCM function only accepts integers.'})
    return float(math.gcd(int(a), int(b)))

