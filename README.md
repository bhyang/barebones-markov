# barebones-markov-implementation
Barebones implementation of Markov chains for text generation.
No added dependencies or libraries.
```
In the clear yet?
In the middle of the woods yet?
Are we out of style
We never grow up
Oh, don't leave;
It's been you all along.
So, why can't tell anyone
That you've got a girl at home,
And everyone knows
That you’ll make it all this time I'm telling you,
Last time I'm wishing star
He's the song in the football team
But I do
Turn the lock and put my head down
Trying to figure out when I let you know it used to the garden to see you again
```
## Features
To get a taste, just clone the repo and run it with the default settings:
```
$ python markov.py
$ python markov.py --output_length 500  # Vary the length of the output
```
You can also run the word-based Markov chain which generates text word-by-word instead of character-by-character:
```
$ python markov.py --word_based 1
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
We can also prompt the Markov chain, though this doesn't do much unless your prompt includes a phrase/chunk that is present in the input data.
```
$ python markov.py --prompt "establish justice, " --input_src data/preamble.txt
```
To store the generated text, we can save it to an output file:
```
$ python markov.py --output_file output.txt
```
## How it works
The script processes the text from `input_src` and tracks how frequently each character/word appears following the previous sequence of characters/words of length `state_size`. Each prediction only uses the previous state in order to predict the next state, which makes this a Markov chain. More on Markov chains [here](https://en.wikipedia.org/wiki/Markov_chain).
The character-based implementation is only about 45 lines long, but when properly tuned it can still learn syntax surprisingly well. With a `state_size` of only 1, we get gibberish:
```
Grow
Ares thou for ove gh
Sare he it you't I'r acate stitas y, thind hacke aghohautch s t d m ckest ley w, don'r bl sthe n alyolela yofume ho fr oong t d ad
Ar s s s kssat a I'mevele ppe gangr r, il w
Satemyou me h, seee d.
Aninicowarisstas whe rouchisatimy, clyoplasapyo
```
At a `state_size` of around 5 or so, we begin to see reasonably coherent text. I've found that a `state_size` of 8 produces the most optimal results for `swift.txt`, which is why it's the default setting. As we increase the `state_size` beyond 15 or so the output looks almost identical, which is because the Markov chain just starts reproducing the original data:
```
So it's gonna be forever
Or it's gonna go down in flames
You can tell me when it's over
If the high was worth the pain
Got a long list of ex-lovers
They'll tell you I'm insane
'Cause you know I love the players
And you love the game
```
The word-based implementation is pretty similar (with scaled down `state_size` values) except the spacing is hard-coded. While the two can produce similar results on certain inputs, the word-based implementation has the advantage with smaller input files since the character-based implementation needs fairly large datasets to learn the syntax. However, the character-based implementation is more flexible/generalizable:
```
充分发挥他们在社会主义的过渡。生产资料的社会保障制度。
第一百三十条 民族自治地方。
第六十二条 国有经济的合法权利和利益，保护珍贵的动物和植物。
禁止任何组织或者个人依照中华人民共和国实行依法治国家。 社会主义初级阶段。
国家发展自然科学和社会帮助安排盲、聋、哑和其他危害国家的、社会团体和个人的干涉。
第五十七条 全国人民代表大会补选。
中华人民共和国主席、自治州、自治州、自治区、直辖市国家权力机关的决定和命令；
```
