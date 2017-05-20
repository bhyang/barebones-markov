# barebones-markov-implementation
Barebones implementation of Markov chains for text generation.
No added dependencies or libraries.
## Features
To get a taste, just clone the repo and run it with the default settings:
```
$ python markov.py
$ python markov.py --output_length 500  # Vary the length of the output
```
You can also run the character-based Markov chain which generates text character-by-character, though the results are noticeably worse without any modification:
```
$ python markov.py --word_based 0
```
By default `input_src` is set to `data/swift.txt`, which contains the lyrics to Taylor Swift's complete discography. There are several examples provided in the directory to play around with.
```
$ python markov.py --input_src data/declaration-of-independence.txt
$ python markov.py --input_src data/bible.txt data/trump.txt   # Also supports multiple input sources!
```
We can increase `state_size` to try and teach more complex patterns. By default `state_size` is only 1, which severely limits the data used to predict words/characters in a sequence. For character-based Markov chains, this means that it can only look at the most recent character to guess the next.
```
$ python markov.py --state_size 10  # This uses the last 10 words/characters to predict the next
```
You can also prompt the Markov chain:
```
$ python markov.py --prompt "We the people" --input_src data/preamble.txt
```
## How it works
The implementation is only around 60 lines long and most of that is just hard-coding basic grammar. The state space of this Markov chain is based only on single words, so it only looks at the most recent word to predict the next one in the sequence (periods, commas, and line breaks are also counted as words). As a result, the Markov chain can't really capture meaning well, though it can produce text with the flavor of the input. More on Markov chains [here](https://en.wikipedia.org/wiki/Markov_chain).
## To-Do
* Prompting is still broken
* Cleaner grammar handling
