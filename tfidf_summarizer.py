import nltk
nltk.download('all')
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
from nltk.corpus import stopwords

# Handicap is a variable that will take values from zero to one and will let us increase or decrease the final threshold
# Bigger the Handicap, shorter the summary
HANDICAP = 0.5

# Function to set handicap based on length of text, if needed
# def set_handicap(text):
#     if (len(text) > 2000):
#         HANDICAP = 0.7
#     ...
#     return HANDICAP

# Function to remove slang from text, if needed
# def remove_slang(text):
#     ...
#     return text


def remove_punctuation_marks(text) :
    punctuation_marks = dict((ord(punctuation_mark), None) for punctuation_mark in string.punctuation)
    return text.translate(punctuation_marks)

def get_lemmatized_tokens(text) :
    normalized_tokens = nltk.word_tokenize(remove_punctuation_marks(text.lower()))
    return [nltk.stem.WordNetLemmatizer().lemmatize(normalized_token) for normalized_token in normalized_tokens]

def get_average(values) :
    greater_than_zero_count = total = 0
    for value in values :
        if value != 0 :
            greater_than_zero_count += 1
            total += value
    return total / greater_than_zero_count

def get_threshold(tfidf_results) :
    i = total = 0
    while i < (tfidf_results.shape[0]) :
        total += get_average(tfidf_results[i, :].toarray()[0])
        i += 1
    return total / tfidf_results.shape[0]

def get_summary(documents, tfidf_results) :
    summary = ""
    i = 0
    while i < (tfidf_results.shape[0]) :
        if (get_average(tfidf_results[i, :].toarray()[0])) >= get_threshold(tfidf_results) * HANDICAP :
                summary += ' ' + documents[i]
        i += 1
    return summary

def run_summarization(text):
    # Set handicap
    # HANDICAP = set_handicap(text)

    # Tokenizing the text
    documents = nltk.sent_tokenize(text)

    # Get TF-IDF values
    tfidf_results = TfidfVectorizer(tokenizer = get_lemmatized_tokens, stop_words = stopwords.words('english')).fit_transform(documents)

    # Return final summary
    return get_summary(documents, tfidf_results)




# Input text - to summarize
# text = """
# Louis Daniel Armstrong (August 4, 1901 – July 6, 1971), nicknamed "Satchmo",[a] "Satch",
# and "Pops",[2] was an American trumpeter, composer, vocalist, and actor who was among the most influential
# figures in jazz. His career spanned five decades, from the 1920s to the 1960s, and different eras in the
# history of jazz.[3] In 2017, he was inducted into the Rhythm & Blues Hall of Fame. Armstrong was born and raised in New Orleans.
# Coming to prominence in the 1920s as an inventive trumpet and cornet player, Armstrong was a foundational influence in jazz,
# shifting the focus of the music from collective improvisation to solo performance.[4] Around 1922, he followed his mentor,
# Joe "King" Oliver, to Chicago to play in the Creole Jazz Band. In Chicago, he spent time with other popular jazz musicians,
# reconnecting with his friend Bix Beiderbecke and spending time with Hoagy Carmichael and Lil Hardin. He earned a reputation
# at "cutting contests", and relocated to New York in order to join Fletcher Henderson's band. With his instantly recognizable rich,
# gravelly voice, Armstrong was also an influential singer and skillful improviser, bending the lyrics and melody of a song.
# He was also skilled at scat singing. Armstrong is renowned for his charismatic stage presence and voice as well as his trumpet
# playing. By the end of Armstrong's career in the 1960s, his influence had spread to popular music in general. Armstrong was one
# of the first popular African-American entertainers to "cross over" to wide popularity with white (and international) audiences.
# He rarely publicly politicized his race, to the dismay of fellow African Americans, but took a well-publicized stand for
# desegregation in the Little Rock crisis. He was able to access the upper echelons of American society at a time when this
# was difficult for black men.
# """

# text = """

