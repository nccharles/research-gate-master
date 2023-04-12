__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import hashlib
from werkzeug.datastructures import FileStorage
import os
import asyncio
from typing import Union
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from base_constants import BaseDirectoryConstants
from sklearn.metrics.pairwise import cosine_similarity

class MD5Hash:
    # initialize the minimum difference
    max_differ = 40
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
            # tokenize the documents and remove stopwords
            nltk.download('stopwords')
            nltk.download('punkt')
            stop_words = set(stopwords.words('english'))
            # initialize the list of similarities
            similarities = []
            # read the file
            temp_file = os.path.join(BaseDirectoryConstants.DOCUMENTS_TEMP_PATH, file.filename)
            file.save(temp_file)
            # read the content
            with open(temp_file, 'r', encoding='iso-8859-1') as file1:
                content1 = file1.read()
            async def check_similarity(document):
                base_name = os.path.join(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, document.document_base_name)
                # check if the file exists
                if os.path.exists(base_name):
                    with open(base_name, 'r', encoding='iso-8859-1') as file2:
                        content2 = file2.read()
                        # check file size
                        content1_size = os.path.getsize(temp_file)
                        content2_size = os.path.getsize(base_name)
                        total_size = content1_size + content2_size
                        difference = round((abs(content1_size - content2_size)* 100 / total_size),2)
                        if difference < MD5Hash.max_differ:
                            MD5Hash.max_differ=difference
                            print("max_differ: ", MD5Hash.max_differ)
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
                        
            async def get_similar(document):
                await asyncio.create_task(check_similarity(document))
               
            # compare the documents
            async def compare_docs():
                # create a list of tasks
                task=[get_similar(doc) for doc in all_documents]
                await asyncio.gather(*task)

            # run the event loop until all tasks are completed
            asyncio.run(compare_docs())
            
            # delete the temporary file
            os.remove(temp_file)
            if len(similarities) > 0:
                return max(similarities)
            else:
                return 0
        except Exception as e:
            print("Error in comparing hash: ", e)
            return 0



        
    
