import numpy as np
from functools import partial

class UHF:
    """A factory for producing a universal family of hash functions"""

    @staticmethod
    def isPrime(k):
        if k%2==0:
            return False
        for i in range(3, int(np.sqrt(k)), 2):
            if k%i == 0:
                return False
        return True

    def __init__(self, n):
        """Universe size is n"""
        self.n = n
        m = 0
        if n%2==0:
            m = n+1
        else:
            m = n+2
        while not(UHF.isPrime(m)):
            m = m+2
        self.p = m

    def makeHash(self, m):
        """Returns a random hash function

        m: table size
        """
        a = np.random.randint(1,self.p-1)
        b = np.random.randint(0,self.p-1)
        return lambda k: ((a*k+b)%self.p)%m



def fnv_hash(s):
    """Returns 32-bit number as slot index

    Uses the FNV algorithm from http://isthe.com/chongo/tech/comp/fnv/

    Args:
        s (str): key to be hashed
    """
    hashval = 0x811c9dc50
    for ch in s:
        hashval *= 0x01000193
        hashval ^= ord(ch)
        hashval &= 0xffffffff
    return hashval


class String_UHF:
    """Universal Hash family for strings

    We will use the Mersenne prime 2**31 - 1 = 2147483647
    in the hash family: while we have not done so here,
    division modulo Mersenne primes can be computed very fast."""

    def __init__(self, p=31):
        self.p = 2**p -1
        self.a = np.random.randint(1, self.p -1)
        self.b = np.random.randint(0, self.p -1)

    def makeHash(self, m):
        """Returns hash function from str -> [0, m)

        Args:
            m (int): table size
        """
        def __rollingHash(x, s):
            """Implements a rolling hash

            Treat the string's ord() values as coefficients
            of a polynomial in x, and evaluate modulo self.p

            Args:
                x (int)
                s (str): string to be hashed
            """
            hashval = 0x811c9dc50
            for ch in s:
                hashval = ((hashval * x) + ord(ch)) % self.p
            return ((self.a * hashval + self.b) % self.p) % m

        k = np.random.randint(1, self.p -1)
        return partial(__rollingHash, k)

class BloomFilter:
    ''' Class creates our bloom filter and accepts the words that we're
    looking for. Code uses the String_UHF from the professor so not currently
    sure how we can read that in yet. Initializes to the optimal bits and hashes.
    
    Args:
        word_list: list of words to be filtered
    '''
    def __init__(self, word_list):
        self.words = word_list
        self.len = len(self.words)
        self.fn_rate = 0.01
        self.bits = int(-self.len*np.log(self.fn_rate) / (np.log(2)**2))
        self.optHash = int(self.bits/self.len * np.log(2))
        self.bloom = np.zeros(self.bits)
        self.hash_fn = String_UHF()
        self.hashes = [self.hash_fn.makeHash(self.bits) for i in range (self.optHash)]
        for elem in self.words:
            for h in self.hashes:
                self.bloom[h(elem)] = 1

    def check_membership(self,elem):
        '''Returns True if all bits corresponding to the element are set
        - by Professor
        '''
        return all([self.bloom[h(elem)] == 1 for h in self.hashes])