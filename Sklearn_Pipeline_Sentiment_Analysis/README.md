End to End pipline for Sklearn for Sentiment Analysis

- Text Preprocessing

- Model Building and Serializing the model

- Build Pipeline 

   pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(lowercase=True,
                                                      max_features=1000,
                                                      stop_words= ENGLISH_STOP_WORDS)),
                            ('model', RandomForestClassifier())])
                            
 - Render output using
 
      1. Get Request 
      2. Post Request
      3. Static HTML
 
 The Data (csv) used here for sentiment analysis is from Analytics Vidhya
 
 Note: The data is polarized for Positive comments, and cannot be used for generic analysis.
 Here agenda was to build a pipeline and Render it using Get, Post and HTML
 
