# Autocomplete
Autocomplete is a simple experiment in building a autocomplete querying system within the console.

## Process
Before starting the project, I had heard about Tries and wanted to experiment with them. So, this project was created. 

### Iteration 1
The first iteration of the project uses a Trie to store the words and query the stored words that start with a particular prefix.

### Iteration 2/Final Iteration
The second iteration of the program uses a Prefix Hash Tree. After doing some research, I found that both a Trie and Radix Tree
will be too slow for our purposes when the there is enough data stored in the structure. [Prexify](https://prefixy.github.io) has 
explanation of what a prefix hash tree is and why it should be used over a Trie and Radix Tree. Using a prefix hash tree, we 
can fetch a list of words that start with the given prefix in O(1), something that is not possible with a Trie or a Radix Tree. 

In this case, we are using more memory to reduce the time in which a fetch a list of completions for a given prefix, but 
since autocomplete suggestion need to be shown very quickly, it is important to prioritize speed. 

So, the second data structure is a dictionary where the key is the prefix and the value is a set of string that will be the
completion strings.

### Thought Process
- ~~Iteration 2: Radix Tree~~ Will not be done due to the fact the runtime for this structure is not fast enough. Replaced by
Prefix Hash Tree.  
- Find other, faster data structures for fetching, even if insertion is slower, has been found, will be using Prefix Hash Tree
because of the explanation at the following link: https://prefixy.github.io

