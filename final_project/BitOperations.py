class BitOperations:
    '''Operations on Bits'''

    def OR(self, bin1: str, bin2: str) -> str:
        '''Binary or operator on '''
        return ''.join(str(int(x) | int(y)) for x, y in zip(bin1, bin2))

    def AND(self, bin1: str, bin2: str):
        return ''.join(str(int(x) & int(y)) for x, y in zip(bin1, bin2))

    def XOR(self, bin1: str, bin2: str):
        return ''.join(str(int(x) ^ int(y)) for x, y in zip(bin1, bin2))

    def complement(self, binary: str):
        ret = ''
        for c in binary:
            ret += '0' if c == '1' else '1'

        return ret

    def right_shift(self, binary: str, shift: int):
        return "0"*shift + binary[:len(binary) - shift]

    def left_shift(self, binary: str, shift: int) -> str:
        return binary[shift:] + "0"*shift

    def ROTR(self, binary: str, shift: int) -> str:
        return self.OR(self.right_shift(binary, shift),
                       self.left_shift(binary, len(binary) - shift))


    def set_len(self, string : str, length) -> str:
        return "0"*(length-len(string)) + string if len(string) < length else string[len(string) - length:]

    def char_bin(self, c: str) -> str:
        assert len(c) == 1
        return self.set_len(bin(ord(c)).replace('b', ''), 8)

    def ascii_bin(self, message : str) -> str:
        return ''.join((self.char_bin(c) for c in message))

    def bin_dec(self, binary: str) -> str:
        num = 0
        for idx, c in enumerate(binary):
            num += int(c)*2**(len(binary) - idx - 1)

        return num

    def dec_bin(self, num : str) -> str:
        return self.set_len(bin(num).replace('b', ''), 32)

    def hex_bin(self, hex: str) -> str:
        return self.set_len(bin(int(hex, 16)).replace('b', ''), 32)

    def bin_hex(self, binary : str) -> str:
        return hex(int(binary, 2)).replace('0x', '')

