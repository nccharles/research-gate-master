__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import hashlib
from werkzeug.datastructures import FileStorage
import os
import asyncio
import nltk
from nltk.tokenize import word_tokenize
from base_constants import BaseDirectoryConstants

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
    def compare_hash(file: FileStorage = None,all_documents: list = None):
        try:
            nltk.download('punkt')
            # initialize the list of similarities
            similarities = []
            # read the file
            new_doc = file.read()
            new_doc = new_doc.decode('iso-8859-1')
            async def check_similarity(document):
                base_name = os.path.join(BaseDirectoryConstants.DOCUMENTS_DIRECTORY_PATH, document.document_base_name)
                # check if the file exists
                if os.path.exists(base_name):
                    with open(base_name, 'rb') as current_file:
                        current_doc = current_file.read()
                        current_doc = current_doc.decode('iso-8859-1')
                        tokenized_docs = [word_tokenize(new_doc.lower()),word_tokenize(current_doc.lower())]

                        # Get the set of unique words in both documents
                        unique_words = set(tokenized_docs[0] + tokenized_docs[1])

                        # Count the number of words that appear in both documents
                        shared_words = [word for word in unique_words if word in tokenized_docs[0] and word in tokenized_docs[1]]
                        num_shared_words = len(shared_words)

                        # Calculate the percentage of words shared between the two documents
                        percent_similarity = (num_shared_words / len(unique_words)) * 100
                        similarities.append(percent_similarity)
                        
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
            # os.remove(temp_file)
            if len(similarities) > 0:
                return max(similarities)
            else:
                return 0
        except Exception as e:
            print("Error in comparing hash: ", e)
            return -1


        
    
