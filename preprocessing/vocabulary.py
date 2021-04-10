'''
Text preprocessing code.
'''
#TODO: Add asynchronous support.
#TODO: Add support for tqdm.
#TODO: Add multi-threading support
#TODO: 

import re
import os
import nltk
import pickle
import argparse
import numpy as np
import pandas as pd
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from embeddings import Embeddings




class Vocabulary():
    """
    A class to handle preprocessing of Text and building vocabulary.
    Steps. 
    1. Build a vocabulary.
    2. Tokenize.
    3. Emcode.
    """
    def __init__(self, language = 'english', embedding_path = None, embedding_dim = 50):
        
        #TODO: Experiment with unknown values
        self.word_to_int = {'<unk>': 1, '<pad>': 0, '<eos>':2}
        self.int_to_word = {0: '<pad>', 1:'<unk>', 2:'<eos>' }
        self.word_frequency = {}
        self.vocab = ['<pad>', '<unk>', '<eos>']
        self.stopwords_list = stopwords.words(language)
        self.embedding_path = embedding_path
        self.embedding_dim = embedding_dim
        self.vectors = []
        self.state = {
            'language': language,
            'ignore_numbers' : False,
            'ignore_puncts' : True,
            'remove_stopwords' : True, 
            'text_normalization' : None
        }

    def build_vocabulary_from_dataframe(self, dataframe, columns, ignore_numbers = False, ignore_puncts = True, remove_stopwords = True, text_normalization = None, word_frequency_threshold = 5 ):
        '''
            dataframe : pd.DataFrame instance containing data along in csv/df rows
            columns: list containing column names, which needed to be processed 
        '''        
        #as we are itereting over all the sentences, better create a single list. 
        sentences = dataframe[columns].values.reshape(-1).tolist()

        #meging all list of sentences to single text.
        sentences = " ".join(sentences)

        self.build_vocabulary(sentences, ignore_numbers, ignore_puncts, remove_stopwords, text_normalization, word_frequency_threshold)
        

    def build_vocabulary(self, text, ignore_numbers = False, ignore_puncts = True, remove_stopwords = True, text_normalization = None, word_frequency_threshold = 5 ):
        '''
        Function to build vocabulary. 

        Input:
            text (string) : String containing all training text to build an vocabulary.  
            ignore_numbers (bool) : A flag to ignore/remove numbers while processing text.
            ignore_puncts (bool): A flag to ignore/remove punctuations while preprocessing text.
        '''
        self.state['ignore_numbers'] = ignore_numbers
        self.state['ignore_puncts'] = ignore_puncts

        #make this functions asyncronous.
        text = self._remove_required(text)
        tokenized_text = self._tokenize_text(text, remove_stopwords = remove_stopwords, text_normalization = text_normalization)
        self.word_frequency = Counter(tokenized_text)
        self.vocab += sorted(self.word_frequency, key = self.word_frequency.get, reverse = True)
        self.word_to_int = {word: count for count, word in enumerate(self.vocab)}
        self.int_to_word = {count: word for word, count in self.word_to_int.items()}
        
        self._init_embeddings()
        
        #TODO: check which one perform better higher int for encode
        #sorting word frquency in assceding order of frquency. 
        # self.vocab = sorted(vocab, key=)
        
        # count = 2
        # for word, frequency in self.word_frequency.items():
        #     if frequency >= word_frequency_threshold:
        #         self.word_to_int[word] = count
        #         count +=1 


    def encode_sentence(self, sentences, sequence_length = 150, padding = True):
        '''
        Function to tokenize and encode sentense

        Input:
            sentences list(string, string, ...): list of texts that needed to encode
            sequence_length (int): desired sequence length 
            padding (bool): flag to add padding 
        '''
        tokenized_sentence = []
        
        if type(sentences) == list:
            for sentence in sentences: 
                sentence = self._remove_required(sentence.lower())
                tokenized_sentence.append(self._tokenize(sentence))
        else:
            sentences = self._remove_required(sentences.lower())
            tokenized_sentence.append(self._tokenize(sentences))

        if padding:
            tokenized_sentence = self._padding(tokenized_sentence, sequence_length)

        mapping_func = lambda  word: self.word_to_int.get(word, 1)
        mapping_func = np.vectorize(mapping_func)

        encoded_sentence = mapping_func(tokenized_sentence)

        if len(encoded_sentence)>1:
            return encoded_sentence
        else:
            return encoded_sentence[0]


    def decode_sentence(self, tokenized_sentence):
        '''Decode given tokenized sentence.
        '''
        mapping_func = lambda  word: self.int_to_word.get(word, '<unk>')
        mapping_func = np.vectorize(mapping_func)

        decoded_sentence = mapping_func(tokenized_sentence)

        return decoded_sentence


    def _padding(self, tokenized_sentence, sequence_length):
        '''Helper function to encode np text array
        '''
        if type(tokenized_sentence) == list:
            tokenized_sentence = np.array(tokenized_sentence)

        padded_sentence = np.full((tokenized_sentence.shape[0], sequence_length), '<pad>', dtype = tokenized_sentence.dtype)
        padded_sentence[:, -tokenized_sentence.shape[1]:] = tokenized_sentence
     
        return padded_sentence



    def _tokenize_text(self, text, remove_stopwords = True, text_normalization = None):
        '''
        A function to tokenize text, remove stopwords.

        Inputs:
            text_normalization : lemma, stem, None
        '''
        self.state['remove_stopwords'] = remove_stopwords
        self.state['text_normalization'] = text_normalization

        tokenized_text = self._tokenize(text)

        return tokenized_text


    def _tokenize(self, sentence):
        #TODO: Add support for remove stopwords flag
        tokenized_sentence = word_tokenize(sentence)

        if self.state['text_normalization'] == "stem":
            stemmer = PorterStemmer()
            tokenized_sentence = [stemmer.stem(word) for word in tokenized_sentence if word not in self.stopwords_list]

        elif self.state['text_normalization'] == "lemma":
            raise "lemma tokenization support yet to be added"
            
            # tokenized_sentence = [word for word in tokenized_sentence if word not in self.stopwords_list]
            # tokenized_sentence = lemmatize_sentence(tokenized_sentence, ignore_pronoun = ignore_pronoun)

        #remove stopwords if specified
        if self.state["remove_stopwords"]:
            tokenized_sentence = [word for word in tokenized_sentence if word not in self.stopwords_list]
                
        return tokenized_sentence


    def _remove_required(self, text):
        '''Remove required element from string based on regex.
        '''            
        text = text.lower()

        if self.state['ignore_numbers'] and self.state['ignore_puncts']:
            text = re.sub(r'[^a-z]', ' ', text)
        else:
            if self.state['ignore_puncts']:
                text = re.sub(r'[^a-z0-9]', ' ', text)
            elif self.state['ignore_numbers']:
                text = re.sub(r'[^a-z.!?\\-]', ' ', text)

        return text


    def save_vocab(self, path = 'vocab.pk'):
        '''
        Function to save state of the vocab
        '''
        pickle_object = {
            'word_to_int' :self.word_to_int,
            'int_to_word': self.int_to_word,
            'word_frequency' : self.word_frequency, 
            'vocab' : self.vocab,
            'stopwords_list' : self.stopwords_list,
            'state' : self.state,
            'vectors': self.vectors
        }

        with open(path, 'ab') as file_:
            pickle.dump(pickle_object, file_)


    def load_vocab(self, path = 'vocab.pk'):
        ''' function to load state of the vocab
        '''
        with open(path, 'rb') as file_:
            pickle_object = pickle.load(file_)

        self.word_to_int = pickle_object['word_to_int']
        self.word_frequency = pickle_object['word_frequency']
        self.vocab = pickle_object['vocab']
        self.stopwords_list = pickle_object['stopwords_list']
        self.state = pickle_object['state']
        self.vectors = pickle_object['vectors']
        self.int_to_word = pickle_object['int_to_word']


    def _init_embeddings(self):

        if self.embedding_path:
            embedings = Embeddings(self.embedding_path, self.embedding_dim)
            self.vectors = embedings.get_embedding_vectors(self.vocab)
        else:
            self.vectors = np.random.normal(loc=0, scale=1, size=(len(self.vocab), self.embedding_dim))
                


