import sys, random
from collections import defaultdict

class MarkovChain:

	def __init__(self):
		self.transition_dict = defaultdict(lambda: [])
		self.state = ""

	# Updates transition matrix with new data
	def update(self, data):
		previous_word, current_word = "", ""
		for char in data:
			if char == ' ':
				if previous_word:
					self.transition_dict[previous_word] += [current_word]
				previous_word, current_word = current_word, ""
			elif char == '.' and previous_word:
				if previous_word:
					self.transition_dict[previous_word] += [current_word]
				previous_word, current_word = current_word, '.'
			elif char == ',' and previous_word:
				if previous_word:
					self.transition_dict[previous_word] += [current_word]
				previous_word, current_word = current_word, ','
			elif char == '\n' and previous_word:
				if previous_word:
					self.transition_dict[previous_word] += [current_word]
				previous_word, current_word = current_word, '\n'
			else:
				current_word += char
		self.transition_dict[previous_word] += [current_word]

	# Predicts next word based on current state
	def next(self):
		possible_states = []
		if not self.state or self.state not in self.transition_dict:
			possible_states = list(self.transition_dict.keys())
		else:
			possible_states = self.transition_dict[self.state]
		self.state = random.choice(possible_states)
		return self.state

	# Generates a sequence of arbitrary length, uses basic sentence syntax
	def generate(self, length=100, prompt=""):
		self.state = "."
		sentence = prompt
		for _ in range(length):
			next_word = self.next()
			if next_word != "." and next_word != "," and sentence != "":
				sentence += " "
			sentence += next_word
		return sentence

# Constructs Markov chain from command-line arguments
markov = MarkovChain()
for src in sys.argv[1:]:
	markov.update(open(src).read())

# Generate stuff
print(markov.generate())