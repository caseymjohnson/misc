from nltk.corpus import words
import numpy as np
import matplotlib.pyplot as plt

# quick program to solve letterboxed (optimally?)
def isInGroup(c, groups):
    for g in range(len(groups)):
        if c in groups[g]:
            return g
    return -1

def isSolution(candidate, groups):
    for char in ''.join(groups):
        if char not in ''.join(candidate):
            return 0
    return 1


# puzzle information
groups = [
    'nxb',
    'dmt',
    'piu',
    'egl'
]

# this approach iterates through every word in a dictionary
# each word is walked through letter by letter
# validity is checked at each step (letters in groups, no back to back same group)
found = []
for w in words.words():
    prevMembership = -1
    valid = True
    while valid:
        for c in w:
            membership = isInGroup(c, groups)
            if membership >= 0 and membership != prevMembership:
                prevMembership = membership
            else:
                valid = False
                break
        if valid:
            found.append(w)
            print(f'found word: {w}')
        break

found = sorted(found, key=len)[::-1]
print(found)


# with all of the words found, we find which sequence of words are solutions
solutions = []
candidates = [[word] for word in found]
print(candidates)
solved = False
while not solved:
    newCandidates = []
    # iteratively try to join found words together
    for c in candidates:
        current = c[-1]
        for other in found:
            if current == other:
                continue
            # if the last letter of one word meets the first letter of the next
            if current[-1] == other[0]:
                candidate = c + [other]
                # if we have a solution of n words, note it and don't try n+1 batch
                if isSolution(candidate, groups):
                    solutions.append(candidate)
                    print(f'found solution: {candidate}')
                    solved = True
                else:
                    newCandidates.append(candidate)

    candidates = newCandidates
    if not candidates:
        break

solutions = sorted(solutions, key=len)
print(solutions)




