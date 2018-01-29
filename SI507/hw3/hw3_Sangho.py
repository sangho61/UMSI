'''
SI 507 W18 homework 3: Classes and Inheritance

Your discussion section:
People you worked with:

######### DO NOT CHANGE PROVIDED CODE ############
'''

#######################################################################
#---------- Part 1: Class
#######################################################################

'''
Task A
'''
from random import randrange
import random
class Explore_pet:
  boredom_decrement = -4
  hunger_decrement = -4
  boredom_threshold = 6
  hunger_threshold = 10
  def __init__(self, name="Coco"):
    self.name = name
    self.hunger = randrange(self.hunger_threshold)
    self.boredom = randrange(self.boredom_threshold)

  def mood(self):
    if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
        return "happy"
    elif self.hunger > self.hunger_threshold:
        return "hungry"
    else:
        return "bored"

  def __str__(self):
    state = "I'm " + self.name + '. '
    state += 'I feel ' + self.mood() + '. '
    if self.mood() == 'hungry':
      state += 'Feed me.'
    if self.mood() == 'bored':
      state += 'You can teach me new words.'
    return state
coco = Explore_pet()
#your code begins here . . .
coco.hunger = 5
coco.boredom = 12
print(coco)
brian = Explore_pet('Brian')
brian.hunger = 11
print(brian)


'''
Task B
'''
#add your codes inside of the Pet class
class Pet:
  boredom_decrement = -4
  hunger_decrement = -4
  boredom_threshold = 6
  hunger_threshold = 10

  def __init__(self, name="Coco"):
    self.name = name
    self.hunger = randrange(self.hunger_threshold)
    self.boredom = randrange(self.boredom_threshold)
    self.words = ["Hello"]

  def mood(self):
    if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
        return "happy"
    elif self.hunger > self.hunger_threshold:
        return "hungry"
    else:
        return "bored"

  def __str__(self):
    state = "I'm " + self.name + '. '
    state += 'I feel ' + self.mood() + '. '
    if self.mood() == 'hungry':
      state += 'Feed me.'
    if self.mood() == 'bored':
      state += 'You can teach me new words.'
    return state

  def clock_tic(self):
      self.hunger = self.hunger + 2
      self.boredom = self.boredom + 2

  def say(self):
      print("I know how to say:")
      for w in self.words:
        print(w)

  def teach(self, word):
    self.words.append(word)
    self.boredom += self.boredom_decrement
    if self.boredom < 0:
      self.boredom = 0

  def feed(self):
    self.hunger += self.hunger_decrement
    if self.hunger < 0:
      self.hunger = 0

  def hi(self):
    print(random.choice(self.words))

'''
Task C
'''

def teaching_session(my_pet,new_words):
  #your code begins here . . .
  new_set = []

  for word in new_words:
    if word not in my_pet.words:
      my_pet.teach(word)
    else:
      new_set.append(word)

  my_pet.hi()
  print(my_pet)
  if my_pet.mood() == "hungry":
    my_pet.feed()
  my_pet.clock_tic()

aroa = Pet("Aroa")
teaching_session(aroa,['I am sleepy', 'You are the best','I love you, too'])


#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################
'''
Task A: Dog and Cat
'''
#your code begins here . . .
class Dog(Pet):
  def __str__(self):
    state = "I'm " + self.name + ', arrf! '
    state += 'I feel ' + self.mood() + ', arrf!'
    if self.mood() == 'hungry':
      state += 'Feed me, arrf!'
    if self.mood() == 'bored':
      state += 'You can teach me new words, arrf!'
    return state

class Cat(Pet):
  def __init__(self, name, meow_count):
    self.name = name
    self.meow_count = meow_count
    self.hunger = randrange(self.hunger_threshold)
    self.boredom = randrange(self.boredom_threshold)
    self.words = ["Hello"]

  def hi(self):
    randomword = random.choice(self.words)
    print(randomword*self.meow_count)


'''
Task B: Poodle
'''
#your code begins here . . .
class Poodle(Dog):
  def dance(self):
    return "Dancing in circles like poodles do!"

  def say(self):
    print(self.dance())
    Dog.say(self)

bob = Poodle("Bob")
bob.say()

kay = Cat("Kay", 5)
kay.hi()
