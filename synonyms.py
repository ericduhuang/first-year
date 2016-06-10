import math
import os
import time


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    numerator = 0 
    denominator = 0
    for word1 in vec1:
        for word2 in vec2:
            if word1 == word2:
                numerator += vec1[word1] * vec2[word2]
    denominator = norm(vec1) * norm(vec2)
    return numerator/denominator

def euclidean(vec1, vec2):
    count = {}
    for word1 in vec1:
        if word1 in vec2:
            count[word1] = vec1[word1] - vec2[word1]
        else: 
            count[word1] = vec1[word1]
    for word2 in vec2:
        if word2 not in vec1:
            count[word2] = -vec2[word2]
    return -1 * norm(count)

def euclidean_norm(vec1, vec2):
    count = 0
    new_vec1 = {}
    new_vec2 = {}
    for word in vec1:
        new_vec1[word] = vec1[word]/norm(vec1)
    for word in vec2:
        new_vec2[word] = vec2[word]/norm(vec2)
    count = euclidean(new_vec1, new_vec2)
    return count
   
    
def build_semantic_descriptors(sentences):
    final_dict = {}
    for word1 in range(len(sentences)):
        for word2 in range(len(sentences[word1])):
            if not sentences[word1][word2] in final_dict:
                final_dict[sentences[word1][word2]] = {}
            for word3 in set(sentences[word1]):
                if word3 != sentences[word1][word2]:
                    if not word3 in final_dict[sentences[word1][word2]]:
                        final_dict[sentences[word1][word2]][word3] = 1
                    else:
                        final_dict[sentences[word1][word2]][word3] += 1
    return final_dict

         
def build_semantic_descriptors_from_files(filenames):
    D = []
    for i in range(len(filenames)):
        temp = []
        f = open(filenames[i], "r", encoding="utf-8").read()
        f = f.replace('.', ' . ')
        f = f.replace('!', ' . ')
        f = f.replace('?', ' . ')
        f = f.replace(',', ' ')
        f = f.replace('-', ' ') 
        f = f.replace('--', ' ')
        f = f.replace(':', ' ')
        f = f.replace('"', ' ')
        f = f.replace("'", " ")
        f = f.lower()
        L = f.split()
        for j in range(len(L)):
            if L[j] == ".":
                D.append(temp)
                temp = []
            else:
                temp.append(L[j])
    # count = len(D)
    # D = D[:int(.6*count)]
    return build_semantic_descriptors(D)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]
    best = choices[0]    
    if choices[0] not in semantic_descriptors:
        temp = -1
    else:
        temp = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[0]])
    for i in choices[1:]:
        if i in semantic_descriptors:
            if similarity_fn(semantic_descriptors[word], semantic_descriptors[i]) > temp:
                temp = similarity_fn(semantic_descriptors[word], semantic_descriptors[i])
                best = i
    return best
    
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    count = 0
    correct = 0
    candidates = []
    text = open(filename, "r", encoding="utf-8").read()
    L = text.split('\n')
    del L[len(L)-1]
    for i in range(len(L)):
        count += 1
        word = L[i].split()
        candidates = word[2:]
        if most_similar_word(word[0], candidates, semantic_descriptors, similarity_fn) == word[1]:
            correct += 1
        candidates = []
        word = []
    return correct/count*100



def f():
   
    os.chdir("/users/erichuang/Desktop/ENGSCI/CSC180/Assignments")
    start = time.time()
    a =  build_semantic_descriptors_from_files(["swannsway.txt", "warandpeace.txt"])
    end = time.time()
    print("the time to run is", end - start)
    print(run_similarity_test("test.txt", a, cosine_similarity))
    print(run_similarity_test("test.txt", a, euclidean))
    print(run_similarity_test("test.txt", a, euclidean_norm))
    

if __name__ == "__main__":
    f()
