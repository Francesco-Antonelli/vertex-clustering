import os
import requests
import urllib3
from bs4 import BeautifulSoup
import random
from crccheck.crc import Crc8
import glob
import sys
from random import randint
from time import sleep

# Input: una pagina html
# Output: una lista dei tag della pagina html
def get_tag(html):
    tag_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all():
        tag_list.append(tag.name)
    return tag_list

# Input: una lista di tag, una lunghezza l.
# Output: un set di stringhe in hash CRC 8. Le stringhe sono formate da l tag della pagina html.
def get_set(tag_list, l):
    if tag_list is not None:
        list_size = len(tag_list)
        n = l - 1
        tag_set = set()
        if (list_size - n)>0 and tag_list is not None:
            for i in range(len(tag_list) - n):
                # Hash dello shingle in 8-bit
                str = ' '.join(tag_list[i:i + l])
                # Hash CRC 8
                crc = Crc8.calc(str.encode('utf-8'))
                tag_set.add(crc)
            return tag_set
        else:
            return tag_set

max_shingle_ID = 2 ** 8 - 1
next_prime = 257

# Genera una lista di k coefficienti random per le funzioni di hash,
# si assicura inoltre che lo stesso valore non appaia due volte nella lista.
def pick_random_coeffs(k):

    rand_list = []

    while k > 0:
        rand_index = random.randint(0, max_shingle_ID)
        while rand_index in rand_list:
            rand_index = random.randint(0, max_shingle_ID)
        rand_list.append(rand_index)
        k -= 1

    return rand_list

# Coefficienti per la funzione di hash
coeffA = pick_random_coeffs(8)
coeffB = pick_random_coeffs(8)

# Applica la funzione hash H(x) = (aX+b)%c (trovata online, x=input, a e b=coefficienti random)

def hash_tuple1(x):
    return ((coeffA[0] * x) + coeffB[0]) % max_shingle_ID

def hash_tuple2(x):
    return ((coeffA[1] * x) + coeffB[1]) % max_shingle_ID

def hash_tuple3(x):
    return ((coeffA[2] * x) + coeffB[2]) % max_shingle_ID

def hash_tuple4(x):
    return ((coeffA[3] * x) + coeffB[3]) % max_shingle_ID

def hash_tuple5(x):
    return ((coeffA[4] * x) + coeffB[4]) % max_shingle_ID

def hash_tuple6(x):
    return ((coeffA[5] * x) + coeffB[5]) % max_shingle_ID

def hash_tuple7(x):
    return ((coeffA[6] * x) + coeffB[6]) % max_shingle_ID

def hash_tuple8(x):
    return ((coeffA[7] * x) + coeffB[7]) % max_shingle_ID

# Applica v[i] = minsh∈S{hi(sh)}
def get_vector(tag_set):
    return min(map(hash_tuple1, tag_set)), min(map(hash_tuple2, tag_set)), min(map(hash_tuple3, tag_set)), min(map(hash_tuple4, tag_set)), min(map(hash_tuple5, tag_set)), min(map(hash_tuple6, tag_set)), min(map(hash_tuple7, tag_set)), min(map(hash_tuple8, tag_set))

def read_file(shingle_size):
    page_shingle_dict = {}
    script_dir = os.path.dirname(__file__)  # path in cui si trova lo script
    rel_path = "dataset/movieDB/*.html"               #da cambiare se si vuole studiare un nuovo dataset
    abs_file_path = os.path.join(script_dir, rel_path)
    files = glob.glob(abs_file_path)
    filenumber = 0

    if(not files):
        sys.exit("La cartella è vuota!")

    try:
        for file in files:
            with open(file, encoding="utf8") as fp:
                tag_list = get_tag(fp)
            if tag_list:
                tag_set = get_set(tag_list, shingle_size)
                if tag_set:
                    vector = get_vector(tag_set)
                    filenumber += 1
                    print(filenumber)
                    abs_file_path, filename = os.path.split(file)
                    page_shingle_dict[filename] = vector
    except KeyboardInterrupt:
        print("\nKeyboard interrupt. Calculating partial results...")
        return page_shingle_dict

    return page_shingle_dict


#raggruppa i vector in dizionari che contengono vector che combaciano
def matching_vectors(vector, shingle_dict):
    matching_dict = {}
    for candidate_vector in shingle_dict:
        if match(candidate_vector, vector):
            matching_dict[candidate_vector] = shingle_dict[candidate_vector]
    return matching_dict

# Input: due shingle vector
# Output: 1 se i vector coincidono, 0 altrimenti
def match(s1, s2):
    for i in range(8):
        if (s1[i] != s2[i] and s1[i] != '*' and s2[i] != '*'):
            return 0
    return 1

#genera gli shingle vector finali
def generate_6_7_from_8_shingle_vec(shingle_vec):
    H = {}
    H_temp = {}

    shingle_dict = {shingle_vec: 0}

    for key in shingle_dict:
        for m in range(8):
            a = ()
            for n in range(8):
                if m != n:
                    a = a + (key[n],)
                else:
                    a = a + ("*",)
            H_temp[a] = 0
    for key in H_temp.keys():
        for m in range(8):
            a = ()
            for n in range(8):
                if m != n:
                    a = a + (key[n],)
                else:
                    a = a + ("*",)
            H[a] = 0
    H[shingle_vec] = 0
    return H

# genera il dizionario da utilizzare per l'algoritmo
def dict_shingle_occurencies(H, a):

    for key in a:
        x = H.get(key)
        if x == None:
            H[key] = 1
        else:
            y = H.get(key)
            y = y+1
            H[key] = y
    return H
