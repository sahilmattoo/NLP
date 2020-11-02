# NLP

Tokenization :

    from nltk.tokenize import sent_tokenize, word_tokenize
    
    from nltk.tokenize import TreebankWordTokenizer 
       
    from nltk.tokenize import WordPunctTokenizer
    
    from nltk.tokenize import RegexpTokenizer 
    
    import spacy
    
    from keras.preprocessing.text import text_to_word_sequence


STEMMING:

    PorterStemmer()
    
    SnowballStemmer()
    
LEMMATIZATION:

    from nltk.stem import WordNetLemmatizer
    
    spacy using token.lemma_
    
    from textblob import TextBlob, Word
    
 from nltk.corpus import wordnet
 
 wordnet.synsets('searchword')
    
Note : This list is the not the finite list.
    
    
BERT_LDA for Topic Modeling.ipynb
        
        ## Install Dependencies for BERT
        
    !pip install "tensorflow_hub>=0.6.0"
    
    !pip install "tensorflow>=2.0.0"
    
    !pip install sentence-transformers
    
    import tensorflow as tf
    
    import tensorflow_hub as hub
    
    from tensorflow.keras import layers
    
    # Load the Predefined BERT
    embedder = SentenceTransformer('bert-base-nli-mean-tokens')
