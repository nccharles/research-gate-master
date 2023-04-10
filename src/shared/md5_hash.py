__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import hashlib
from werkzeug.datastructures import FileStorage
import os
from typing import Union
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from base_constants import BaseDirectoryConstants
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
            similarities = [0]
            # read the file
            temp_file = os.path.join(BaseDirectoryConstants.DOCUMENTS_TEMP_PATH, file.filename)
            file.save(temp_file)
            # read the content
            with open(temp_file, 'r', encoding='iso-8859-1') as file1:
                content1 = file1.read()
            for document in all_documents:
                base_name = os.path.join(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, document.document_base_name)
                with open(base_name, 'r', encoding='iso-8859-1') as file2:
                    content2 = file2.read()
                    # check file size
                    content1_size = os.path.getsize(temp_file)
                    content2_size = os.path.getsize(base_name)
                    print(f"File 1 size: {content1_size} bytes")
                    print(f"File 2 size: {content2_size} bytes")
                    total_size = content1_size + content2_size
                    difference = abs(content1_size - content2_size)* 100 / total_size 
                    if difference < 40:
                        # tokenize the documents and remove stopwords
                        nltk.download('stopwords')
                        nltk.download('punkt')
                        stop_words = set(stopwords.words('english'))
                        tokenized_docs = [word_tokenize(content1.lower()),word_tokenize(content2.lower())]
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
                        similarities.append(similarity_percentage)
            return max(similarities)
        except Exception as e:
            print("Error in comparing hash: ", e)
            return 0


        
    
