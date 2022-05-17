

from cmath import exp
try:
    from nltk.stem import WordNetLemmatizer
except ImportError:
    import pip 
    pip.main(['install', 'nltk'])
    from nltk.stem import WordNetLemmatizer

try: 
    import numpy as np
except ImportError:
    import pip 
    pip.main(['install', 'numpy'])
    import numpy as np

try: 
    import pandas as pd
except ImportError:
    import pip 
    pip.main(['install', 'pandas'])
    import pandas as pd 


"""
Vector Space Model Class: 

Description: 
    This class is used to convert text data from documents into a vector space to be used for clustering analysis.
    Each document in the corpus is converted into a vector space where each term in the document is weighted according 
    to how common the word is in the document and the corpus. 
     
    For reference, see https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction [Section 6.2.3.4. Tf–idf term weighting]

    Inputs: 
        corpus (dict): Dictionary of documents with the title of each document as the key
    Methods: 
    _get_clean_corpus
        Inputs: 
            self
        Returns: 
            None 
    _get_tf
        Inputs: 
            self
        Returns: 
            None
   
    _get_idf
        Inputs: 
            self
        Returns: 
            None

    _vector_norm
        Inputs: 
            self
            vector (list): list of numbers representing a vector
        Returns: 
            norm_vector (list): list of numbers representing a normalized vector in unit length
    
    tf_idf
        Inputs: 
            self
            norm_length (Bool, Default = True): Standardizes vector into unit length
        Returns: 
            DataFrame: Data Frame with the normalized word vectors of each document and IDF of each term

"""
class Vector_Space_Model:

    def __init__(self, corpus):
        self.__corpus = corpus
        self.__N = len([doc_name for doc_name in corpus.keys()])

    def _get_clean_corpus(self,):
        """
        Description: 
            Cleans the corpus by removing punctiation, removing stop words, lemmatizes words and converting the document strings into lists of words.

        Notes: 
            Stopwords from nltk 4/10/2022
                import nltk
                nltk.download()
                from nltk.corpus import stopwords
                print(stopwords.words('english'))
            
            Lemmatizer also from NLTK 
            
            If nltk.download() does not work due to certificate error, see here https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
        """
    
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        #made by author
        disallowed_characters = ['’','—',',','î','Ä',',',"\'","\"",'%','#','!','*','@','$','^','&','(',')',':',';','.','/','|','?','`','{','}','[',']','-','_','+','=','<','>']
        lemmatizer = WordNetLemmatizer()
        clean_corpus = dict()
        doc_names = [key for key in self.__corpus.keys()]
        #iterate through each document to lemmatize words and remove stop words
        for doc_name in doc_names: 
                doc_str = self.__corpus[doc_name]
                doc_list = doc_str.split()
                cleaned_doc_list = list()

                for word in doc_list:
                    if word.lower() not in stop_words:
                        clean_word = ""
                        for char in word: 
                            try:
                                number = float(char)
                            except: 
                                if char not in disallowed_characters:
                                    clean_word = clean_word+char
                                    #remove numbers 
                        if len(clean_word) > 2: 
                            cleaned_doc_list.append(lemmatizer.lemmatize(clean_word.lower()))
            
                clean_corpus[doc_name] = cleaned_doc_list

        self.__clean_corpus = clean_corpus 

    def _get_df(self,):
        """
        Description: 
        Generates the document frequency for each word in the document. Term frequency is the count of documents
        the term appears in. 

        Notes: 
            Dependency on _get_clean_corpus()
        """
        #returns term document frequency of each term in corpus as global variable
        #clean corpus
        self._get_clean_corpus()
        word_df_dict = dict()
        
        for doc_key in self.__clean_corpus.keys(): 
            used_words = list()
            for word in self.__clean_corpus[doc_key]: 
                if word not in word_df_dict.keys():
                    word_df_dict[word] = 0
                if word not in used_words: 
                    word_df_dict[word] = word_df_dict[word] + 1
                    used_words.append(word)

        self.__word_df_dict = word_df_dict



    def _get_idf(self,):
        """
        Description: 
        Generates the inverse document frequency for each word in the document. The inverse
        document frequency of a word is a measure of how much information the word provides. 
        Words with a higher inverse document frequency are more unique in the corpus. 

        Notes: 

        """

        word_idf_dict = dict()
        for word in self.__word_df_dict: 
            if word not in word_idf_dict.keys():
                #number of documents divided by the term's document frequency
                word_idf_dict[word] = np.log10(self.__N/self.__word_df_dict[word]) + 1
            else:
                print('repeated word')

        self.__word_idf_dict = word_idf_dict
        
    def _vector_norm(self,vector):
        """
        Description:
            Normalizes the length of vectors so the document vectors in the tf-idf document representation are
            standardized in length. Standardizing the document vectors is necessary to avoid the 
            length of the document affecting the similarity measure in clustering analysis. 
        Notes:
        """
        #sqrt sum of squares
        sum_sqr = 0
        for n in vector:
            sum_sqr =  sum_sqr+n*n
        sqrt_sum_sqr = np.sqrt(sum_sqr)
        
        norm_vector = list()
        for n1 in vector:
            norm_vector.append(n1/sqrt_sum_sqr)

        check = 0 
        for norm_n in norm_vector:
            check = check + norm_n*norm_n
        #check = np.sqrt(sum([n*n for n in norm_vector]))
        
        if abs(check - 1) < .000001:
            return norm_vector 
        else:
            print('Vector Normalizaton Error\nSum of normalized vector does not equal 1')
            print('check',check)
            raise ValueError

    def tf_idf(self,norm_length = True): 
        """
        Description:
            Function for user to convert documents into tf-idf vectors. If norm_length == True, vectors 
            are standardized to have unit length. If length of the document plays a role in how similar documents 
            should be, set norm_length = False. 

        Notes: 
            Dependant on _get_df and get_idf

        """
        self._get_df() #generare self.__word_df_dict
        self._get_idf() #generare self.__word_idf_dict
        word_list = [word for word in self.__word_df_dict.keys()]
        words_check = [word for word in self.__word_idf_dict.keys()]
        if word_list != words_check:
            print('Warning: Words check off in tf_idf')

        out_dict = dict()
        idf_list = list()
        for word in word_list :
            idf_list.append(self.__word_idf_dict[word])
        out_dict['idf'] = idf_list
        for doc_name in self.__clean_corpus.keys():
            doc = self.__clean_corpus[doc_name]
            tf_list = list()
            for word in word_list:
                tf_list.append(doc.count(word))

            tfidf_list = list()
            for tf, idf in zip(tf_list,idf_list):
                tfidf_list.append(tf*idf)
            if norm_length == True:
                norm_tfidf_list = self._vector_norm(tfidf_list)
                out_dict[doc_name] =  norm_tfidf_list
            else: 
                out_dict[doc_name] =  tfidf_list

        return pd.DataFrame(out_dict,index = word_list )
