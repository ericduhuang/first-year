import math
import os
import time
import copy

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
    count1 = 0
    count2 = 0
    for word1 in vec1:
        for word2 in vec2:
            if word1 == word2:
                numerator += vec1[word1] * vec2[word2]
    for word in vec1:
        count1 += (vec1[word])**2
    for i in vec2:
        count2 += (vec2[i])**2
    denominator = (math.sqrt(count1)) * (math.sqrt(count2))
    return numerator/denominator
    
    
def build_semantic_descriptors(sentences):
    words = []
    values = []
    d = {}
    temp_dict = {}
    final_dict = {}
    temp_value = 0
    counter = 0
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            if sentences[i][j] not in words:
                words.append(sentences[i][j])
        for k in range(len(words)):
            if words[k] in d:
                d[words[k]] = d[words[k]] + 1
            else:
                d[words[k]] = 1
        #print(d)
        for h in words:
            #temp_value = d[h]
            #del d[h]
            temp_dict[h] = copy.deepcopy(d)
            for x in temp_dict[h]:
                values.append(temp_dict[h][x])
            #print(values)
            #print(d)
            if h in final_dict:
                for key in temp_dict[h]:
                    if key != h:
                        if key in final_dict[h]:
                            final_dict[h][key] += values[counter]
                            #del temp_dict[h][key]
                        else:
                            final_dict[h][key] = copy.deepcopy(temp_dict[h][key])
                        counter += 1
                counter = 0
            else:
                final_dict[h] = copy.deepcopy(temp_dict[h])
                temp_dict[h] = d
            
            values = []
            #d[h] = temp_value
        words = []
        d = {}
        temp_dict = {}
    for key in final_dict:
        d = copy.deepcopy(final_dict[key])
        #print(d)
        del d[key]
        final_dict[key] = d
    return final_dict
build_semantic_descriptors([['i', 'am', 'a', 'sick', 'man'], ['i', 'am', 'a', 'spiteful', 'man'],['i', 'am', 'an', 'unattractive', 'man'],['i', 'believe', 'my', 'liver', 'is', 'diseased'],['however', 'i', 'know', 'nothing', 'at', 'all', 'about', 'my','disease', 'and', 'do', 'not', 'know', 'for', 'certain', 'what', 'ails', 'me']])
        
         
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
    return build_semantic_descriptors(D)

#b = build_semantic_descriptors_from_files(["swannsway.txt", "warandpeace.txt"])
#c = build_semantic_descriptors(b)
        
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if not word in semantic_descriptors:
        return choices[0]
    temp = -1
    best = choices[0]
    for i in range(len(choices)):
        if choices[i] in semantic_descriptors:
            if similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]]) > temp:
                temp = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
                best = choices[i]
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
    return correct/count



if __name__ == "__main__":
    os.chdir("/users/erichuang/Desktop/ENGSCI/CSC180/Assignments/")
    start = time.time()
    a=  build_semantic_descriptors_from_files(["swannsway.txt", "warandpeace.txt"])
    end = time.time()
    print("the time to run is", end - start)
    
    


