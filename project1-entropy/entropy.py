from __future__ import division

__author__ = 'ajhr'
__author__ = 'javierfdr'

from auxiliar import *
import math

brown_file = "./docs/corpus/taggedBrown.txt"
en_file = "./docs/corpus/en.txt"
es_file = "./docs/corpus/es.txt"

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

def ngram_prob(ngram,n):
    total_ngram = 0
    for item in ngram.items():
        total_ngram+=int(item[1])

    div_total = lambda(x): x/total_ngram
    prob_dic = {k: div_total(v) for k,v in ngram.items()}
    return prob_dic

def compute_unigram_entropy(ngram_prob):
    entropy = 0
    # -sum(p(x)*log(p(x)))
    for unigram in ngram_prob.items():
        px = unigram[1]
        log = math.log(px,2)
        entropy+=(px*log)
    return entropy*-1

def get_bigram_for_unigram(bigram_prob, word):
    bigrams_with_word = []
    for bigram in bigram_prob.items():
        if bigram[0][0]==word:
            bigrams_with_word.append(bigram)
    return bigrams_with_word

def compute_bigram_entropy(unigram_freqs, bigram_freqs):
    entropy = 0
    # -sum(p(x)*sum(p(y|x)*.log(p(y|x))))

    # takes the form {'bigram': (p(x),sum(p(y|x).log(p(y|x)))}
    ubprob = {}

    for bigram,freq in bigram_freqs.items():
        unigram_key = bigram[0]
        uni_freq = unigram_freqs[unigram_key]
        prob = freq / uni_freq
        inner_product = prob*math.log(prob,2)
        if not ubprob.has_key(unigram_key):
            ubprob[unigram_key] = (uni_freq,inner_product)
        else:
            inner_sum = ubprob[unigram_key][1] + inner_product
            ubprob[unigram_key] = (uni_freq,inner_sum)

    entropy = 0
    for item in ubprob.values():
        entropy+=(item[0]*item[1])

    return entropy*-1

def compute_trigram_entropy(unigram_freqs, bigram_freqs, trigram_freqs):
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
        inner_product = (probs[0]/uni_freq)*probs[1]
        # we will accum the sums of inner_products for
        # bigrams starting with each unigram x
        if not ubprob.has_key(unigram_key):
            ubprob[unigram_key] = (uni_freq,inner_product)
        else:
            inner_sum =  ubprob[unigram_key][1] + inner_product
            ubprob[unigram_key] = (uni_freq,inner_sum)

    entropy = 0
    for item in ubprob.values():
        entropy+=(item[0]*item[1])

    return entropy*-1

def perplexity(entropy):
    return math.pow(2,entropy)

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
    biprob = ngram_prob(be,1)
    bigram_entropy = compute_bigram_entropy(uniprob,biprob)
    print "Bigram entropy"
    print bigram_entropy

    triprob = ngram_prob(te,2)
    trigram_entropy = compute_trigram_entropy(uniprob,biprob,triprob)
    print "Trigram entropy"
    print trigram_entropy

def process_brown():
    # Script for running the requested questions
    # Read data for three given files
    brown_words, brown_wpos = read_brown();

    print "Computing perplexity: full"
    perplexity = compute_trigram_perplexity(brown_words, len(brown_words))
    print perplexity

    print "Computing perplexity: half"
    perplexity = compute_trigram_perplexity(brown_words, int(len(brown_words)/2))
    print perplexity

    print "Computing perplexity: quarter"
    perplexity = compute_trigram_perplexity(brown_words, int(len(brown_words)/4))
    print perplexity

def compute_trigram_perplexity(words, size):

    ue,be,te = countNgrams(words,0,size)
    # Computing the 0-order mode
    uniprob = ngram_prob(ue,0)
    #unigram_entropy = compute_unigram_entropy(uniprob)
    #print "UNI Entropy: "+str(unigram_entropy)

    # Computing the 1-order model
    biprob = ngram_prob(be,1)
    #bigram_entropy = compute_bigram_entropy(uniprob,biprob)
    #print "BI Entropy: "+str(bigram_entropy)

    triprob = ngram_prob(te,2)
    trigram_entropy = compute_trigram_entropy(uniprob,biprob,triprob)
    #print "TRI Entropy: "+str(trigram_entropy)

    return perplexity(trigram_entropy)



#Question 1,2,3
#process_corpus(en_file)

#Question 4
#process_corpus(es_file)

# QUestion 5
#process_brown()



