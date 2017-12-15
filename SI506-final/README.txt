SI 506 Final Project README
Sangho Eum


Your readme should include ALL of the following in order to earn full points for it.

You should include these README instructions and fill in your answers below/beside the questions.

You may submit this .txt file edited, or a .PDF if you want to format it more (just like the project plan).


* In ~2-3 sentences, what does your project do?
My project has two parts. First part grabs recent 30 posts from Facebook Graph API, caches those posts, collect words from those posts except stop words, and saves the most common word in the collection.
Second part then searches that words on iTunes and gets a list of songs and their details and create a csv file that orders those songs from longest to shortest.
Both of parts make cache files.

* What files (by name) are included in your submission? List them all! MAKE SURE YOU INCLUDE EVERY SINGLE FILE YOUR PROGRAM NEEDS TO RUN, as well as a sample of its output file.

- SI506_finalproject.py
- SI506finalproject_cache.json
- facebook_cache.json
- sangho.csv.csv (sample results)
- stopwords_list.txt (stopwords list)
- your_app_data.py (app data for Facebook)
- README.txt


* What Python modules must be pip installed in order to run your submission? List them ALL (e.g. including requests, requests_oauthlib... anything someone running it will need!). Note that your project must run in Python 3.

requests
requests_oauthlib import OAuth2Session
requests_oauthlib.compliance_fixes import facebook_compliance_fix



* Explain SPECIFICALLY how to run your code. We should very easily know, after reading this:
    - What file to run
    	- SI506_finalproject.py


    - Anything else
    	- your_app_data.py should be filled with the Facebook key and secret, but I have already filled it out with my data


    - Anything someone should know in order to understand what's happening in your program as it runs


* Where can we find all of the project technical requirements in your code? Fill in with the requirements list below.

REQUIREMENTS LIST:
* Get and cache data from 2 REST APIs (list the lines where the functions to get & cache data begin and where they are invoked):
    - FB cache
	- get: 37, 42-68
	- invoked: 39-41
    - iTunes cache
	- get: 181-186, 190-200
	- invoked: 187-189

* Define at least 2 classes, each of which fulfill the listed requirements:
	- class Post(): 85-125
	- class Song(): 205-219

* Create at least 1 instance of each class:
	- Post: 128-130
	- Song: 227-228

* Invoke the methods of the classes on class instances:
	- Post() method 1: 132
	- Post() method 2: 133
  - Post() method 3: 134
	- Song() method 1: 230
	- Song() method 2: 231

* At least one sort with a key parameter:
	- 234

* Define at least 2 functions outside a class (list the lines where function definitions begin):
	- function 1: 147-154
	- function 2: 237-244

* Invocations of functions you define:
	- function 1: 156
	- function 2: 246

* Create a readable file:
	- 246
	- included and titled “sangho.csv"

END REQUIREMENTS LIST

* Put any citations you need below. If you borrowed code from a 506 problem set directly, or from the textbook directly, note that. If you borrowed code from a friend/classmate or worked in depth with a friend/classmate, note that. If you borrowed code from someone else's examples on a website, note that.

	- params_unique_combination function from problem set 9
	- making requests function from problem set 9


* Explain in a couple sentences what should happen as a RESULT of your code running: what CSV or text file will it create? What information does it contain? What should we expect from it in terms of how many lines, how many columns, which headers...?

	- It will create a csv file “sangho.csv”
	- # lines: 1 line for header, # lines for # songs
	- # columns: Track Title, Artist, #####, ####..


* Make sure you include a SAMPLE version of the file this project outputs (this should be in your list of submitted files above!).


* Is there anything else we need to know or that you want us to know about your project? Include that here!
