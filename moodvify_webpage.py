from flask import Flask, render_template, request, redirect
import string
import movielisttodb as mldb
import random
app = Flask(__name__)

NUMMOVIESSHOWN = 5

@app.route('/')
def welcome_message():
	author = "Moodvify Staffs"
	name = "(Username)"
	return render_template('index.html', author=author, name=name)

@app.route('/mood', methods = ['POST'])
def mood():
    """
        Returns baseurl/mood, a list of a bunch of movies of that mood
    """

    moods_chosen = []
    moodvified_list = []
    #get numbers of moods chosen
    for x in request.form:		
        moods_chosen.append(int(x))

    #get list of list of movies
    for mood in moods_chosen:
        moodvified_list.append(mldb.movieCatList()[mood])

    aggr_list = moodvified_list[0]
    for mlist in moodvified_list:
        aggr_list = list(set(aggr_list) & set(mlist))

    moodvified_list = []
    for i in range(NUMMOVIESSHOWN):
        movie = random.choice(aggr_list)
        moodvified_list.append(movie)
        aggr_list.remove(movie)

    return render_template('mood.html', moodvified_list=moodvified_list)

if __name__=='__main__':
	app.run(debug=True)
