class Animal:
  legs = 4

  def __init__(self, nm):
    self.name = nm

  def get_num_legs(self):
    return self.legs

  def greeting(self):
    return "cowers"

  def speak(self):
    return "Woof"

class Dog(Animal):
  breed = ''

  def __init__(self, nm, br):
    super().__init__(nm)
    self.breed = br

  def greeting(self):
    return "wags"

  def speak(self):
    return "bark"

class Cow(Animal):
  pass

class Bird(Animal):
  legs = 2

  def speak(self):
    return "chirp!"

class Spider(Animal):
  legs = 8

class Snake(Animal):
  legs = 0

  def speak(self):
    return "Ssssssssss"

  def greeting(self):
    return "rattle"

d1 = Dog('Fido', 'Dachsund')
c1 = Cow('Bessie')
b1 = Bird('Polly')
s1 = Spider('Charlotte')
s2 = Snake('Jack')

animals = [d1, c1, b1, s1, s2]

class Labrador(Dog):
    def __init__(self, nm):
      super().__init__(nm, 'Labrador')

    def greeting(self):
      return super().greeting() + " enthusiastically"


# add a ‘speak’ method to Animal—make up something that a generic Animal would say
# add ‘speak’ methods to Dog and Bird (but not Spider) that are like the one we added to Dog earlier. Have them say what you think Dogs and Birds would say.
# Make all the animals speak
# Add a Snake class, with appropriate choices for number of legs, greeting, and speak. Test your Snake.

for a in animals:
  print (a.name, "speaks as", a.speak(), "and", a.greeting())
