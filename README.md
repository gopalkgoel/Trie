# Code Sample for DE Shaw

This code implements the Trie (prefix tree) data structure in python. Tries are useful for things like efficient data retrieval, searching, and prefix matching.

Along with the data structure implementation, I’ve also implemented two useful algorithms, namely `autocomplete` and `word_filter`. Given a Trie which contains some database of words, the `autocomplete` function allows you to find the most commonly used words starting with a certain prefix, and the `word_filter` function allows you to find all words matching simple regex patterns that only use characters and `*` and `?`.

To initialize a Trie, write `trie = Trie()`. Adding keys and values to the Trie work syntactically the same as a dictionary in python.
