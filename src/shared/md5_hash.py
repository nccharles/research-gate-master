__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import hashlib
from werkzeug.datastructures import FileStorage
import os
from typing import Union
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from base_constants import BaseDirectoryConstants
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MD5Hash:
    @staticmethod
    def compute_hash(file: FileStorage = None):
        """
        Computes MD5 hash of a given file.
        """
        md5_hash: hashlib.md5 = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
        hashString: str = md5_hash.hexdigest()
        file.stream.seek(0)
        return hashString
    @staticmethod
    def compare_hash(file: Union[FileStorage, None] = None,all_documents: list = None):
        try:
            documents = []
            # read the file
            temp_file = os.path.join(BaseDirectoryConstants.DOCUMENTS_TEMP_PATH, file.filename)
            file.save(temp_file)
            # read the content
            with open(temp_file, 'r', encoding='iso-8859-1') as file1:
                content1 = file1.read()
                documents.append(content1)
            for document in all_documents:
                base_name = os.path.join(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, document.document_base_name)
                with open(base_name, 'r', encoding='iso-8859-1') as file2:
                    content2 = file2.read()
                    documents.append(content2)
            # tokenize the documents and remove stopwords
            nltk.download('stopwords')
            nltk.download('punkt')
            stop_words = set(stopwords.words('english'))
            tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]
            filtered_docs = [[word for word in doc if word not in stop_words] for doc in tokenized_docs]
            # create a set of unique words from all documents
            all_words = set()
            for doc in filtered_docs:
                all_words.update(doc)
            # create frequency vectors for each document
            doc_vectors = []
            for doc in filtered_docs:
                doc_vector = [doc.count(word) for word in all_words]
                doc_vectors.append(doc_vector)
            # compute the cosine similarity between the documents
            cos_sim = cosine_similarity(doc_vectors)[0][1]
            # calculate the percentage of similarity
            similarity_percentage = round(cos_sim * 100, 2)
            print(f"The documents are {similarity_percentage}% similar.")
            return similarity_percentage
        except Exception as e:
            print("Error in comparing hash: ", e)
            return 0


        
    
