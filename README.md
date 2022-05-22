# Business-Description-Clustering
Grouping stocks using machine learning and text analysis.

The code and paper was completed as a part of my data science class project at Baylor University. I used the code and data in this repository to answer if stocks in the same GICS sector use the same terms in their business description? Please contact me on LinkedIn if you have any questions, comments, or suggestions for improvements. https://www.linkedin.com/in/drake-cody-0a1001125/


EDGAR_10K_Puller.py contains a class that pulls 10K documents from the SEC EDGAR Python API. You can get your first 100 pulls free by signing up for an API here https://sec-api.io/docs. Documentation for the class can be found in the EDGAR_10K_Puller.py file

Vector_Space_Model.py contains a class that converts a dictionary of documents into TF-IDF vectors. The code was based on the user guide from Scikit-Learn found here https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction. Documentation for the class can be found in the Vector_Space_Model.pyfile. 

The full set of references used for the project can be found in the reference section of the writeup in the analysis folder. 
