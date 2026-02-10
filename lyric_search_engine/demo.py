from lyric_search_engine.models import LyricDoc
from lyric_search_engine.engine import LLSearchEngine
from lyric_search_engine.storage import SQLiteFeedbackStore
from lyric_search_engine.feedback import Feedback


docs = [
    LyricDoc("1", "Midnight Echoes", "midnight echoes in my head i can't sleep"),
    LyricDoc("2", "Sunrise", "new day new light i'm healing slowly"),
    LyricDoc("3", "Ghost Notes", "i write verses like ghosts in the walls"),
    LyricDoc("4", 
    "hypnagogia", 
    """
    Chorus:
Losing myself, finding less comfort
and losing more sleep
I'm losing more sleep than secrets can keep
Chased by the echoes of what is to be
sadness and drowsy are paired just like rhymes
Melancholia, hypnagogia
feeling phobia, hypnagogia

Verse
I talk to myself and talk about myself this talk recursive
talk is cheap is and I buy a lot, it's discounting being discursive
World is noisy need some introversion for my introspection
We see eye to eye I need a new perspective causa ya vision blurry
I've been losing sleep over trynna be lose my losing streak and add some wins but it's inversive
not Counting sheep I can't count my blessings I've been adding curses

I put it on me and if I don't make it my bad
I've been a wake for so long that I can't the last time I had to be making my bed
I live on the edge I'll sleep when I am dead and if I slip then I am dead
Life is a gab and I'm trying slip through the crack
we never make it out of live alive so I gotta make this my best

I want some help and I want some sleep
I need to love and I need to live
I want to take but I need to give
I think that I am at a point were I want my needs and need my wants

    """),

    LyricDoc("5", "Last time I saw you", 
    """ 
Pre-chorus
I had a vision you were the one
I hope that I am tripping and fall in your arms
I wish I could give you all of the flowers I never could
I wish I could give you all of the flowers they never do
I hope I ain't tripping I am falling for ya
I had a vision I was your one

Chorus:
I miss you, it's a nightmare the last time I saw you was in a dream
I woke up, you were not there ya the reason I wake or fall asleep
It's not fair and I know that but you're the one that I want to need
I miss you in this nightmare the last time I saw you, you was a dream

Verse 1:
I woke up, you were gone so I fell asleep to being you the second time
It's not the first time I've said that it's the last time
so last time is another time
What a time! man time flies
I think of you every time that I picture perfect
I stored all the fantasies and memories we had
I still recall everything about you from you favorite colors to your deepest secrets
Favorite colors - Pink and purple
Deepest secrets - I'm keepin' 'em til the day I am buried
    """),
]

store = SQLiteFeedbackStore("ll_feedback.db")
engine = LLSearchEngine(feedback_store=store)
engine.index(docs)

print("Search:", engine.search("miss you", top_k=3))

fb = Feedback(store)
fb.clicked("miss you", "5") # user liked it
fb.thumbs_up("miss you", "5")

print("Search after feedback:", engine.search("miss you", top_k=3))


# store.clear()