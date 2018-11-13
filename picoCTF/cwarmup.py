# import string
# letters = {}
# for idx, l in enumerate(string.ascii_lowercase):
#     letters[l] = idx + 1

# print letters
message = "llkjmlmpadkkc"
key =  "thisisalilkey"
new_message = ""
buffer = 96

for x,y in zip(message, key):
    a = ord(x) - 96
    b = ord(y) - 96
    char = chr(((a + b - 1)%26) + 96)
    new_message += char
    print x, y, char
    # print ord(x), ord(y), (((ord(x) + ord(y) - 1)% 96) + 96)
    # new_message += chr(((ord(x) + ord(y) - 1) % 96) + 96)

print new_message

# text = ''
# for l in key:
#     print l
# for idx, l in enumerate(message):
#     print l, message[idx], letters[l], key[idx]
#     res = (letters[l] + letters[key[idx]] - 1) % 26
#     for key, value in letters.items():
#         if res == value:
#             text += key

# print text


    