alfabeto = list('abcdefghijklmnopqrstuvwxyz')
chr_indexes = {i : c for (i,c) in zip(alfabeto, range(0, len(alfabeto)))}

'''

	Utility method per cambiare l'alfabeto a cui ci si riferisce
	alph : list di caratteri ognuno rappresentante un simbolo dell'alfabeto

'''
def change_alphabet(alph):
	if type(alph) is not list:
		print 'alphabet deve essere una lista di caratteri! (vedi sorgente del modulo)'
		return

	global alfabeto
	global chr_indexes
	alfabeto = alph
	chr_indexes = {i : c for (i,c) in zip(alfabeto, range(0, len(alfabeto)))}

'''

    Effettua la cifratura del testo con il cifrario di cesare

    key = chiave (intero)
    msg = messaggio da cifrare

    E(msg[i]) = alfabeto[indice_alfabeto(msg[i]) + key]

'''

def caesar_enc(msg, key):
	if type(key) is not int or key <= 0:
		print 'key deve essere un intero > 0'

	ret = ''

	for char in msg.lower():
			if char == ' ':
				ret += char
			else:
				ret += alfabeto[(chr_indexes[char]+key)%len(alfabeto)]
	return ret
'''

    Effettua la decifratura del testo con il cifrario di cesare

    key = chiave (intero)
    msg = messaggio da cifrare

    D(cyphr[i]) = alfabeto[indice_alfabeto(cyphr[i]) - key]

'''

def caesar_dec(cyphr, key):
	if type(key) is not int or key <= 0:
		print 'key deve essere un intero > 0'

	ret = ''

	for char in cyphr.lower():
			if char == ' ':
				ret += char
			else:
				ret += alfabeto[(chr_indexes[char]-key)%len(alfabeto)]
	return ret
'''

    Effettua la cifratura del testo con il cifrario di vigenere.
    La tabella di vigenere non viene calcolata, si affronta invece la cifratura come l'applicazione
    di un cifrario di cesare con chiavi multiple date dagli indici nell'alfabeto della chiave

    key = chiave (stringa)
    msg = messaggio da cifrare

    E(msg[i]) = cifrario_cesare(msg[i],key[i%len(key)])

'''

def vigenere_enc(msg, key):
	if type(key) is not str or key == '':
		print 'key deve essere una stringa non vuota'

	ret = ''
	keys = []

	for (char, i) in zip(msg.lower(), range(0, len(msg))):
		if char == ' ':
			ret += char
		else:
			it_key = chr_indexes[key[i%len(key)].lower()]
			ret += alfabeto[(chr_indexes[char]+it_key)%len(alfabeto)]

	return ret

'''

    Effettua la decifratura del testo con il cifrario di vigenere.
    La tabella di vigenere non viene calcolata, si affronta invece la decifratura come l'applicazione
    di un cifrario di cesare con chiavi multiple date dagli indici nell'alfabeto della chiave

    key = chiave (stringa)
    msg = messaggio da cifrare

    E(cyphr[i]) = decifra_cesare(cyphr[i], key[i%len(key)])

'''
def vigenere_dec(cyphr, key):
	if type(key) is not str or key == '':
		print 'key deve essere una stringa non vuota'

	ret = ''
	keys = []

	for (char, i) in zip(cyphr.lower(), range(0, len(cyphr))):
		if char == ' ':
			ret += char
		else:
			it_key = chr_indexes[key[i%len(key)].lower()]
			ret += alfabeto[(chr_indexes[char]-it_key)%len(alfabeto)]

	return ret


'''

    Divide la stringa in input in sottostringhe tali che len(sottostringa) <= n

    s = stringa
    n = lunghezza sottostringa

'''
def chunks(s, n):
    chs = []
    for i in range(0, len(s), n):
        chs.append(s[i:i+n])
    return chs

'''

    Effettua la cifratura del testo con un cifrario a trasposizione

    key = chiave (intero)
    msg = messaggio da cifrare

'''

def transpose_enc(msg, key):
    if key <= 0:
        print "la chiave deve essere un intero > 0!"
        return

    chs = chunks(msg, key)
    crt = ''
    for i in range(0, key):
        for c in chs:
            if len(c) < i + 1:
                crt += '*'
            else:
                crt += c[i]
    return crt


'''

    Effettua la decifratura del testo cifrato sfruttando la funzione transpose_enc
    la chiave passata a transpose_enc (key_d) e' uguale alla lunghezza del testo cifrato
    diviso la chiave usata per la cifratura (key_e)

    key_d = len(cypher_text) / key_e

    key_e = chiave usata per la cifratura
    msg = testo cifrato da decifrare

'''
def transpose_dec(msg, key_e):
    if key_e <= 0:
        print "la chiave deve essere un intero > 0"
        return

    key_d = len(msg) / key_e
    return transpose_enc(msg, key_d)
