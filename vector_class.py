import math,operator
#by gloop#5445
import math,operator
#by gloop#5445
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __iter__(self):
        yield from (self.x,self.y,self.z)
    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val or self.z == val)
    def __bool__(self):
        return bool(self.x or self.y or self.z)
    def length(self):
        return math.hypot(self.x,self.y,self.y)
    def lerp(self,other,t):
        return vec3(
            (1-t)*self.x+t*other.x,
            (1-t)*self.y+t*other.y,
            (1-t)*self.z+t*other.z
            )
    def distance(self,other):
        return math.hypot(self.x-other.x,self.y-other.y,self.z-other.z)
    def sign(self):
        return vec3(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0,
        1 if self.z>0 else -1 if self.y<0 else 0
        )
    def in_box(self,minimum,maximum,inclusive=True):
        min_x,min_y,min_z = minimum
        max_x,max_y,max_z = maximum
        if inclusive:
            return min_x<=self.x<=max_x and min_y<=self.y<=max_y and min_z<=self.z<=max_z
        else:
            return min_x<self.x<max_x and min_y<self.y<max_y and min_z<self.y<max_z
    def clamp(self,minimum,maximum):
        return vec3(
        max(minimum.x, min(maximum.x, self.x)),
        max(minimum.y, min(maximum.y, self.y)),
        max(minimum.z, min(maximum.z, self.z))
        )
    def _equality_op(op):
        def _vec_op(a,b):
            if type(b) == vec3:
                return op(a.x,b.x) and op(a.y,b.y) and op(a.z,b.z)
            if type(b) in (list,tuple):
                return op(a.x,b[0]) and op(a.y,b[1]) and op(a.z,b[2])
            if type(b) in (int,float):
                return op(a.x,b) and op(a.y,b) and op(a.z,b)
        return _vec_op
    def _arithmetic_op(op):
        def _vec_op(a,b):
            if type(b) == vec3:
                return vec3(op(a.x,b.x), op(a.y,b.y), op(a.z,b.z))
            if type(b) in (list,tuple):
                return vec3(op(a.x,b[0]), op(a.y,b[1]), op(a.z,b[2]))
            if type(b) in (int,float):
                return vec3(op(a.x,b), op(a.y,b), op(a.z,b))
        return _vec_op
    def _generic_op(op):
        def _vec_op(a):
            return vec3(op(a.x), op(a.y), op(a.z))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _arithmetic_op(operator.mul)
    __radd__ = _arithmetic_op(operator.add)
    __rsub__ = _arithmetic_op(operator.sub)
    __rtruediv__ = _arithmetic_op(operator.truediv)
    __rfloordiv__ = _arithmetic_op(operator.floordiv)
    __rmod__ = _arithmetic_op(operator.mod)
    __rpow__ = _arithmetic_op(operator.pow)

    __mul__ = _arithmetic_op(operator.mul)
    __add__ = _arithmetic_op(operator.add)
    __sub__ = _arithmetic_op(operator.sub)
    __truediv__ = _arithmetic_op(operator.truediv)
    __floordiv__ = _arithmetic_op(operator.floordiv)
    __mod__ = _arithmetic_op(operator.mod)
    __pow__ = _arithmetic_op(operator.pow)
    __floor__ = _generic_op(math.floor) 
    __round__ = _generic_op(round)
    __ceil__ = _generic_op(math.ceil)
    __trunc__ = _generic_op(math.trunc)
    __abs__ = _generic_op(abs)

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __iter__(self):
        yield from (self.x,self.y)
    def __repr__(self):
        return f"vec2({self.x}, {self.y})"
    def __hash__(self):
        return hash((self.x, self.y))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val)
    def __bool__(self):
        return bool(self.x or self.y)
    def length(self):
        return math.hypot(self.x,self.y)
    def lerp(self,other,t):
        return vec2((1-t)*self.x+t*other.x,(1-t)*self.y+t*other.y)
    def distance(self,other):
        return math.hypot(self.x-other.x,self.y-other.y)
    def sign(self):
        return vec2(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0
        )
    def in_box(self,minimum,maximum,inclusive=True):
        min_x,min_y = minimum
        max_x,max_y = maximum
        if inclusive:
            return min_x<=self.x<=max_x and min_y<=self.y<=max_y
        else:
            return min_x<self.x<max_x and min_y<self.y<max_y
    def clamp(self,minimum,maximum):
        return vec2(
        max(minimum.x, min(maximum.x, self.x)),
        max(minimum.y, min(maximum.y, self.y))
        )
    def _equality_op(op):
        def _vec_op(a,b):
            if type(b) == vec2:
                return op(a.x,b.x) and op(a.y,b.y)
            if type(b) in (list,tuple):
                return op(a.x,b[0]) and op(a.y,b[1])
            if type(b) in (int,float):
                return op(a.x,b) and op(a.y,b)
        return _vec_op
    def _arithmetic_op(op):
        def _vec_op(a,b):
            if type(b) == vec2:
                return vec2(op(a.x,b.x), op(a.y,b.y))
            if type(b) in (list,tuple):
                return vec2(op(a.x,b[0]), op(a.y,b[1]))
            if type(b) in (int,float):
                return vec2(op(a.x,b), op(a.y,b))
        return _vec_op
    def _generic_op(op):
        def _vec_op(a):
            return vec2(op(a.x), op(a.y))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _arithmetic_op(operator.mul)
    __radd__ = _arithmetic_op(operator.add)
    __rsub__ = _arithmetic_op(operator.sub)
    __rtruediv__ = _arithmetic_op(operator.truediv)
    __rfloordiv__ = _arithmetic_op(operator.floordiv)
    __rmod__ = _arithmetic_op(operator.mod)
    __rpow__ = _arithmetic_op(operator.pow)

    __mul__ = _arithmetic_op(operator.mul)
    __add__ = _arithmetic_op(operator.add)
    __sub__ = _arithmetic_op(operator.sub)
    __truediv__ = _arithmetic_op(operator.truediv)
    __floordiv__ = _arithmetic_op(operator.floordiv)
    __mod__ = _arithmetic_op(operator.mod)
    __pow__ = _arithmetic_op(operator.pow)
    __floor__ = _generic_op(math.floor) 
    __round__ = _generic_op(round)
    __ceil__ = _generic_op(math.ceil)
    __trunc__ = _generic_op(math.trunc)
    __abs__ = _generic_op(abs)

