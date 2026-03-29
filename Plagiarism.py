from difflib import SequenceMatcher
from collections import deque

d1 = ""
d2 = ""
similarity = 0
fb = ""

def check(name):
    global d1, d2
    file = open(name, 'r')
    content = file.read()
    file.close()
    if d1 == "":
        d1 = content
    else:
        d2 = content

def checker(t1, t2):
    global similarity
    obj = SequenceMatcher(None, t1, t2)
    rv = obj.ratio()
    pv = rv * 100
    match = round(pv, 2)
    similarity = match

def remarks1(percent):
    global fb
    if percent < 10:
        fb = "completely different"
    elif percent < 20:
        fb = "somewhat similar majority portion is original"
    elif percent < 40:
        fb = "a little bit of similarity"
    elif percent < 60:
        fb = "very much same"
    elif percent < 80:
        fb = "too much identical very high copied content"
    else:
        fb = "almost totally same"

# ── BFS: find the first common block of length >= min_len ──────────────────
def bfs_find_common_block(t1, t2, min_len=10):
    
    words1 = t1.split()
    words2 = t2.split()
    n1, n2 = len(words1), len(words2)

    # Start BFS from every possible (i, j) pair at length = min_len
    visited = set()
    queue = deque()

    for i in range(n1 - min_len + 1):
        for j in range(n2 - min_len + 1):
            state = (i, j, min_len)
            queue.append(state)
            visited.add(state)

    while queue:
        i, j, length = queue.popleft()

        # Check if the block of `length` words matches
        if words1[i:i+length] == words2[j:j+length]:
            return " ".join(words1[i:i+length]), length   # found a match

        # Expand: try a longer block (BFS goes breadth = length levels)
        next_len = length + 1
        if i + next_len <= n1 and j + next_len <= n2:
            state = (i, j, next_len)
            if state not in visited:
                visited.add(state)
                queue.append(state)

    return None, 0


heading = "\nSimple Plagiarism Checker\n"
print(heading)

first  = input("Give the first file which needs to be checked: ")
second = input("Give the other file for checking: ")

check(first)
check(second)
checker(d1, d2)

similarity_score = similarity
score = similarity_score
remarks1(score)
final = fb

print(f"\nSimilarity: {similarity}%")
print(f"Feedback: {fb}\n")


MIN_BLOCK = 5   # minimum word-count for a "suspicious" common block
block, length = bfs_find_common_block(d1, d2, min_len=MIN_BLOCK)

if block:
    print(f"[BFS] First common block found ({length} words):")
    print(f"  \"{block}\"\n")
else:
    print(f"[BFS] No common block of {MIN_BLOCK}+ words found.\n")
