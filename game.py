#!/usr/bin/env python3
"""Offline fictional pizza-shop cooking puzzle, not cooking safety advice."""
import curses,random
from ui import put,run
INGREDIENTS=('Sauce','Cheese','Pepperoni','Mushroom','Olive','Pepper')
RECIPES=(('Classic cheese',{0,1}),('Pepperoni',{0,1,2}),('Garden',{0,1,3,4,5}),('Mushroom',{0,1,3}),('Olive pepper',{0,1,4,5}))
class Shop:
 def __init__(self,seed=0):self.rng=random.Random(seed);self.number=0;self.total=0;self.new()
 def new(self):self.recipe=self.rng.choice(RECIPES);self.toppings=set();self.phase='dough';self.bake=0;self.message='Roll the dough: Enter.'
 def advance(self):
  if self.phase=='dough':self.phase='toppings';self.message='Toggle toppings1-6. Enter to bake.'
  elif self.phase=='toppings':self.phase='oven';self.message='Space adds one oven tick. Aim for5. Enter serves.'
  elif self.phase=='oven':
   correct=self.toppings==self.recipe[1];baked=self.bake==5;points=(60 if correct else max(0,60-15*len(self.toppings^self.recipe[1])))+(40 if baked else max(0,40-10*abs(self.bake-5)));self.total+=points;self.number+=1;self.phase='served';self.message=f'Pizza served: {points}/100. '+('Perfect!' if points==100 else 'Check toppings and oven next time.')+' Enter for next order.'
  elif self.phase=='served' and self.number<5:self.new()
 def toggle(self,i):
  if self.phase!='toppings' or i not in range(6):return
  if i in self.toppings:self.toppings.remove(i)
  else:self.toppings.add(i)

def loop(s):
 g=Shop()
 while True:
  h,w=s.getmaxyx();s.erase()
  if w<60 or h<23:
   put(s,2,1,'Resize to60x23. Esc/q exits.');s.refresh();key=s.getch()
   if key in (27,ord('q')):return
   continue
  put(s,0,1,f'PIZZA SHOP SIM  order {min(5,g.number+1)}/5 total {g.total}/500',curses.A_BOLD)
  put(s,2,2,'Customer wants: '+g.recipe[0]);put(s,3,2,'Recipe: '+', '.join(INGREDIENTS[i] for i in sorted(g.recipe[1])))
  for i,name in enumerate(INGREDIENTS):put(s,5+i*2,2,f'{i+1}. '+('[x] ' if i in g.toppings else '[ ] ')+name)
  if w>=60 and h>=23:
   cx=w*3//4;cy=h//2;radius=min((w//2-4)//2,(h-8)//2)
   for y in range(-radius,radius+1):
    for x in range(-radius,radius+1):
     if x*x+y*y<=radius*radius:put(s,cy+y,cx+x*2,'██' if x*x+y*y>(radius-1)**2 else '░░')
   for j,i in enumerate(sorted(g.toppings)):put(s,cy-3+j,cx-4,INGREDIENTS[i][:8],curses.A_BOLD)
  put(s,h-5,2,'Stage: '+g.phase+'  Oven: '+'■'*g.bake+' '+str(g.bake)+'/5');put(s,h-3,2,'Shift finished. R starts a new shift.' if g.number>=5 else g.message);put(s,h-1,1,'1-6 toppings | Enter next/serve | Space oven tick | R restart | Esc/q exit');s.refresh();key=s.getch()
  if key in (27,ord('q')):return
  if key==ord('r'):g=Shop()
  elif ord('1')<=key<=ord('6'):g.toggle(key-ord('1'))
  elif key==ord(' ') and g.phase=='oven':g.bake=min(10,g.bake+1)
  elif key in (10,13) and g.number<5:g.advance()
if __name__=='__main__':
 import sys
 if '--version' in sys.argv:print('1.0.0')
 else:raise SystemExit(run(loop))
