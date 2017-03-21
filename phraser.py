#!/usr/bin/env python3

'''Module to find the top most frequently repeated phrases in 
a text document. A phrase is a sequence of words, of minimum 
and maximum length (as defined in the module), which does not span 
sentences.

The top most frequently repeated phrases will be printed to 
standard output with the format:
#rank:  (count) phrase

Note that ties will be ranked in arbitrary order.'''

import sys, getopt, re, string, heapq

''' Set problem parameters: '''
minlen = 3 # minimum length of phrases, must be 1 or greater
maxlen = 10 # maximum length of phrases
top_x = 10 # return the top_x most frequently repeated phrases

def main(argv):
    '''Performs basic input checking, then performs three major steps in algorithm:
    1. Generate tree which describes all possible phrases in its depth first traversal
    2. Get all valid phrases and their appearance count from tree
    3. Sort phrases by appearance count and print top phrases'''

    inputfile = ''
    phrases = {}

    # input checking
    try:
        opts, args = getopt.getopt(argv,"hi:")
    except getopt.GetoptError:
        print("phraser.py -i <inputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("phraser.py -i <inputfile>")
            sys.exit(0)
        elif opt == '-i':
            inputfile = arg
    
    with open(inputfile, "r") as f:
        tree = build_tree(f.read())
        get_phrases(tree, "", phrases, 0)
        #print(phrases)
        print_top_x(phrases)        


def build_tree(sentences):
    '''Clean Input: Separate string into sentences based on sentence-ending 
    punctuation (; ! ?) and then strip all other punctuation.
    
    Then, Add Nodes to Tree: For each valid starting word, add the longest 
    possible phrase starting at that word to the tree. Only the longest possible 
    phrase needs to be added to the tree, because sub-phrases appear as we perform 
    depth first traversal.'''

    root = Node(0, {})

    # replace all sentence-ending punctuation with a period .
    sentences = re.sub('[;!?]', '.', sentences)
    
    for s in sentences.split('.'):
        
        # removes all punctuation in each sentence
        translator = str.maketrans('', '', string.punctuation)
        s = s.translate(translator)
        words = s.strip().split()

        # discard any empty sentences
        if (len(words) == 0):
            continue
        
        # add each largest phrase in sentence to tree
        for start in range(len(words)-minlen+1): # start index of phrase
            end = min(len(words), start+maxlen) # largest end index still in sentence
            root = add_to_node(root, words[start:end])

    return root


def add_to_node(node, phrase):
    '''Recursively add phrase to tree. Root node has all first words as its 
    children, and each other node has as its children all words which may
    follow that node's word in a phrase. Track count of phrase appearances
    while adding to tree.'''

    if (len(phrase) == 0): # end recursion when phrase is exhausted
        return node
    
    # if node has the first word of phrase as one of its children:
    if (node.children and phrase[0] in node.children):
        oldchild = node.children[phrase[0]]
        oldchild.count += 1
        oldchild = add_to_node(oldchild, phrase[1:])
        return node
    
    else: # node does not have first word of phrase as child
        newchild = Node(1, {})
        node.children[phrase[0]] = newchild
        newchild = add_to_node(newchild, phrase[1:])
        return node


class Node():
    '''Node class to store count and children of word in tree.
    count: the number of times the phrase constructed from the words between root
        and this word, in order, appears in the text
    children: a set of all possible words which follow this one in valid phrases.'''
    
    def __init__(self, count, children):
        self.count = count
        self.children = children
    
    def __repr__(self):
        return "Node: {count: %s, children: %s}" % (self.count, self.children)
    
    def has_children(self):
        return self.children == {}


def get_phrases(node, current_phrase, phrases, word_len):
    '''Generates valid phrases and counts their appearance based on tree.
    Based on recursive depth first traversal.'''

    # this is last word of phrase, add to phrases dict if phrase is long enough
    if not node.children and word_len >= minlen:
        #print(current_phrase)
        phrases[current_phrase.strip()] = node.count
        return

    # this word ends a sub-phrase of a longer phrase
    for word, child_node in node.children.items():
    
        # add to phrases dict if the sub-phrase appears more frequently than the longer phrase i.e.
        # the sub-phrase appears in places other than inside the longer phrase
        if node.count > child_node.count and word_len >= minlen:
            #print(current_phrase)
            phrases[current_phrase.strip()] = node.count
        # recurse to examine longer phrase
        get_phrases(child_node, current_phrase + str(word) + " ", phrases, word_len+1)


def print_top_x(phrases):
    '''Sorts (phrase, count) pairs by count, then prints a subset of the phrases 
    with highest count frequency. The length of the subset printed is defined by global
    variable top_x.'''
    
    i = 1
    for p in sorted(phrases.keys(), key = lambda x: phrases[x], reverse=True):
        if (i > top_x):
            break
        print("#" + str(i) + ":\t(" + str(phrases[p]) + ") " + p)
        i += 1


if __name__ == "__main__":
    main(sys.argv[1:])