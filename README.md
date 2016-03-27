Article Summarizer
==================

A simple Flask web application that allows the user to pass in a URL and return a summarized article

Installation
------------

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
	

