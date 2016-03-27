Article Summarizer
==================

A simple Flask web application that allows the user to pass in a URL and return a summarized article. 
This program uses a summarizer algorithm that extracts the key sentence from each paragraph in the text
and it usually cuts articles, blogs, news reports around 60-70% of the original text.
This program also uses the Goose API that extracts contents from a URL.

Installation
------------

First you need to pull this repository to your computer

	$ git clone https://github.com/sxm6616/article-summarizer.git

We need to install Python 2.7 and Virtualenv on the machine.
We will then need to install the Goose Extractor and Flask framework

	$ cd article-summarizer
	$ virtualenv venv --python=python2.7
	$ . venv/bin/activate
	$ pip install goose-extractor
	$ pip install flask

Getting Started
---------------

Start the application

	$ python app.py

Then open your browser and type in:
	
	$ http://127.0.0.1:5000/
	

