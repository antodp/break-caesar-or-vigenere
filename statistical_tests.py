import breakciphers as bc
from random import randrange

def enc_phrase(ph):

	if len(ph) < 5:
		return None

	cipher = randrange(0,2)

	if cipher == 0:
		return bc.oc.caesar_enc(ph, randrange(2, 26))
	else:
		return bc.oc.transpose_enc(ph, randrange(2, len(ph)))

nsuccess = 0
ntested = 0
sources = ['Soffocare-20--20Chuck-20Palahniuk.txt', 'promessi_sposi_cap1.txt', 'mattiapascal.txt']

print 'Initializing the tests...'

for s in sources:
	print 'Testing phrases in ' + s
	with open(s) as f:
		txt = f.read()
		phrases = txt.split('.')
		phrases = [''.join(ch.lower() for ch in ph if ch.isalpha()) for ph in phrases]

	for ph in phrases:
		if len(ph) > 0:
			ph_enc = enc_phrase(ph)
			if ph_enc is not None:
				found_key, ph_dec = bc.break_cipher_unknown(ph_enc)
				ph_dec = ''.join(ch.lower() for ch in ph_dec if ch.isalpha())
				if ph_dec == ph:
					nsuccess += 1
				ntested += 1

success_percentage = round(float(nsuccess * 100.0) / ntested, 2)

print 'Tested ' + str(ntested) + ' and found ' + str(nsuccess) + ' valid keys'
print 'Success percentage: ' + str(success_percentage) + '%'
