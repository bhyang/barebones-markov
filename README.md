# barebones-markov-implementation
Barebones implementation of Markov chains for text generation.
No added dependencies or libraries.
## Getting started
To get a taste, just clone the repo and try:
```
$ python markov.py data/swift.txt
```
It can also take multiple command-line arguments, which makes for some interesting combinations:
```
$ python markov.py data/swift.txt data/trump.txt data/bible.txt
```
## How it works
The implementation is only around 60 lines long and most of that is just hard-coding basic grammar. The state space of this Markov chain is based only on single words, so it only looks at the most recent word to predict the next one in the sequence (periods, commas, and line breaks are also counted as words). As a result, the Markov chain can't really capture meaning well, though it can produce text with the flavor of the input. More on Markov chains [here](https://en.wikipedia.org/wiki/Markov_chain).
## To-Do
* Character-by-character Markov chain
* Allow prompting
* Cleaner grammar handling
