import urllib2
import re
import string

def getSynonyms(word): # Returns a list


	req = urllib2.Request('http://thesaurus.com/browse/' + word)
	response = urllib2.urlopen(req)
	page = response.read()
	
	# Exclude antonyms
	synonyms = re.sub(r'<section class=\"container-info antonyms\" >[^(</section>)]</section>', "", page)
	# This isn't working correctly right now. Porbably best to switch to an
	
	# Extract synonyms
	synonyms = re.findall(r'<span class=\"text\">[^<]*</span>', page) # Extract synonymss
	synonyms = [syn[19:-7] for syn in synonyms] # Remove span tags

	return synonyms


def getRhymes(word): # Returns a list

	# Look up rhymes on rhymezone.com
	req = urllib2.Request('http://www.rhymezone.com/r/rhyme.cgi?Word=' + word + '&typeofrhyme=perfect&org1=syl&org2=l&org3=y');
	response = urllib2.urlopen(req)
	page = response.read()

	i = string.find(page, "Words and phrases that almost rhyme")
	if(i > 0):
		page = page[:i]

	rhymes = re.findall(r'HREF=\"d=[^>]*>[^<]*<\/A>', page) # Extract rhymes
	rhymes = [re.sub(r'[^>]*>', '', rhyme, count=1) for rhyme in rhymes] # Remove open tags
	rhymes = [rhyme[:-4] for rhyme in rhymes] # Remove close tags
	rhymes = [re.sub(r'&nbsp;', ' ', rhyme) for rhyme in rhymes] # Replace &nbsp; with spaces
	return rhymes



word1 = raw_input("Enter a word: ")
word2 = raw_input("Enter a word: ")
syn1 = getSynonyms(word1)
syn2 = getSynonyms(word2)
rhymes1 = []
for syn in syn1:
	tmp = getRhymes(syn)
	intersection = [word for word in tmp if word in syn2]
	if intersection:
		print syn
		print intersection
	rhymes1.extend(tmp)

# To do:
#	Error check user input
#	Handle empty case
#	Exclude duplicates
# 	Make output prettier
#	Fix antonym exclusion regex / use HTML parser
#	Optimize - find rhymes of shorter of lists syn1 and syn2

