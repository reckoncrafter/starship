import itertools

cycle = itertools.cycle("Aenigmata Ostraka")
counter = itertools.count(0, 2)
repeater = itertools.repeat(42, 4)

# ----

accumulator = itertools.accumulate(['einn', 'tvö', 'dru'])

chain1 = ['A', 'B', 'C']
chain2 = [1,2,3]
chained = itertools.chain(chain1, chain2)

# itertools.compress(list, selector = [0,0,1,1])
# itertools.dropwhile(lambda x: x<3, list)