# Alright, I want to check out kubuntu, what is the best method? I have 4.10 ubuntu on a cd, should I install that and just grab the KDE files or download the install CD for Kubuntu?
# http://cdimage.ubuntu.com/kubuntu/releases/hoary/preview/
# if you install Ubuntu 4.10, you will need to upgrade to the development release anyway in order to install the Kubuntu desktop
# so it is probably simpler to download a new ISO
# Thanks mdz, will do
# http://www.kde-look.org/content/show.php?content=22008
# i will post a amd64 and ix86 iso in about 10 hours
# SuperL4g what you at now?
# 20%
# 21% here :(
# did you receive the URL I sent you, where the .torrents are available?
# they are in the same directory as the isos; we always publish torrents at the same time
# torrents did not work
# if they did not work for you, the problem is on your end (I am using them right now)
# mdz: yes sir, and unfortunately, no one wants or is going after the PPC .iso at the moment :)
# Torrents are working for me
# i have access to two fast servers
# brb
# http and ftp will work for everyone
# yes, but they will also take 10 hours
# bittorrent not only saves bandwidth on the server side, it'll get you the file faster
# mdz not at 200+ and 300+ k
# did ne one like my ss?
# 16.9k is no good
# i have tons of bandwith to use
# Give me some...I have low bandwidth.. :(
# lol
# ;-)
# 25k is pegging me LMAO
# yeah, no one wants the PPC one like I do, at this point :)
# I'm seeding it, zero peers
# you have it already?
# I built it :)
# can site that host kubuntu isos use the kubuntu logo?
# Good way to get it ;-)
# I have a seed running with all 6 images; currently ~75kb/sec on -live-powerpc.iso, 0kb on -install-powerpc.iso
# i think i will also offer a isos in parts
# I don't see why not, as long as you are offering the official images
# I wonder why I can't see it...?
# mdz i want to be shure
# we do not want issues later
# I suppose I could be hitting the limit on the number of peers
# hmm, no, that limit is per torrent
# every other torrent is active, and I've served 3.6GB worth of the powerpc install iso previously, so I think it's OK on this end
# i do not see a point of contact on the site
# i will just not use the logo :(
# that's fine too
# we don't use the logo on the official download page either
# i want to i just do not want to get hit later
# I've told you that it's fine, but I don't think it's important
# ok
# is it ok to host other distros in same dir
# who are ops in #ubuntu?
# i'm banned, and the person who banned me won't reply or tell me why he did it.
# """



#text = open('ubuntu_sample.txt', 'r').read()

# text = """
# Someone should suggest to Mark that the best way to get people to love you is to hire people to work on reverse-engineering closed drivers
# heh
# heh
# HELLO
# your job is to entertain me so I don't fall asleep at 2pm and totally destroy my migration to AEST
# see you next week?
# oh, auug, right. rock.
# just drop me an email, or call +61 403 505 896
# I arrive Tuesday morning your time, depart Fri morning, will be staying at the Duxton
# ... three days?
# or ten?
# hey guys
# fabbione: hey dude. sorry to hear about your multiple losses :\
# daniels: it sucks :/
# anyway time to look forward
# daniels: got my mail?
# fabbione: which one?
# about the different "stuff"
# i just spent like an hour clearing my inbox in a half-dazed state (middle of the day after arriving at 5:30am from london)
#  er yeah, i think i might have got that in stuttgart, maybe. thanks, it does mean a lot :)
# ok
# i haven't had time to sit down and give a proper reply, though
# no need to
# oh FUCK OFF SPAMMERS
# but remember for the next time
# my entire +debian was spam
# i shall
# ahha
# i found a bunch of bugs in X
# i will have to get them fixed
# some of them are related to debconf and we need to workaround them
# we will have a dynamic templates system
# (otherwise stuff simply doesn't work)
# cya around
# heh :) awesome
# seeya dude, take care
# you too kid
# short visit this time, my daughter is participating in a state-level violin competition a week from tomorrow, I want to be home for that.
# welcome home?
# oh wow, sounds cool
# yah. logged in to jabber, got your ping.
# "you've got bugs" :-)
# i saw all your reassignments; i'm going to do stuff like minigolf right now though
# yeah :) just a couple
# anyway, minigolf time. time to get on my feet and move around to stay awake for the next 5 and a half hours
# is it possible to put a laptop to sleep without closing the lid?
# talking about hppa...
# do you think you can get me a small one from hp.dk ?
# i know they throw away a lot of them
# perhaps there are still a few hidden
# yo dude
# hey dani
# what was the name of the little application to strip ^M from MSDOS files?
# """


#print(run_summarization(text))
