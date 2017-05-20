import random, argparse
from collections import defaultdict

# default char-markov
class MarkovChain:

	def __init__(self, n=1):
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
			chunk = ''.join([data[n] for n in range(i, i + self.state_size + 1)])
			tuplified.append((' '.join([data[n] for n in range(i, i + self.state_size)]), data[i + self.state_size]))
		return tuplified

	# Predicts next word based on current state
	def next(self):
		possible_states = []
		if not self.state or self.state not in self.transition_dict:
			possible_states = list(self.transition_dict.keys())
		else:
			possible_states = self.transition_dict[self.state]
		self.state = random.choice(possible_states)
		return self.state

	# Generates a sequence of arbitrary length
	def generate(self, length=100, prompt=""):
		self.state = prompt
		return_seq = ""
		for _ in range(length):
			return_seq += self.next()
		return return_seq

punctuation = ['.', ',', '\n', '\"']

class WordMarkovChain(MarkovChain):

	def tupleify(self, data):
		# Turn data into list of words, then call parent
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
	def generate(self, length=500, prompt=""):
		self.state = prompt
		return_seq = ""
		for _ in range(length):
			nex = self.next()
			if nex in punctuation:
				return_seq = return_seq[:-1]
			if nex != '\n':
				nex += ' '
			return_seq += nex
		return return_seq

# Constructs Markov chain from command-line arguments

# Defaults
state_size = 1
word_based = True
output_length = 100
input_src = "data/swift.txt"
prompt = ""

parser = argparse.ArgumentParser()
parser.add_argument("--state_size", type=int, help="Size of each state, measured in either words or characters based on type")
parser.add_argument("--word_based", type=int, help="Construct Markov chain using words instead of characters")
parser.add_argument("--output_length", type=int, help="Length of generated output, measured in either words of characters based on type")
parser.add_argument("--input_src", type=str, help="Path of input file (must be .txt)")
parser.add_argument("--prompt", type=str, help="User-determined starting state for the Markov chain")
args = parser.parse_args()

if args.state_size:
	state_size = args.state_size
if args.word_based != None:
	word_based = args.word_based
if args.output_length:
	output_length = args.output_length
if args.input_src:
	input_src = args.input_src
if args.prompt:
	prompt = args.prompt

markov = MarkovChain(state_size)
if word_based:
	markov = WordMarkovChain(state_size)
markov.update(open(input_src).read())

# Generate stuff
print(markov.generate(length=output_length, prompt=prompt))