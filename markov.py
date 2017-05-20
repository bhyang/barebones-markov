import random, argparse
from collections import defaultdict

class MarkovChain:

	def __init__(self, n=8):
		self.transition_dict = defaultdict(lambda: [])
		self.state = ""
		self.state_size = n

	# Updates transition matrix with new data
	def update(self, data):
		tupled_data = self.tupleify(data)
		for c in range(len(tupled_data)):
			self.transition_dict[tupled_data[c][0]].append(tupled_data[c][1])

	# Returns a list of 2-tuples, where the first element is the state and the second is the rest
	def tupleify(self, data):
		assert self.state_size < len(data), "state_size exceeds the total length of the data"
		tuplified = []
		for i in range(len(data) - self.state_size):
			chunk = tuple([data[n] for n in range(i, i + self.state_size + 1)])
			tuplified += [(chunk[:-1], chunk[1:])]
		return tuplified

	# Predicts next word based on current state
	def next(self):
		possible_states = []
		if not self.state or self.state not in self.transition_dict:
			possible_states = list(self.transition_dict.keys())
		else:
			possible_states = self.transition_dict[self.state]
		self.state = random.choice(possible_states)
		return self.state[-1]

	# Generates a sequence of arbitrary length
	def generate(self, prompt, length=500):
		assert length > len(prompt), "Prompt can't be longer than output_length"
		if self.state_size < len(prompt):	# If the prompt is too small, randomly pick from all states that contain the prompt
			self.state = random.choice([state for state in self.transition_dict if prompt in state] or self.transition_dict)
		else:
			self.state = prompt[-self.state_size:]
		return_seq = prompt
		for _ in range(length - len(prompt)):
			return_seq += self.next()
		return return_seq

punctuation = ['.', ',', '\n', ':', '?']

class WordMarkovChain(MarkovChain):

	def __init__(self, n=2):
		MarkovChain.__init__(self, n)

	def tupleify(self, data):
		assert self.state_size < len(data), "state_size exceeds the total length of the data"
		word_list = []
		current_word = ""
		for c in range(len(data)):
			if data[c] == ' ':
				if current_word:
					word_list.append(current_word)
					current_word = ""
			elif data[c] in punctuation:
				if current_word:
					word_list.append(current_word)
					word_list.append(data[c])
					current_word = ""
			else:
				current_word += data[c]
		word_list += current_word

		return MarkovChain.tupleify(self, word_list)

	# Generates a sequence of arbitrary length
	def generate(self, prompt, length=100):
		self.state = prompt
		return_seq = ""
		for _ in range(length):
			return_seq += self.next() + ' '
		return scrub(return_seq)

# Uses some basic guidelines to clean up the generated texts
def scrub(text):
	while text[0] in punctuation + [' ']:
		text = text[1:]
	delete = []
	for i in range(len(text)):
		if text[i - 1] == '\n' and text[i] == ' ':
			delete += [i]
		if text[i] in punctuation and text[i - 1] == ' ':
			delete += [i - 1]
	return ''.join([text[i] for i in range(len(text)) if i not in delete])

# Constructs Markov chain from command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--state_size", type=int, help="Size of each state, measured in either words or characters based on type")
parser.add_argument("--word_based", default=0, type=int, help="Construct Markov chain using words instead of characters")
parser.add_argument("--output_length", type=int, help="Length of generated output, measured in either words of characters based on type")
parser.add_argument("--input_src", nargs="+", default="data/swift.txt", type=str, help="Path of input file (must be .txt)")
parser.add_argument("--prompt", default="", type=str, help="User-determined starting state for the Markov chain")
parser.add_argument("--output_file", type=str, help="Can print the output to a user-specified path")
args = parser.parse_args()

if args.state_size:
	markov = MarkovChain(args.state_size)
	if args.word_based:
		markov = WordMarkovChain(args.state_size)
else:
	markov = MarkovChain()
	if args.word_based:
		markov = WordMarkovChain()

if type(args.input_src) == str:
	markov.update(open(args.input_src).read())
else:
	for src in args.input_src:
		markov.update(open(src).read())

# Generate stuff
if args.output_length:
	output = markov.generate(length=args.output_length, prompt=args.prompt)
else:
	output = markov.generate(prompt=args.prompt)
if args.output_file:
	with open(args.output_file, 'w') as dest:
		dest.write(output)
print(output)