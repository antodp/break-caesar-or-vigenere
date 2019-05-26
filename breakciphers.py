import frequtil as fu
import oldCiphers as oc

ITALIAN_OCC = fu.calculate_occourrences_f('Soffocare-20--20Chuck-20Palahniuk.txt')
ITALIAN_FREQS = fu.calculate_frequencies(ITALIAN_OCC)
DEF_MEAN_VAL = fu.calculate_mean_val_transp('Soffocare-20--20Chuck-20Palahniuk.txt', ITALIAN_FREQS)
QUAD_OCC = fu.ngrams_occ('Soffocare-20--20Chuck-20Palahniuk.txt', 4)

def transpose_or_caesar(txt, alpha = DEF_MEAN_VAL, padding = '*', printprog = False):


	'''

	transpose_or_caesar find the cipher used to encrypt the text (@txt)

	@alpha : chi-test value used as discriminant to indicate the cipher
	@padding : padding character needed to detect if a transpose cipher was used
	@printprog : boolean value, if True progress is printed

	'''


	if padding in txt:
		if printprog: print 'Separator character found in the cyphertext! Transpose cipher was used!'
		return 'transpose'

	txt_chi = fu.chi_squared(txt, ITALIAN_FREQS)

	if txt_chi > alpha: #if chi-test value > alpha : caesar cipher is detected
		if printprog: print 'Probably the used cipher is caesar cypher.. trying to decipher..'
		return 'caesar'
	else: #else : transpose cipher is detected
		if printprog: print 'Probably the used cipher is transpose cypher.. trying to decipher..'
		return 'transpose'

def score_msg(msg, qdgrams = QUAD_OCC):

	'''

	score_msg return fit score given quadgrams occourrences
	return value @score is given by adding frequencies of quadgrams found in @msg

	@msg : encrypted text
	@qdgrams : quadgrams occourrences (previously calculated)

	'''
	score = 0
	msg = ''.join(ch.lower() for ch in msg if ch.isalpha()) #remove non alphabetic characters
	for qg in range(0, len(msg)-4): #test score for each quadgram in @msg
		if msg[qg:qg+4] in qdgrams:
			score += (float(qdgrams[msg[qg:qg+4]])/len(qdgrams))
	return score

def break_caesar(msg, freq = ITALIAN_FREQS, alphabet = fu.alfabeto, printprog = False):

	'''

	break_caesar perform a brute-force attack on @msg and return the key such that caesar_dec(msg, found_key) has the lowest chi-test value

	@msg : encrypted text (with caesar cipher)
	@freq : letter frequency dictionary
	@alphabet : alphabet used in msg
	@printprog : boolean value, if True progress is printed

	'''
	encr_strings = []
	chi_values = []
	for i in range(0,len(alphabet)):
		imsg = oc.caesar_dec(msg, i+1)
		chi_values.append(fu.chi_squared(imsg, freq))
		encr_strings.append(imsg)
		if printprog: print 'key : ' + str(i+1) + ' plaintext : ' + imsg + '\tchi_squared_val : ' + str(chi_values[i])

	min_index = chi_values.index(min(chi_values))
	key = min_index + 1

	if printprog:
		print 'plaintext: ' + encr_strings[min_index]
		print 'key is probably: ' + str(key)

	return key

def break_transpose(msg, quad_occ = QUAD_OCC, printprog = False):

	'''

	break_transpose perform a brute-force attack on @msg and return the key such that transpose_dec(msg, found_key) has the highest score

	@msg : encrypted text (with transpose cipher)
	@quad_occ : quadgrams occourrences dictionary (previously calculated)
	@printprog : boolean value, if True progress is printed

	'''

	scores = []
	for i in range(0, len(msg)/2):
		to_ex = oc.transpose_dec(msg, i+1)
		scores.append(score_msg(to_ex, quad_occ))
		if printprog: print 'key : ' + str(i+1) + ' plaintext: ' + to_ex + '\t score: ' + str(scores[i])

	max_index = scores.index(max(scores))
	if printprog: print 'key is probably ' + str(max_index+1) + ' and the message is: ' + oc.transpose_dec(msg, max_index+1)

	return max_index+1

def break_cipher_unknown(msg):

	'''

	break_cypher_unknown takes only @msg argument and test with transpose_or_caesar function which cipher is used
	return value is a tuple having for first component the key calculated and second is the decrypted text

	@msg : encrypted text

	'''

	if transpose_or_caesar(msg) == 'caesar':
		key = break_caesar(msg)
		return key, oc.caesar_dec(msg, key)
	else:
		key = break_transpose(msg)
		return key, oc.transpose_dec(msg, key)
