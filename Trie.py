import re

class Node:
    def __init__(self):
        self.value = None
        self.is_end = False #whether this node corresponds to a word in the Trie
        self.children = {} # dict of children with key = char corresponding to edge, value = child Node
    
    def __str__(self):
        s = f"({self.value},{self.is_end})"

        if(not self.children):
            return s
        
        s += " -> ["

        for c in self.children:
            s += f"{c}: {self.children[c]}, "

        return s[:-2] + "]"
    
    def __iter__(self):
        """
        Generator of all nodes at or below self
        yields (node, string corresponding to node)
        """

        stack = [(self, "")]

        while(stack):
            node, s = stack.pop()
            yield node, s
            for child in reversed(sorted(node.children.keys())):
                stack.append((node.children[child], s + child))

class Trie:
    def __init__(self):
        self.root = Node()
    
    def __str__(self):
        return str(self.root)

    def __setitem__(self, key, value):
        """
        Adds a key with the given value to the trie,
        or reassigns the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """

        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        curr = self.root # curr will iterate through the relevant nodes

        for c in key:
            if c in curr.children:
                curr = curr.children[c]
            else:
                curr.children[c] = Node()
                curr = curr.children[c]
        curr.is_end = True
        curr.value = value



    def __getitem__(self, key):
        """
        Returns the value for the specified prefix.
        Raises a KeyError if the given key is not in the trie.
        Raises a TypeError if the given key is not a string.
        """

        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        curr = self.root

        for c in key:
            if c not in curr.children:
                raise KeyError(f"key {key} is not in the trie")
            curr = curr.children[c]
        
        if not curr.is_end:
            raise KeyError(f"key {key} is not in the trie")
        
        return curr.value
                    

    def __delitem__(self, key):
        """
        Deletes the given key from the trie if it exists.
        Raises a KeyError if the given key is not in the trie.
        Raises a TypeError if the given key is not a string.
        """

        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        if key == "":
            if not self.root.is_end:
                raise KeyError(f"key {key} is not in the trie")
            self.root.is_end = False
            return


        curr = self.root
        last = self.root # this represents the last node encountered that had more than one children or was an end node
        lastC = key[0] # this is the first edge in the path from last to key

        for c in key:
            if c not in curr.children:
                raise KeyError(f"key {key} is not in the trie")
            if(curr.is_end or len(curr.children)>1):
                last = curr
                lastC = c
            curr = curr.children[c]

        if not curr.is_end:
            raise KeyError(f"key {key} is not in the trie")
        
        curr.is_end = False

        # In the case that curr is a leaf, we have to delete all nodes from last to curr
        # effectively we are just removing the connection between last and its child in the path to curr
        if not curr.children:
            if(curr != self.root):
                del last.children[lastC]
        

    def __contains__(self, key):
        """
        Is key a key in the trie?  Returns True or False.
        Raises a TypeError if the given key is not a string.
        """

        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        try:
            v = self[key]
            return True
        except KeyError:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie
        and its children.
        Outputs in alphabetical order
        """

        for node,s in self.root:
            if(node.is_end):
                yield s, node.value


def word_frequencies(text):
    """
    Given a piece of text as a single string, creates a trie whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """

    if not isinstance(text, str):
        return TypeError("text must be a string")

    words = re.findall(r'\w+', text)
    trie = Trie()

    for word in words:
        if word in trie:
            trie[word] += 1
        else:
            trie[word] = 1
    
    return trie


def autocomplete(trie, prefix, max_count=None):
    """
    Returns the list of the most-frequently occurring elements that start with
    the given prefix.  Includes only the top max_count elements if max_count is
    specified, otherwise return all.

    Raises a TypeError if the given prefix is not a string.
    """

    if not isinstance(prefix, str):
        return TypeError("key must be a string")

    curr = trie.root
    for c in prefix:
        if c not in curr.children:
            return []
        curr = curr.children[c]

    subTrie = Trie()
    subTrie.root = curr

    subWords = [] # has (frequency, word) for all word that have prefix as prefix
    for word, freq in subTrie:
        subWords.append((freq, prefix + word))
    subWords.sort(reverse=True)

    subWords = [word for freq, word in subWords]

    if(max_count == None):
        return subWords
    
    return subWords[:max_count]


def word_filter(trie, pattern, isClean=False, dp=None):
    """
    Returns list of (word, trie[word]) for all words in the given trie that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """

    if dp == None:
        dp = {}
    
    if (trie.root, pattern) in dp:
        return dp[(trie.root, pattern)]

    if not isClean:
        pattern = re.sub(r"\*+", "*", pattern)

    if pattern == "":
        if "" in trie:
            dp[(trie.root, pattern)] = [("", trie[""])]
            return dp[(trie.root, pattern)]
        dp[(trie.root, pattern)] = []
        return dp[(trie.root, pattern)]

    # if pattern[0] is a letter traverse down that edge and recurse    
    if re.match(r'^[a-z]$', pattern[0]):
        if pattern[0] not in trie.root.children:
            dp[(trie.root, pattern)] = []
            return dp[(trie.root, pattern)]
        
        subTrie = Trie()
        subTrie.root = trie.root.children[pattern[0]]
        dp[(trie.root, pattern)] = [(pattern[0] + s, f)  for s,f in word_filter(subTrie, pattern[1:], True)]
        return dp[(trie.root, pattern)]

    # if pattern[0] is ? then traverse down all edges and recurse
    if pattern[0] == "?":
        if not trie.root.children:
            dp[(trie.root, pattern)] = []
            return dp[(trie.root, pattern)]
        ans = []
        for c in reversed(sorted(trie.root.children.keys())):
            subTrie = Trie()
            subTrie.root = trie.root.children[c]
            ans += [(c + s, f) for s,f in word_filter(subTrie, pattern[1:], True)]
        dp[(trie.root, pattern)] = ans
        return dp[(trie.root, pattern)]
    
    # if pattern[0] is * then traverse down all nodes below root and recurse
    if pattern[0] == "*":
        ans = []
        for node,t in trie.root:
            subTrie = Trie()
            subTrie.root = node
            ans += [(t + s, f) for s,f in word_filter(subTrie, pattern[1:], True)]
        dp[(trie.root, pattern)] = ans
        return dp[(trie.root, pattern)]
        
    else:
        raise KeyError("pattern must only contain lowercase english letters and * and ?")
