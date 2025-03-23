"""
Liskov Substitution Principle

An object (such as a class) should be able to be replaced by a sub-object (such as a class that extends the first class) without breaking the program.

This code may seem a little convoluted and does not have any "fix" to the LSP violation.
"""

class Rectangle:
    """
    Rectangle base class with private properties, setters and getters
    A property is a special kind of attribute that has __get__, __set__ and/or __delete__ methods
    """
    def __init__(self, width, height):
        self._height = height # private property
        self._width = width # private property

    @property # The property decorator is used for getter methods
    def width(self):
        return self._width

    @width.setter # setter decorator for the width property 
    def width(self, value): # note that the method has the same name as the getter but different amount of params
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def area(self):
        return self._width * self._height

    def __str__(self): # string representation of a rectangle
        return f'Width: {self.width}, height: {self.height}'

class Square(Rectangle):
    """
    A square is a special case of rectangle whose height and width are equal.
    We try to represent this case with a subclass that tries to enforce a square.
    """
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    # The following 2 methods break LSP, because when we update a property, we also update the other.
    @Rectangle.width.setter
    def width(self, value):
        _width = _height = value

    @Rectangle.height.setter
    def height(self, value):
        _width = _height = value


def use_it(rc):
    """
    We'll use this method to showcase the LSP violation
    The line `rc.height = 10` will also update the width if we're using a square, which means that the value of w in the previous line will not match the actual width of our square
    LSP is broken because using a subclass (square) of our regular class (rectangle) will show different and unexpected behaviour; this happens because the setters of our square have unexpected side effects.
    """
    w = rc.width
    rc.height = 10  # we update the height of our rectangle and experience unpleasant side effects
    expected_area = int(w * 10)
    print(f'Expected an area of {expected_area}, got {rc.area}')


# This will work as expected
rc = Rectangle(2, 3)
use_it(rc)

# This will not work! LSP has been violated and you will have 2 different values
sq = Square(5)
use_it(sq)

"""
There are multiple ways of fixing this specific problem.
You probably don't need a separate subclass for a square.
You could simply add a boolean property to a rectangle that tells you whether or not it's a square.
Or maybe create a factory method.
"""