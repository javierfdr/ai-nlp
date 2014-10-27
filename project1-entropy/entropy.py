from __future__ import division

#---------------------------------------#
#     Project on Entropy                #
#  Master in Artificial Intelligence    #
#  Natural Language Processing          #
#            UPC                        #
#                                       #
#    Alejandro Hernandez                #
#     Javier Fernandez                  #
#                                       #
# --------------------------------------#

from auxiliar import *
import math
import sys
import random

brown_file = "./docs/corpus/taggedBrown.txt"
en_file = "./docs/corpus/en.txt"
es_file = "./docs/corpus/es.txt"

# reads tagged brown corpus
def read_brown():
    return getTaggedWordsFromFileTuple(brown_file)

def read_data(file):
    return getWordsFromFile(file)

# Calculates the probability of the word x appearing
# in the list of words l. Returns a dictionary
# of the type {<word,prob>}
def generate_gram_prob(l):
    wcount = len(l)
    word_dic = {}

    for w in l:
        if w not in word_dic.keys():
            word_dic[w]  = 1
        else:
            word_dic[w]+=1

    # calculates probability by dividing word count and total word
    div_total = lambda(x): x/wcount
    prob_dic = {k: div_total(v) for k,v in word_dic.items()}
    return prob_dic

# calculate the probability of appearance of each word
def ngram_prob(ngram,n):
    total_ngram = 0
    for item in ngram.items():
        total_ngram+=int(item[1])

    div_total = lambda(x): x/total_ngram
    prob_dic = {k: div_total(v) for k,v in ngram.items()}
    return prob_dic

# Calculates the unigram entropy given the probability of a
# appearance of each word
def compute_unigram_entropy(ngram_prob):
    entropy = 0
    # -sum(p(x)*log(p(x)))
    for unigram in ngram_prob.items():
        px = unigram[1]
        log = math.log(px,2)
        entropy+=(px*log)
    return entropy*-1

# Calculates all the bigram where a specifi unigram (word) appears
def get_bigram_for_unigram(bigram_prob, word):
    bigrams_with_word = []
    for bigram in bigram_prob.items():
        if bigram[0][0]==word:
            bigrams_with_word.append(bigram)
    return bigrams_with_word

# Computes de bigram entropy given de unigram probabilities, the unigram
# frequence and the bigram frequency
def compute_bigram_entropy(unigram_probs, unigram_freqs, bigram_freqs):
    entropy = 0
    # -sum(p(x)*sum(p(y|x)*.log(p(y|x))))

    # takes the form {'bigram': (p(x),sum(p(y|x).log(p(y|x)))}
    ubprob = {}

    for bigram,freq in bigram_freqs.items():
        unigram_key = bigram[0]
        uni_freq = unigram_freqs[unigram_key]
        uni_prob = unigram_probs[unigram_key]
        prob = freq / uni_freq
        inner_product = prob*math.log(prob,2)
        if not ubprob.has_key(unigram_key):
            ubprob[unigram_key] = (uni_prob,inner_product)
        else:
            inner_sum = ubprob[unigram_key][1] + inner_product
            ubprob[unigram_key] = (uni_prob,inner_sum)

    entropy = 0
    for item in ubprob.values():
        entropy+=(item[0]*item[1])

    return entropy*-1

# Computes de trigram entropy given de unigram probabilities and the unigram, bigram
# and trigram frequency
def compute_trigram_entropy(unigram_probs, unigram_freqs, bigram_freqs, trigram_freqs):
    entropy = 0
    # -sum(p(x)*sum(p(y|x)*.log(p(y|x))))

    # takes the form {'bigram': (p(x),sum(p(y|x).log(p(y|x)))}
    ubtprob = {}

    btprob = {}
    ubprob = {}
    for trigram, freq in trigram_freqs.items():
        bigram_key = (trigram[0],trigram[1])
        bi_freq = bigram_freqs[bigram_key]
        prob = freq / bi_freq
        inner_product = prob*math.log(prob,2)
        if not btprob.has_key(bigram_key):
            btprob[bigram_key] = (bi_freq, inner_product)
        else:
            inner_sum = btprob[bigram_key][1] + inner_product
            btprob[bigram_key] = (bi_freq, inner_sum)

    inner_sum = 0
    inner_product = 0
    for bigram, probs in btprob.items():
        unigram_key = bigram[0]
        # computes SUM p(y|x) * p(z|xy)logp(z|xy)
        # for each bigram
        uni_freq = unigram_freqs[unigram_key]
        uni_prob = unigram_probs[unigram_key]
        inner_product = (probs[0]/uni_freq)*probs[1]
        # we will accum the sums of inner_products for
        # bigrams starting with each unigram x
        if not ubprob.has_key(unigram_key):
            ubprob[unigram_key] = (uni_prob,inner_product)
        else:
            inner_sum =  ubprob[unigram_key][1] + inner_product
            ubprob[unigram_key] = (uni_prob,inner_sum)

    entropy = 0
    for item in ubprob.values():
        entropy+=(item[0]*item[1])

    return entropy*-1

# Computes perplexity given the entropy
def perplexity(entropy):
    return math.pow(2,entropy)

