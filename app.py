
# coding=UTF-8
from __future__ import division
from flask import Flask, request, render_template,jsonify
from goose import Goose
import re, urllib2


# This is a web application that allows the user to pass in a URL and return a summarized article
# Created by Sergio Molina
# March 2016
 
# This program uses a summarizer algorithm that extracts the key sentence from each paragraph in the text
# and it usually cuts articles, blogs, news reports around 60-70% of the original text
# This program also uses the Goose API that extracts contents from a URL.

app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
 
@app.route('/api/v1/extract')
def extract():
	url = request.args.get('url')
	g = Goose()
	article = g.extract(url=url)
				
	title = article.title
	content = article.cleaned_text[:10000]
	st = SummaryTool()
	sentences_dic = st.get_sentences_ranks(content)
	summary = st.get_summary(title, content, sentences_dic)

	if article.top_image == None:
		response = {'title' : article.title , 'text' : summary, 'image' : ''}
		return jsonify(response)
	response = {'title' : article.title , 'text' : summary,'image': article.top_image.src}

	return jsonify(response)

 
@app.route('/summarize')
def summarize():
    title = urllib2.unquote(request.args.get('title'))
    content = urllib2.unquote(request.args.get('content'))

    st = SummaryTool()
    sentences_dic = st.get_sentences_ranks(content)
    summary = st.get_summary(title, content, sentences_dic)
    return jsonify(result=summary)

# This is a naive text summarization algorithm
# Created by Shlomi Babluki
# April, 2013
	
class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_sentences_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return (". ").join(summary)


if __name__ == "__main__":
    app.run(debug=True)



