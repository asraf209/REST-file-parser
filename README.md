REST-file-parser
================

A RESTful web service, capable of uploading and parsing a text file. It returns total word counts, word frequencies 
in the HTTP response body. It provides an end point to upload arbitrary file of size <= 10MB. It also provides end points to view uploaded files, files meta-data, parsing a file, parsing file with substring etc.

Setting up environment
----------------------
I have used Flask web framework to implement this project. So set up your Flask environment as follows:
  1. Install `virtualenv` in your system:
   1. For Ubuntu: `sudo apt-get install python-virtualenv`
   * For Linux/Mac: `sudo pip install virtualenv`
  2. Go to the project root directory *(REST-file-parser)*
  3. Run: `virtualenv venv`
  4. Activate it: `. venv/bin/activate`
  5. Now install Flask: `pip install Flask`
