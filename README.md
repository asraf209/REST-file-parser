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
  5. Now install Flask: `pip install Flask`. *Done!*


How to Run
-----------
1. The main entry point of this webservice is `fileparser.py`. So open a terminal and execute: `./fileparser.py`. It will be running on your localhost *`http://127.0.0.1:5000`*
2. To check ***running status***, open another terminal and run: `curl -X GET http://127.0.0.1:5000`. You can also use web browser instead of `curl`
3. To ***upload a text file***: `curl -X POST -F "file=@/path/to/your/file/test.txt" http://127.0.0.1:5000/upload`. You should see some responses in JSON format:
```
    {
      "File Name": "test.txt",
      "Line Count": 1,
      "Word Count": 4,
      "Word List": {
          "all": 1,
          "hello": 2,
          "world": 1
      }
    }
```
4. After uploading, the file will be saved in the `uploads/` folder under project root
5. File size is limited to 10MB at most. So any file bigger than that will throw error response:
```
  <title>413 Request Entity Too Large</title>
  <h1>Request Entity Too Large</h1>
  <p>The data value transmitted exceeds the capacity limit.</p>
```
6. Also, only file with these extensions `{'txt', 'md', 'rst', 'c', 'cpp', 'java', 'scala', 'py', 'sh', 'log'}` are currently being supported. Any other type of file will throw error response
7. To ***check list of files*** that are already been uploaded: `curl -X GET http://127.0.0.1:5000/files`
```
    [
      {
          "File Name": "test.txt",
          "Last Access Time": "Fri Dec 19 01:45:49 2014",
          "Last Modify Time": "Fri Dec 19 01:38:22 2014",
          "Size": 23
      },
      {
          "File Name": "jingle.txt",
          "Last Access Time": "Fri Dec 19 00:39:22 2014",
          "Last Modify Time": "Fri Dec 19 00:38:49 2014",
          "Size": 404
      }
    ]
```
8. To ***get metadata of a specific file***: `curl -X GET http://127.0.0.1:5000/files/jingle.txt`
```
    {
      "File Name": "jingle.txt",
      "Last Access Time": "Fri Dec 19 00:39:22 2014",
      "Last Modify Time": "Fri Dec 19 00:38:49 2014",
      "Size": 404
    }
```
9. To ***parse a specific file*** that is already been uploaded: `curl -X GET http://127.0.0.1:5000/parse/test.txt`
```
    {
        "File Name": "test.txt",
        "Line Count": 1,
        "Word Count": 4,
        "Word List": {
            "all": 1,
            "hello": 2,
            "world": 1
        }
    }
```
10. Parse a file and ***discard all words who have a matching sub-string***. Like, get frequencies for words who do not contain `ll` within them, in `test.txt` file: `curl -X GET http://127.0.0.1:5000/parse/test.txt?discard=ll`
```
    {
        "File Name": "test.txt",
        "Line Count": 1,
        "Word Count": 4,
        "Word List": {
            "world": 1
        }
    }
  Here, 'Word Count' shows the total number of words present in the file. 
  Whereas, 'Word List' shows the filtered words only
```
11. Parse a file and ***keep those words who contain a matching sub-string***. Like, get frequencies for those words who contain `ing` within them, in `jingle.txt` file: `curl -X GET http://127.0.0.1:5000/parse/jingle.txt?only=ing`
```
    {
        "File Name": "jingle.txt",
        "Line Count": 17,
        "Word Count": 77,
        "Word List": {
            "dashing": 1,
            "jingle": 6,
            "laughing": 1,
            "making": 1,
            "ring": 1,
            "sing": 1,
            "sleighing": 1
        }
    }
  Here, 'Word Count' shows the total number of words present in the file. 
  Whereas, 'Word List' shows the filtered words only
```
12. Parse a file and ***discard and keep matching words at the same time***. Like, get frequencies for those words who contain `ing` but not `dash` within them, in `jingle.txt` file: `curl -X GET http://127.0.0.1:5000/parse/jingle.txt?only=ing\&discard=dash`
```
    {
        "File Name": "jingle.txt",
        "Line Count": 17,
        "Word Count": 77,
        "Word List": {
            "jingle": 6,
            "laughing": 1,
            "making": 1,
            "ring": 1,
            "sing": 1,
            "sleighing": 1
        }
    }
```
```
  Be careful about '\&'. If you use web browser then only '&' is needed
```

Run Test
--------
```
  $ ./test_fileparser.py 
```
```
    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 0.127s
    
    OK

```
