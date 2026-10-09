import unittest,random,collections
import game
modules={'pizza-sim':game}
class Tests(unittest.TestCase):
 def test_pizza_perfect(self):
  g=modules['pizza-sim'].Shop();g.advance();g.toppings=g.recipe[1].copy();g.advance();g.bake=5;g.advance();self.assertEqual(g.total,100)
 def test_pizza_wrong(self):
  g=modules['pizza-sim'].Shop();g.advance();g.advance();g.advance();self.assertLess(g.total,100)
 def test_pizza_toppings(self):
  g=modules['pizza-sim'].Shop();g.toggle(1);self.assertFalse(g.toppings);g.advance();g.toggle(1);g.toggle(1);self.assertFalse(g.toppings)
if __name__=="__main__":unittest.main()
