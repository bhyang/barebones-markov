import sys, random
from collections import defaultdict

# default char-markov
class MarkovChain:

	def __init__(self, n):
		self.transition_dict = defaultdict(lambda: [])
		self.state = ""
		self.state_size = n    # state_size is just the number of values in each state

	# Updates transition matrix with new data
	def update(self, data):
		tupled_data = self.tupleify(data)
		for c in range(len(tupled_data)):
			self.transition_dict[tupled_data[c][0]].append(tupled_data[c][1])
		# print(self.transition_dict)

	# Returns a list of 2-tuples, where the first element is the state and the second is the rest
	def tupleify(self, data):
		assert self.state_size < len(data), "state_size exceeds the total length of the data"
		tuplified = []
		for i in range(len(data) - self.state_size):
			chunk = ''.join([data[n] for n in range(i, i + self.state_size + 1)])
			tuplified.append((' '.join([data[n] for n in range(i, i + self.state_size)]), data[i + self.state_size]))
		# print(tuplified)
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

	# # Updates transition matrix with new data
	# def update(self, data):
	# 	previous_word, current_word = "", ""
	# 	for char in data:
	# 		if char == ' ':
	# 			if previous_word:
	# 				self.transition_dict[previous_word] += [current_word]
	# 			previous_word, current_word = current_word, ""
	# 		elif char == '.' and previous_word:
	# 			if previous_word:
	# 				self.transition_dict[previous_word] += [current_word]
	# 			previous_word, current_word = current_word, '.'
	# 		elif char == ',' and previous_word:
	# 			if previous_word:
	# 				self.transition_dict[previous_word] += [current_word]
	# 			previous_word, current_word = current_word, ','
	# 		elif char == '\n' and previous_word:
	# 			if previous_word:
	# 				self.transition_dict[previous_word] += [current_word]
	# 			previous_word, current_word = current_word, '\n'
	# 		else:
	# 			current_word += char
	# 	self.transition_dict[previous_word] += [current_word]



	# # Generates a sequence of arbitrary length, uses basic sentence syntax
	# def generate(self, length=100, prompt=""):
	# 	self.state = "."
	# 	sentence = prompt
	# 	for _ in range(length):
	# 		next_word = self.next()
	# 		if next_word != "." and next_word != "," and sentence != "":
	# 			sentence += " "
	# 		sentence += next_word
	# 	return sentence

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
		# print(word_list)
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
markov = WordMarkovChain(2)
for src in sys.argv[1:]:
	markov.update(open(src).read())

# Generate stuff
print(markov.generate())