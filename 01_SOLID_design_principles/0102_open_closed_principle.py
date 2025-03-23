"""
Open-Closed Principle

When you add a functionality, you should add it by extension rather than by modification > open for extension, closed for modification.
"""

# Let's define a Product class and some properties that a product may have, such as Color and Size
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

# Now we want to be able to filter by product properties
class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color: yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size: yield p

    def filter_by_size_and_color(self, products, size, color):
        for p in products:
            if p.color == color and p.size == size:
                yield p

# This doesn't scale at all! If we had 3 or more features, the amount of methods would explode!
# This is called the State Space Explosion.

# You would also be violating OCP each time you added a new feature to your products because you'd have to add new filters to this class.

# We will now use the Specification design pattern to make our solution scalable and keep the Open-Closed Principle.
# https://en.wikipedia.org/wiki/Specification_pattern
# We will create a Specification base class that contains a single is_satisfied() -> Bool method that will return True if a condition is met, and we'll create separate FeatureSpecifications classes for each feature that will implement that method.

class Specification:
    '''Base class'''
    def is_satisfied(self, item):
        """
        All classes that inherit from Specification must implement this method
        """
        raise NotImplementedError()

    def __and__(self, other):
        """
        Overloads the ampersand (&) operator, allowing us to use AND operations with different Specification objects.
        We overload the & operator because we cannot overload the "and" keyword.
        Check below for the AndSpecification code
        """
        return AndSpecification(self, other)
    
# We will now create a Filter class.
# Its method will simply pass, because the idea is that you extend by inheriting from other classes and add functionality there
# This is how you avoid modifying already existing classes!

class Filter:
    def filter(self, items, spec):
        pass

class BetterFilter(Filter):
    def filter(self, items, spec):
        """
        We're making assumptions about what items are.
        In this implementation, items are iterable.
        This is why we extend from Filter, because your logic may change according to your needs.
        """
        for item in items:
            if spec.is_satisfied(item):
                yield item

# Let's create our feature specifications

class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size

class AndSpecification(Specification):
    """
    Combinator class.
    A Combinator is a structure that combines other structures.
    """
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        """
        We will go through all of our stored args and make sure that they're all satisfied
        map() goes through every single element of self.args and applies a lambda function to them.
        The lambda takes a specification (a single argument from self.args) and checks that it's satisfied for the item we're passing as a param.
        all() checks that every single element in the map (the returns of is_satisfied) is a boolean value of True
        """
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args))

# Now let's create our sample products and product list
apple = Product('Apple', Color.GREEN, Size.SMALL)
tree = Product('Tree', Color.GREEN, Size.LARGE)
house = Product('House', Color.BLUE, Size.LARGE)

products = [apple, tree, house]

# This is how we could filter using the old/bad filter
pf = ProductFilter()

print('Green products (old):')
for p in pf.filter_by_color(products, Color.GREEN):
    print(f' - {p.name} is green')

# Let's filter now using our new and improved filter that respects OCP
bf = BetterFilter()

print('Green products (new):')
green = ColorSpecification(Color.GREEN) # We instantiate a ColorSpecification for Green
for p in bf.filter(products, green):
    print(f' - {p.name} is green')

print('Large products:')
large = SizeSpecification(Size.LARGE) # We instantiate a SizeSpecification for Large
for p in bf.filter(products, large): # Note that we're using the same filter method for both color and size
    print(f' - {p.name} is large')

print('Large blue items:')
large_blue = large & ColorSpecification(Color.BLUE) # We instantiate an AndSpecification of Large and Blue using our & overloading
for p in bf.filter(products, large_blue):
    print(f' - {p.name} is large and blue')