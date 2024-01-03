import abc
from queue import Queue
from collections import defaultdict
from math import lcm

class Module(abc.ABC):
  def __init__(self,name):
    self.name = name
    self.sources = []
    self.destinations = []
    self.queue = Queue()
    self.high_pulses = 0
    self.low_pulses = 0 

  def register_source(self, module):
    self.sources.append(module)

  def register_dest(self, module):
    self.destinations.append(module)

  @abc.abstractmethod
  def process_pulse(self):
    """to be implemented by each type of module"""

  def receive_pulse(self, pulse, source):
    self.queue.put((pulse,source))

  def send_pulse(self,pulse):
    for output in self.destinations:
      if pulse:
        self.high_pulses += 1
      else:
        self.low_pulses += 1
      #print(f"{self.name} -{'high' if pulse else 'low'}-> {output.name}")
      output.receive_pulse(pulse, self)


class FlipFlop(Module):
  def __init__(self, name):
    super().__init__(name)
    self.state = False
    
  def process_pulse(self):
    if self.queue.empty():
      return False
    else:
      pulse,_ = self.queue.get()
      if not pulse:
        self.state = not self.state
        self.send_pulse(self.state)
    return True

class Conjunction(Module):

  def __init__(self, name):
    super().__init__(name)
    self.state = defaultdict(lambda:False)

  def process_pulse(self):
    if self.queue.empty():
      return False
    else:
      pulse,source = self.queue.get()
      self.state[source.name] = pulse
      all_high = True
      for src in self.sources:
        if not self.state[src.name]:
          all_high = False
          break
      if all_high:
        self.send_pulse(False)
      else:
        self.send_pulse(True)
    return True

class Broadcaster(Module):
    def __init__(self):
      super().__init__("broadcaster")

    def process_pulse(self):
      if self.queue.empty():
        return False
      else:
        pulse, _ = self.queue.get()
        self.send_pulse(pulse)
      return True

class Dummy(Module):
  def __init__(self, name):
    super().__init__(name)
  
  def process_pulse(self):
    if self.queue.empty():
      return False
    else:
      pulse, _ = self.queue.get()
      if pulse: 
        self.high_pulses += 1
      else: 
        self.low_pulses += 1
    return True


with open("input.txt", "r") as f:
  lines = f.read().splitlines()

broadcaster = None
modules = {}
output_modules={}

for line in lines:
  module_id, destinations = line.split("->")
  if module_id.strip() == "broadcaster":
    broadcaster = Broadcaster()
    modules['braodcaster'] = (broadcaster, destinations)
  else:
    module_type, module_name = module_id[0], module_id[1:].strip()
    module = None
    match module_type:
      case "&":
        module = Conjunction(module_name)
      case "%":
        module = FlipFlop(module_name)
    modules[module_name] = (module, destinations)

for mod_name,(mod, destinations) in modules.items():
  for dest_name in [d.strip() for d in destinations.split(",")]:
    if dest_name in modules:
      dest = modules[dest_name][0] 
    else:
      dest = Dummy(dest_name)
      output_modules[dest_name] = dest
    mod.register_dest(dest)
    dest.register_source(mod)


def solve_part1():
  low_pulses = high_pulses = 0

  for i in range(1000):
    low_pulses += 1
    broadcaster.receive_pulse(False,None)
    queue = Queue()
    queue.put(broadcaster)
    while not queue.empty():  
      mod = queue.get()
      if mod.process_pulse():
        for dest in mod.destinations:
          queue.put(dest)
  for mod, _ in modules.values():
    low_pulses += mod.low_pulses
    high_pulses += mod.high_pulses
  print(f"Part 1: {low_pulses*high_pulses}")


def solve_part2():
  #these 4 conjunctions feed into a final conjunction which feeds to the "rx" module
  #As a result these 4 must emit a High Pulse so that "rx" get a low pulse
  final_layer_modules = [m[0] for m in modules.values() if m[0].name in ["sg", "lm", "dh", "db"]]
  high_pulse_markers ={"sg":[], "lm":[], "dh":[], "db":[]}
  high_pulse_counter = {"sg":0, "lm":0, "dh":0, "db":0}
  total_button_presses = 0

  while True:
    total_button_presses += 1
    broadcaster.receive_pulse(False,None)
    queue = Queue()
    queue.put(broadcaster)
    while not queue.empty():  
      mod = queue.get()
      if mod.process_pulse():
        for dest in mod.destinations:
          queue.put(dest)
    all_done = True
    for mod in final_layer_modules:
      if mod.high_pulses > high_pulse_counter[mod.name]:
        high_pulse_counter[mod.name] = mod.high_pulses
        high_pulse_markers[mod.name].append(total_button_presses)
        #print(f"{mod.name} high:{mod.highpulses} low:{mod.lowpulses} total: {total_button_presses}")
      if len(high_pulse_markers[mod.name]) < 2:
        all_done = False
    if all_done:
      break
  
  ans = lcm(*[v[1]-v[0] for v in high_pulse_markers.values()])
  print(f"Part 2: {ans}")

solve_part1()
solve_part2()