# process a corpus file en prints
# the unigram, bigram and trigram entropy
def process_corpus(file):
    print "Processing Corpus: "+file
    corpus = read_data(file)
    # Count unigram, bigrams and trigrams for English Corpora
    [ue,be,te]= countNgrams(corpus,0)

    # Count unigram, bigrams and trigrams for Spanish Corpora
    #[us,bs,ts]= countNgrams(wes,0)

    # Computing the 0-order model of English Corpora
    uniprob = ngram_prob(ue,0)
    unigram_entropy = compute_unigram_entropy(uniprob)
    print "Unigram entropy"
    print unigram_entropy

    # Computing the 1-order model of English Corpora
    bigram_entropy = compute_bigram_entropy(uniprob,ue,be)
    print "Bigram entropy"
    print bigram_entropy

    trigram_entropy = compute_trigram_entropy(uniprob,ue,be,te)
    print "Trigram entropy"
    print trigram_entropy

# Obtains the perplexity of full, half and quarter of the trigrams on
# corpus defined by words
def get_perplexities(words, smooth=0, tagged_words={}):
    p1 = compute_trigram_perplexity(words, len(words),smooth, tagged_words)
    p2 = compute_trigram_perplexity(words, int(len(words)/2),smooth, tagged_words)
    p3 = compute_trigram_perplexity(words, int(len(words)/4),smooth, tagged_words)

    return [p1,p2,p3]

# Pretty print function for entropy and perplexity calculation
def compute_and_print(func, *args):
    sys.stdout.write("Computing...")
    sys.stdout.flush()
    result = func(*args)
    sys.stdout.write("\r")
    sys.stdout.flush()
    print "\t".join(map(str,result))

# Process the brown corpus to obtain the perplexity of
# the trigram of full, half and quarter size of it.
def process_brown():
    # Script for running the requested questions
    # Read data for three given files
    brown_words, tagged_words = read_brown()
    print "\nBrown Words Perplexity \n"
    print "full\t\thalf\t\tquarter <x,y,z>"
    compute_and_print(get_perplexities, brown_words)

    print "\nBrown Words POS Perplexity <x',y,z> \n"
    print "full\t\thalf\t\tquarter"
    compute_and_print(get_perplexities, brown_words, 1, tagged_words)

    print "\nBrown Words POS Perplexity <x',y',z> \n"
    print "full\t\thalf\t\tquarter"
    compute_and_print(get_perplexities, brown_words, 2, tagged_words)

    print "\nBrown Words POS Perplexity <x',y',z'> \n"
    print "full\t\thalf\t\tquarter"
    compute_and_print(get_perplexities, brown_words, 3, tagged_words)

# Smooth must be one of [1,2,3]
def smooth_ngram(ngrams,tagged_words, smooth):
    smoothed_ngrams = {}
    for ngram_key, count in ngrams.items():
        lenkey = 0
        if not isinstance(ngram_key,str):
            key = ngram_key[0]
            lenkey = len(ngram_key)
        else:
            key = ngram_key
            lenkey = 1

        if smooth >0 and lenkey >0:
            pos = tagged_words[key]

            if lenkey==3:
                new_key = (pos,ngram_key[1], ngram_key[2])
            if lenkey==2:
                new_key = (pos,ngram_key[1])
            if lenkey==1:
                new_key = (pos)

        if smooth >1 and lenkey >1:
            key = ngram_key[1]
            pos = tagged_words[key]

            if lenkey==3:
                new_key = (new_key[0],pos, ngram_key[2])
            if lenkey==2:
                new_key = (new_key[0],pos)

        if smooth >2 and lenkey >2:
            key = ngram_key[2]
            pos = tagged_words[key]

            if lenkey==3:
                new_key = (new_key[0],new_key[1], pos)

        if not smoothed_ngrams.has_key(new_key):
            smoothed_ngrams[new_key] = count
        else:
            smoothed_ngrams[new_key] = smoothed_ngrams[new_key] + count

    return smoothed_ngrams

# Computes the perplexity of trigrams on corpus word applying the
# given smooth
def compute_trigram_perplexity(words, size, smooth=0, tagged_words={}):

    ue,be,te= countNgrams(words,0,size)

    if smooth>0:
        ue = smooth_ngram(ue,tagged_words, smooth)
        be = smooth_ngram(be,tagged_words, smooth)
        te = smooth_ngram(te,tagged_words, smooth)

    # Computing the 0-order model of English Corpora
    uniprob = ngram_prob(ue,0)
    trigram_entropy = compute_trigram_entropy(uniprob,ue,be,te)

    return perplexity(trigram_entropy)

print "\n---------------------------------------------------------"
print "Computing entropies on English corpus (Questions 1,2,3)"
print "---------------------------------------------------------"
#Question 1,2,3
process_corpus(en_file)


print "\n---------------------------------------------------------"
print "Computing entropies on Spanish corpus (Question 4)"
print "---------------------------------------------------------"
#Question 4
process_corpus(es_file)


print "\n----------------------------------------------------------------------------"
print "Computing perplexities on Brown and Pos-Tagged browned corpus (Questions 5,6)"
print "-----------------------------------------------------------------------------"
# Question 5 and 6
process_brown()



