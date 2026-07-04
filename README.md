
# 🎵 TuneTrack — Decode Your Musical DNA

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)

> "Every song you replay tells a story.
> Every artist you return to reveals a part of you.
> TuneTrack doesn't just track music—
> it decodes your Musical DNA."


## 🎧 What is TuneTrack?

Music isn't just something we listen to.

It's how we celebrate.
It's how we heal.
It's how we remember moments that words fail to describe.

That song you've replayed 47 times? It's not random.
That artist you always return to? There's a reason.
That playlist you made at 2 AM? It was never just about the music.

TuneTrack is an intelligent music analytics platform that transforms your listening history into meaningful insights. Instead of simply counting songs, it discovers the patterns hidden inside your listening behavior — revealing your unique Musical DNA.

Whether you're a late-night listener, an early-morning motivator, or someone who lives their entire life through playlists — TuneTrack helps you understand the soundtrack of your life.

**Because your music has been keeping a diary about you. It's time you read it.**


## ✨ Why TuneTrack?

Most music platforms tell you **what** you listened to.

TuneTrack tells you **why your music habits make you unique.**

Because every playlist tells a story.
Every replay reflects an emotion.
Every skipped song is a feeling you weren't ready for.
Every listener has a musical identity — waiting to be discovered.

There are a million music apps in the world.
But none of them ever asked the most important question:

**What does your music say about you?**

TuneTrack does.


## 🧬 Decode Your Musical DNA

TuneTrack analyzes your listening history to uncover insights like:

Insight                             |             What It Reveals About You
-------------------------------------------------------------------------------------------------
🎵Most Played Artists                            The voices you keep coming back to
🎼Favorite Genres                                The world you live in when nobody's watching
🌅Peak Listening Hours                           When music matters most to you
😊Mood Patterns                                  How your emotions shape your playlist
📅Listening Consistency                          The rhythm of your daily life
🔥Music Streaks                                  How deeply music is woven into your routine
🎧Recently Played Tracks                         The story of your last few days
📊Personalized Analytics                         Your complete musical identity, visualized


## 🚀 Features
* 👤Secure User Authentication — your data, only yours
* 🗄️ PostgreSQL Relational Database — normalized, indexed, production-grade design
* 🎵 Listening History Tracking — every play, every pattern, every moment
* 🎤 Artist & Genre Analysis — discover what you truly love
* 😊 Mood Detection from Listening Patterns — your emotions, decoded
* 📈 Interactive Music Insights — beautiful charts that tell your story
* 🧬 Personalized Musical DNA Dashboard — your identity, visualized
* ⚡ Optimized SQL Queries — fast, indexed, built for real performance


## 🛠️ Tech Stack

Backend : Python 3.10+

Database : PostgreSQL 16

Libraries :
           1. Streamlit — interactive web dashboard
           2. Pandas — data cleaning and processing
           3. psycopg2 — PostgreSQL connection
           4. python-dotenv — secure environment variables
           5. Plotly — beautiful interactive charts
Version Control : Git & GitHub

## 🗄️ Database Design

TuneTrack follows a fully normalized relational database architecture — designed from scratch before a single line of Python was written.


users ──────────────────┐
                        ├──► listening_history ◄──── tracks ◄──── artists
user_moods ─────────────┘                                              │
                                                               artist_genres
genres ────────────────────────────────────────────────────────────────┘


* 7 core tables:

Table                                  Purpose
users                                  Secure multi-user authentication
artists                                Every unique artist in the dataset
genres                                 Master genre list
artist_genres                          Many-to-many junction table — one artist, many genres
tracks                                 Songs with popularity score, release year, duration
listening_history                      Every play event — the core analytics table
user_moods                             Mood tags per play — unique to TuneTrack


What makes this design stand out:

* Junction table for artist-genre many-to-many relationships
* Indexed foreign keys on all high-frequency query columns
* popularity_score and release_year unlock decade analysis and mainstream vs underground insights
* Dedicated user_moods table — a feature no similar student project has


**Full schema → schema.sql**

## 💡 Project Vision

Imagine opening your music history and discovering:

"You listen to calm music after stressful days."
"You become more energetic on Friday evenings."
"You've been loyal to one artist for over three years."

That's not just data. That's self-awareness.

That's the future TuneTrack is designed to build.

**Music is data.**
**Emotions leave patterns.**
**TuneTrack connects both.**


## 📁 Project Structure

TuneTrack/
│
├── 📂 database/
│   └── db.py
│    └── schema.sql
│    └── seed_data.sql
│
├── 📂 docs/
│   └── setup.md
│
├── 🐍 .gitignore 
├── 🐍 app.py                             
├── 📄 requirements.txt
└── 📄 README.md

**for the full setup guide -> setup.md**


## 🎯 Future Roadmap

* Spotify API Integration — live personal data, not just CSV
* Last.fm Dataset Support
* AI-powered Mood Prediction
* Music Recommendation Engine
* Weekly Listening Reports — every Sunday, your week in music
* Playlist Personality Analysis
* Friend Comparison — whose Musical DNA matches yours?


## ❤️ Built For

People who don't just listen to music.
They live through it.

If you've ever replayed one song because it reminded you of someone —
If you've ever made a playlist for a feeling you couldn't explain —
If you've ever sat alone at night with your headphones in, and felt completely understood —
If music has ever said the thing you couldn't find the words for —

Then TuneTrack was built for you.

**"For the one who don't just hear music — they feel it."**


# 👨‍💻 Developer

Built with Python, PostgreSQL, and countless playlists —
TuneTrack began with one question:
    "What is my music actually telling me?"

Every table in the database was designed with intention.
Every query was written to answer something real.
Every chart on the dashboard tells a story I wanted to see.

        "Because sometimes the best way to understand ourselves…
        is to understand the music we never skip."


<div align="center">
🎵 TuneTrack Is Now Yours

You've read this far — which means you're not just a visitor.
You're someone who felt something reading this.

Maybe you're a developer who wants to contribute.
Maybe you're a recruiter who sees something worth noticing.
Maybe you're just a music lover who finally found an app that gets it.

Whoever you are — TuneTrack is now yours to explore.

Fork it. Star it. Build on it. Make it your own.

Because music was never meant to be kept to yourself.

⭐ If this project moved you even a little — leave a star. It means the world.

**TuneTrack — Because your playlist knows you better than you think.**