from BitOperations import BitOperations

class SHA_256:
    '''A python implementation of the SHA-256 Hash Function based on documentation here
     https://csrc.nist.gov/csrc/media/publications/fips/180/4/final/documents/fips180-4-draft-aug2014.pdf'''

    def __init__(self):
        '''initialize bit operator and constants K and H'''
        self.operator = BitOperations()

        self.K = list(map(self.operator.hex_bin, ["428a2f98", "71374491", "b5c0fbcf", "e9b5dba5", "3956c25b", "59f111f1", "923f82a4", "ab1c5ed5",
                                                  "d807aa98", "12835b01", "243185be", "550c7dc3", "72be5d74", "80deb1fe", "9bdc06a7", "c19bf174",
                                                  "e49b69c1", "efbe4786", "0fc19dc6", "240ca1cc", "2de92c6f", "4a7484aa", "5cb0a9dc", "76f988da",
                                                  "983e5152", "a831c66d", "b00327c8", "bf597fc7", "c6e00bf3", "d5a79147", "06ca6351", "14292967",
                                                  "27b70a85", "2e1b2138", "4d2c6dfc", "53380d13", "650a7354", "766a0abb", "81c2c92e", "92722c85",
                                                  "a2bfe8a1", "a81a664b", "c24b8b70", "c76c51a3", "d192e819", "d6990624", "f40e3585", "106aa070",
                                                  "19a4c116", "1e376c08", "2748774c", "34b0bcb5", "391c0cb3", "4ed8aa4a", "5b9cca4f", "682e6ff3",
                                                  "748f82ee", "78a5636f", "84c87814", "8cc70208", "90befffa", "a4506ceb", "bef9a3f7", "c67178f2"]))

        self.H = list(map(self.operator.hex_bin, ["6a09e667", "bb67ae85", "3c6ef372", "a54ff53a",
                                                  "510e527f", "9b05688c", "1f83d9ab", "5be0cd19"]))

    def Ch(self, x, y, z):
        '''Ch function as defined in docs'''
        return self.operator.XOR(self.operator.AND(x, y),
                                 self.operator.AND(self.operator.complement(x), z))

    def Maj(self, x, y, z):
        '''Maj function as defined in docs'''
        return self.operator.XOR(self.operator.XOR(self.operator.AND(x, y),
                                                   self.operator.AND(x, z)), self.operator.AND(y, z))

    def upper_sigma_0(self, x):
        '''Uppercase sigma 0 function as defined in docs'''
        return self.operator.XOR(self.operator.XOR(self.operator.ROTR(x, 2),
                                                   self.operator.ROTR(x, 13)), self.operator.ROTR(x, 22))

    def upper_sigma_1(self, x):
        '''Uppercase sigma 1 function as defined in docs'''
        return self.operator.XOR(self.operator.XOR(self.operator.ROTR(x, 6),
                                                   self.operator.ROTR(x, 11)),  self.operator.ROTR(x, 25))

    def lower_sigma_0(self, x):
        '''Lowercase sigma 0 function as defined in docs'''
        return self.operator.XOR(self.operator.XOR(self.operator.ROTR(x, 7),
                                                   self.operator.ROTR(x, 18)), self.operator.right_shift(x, 3))

    def lower_sigma_1(self, x):
        '''Lowercase sigma 1 function as defined in docs'''
        return self.operator.XOR(self.operator.XOR(self.operator.ROTR(x, 17),
                                                   self.operator.ROTR(x, 19)), self.operator.right_shift(x, 10))

    def add(self, x, y):
        ''' addtion modulo 2^32'''
        return self.operator.dec_bin((self.operator.bin_dec(x) + self.operator.bin_dec(y)) % (2**32))

    def add_padding(self, binary):
        '''pad the binary with a 1 bit, 0 bits, and the length of the binary'''
        length = self.operator.set_len(
            bin(len(binary)).replace('b', ''), 64)
        diff = 448 - len(binary) % 512 if (len(binary) %
                                           512) <= 448 else 960 - len(binary) % 512
        return binary + "1" + "0" * (diff - 1) + length

    def parse_message(self, binary):
        '''Parsing message as in docs'''
        # always a multiple of 512, // is to cast to int
        num_sections = len(binary) // 512
        N = {}
        for n in range(num_sections):
            N[n] = {}
            section = binary[512*n: 512*(n+1)]
            for i in range(16):
                N[n][i] = section[32*i:32*(i+1)]
        return N

    def hash(self, message):
        '''Hash function as defined in docs'''
        binary = self.operator.ascii_bin(message)
        padded_binary = self.add_padding(binary)
        parse_dict = self.parse_message(padded_binary)
        for idx, section in enumerate(parse_dict.values()):
            W = []
            for t in range(64):
                if t < 16:
                    W.append(section[t])
                else:
                    W.append(self.add(self.add(self.lower_sigma_1(W[t-2]), W[t-7]),
                                      self.add(self.lower_sigma_0(W[t-15]), W[t-16])))

            a, b, c, d, e, f, g, h = self.H
            for t in range(64):
                temp_H = [a, b, c, d, e, f, g, h]
                T_1 = self.add(self.add(self.add(
                    self.add(h, self.upper_sigma_1(e)), self.Ch(e, f, g)), self.K[t]), W[t])
                T_2 = self.add(self.upper_sigma_0(a), self.Maj(a, b, c))
                h = temp_H[6]  # g
                g = temp_H[5]  # f
                f = temp_H[4]  # e
                e = self.add(temp_H[3], T_1)  # d
                d = temp_H[2]  # c
                c = temp_H[1]  # b
                b = temp_H[0]  # a
                a = self.add(T_1, T_2)
            self.H = [self.add(a, self.H[0]), self.add(b, self.H[1]), self.add(c, self.H[2]), self.add(d, self.H[3]),
                      self.add(e, self.H[4]), self.add(f, self.H[5]), self.add(g, self.H[6]), self.add(h, self.H[7])]

        return self.operator.bin_hex(''.join(self.H))
