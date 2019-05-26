from random import randrange

alfabeto = list('abcdefghijklmnopqrstuvwxyz') #default alphabet

def calculate_occourrences_f(filename, alphabet = alfabeto):
	'''
	calculate_occourrences_f calculates letters occourrences given a filename
	for occourrences calculation calculate_occ function is used
	'''
	f = open(filename)
	return calculate_occ(f, alphabet)


def calculate_occ(txt, alphabet = alfabeto):

	'''
	calculate_occ calculates letters occourrences given a text (@txt)

	return value : dict containing letters and respective occourrence count
	'''

	occourrences = {letter : 0 for letter in alphabet}
	for w in txt:
		for letter in w:
			if letter.isalpha():
				occourrences[letter.lower()] += 1
	return occourrences


def calculate_frequencies(occourrences):

	'''
	calculate_frequencies calculates letters frequencies given a dict containing occourrence count
	@occourrences : occourrence count (e.g calculate_occ return value)
	'''
	sum_occ = sum(occourrences.values());
	freq = {letter : 0 for letter in occourrences}
	for i in occourrences:
		freq[i] = float(occourrences[i])/float(sum_occ)
	return freq


def chi_squared(msg, ex_freq):
	'''
	chi_squared perform chi-test for monograms (single letters) in @msg given expected frequencies (@ex_freq)
	'''

	msg_occ = calculate_occ(msg)
	chi_values = []
	nmsg = ''.join(ch for ch in msg if ch.isalpha())
	ln = len(nmsg)
	for l in msg_occ:
		if l.isalpha():
			exp = 1.0*ln*ex_freq[l]
			if exp: #if not zero
				chi_values.append(float(msg_occ[l] - exp)**2 / float(exp))
	return sum(chi_values) #return finite sum


def calculate_mean_val_transp(filename, ex_freq):

	'''
	calculate_mean_val_transp is used to calculate mean chi-test value of transposition-encrypted messages

	@filename : file name from where messages are taken
	@ex_freq : expected values for single letter frequency (input argument for chi_squared function)

	returns mean chi-test value
	'''

	chi_val = []
	with open(filename) as f:
		line = f.readline()
		while line:
			line = ''.join(ch.lower() for ch in line if ch.isalpha())
			if len(line) >= 2:
				line_value = chi_squared(line, ex_freq)
				chi_val.append(line_value)
			line = f.readline()

	return sum(chi_val)/len(chi_val)


def ngrams_occ(filename, n):

	'''

	ngrams_occ calculates n-grams occourrences in file with name @filename


	@filename : filename where n-grams are taken
	@n : length of n-gram (e.g. 4 -> quadgrams)

	return value : dict containing n-grams occourrence count

	'''

	ngrams = {}
	with open(filename) as f:
		line = f.readline()
		while line:
			line = ''.join(ch.lower() for ch in line if ch.isalpha())
			if len(line) >= n:
				for qg in range(0, len(line)-n):
					if line[qg:qg+n] in ngrams:
						ngrams[line[qg:qg+n]] += 1
					else:
						ngrams[line[qg:qg+n]] = 1
			line = f.readline()
	return ngrams
