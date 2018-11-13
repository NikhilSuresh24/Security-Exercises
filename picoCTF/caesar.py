import string
num_chars = len(string.ascii_lowercase)
print num_chars

def brute_force(text):
    new_message = []
    for v in text:
        new_message.append(ord(v))
    print new_message
    for i in range(num_chars):
        new_message2 = []
        for v in new_message:
            v += i
            new_message2.append(chr(v%num_chars))
            # print v, type(v)
            print new_message2
        print "".join(new_message2)

brute_force("payzgmuujurjigkygxiovnkxlcgihubb")