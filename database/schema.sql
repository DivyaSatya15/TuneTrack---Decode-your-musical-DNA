
-- ============================================================
--  TuneTrack — Full PostgreSQL Database Schema
--  Command:  psql -U postgres -d tunetrack -f schema.sql
-- ============================================================


-- CREATE DATABASE tunetrack;


-- ── 1. USERS ─────────────────────────────────────────────────
--  Stores everyone who logs into TuneTrack
-- ─────────────────────────────────────────────────────────────
CREATE TABLE users (
    user_id       SERIAL          PRIMARY KEY,
    username      VARCHAR(50)     NOT NULL UNIQUE,
    email         VARCHAR(100)    NOT NULL UNIQUE,
    password_hash VARCHAR(255)    NOT NULL,        -- never store plain passwords
    created_at    TIMESTAMP       DEFAULT NOW(),
    last_login    TIMESTAMP
);


-- ── 2. ARTISTS ───────────────────────────────────────────────
--  Every unique artist that appears in the dataset
-- ─────────────────────────────────────────────────────────────
CREATE TABLE artists (
    artist_id   SERIAL        PRIMARY KEY,
    artist_name VARCHAR(150)  NOT NULL UNIQUE,
    country     VARCHAR(80),
    created_at  TIMESTAMP     DEFAULT NOW()
);


-- ── 3. GENRES ────────────────────────────────────────────────
--  Master list of genres (Pop, Hip-Hop, Rock, Lo-fi, Classical etc.)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE genres (
    genre_id   SERIAL       PRIMARY KEY,
    genre_name VARCHAR(80)  NOT NULL UNIQUE
);


-- ── 4. ARTIST_GENRES ─────────────────────────────────────────
--  One artist can belong to many genres.
--  This is a junction / bridge table.
--  Example: Coldplay → Pop Rock, Alternative
-- ─────────────────────────────────────────────────────────────
CREATE TABLE artist_genres (
    artist_id  INT  NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    genre_id   INT  NOT NULL REFERENCES genres(genre_id)   ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)   -- composite key, no duplicates
);


-- ── 5. TRACKS ────────────────────────────────────────────────
--  Every unique song in the dataset
-- ─────────────────────────────────────────────────────────────
CREATE TABLE tracks (
    track_id          SERIAL        PRIMARY KEY,
    track_name        VARCHAR(200)  NOT NULL,
    artist_id         INT           NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    duration_sec      INT,                      
    release_year      SMALLINT,
    popularity_score  NUMERIC(4,1),
    UNIQUE (track_name, artist_id)
);


-- ── 6. LISTENING_HISTORY ─────────────────────────────────────
--  The CORE table. Every single play event lives here.
--  This is where all your SQL queries will run.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE listening_history (
    play_id             SERIAL          PRIMARY KEY,
    user_id             INT             NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    track_id            INT             NOT NULL REFERENCES tracks(track_id) ON DELETE CASCADE,
    played_at           TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    session_duration    INT,
    is_completed        BOOLEAN         DEFAULT TRUE
);

-- ── 7. USER_MOODS ─────────────────────────────────────────────
--  Mood tags linked to specific play events.
--  mood_label values: 'Morning Boost', 'Afternoon Focus',
--                     'Evening Chill', 'Night Owl'
--  These are either auto-assigned or manually set by the user.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE user_moods (
    mood_id      SERIAL PRIMARY KEY,
    play_id      INT NOT NULL UNIQUE
                 REFERENCES listening_history(play_id)
                 ON DELETE CASCADE,
    mood_label   VARCHAR(50) NOT NULL
                 CHECK (mood_label IN (
                     'Morning Boost',
                     'Afternoon Focus',
                     'Evening Chill',
                     'Night Owl',
                     'Happy',
                     'Calm',
                     'Energetic',
                     'Relaxed',
                     'Focused'
                 )),
    tagged_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  INDEXES — makes your queries faster
-- ============================================================

CREATE INDEX idx_lh_user_id
ON listening_history(user_id);

CREATE INDEX idx_lh_track_id
ON listening_history(track_id);

CREATE INDEX idx_lh_played_at
ON listening_history(played_at);

-- Composite index for a user's listening history sorted by time

CREATE INDEX idx_user_played_at
ON listening_history(user_id, played_at DESC);

CREATE INDEX idx_song_artist
ON tracks(artist_id);

CREATE INDEX idx_um_mood_label
ON user_moods(mood_label);