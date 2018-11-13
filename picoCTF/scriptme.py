def process(a):
    terms = a.replace(' ', '').replace('(', '0').replace(')', '1').split('+')
    return terms

def convert(a):
    print a.replace(' ', '').replace('(', '0').replace(')', '1')
def unprocess(a):
    return a.replace('0', '(').replace('1', ')')

def getZScore(term):
    max_z = 0
    z = 0
    z_count = 0
    for c in term:
        if c == '0':
            z += 1
            z_count += 1
        else:
            if z > max_z:
                max_z = z
            z = 0
    return max_z

def sum(terms, scores):
    idx = chooseTerms(scores)
    max_z0 = scores[idx]
    max_z1 = scores[idx + 1]
    scores[idx] = max(scores[idx], scores[idx + 1])
    scores.pop(idx + 1)
    print terms[idx], terms[idx + 1], max_z0, max_z1
    if max_z0 > max_z1:
        new_term = terms[idx][:-1] + terms[idx + 1] + terms[idx][-1]

    elif max_z0 < max_z1:
        new_term = terms[idx + 1][0] + terms[idx] + terms[idx + 1][1:]

    else:
        new_term = terms[idx] + terms[idx + 1]

    terms[idx] = new_term
    terms.pop(idx + 1)

    if len(terms) > 1:
        print("recurse")
        sum (terms, scores)
    else:
        print("done", terms[0])
        print unprocess(terms[0])

def chooseTerms(scores):
    # print len(scores)
    for idx, score in enumerate(scores):
        if idx != len(scores) - 1:
            print idx, score, scores[idx + 1]
            if score == scores[idx + 1]:
                return idx
    
    return 0

def scriptme(a):
    terms = process(a)
    print terms
    scores = [getZScore(i) for i in terms]    
    print scores
    out = sum(terms, scores)
    print out

scriptme('(()(())) + (()()()) + (()()()) + (()(())) + ()()')
convert("(()(())(()()())(()()()))(()(())()())")

