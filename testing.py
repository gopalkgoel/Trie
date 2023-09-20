from Trie import Trie, Node
from Trie import word_frequencies, autocomplete, word_filter

def test1():    
    t = Trie()
    
    t["bar"] = 7
    t["foo"] = 2
    t["ba"] = 1
    t["bar"] = 5
    t[""] = 15
    print(t)

    # del t["ba"]
    # print(t)

    #print(t["bar"])
    #print(t["b"]) # KeyError 
    #print(t["fo"]) # KeyError
    #print(t["ba"])

    del t["bar"]
    print(t)

    del t[""]
    print(t)

def test2():    
    t = Trie()
    
    t["bar"] = 7
    t["foo"] = 2
    t["ba"] = 1
    t["bar"] = 5
    t[""] = 15
    print(t)

    print(t["bar"])
    print(t["b"]) # KeyError 
    print(t["fo"]) # KeyError
    print(t["ba"])

def test3():    
    t = Trie()
    
    t["bar"] = 7
    t["foo"] = 2
    t["ba"] = 1
    t["bar"] = 5
    t[""] = 15
    print(t)

    print("bar" in t)
    print("" in t)
    print("b" in t)

def test4():
    t = Trie()

    t["bar"] = 7
    t["foo"] = 2
    t["ba"] = 1
    t["bar"] = 5
    t[""] = 15

    assert "bar" in t
    assert "bab" not in t

    for s,v in t:
        print(s,v)

def test5():
    text = "sally sells sally seashells on the seashore on god"
    print(word_frequencies(text))

def test6():
    text = "In the park, children played together, jumping and running with joy. Their laughter filled the air as they raced around, their tiny feet pounding the ground. The sun shone brightly overhead, casting a warm glow on the green grass. Nearby, a group of friends gathered for a picnic, spreading out a checkered blanket on the soft turf. They unpacked their lunch, sharing sandwiches, fruit, and snacks. Laughter and chatter filled the picnic area as they enjoyed their meal. As the day went on, families arrived with their furry pets, eager to enjoy the outdoors. Dogs of all sizes played fetch, chasing after balls and sticks. Cats lounged in the shade, occasionally stretching their paws. The atmosphere was one of pure delight, with everyone coming together to embrace the simple pleasures of a sunny day in the park."

    t = word_frequencies(text)
    print(autocomplete(t, "th"))

def test7():
    text = "a arch aba aqua auto aero anti area able atom avid ache error ergo euro erin eros erase"

    t = word_frequencies(text)
    print(word_filter(t, "a*o"))

# you can include test cases of your own in the block below.
if __name__ == "__main__":
    test4() 