#TODO: add CLI support
# def main():
#     parser = argparse.ArgumentParser(description="function to create corpus based on given csv file and column names in file")
#     parser.add_argument('-f', "--file", help="data csv files", default="../downloads/preprocessed_data/train.csv")
#     parser.add_argument("-c", "--columns", help="columns to read in csv file", nargs="+", default=["input", "output"])
#     parser.add_argument('-e', "--embeddings", help="embeddiing file path", default="../downloads/glove.6B/glove.6B.50d.txt")
#     parser.add_argument('-d', "--embeddingdims", help="embedding dimension", default=50)
#     parser.add_argument('-s', "--save", help="dict save location", default="../data/corpus.pb")

#     test_text = "First, some of the description and reviews led me to believe that the fans direct hot air out of the back and/or sides of the Chill Pad. This is not the case. The fans only blow straight through top-bottom.  Second, if the Chill Pad is sitting on anything -- even though the legs provide a small gap, the air flow is reduced to practically nothing.I bought this to put on top of my DirecTV DVR, to help pull hot air away from the DVR. It actually raised the internal temperature by 2 degrees, probably because the air flow it created was very minimal and it blocked some of the vented area on the top of the DVR.Good idea, but the implementation leaves it pretty worthless in my opinion."
#     parser.add_argument('-t', "--test", help="run on test sequence", default=test_text)


#     args = parser.parse_args()



if __name__ == "__main__":

    # main()
    text = "First, some of the description, and reviews led me to believe that the fans direct hot air out of the back and/or sides of the Chill Pad. This is not the case. The fans only blow straight through top-bottom.  Second, if the Chill Pad is sitting on anything -- even though the legs provide a small gap, the air flow is reduced to practically nothing.I bought this to put on top of my DirecTV DVR, to help pull hot air away from the DVR. It actually raised the internal temperature by 2 degrees, probably because the air flow it created was very minimal and it blocked some of the vented area on the top of the DVR.Good idea, but the implementation leaves it pretty worthless in my opinion."
    vocab = Vocabulary(embedding_path='../downloads/glove.6B/glove.6B.50d.txt')
    vocab.build_vocabulary(text, word_frequency_threshold = 1, ignore_puncts = False, remove_stopwords = False)
    text = vocab.encode_sentence(["I believe in reviews"])
    print(vocab.word_to_int)
    print(text)
