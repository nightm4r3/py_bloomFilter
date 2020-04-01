#!/usr/bin/env python2.7


import hashlib
import mmh3
import sys
import getopt

SIZE = 100000000 #10 million size: bloom filter array
dictionary_SIZE = 623518
bloom3 = [0] * SIZE
bloom5 = [0] * SIZE
dictionary = [None] * dictionary_SIZE 


def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def is_ascii(s): return all(ord(c) < 128 for c in s)


def FlipBits(hash_object, bloomFilter):
    hex_dig = hash_object.hexdigest()
    index = int(hex_dig, 16)
    index = index % SIZE
    bloomFilter[index] = 1

#### Hash Functions #####
def MD5(plaintext, bloomFilter):
    hash_object = hashlib.md5(plaintext.encode())
    FlipBits(hash_object, bloomFilter)

def SHA256(plaintext, bloomFilter):
    hash_object = hashlib.sha256(plaintext.encode())
    FlipBits(hash_object, bloomFilter)

def SHA512(plaintext, bloomFilter):
    hash_object = hashlib.sha512(plaintext.encode())
    FlipBits(hash_object, bloomFilter)

def Murmur(plaintext, bloomFilter):
    hash_object = mmh3.hash64(plaintext)
    index = abs(hash_object[1])
    index = index % SIZE
    bloomFilter[index] = 1

def siphash(plaintext, bloomFilter):
    import siphash
    key = '0123456789ABCDEF'
    sip = siphash.SipHash_2_4(key)
    sip.update(plaintext)
    h = sip.hash()
    index = h % SIZE
    bloomFilter[index] = 1




#getting input from command line
dict_file = ''
inputfile = ''
outputfile3 = ''
outputfile5 = ''

output_filename = 'default.out'
options, remainder = getopt.getopt(sys.argv[1:], 'd:i:o:')

for opt, arg in options:
    if opt == '-d':
        dict_file = arg
    elif opt == '-i':
        inputfile = arg
    elif opt == '-o':
        outputfile3 = arg
    if is_ascii(sys.argv[7]):
        outputfile5 = sys.argv[7]



## Loading dictionary.txt to dictionary array ##
fd = open(dict_file, 'r')
line = fd.readline()
i = 0
while (line != ''):
    line = line.split(' ')
    str1 = ''.join(line)
    str1 = str1.rstrip()
    dictionary[i] = str1
    if (is_ascii(dictionary[i]) == False):
        dictionary[i] = removeNonAscii(dictionary[i]) #index has non-ascii character
    line = fd.readline()
    i += 1
fd.close



###### Hashing bloom3 ######
# Bloom Filter with 3 Hash Functions: SHA256, siphash, and Murmur
i = 0
for i in range(0, dictionary_SIZE):
    SHA256(dictionary[i], bloom3)
    siphash(dictionary[i], bloom3)
    Murmur(dictionary[i], bloom3)
    
###### Hashing bloom5 ######
# Bloom Filter with 5 Hash Functions: SHA256, siphash, and Murmur, MD5, and SHA512
i = 0
for i in range(0, dictionary_SIZE):
    SHA256(dictionary[i], bloom5)
    siphash(dictionary[i], bloom5)
    Murmur(dictionary[i], bloom5)
    MD5(dictionary[i], bloom5)
    SHA512(dictionary[i], bloom5)
 




#Taking input & Checking bloom3
fd_input = open(inputfile, 'r')
fd_output = open(outputfile3, 'w+')
i = 0
flag_arr = [False] * 3
line = fd_input.readline()
while (line != ''):
    for i in range(0,3): #initializing flag_arr
        flag_arr[i] = False

    str1 = line.rstrip()
    if is_ascii(str1) == False:
        str1 = removeNonAscii(str1)
    
    hash_object = hashlib.sha256(str1.encode()) #SHA256
    hex_dig = hash_object.hexdigest()
    index = int(hex_dig, 16)
    index = index % SIZE
    if bloom3[index] == 1:
        flag_arr[0] = True

    import siphash
    key = '0123456789ABCDEF' #siphash
    sip = siphash.SipHash_2_4(key)
    sip.update(str1)
    h = sip.hash()
    index = h % SIZE
    if bloom3[index] == 1:
        flag_arr[1] = True

    hash_object = mmh3.hash64(str1) #Murmur
    index = abs(hash_object[1])
    index = index % SIZE
    if bloom3[index] == 1:
        flag_arr[2] = True


    if flag_arr[0] == True and flag_arr[1] == True and flag_arr[2] == True:
        fd_output.write("maybe\n")
    else:
        fd_output.write("no\n")

    line = fd_input.readline()

fd_output.close
fd_input.close




#Taking input & Checking bloom5
fd_input = open(inputfile, 'r')
fd_output5 = open(outputfile5, 'w+')
i = 0
flag_arr5 = [False] * 5
line = fd_input.readline()
while (line != ''):
    for i in range(0,5): #initializing flag_arr5
        flag_arr5[i] = False

    str1 = line.rstrip()
    if is_ascii(str1) == False:
        str1 = removeNonAscii(str1)
    
    hash_object = hashlib.sha256(str1.encode()) #SHA256
    hex_dig = hash_object.hexdigest()
    index = int(hex_dig, 16)
    index = index % SIZE
    if bloom5[index] == 1:
        flag_arr5[0] = True

    import siphash
    key = '0123456789ABCDEF' #siphash
    sip = siphash.SipHash_2_4(key)
    sip.update(str1)
    h = sip.hash()
    index = h % SIZE
    if bloom5[index] == 1:
        flag_arr5[1] = True

    hash_object = mmh3.hash64(str1) #Murmur
    index = abs(hash_object[1])
    index = index % SIZE
    if bloom5[index] == 1:
        flag_arr5[2] = True
    
    hash_object = hashlib.md5(str1.encode()) #MD5
    hex_dig = hash_object.hexdigest()
    index = int(hex_dig, 16)
    index = index % SIZE
    if bloom5[index] == 1:
        flag_arr5[3] = True
 
    hash_object = hashlib.sha512(str1.encode()) #SHA512
    hex_dig = hash_object.hexdigest()
    index = int(hex_dig, 16)
    index = index % SIZE
    if bloom5[index] == 1:
        flag_arr5[4] = True


    if flag_arr5[0] == True and flag_arr5[1] == True and flag_arr5[2] == True and flag_arr5[3] == True and flag_arr5[4] == True:
        fd_output5.write("maybe\n")
    else:
        fd_output5.write("no\n")

    line = fd_input.readline()


fd_output.close
fd_input.close

