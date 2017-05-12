# Phraser

Module to find the top most frequently repeated phrases in a text document. A phrase is a sequence of words, of minimum and maximum length (as defined in the module), which does not span 
sentences.

The top most frequently repeated phrases will be printed to standard output with the format:

```
#rank:  (count) phrase
```

Note that ties will be ranked in arbitrary order.

## Usage

Run the program on a text file using the following command:

```
python phraser.py -i <inputfile>
```

## Known Issues

- Phraser detects and omits subphrases which are proper prefixes of phrase, but does not omit subphrases which are proper suffixes.
- Phraser currently omits all punctuation, including punctuation which might differentiate between words (i.e. well vs we'll).
