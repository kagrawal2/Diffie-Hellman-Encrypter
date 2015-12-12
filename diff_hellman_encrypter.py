import math
import random
import time

"""
	The Diffie-Hellman-Encrypter with its application as an 
	encrypter for an inputted message.

	To Do: Add a message encrypter with an input message

	by Kireet Agrawal 2015
"""


def is_prime(n):
	"""
	>>> is_prime(2)
	True
	>>> is_prime(8)
	False
	>>> is_prime(7)
	True
	"""
	b = 2
	while b <= math.sqrt(n):
		if n % b == 0:
			return False
		b += 1
	return True

def next_prime(n):
	if is_prime(n + 1):
		return n + 1
	else:
		return next_prime(n + 1)


def get_prime(x, y):
	a = 4
	while not is_prime(a):
		a = random.randint(x, y)
	return a


def get_generator(modulus, k, m):
	"""
	Returns a random primitive root modulo of a given prime mod and
	a range for which the primitive root can be found within.
	- Shows process by which this root is found.
	- mod is an input from the next_prime function return value
	"""
	tries = 0
	while tries <= ((m-k) + 1):
		gen = get_prime(k, m)
		print(gen)
		pows = [gen]
		for x in range(modulus):
			a = pows[0]
			pows.insert(0, a*gen)
		remainders = set([(x % modulus) for x in pows])
		if len(remainders) == modulus - 1:
			return gen
		tries += 1
	print("No generator found. Increasing generator range by 10 on each side.")
	l = k - 10
	n = m + 10
	if l <= 0:
		l = 1
	return get_generator(modulus, l, n)


class pEncryptor(object):

	def __init__(self, modulus, generator, name):
		self.modulus = modulus
		self.generator = generator
		self.name = name
		self.secret = 0

	def __repr__(self):
		return 'pEncryptor object called {0}'.format(self.name)

	def encrypt(self):
		self.remainder = pow(self.generator, self.secret, self.modulus)
		return self. remainder

	def decrypt(self, passed_key):
		self.key = pow(passed_key, self.secret, self.modulus)
		return self.key


def encryption_process(name, modulus, generator, secret, key):
	"""	
	Explanation of the process by which the encyption occurs with secret numbers.
	"""

	print('\n', name, 'raises the publically known generator--', str(generator),
		'by the power of their secret key number--', str(secret) + '.')
	print('Then,', name, 'takes the modulus of that number with the publically known modulus--',
		str(modulus), 'and obtains the secret key--', str(key))
	print("This process's equation is as follows:", str(generator) + '^' + str(secret),
		'mod', str(modulus), "=", str(key))

def decryption_process(name, modulus, passed, secret, key):
	"""	
	Explanation of the process by which the encyption occurs with secret numbers.
	"""
	print('\n', name, 'uses the public number they were sent--', str(passed), 
	'and raises it to the power of their original secret key number--', str(secret))
	print('Then', name, 'uses the original public modulus--', str(modulus), 'and takes the modulus to find the shared secret key',
		str(key) + '.')
	print("This process's equation is as follows:", str(passed) + '^' + str(secret), 'mod', 
		str(modulus), '=', str(key))


def pause(length):
	for x in range(length):
		time.sleep(1)
		print(".")

def demonstrate():
	"""
	Obtains input names 
	Obtains an input max value for possibility of the secret key
	Prints generator and modulus
	Shows process
	"""
	print('The following is a demonstration of the Diffie-Hellman-Encrypter.')
	print('Requires two private values and max input for possibilites; returns a secret key')

	person1 = input('Person 1: Please enter your name: ')
	person2	= input('Person 2: Please enter your name: ')

	possible = input("Enter a maximum number of possibilites (Example: 10000) for your encrypter key: ")
	publicMod = next_prime(int(possible))
	# publicMod = get_prime(20, 99999)
	print("The public Modulus is", str(publicMod) + '.')
	print("Calculating random possible generators for", str(publicMod) +':')
	publicGen = get_generator(publicMod, 3, 999)
	print("The public generator is", str(publicGen) + '.')

	global MAX
	MAX = int(input("Choose an upper limit for your secret numbers."
		"\nCaution: Smaller values increase potential for hacking. "))

	person1 = pEncryptor(publicMod, publicGen, person1)
	person2 = pEncryptor(publicMod, publicGen, person2)

	pause(1)

	while person1.secret > MAX or person1.secret <= 0:
		person1.secret = int(input(person1.name + ", what's your secret number between" 
				+ " 1 and " + str(MAX) + "? "))
	while person2.secret > MAX or person2.secret <= 0:
		person2.secret = int(input(person2.name + ", what's your secret number between" 
				+ " 1 and " + str(MAX) + "? "))

	pause(2)

	person1_pass = person1.encrypt()
	encryption_process(person1.name, person1.modulus, person1.generator, person1.secret, person1_pass)
	pause(1)
	print('\n' + person2.name, 'performs the same calculation...')
	pause(1)
	person2_pass = person2.encrypt()
	encryption_process(person2.name, person2.modulus, person2.generator, person2.secret, person2_pass)

	pause(5)

	print('\nThen, they pass their calculated key values to one another: ')
	print(person1.name + " passes the number " + str(person1_pass) 
		+ " to " + person2.name + ".")
	print(person2.name + " passes the number " + str(person2_pass) 
		+ " to " + person1.name + ".")

	pause(2)

	print("\nThen, they both calculate the secret shared key with their own personal private value" 
		"that is unlikely to be found by anyone attempting to find the secret shared key.")

	person1Message = person1.decrypt(person2_pass)
	decryption_process(person1.name, person1.modulus, person2_pass, person1.secret, person1.key)
	pause(1)
	print('\n'+ person2.name, 'then does the same...')
	pause(1)
	person2Message = person2.decrypt(person1_pass)
	decryption_process(person2.name, person2.modulus, person1_pass, person2.secret, person2.key)

	pause(2)

	if person1Message == person2Message:
		print("Success! The shared private message is:", str(person1Message))
		pause(1)
		print("This number is a secret key for secure communication")
	else:
		print("Uh Oh. Something went wrong :( Messages obtained were:", str(person1Message), 
			'and', str(person2Message) +'.\n')

	print("For more info, go to https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange\
	to learn more about the Diffie–Hellman Key Exchange\n")

if __name__ == '__main__':
	demonstrate()








