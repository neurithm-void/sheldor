import os
import numpy as np



class Embeddings():
    def __init__(self, embedding_path, embedding_dim = 50):
        '''
        Inputs:
            embedding_path (str): a path for embedding vectors file (only supports glove embeddings)
            embedding_dim (int): dimensions of embeddings, default = 50
        '''

        if os.path.exists(embedding_path):
            self.vectors = self._create_embedding_dict(embedding_path)
            self.vector_dim = embedding_dim
        else:
            raise f"embedding path {embedding_path} do not exists."


    def _create_embedding_dict(self, embedding_path):
        
        vectors = {}
        if os.path.exists(embedding_path):
            embeddings = []
            with open(embedding_path, encoding='utf-8') as f_:
                embeddings = f_.readlines()

            for vector in embeddings:
                vector = vector.split()
                vectors[vector[0]] = np.array(vector[1:], dtype = 'float')

        return vectors
        

    def _get_word_vector(self, word):
        '''
        Return a vector for the word from the embeddings dictionary. 
        if word is not there is embeddings, create a random vector with values from a normal (Gaussian) distribution, with mean 0 and std 1.
        '''
        vector = self.vectors.get(word, np.random.normal(loc = np.random.normal(loc=0, scale = 1, size = self.vector_dim)))
        return vector


    def get_embedding_vectors(self, vocab):
        '''
        Inputs:
            vocab (list): a list of vocab to for which vectors are needed to be calculate.
        '''
        vectors = []

        for word in vocab:
            vectors.append(self._get_word_vector(word))

        return np.array(vectors)

