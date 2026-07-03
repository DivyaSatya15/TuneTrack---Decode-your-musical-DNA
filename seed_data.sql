
-- ============================================================
--  SEED DATA — insert some starter records to test with
-- ============================================================

-- Genres
INSERT INTO genres (genre_name) VALUES
    ('Pop Rock'),
    ('Hip Hop'),
    ('Electronic'),
    ('Pop'),
    ('Metal'),
    ('Soul'),
    ('R&B'),
    ('Rock'),
    ('Indie Pop'),
    ('Alternative'),
    ('Classic Rock'),
    ('Grunge');

-- Artists
INSERT INTO artists (artist_name, country) VALUES
    ('Coldplay',      'UK'),
    ('Eminem',        'USA'),
    ('Daft Punk',     'France'),
    ('Ed Sheeran',    'UK'),
    ('Metallica',     'USA'),
    ('Adele',         'UK'),
    ('The Weeknd',    'Canada'),
    ('Linkin Park',   'USA'),
    ('Billie Eilish', 'USA'),
    ('Radiohead',     'UK');

-- Artist → Genre links
INSERT INTO artist_genres (artist_id, genre_id) VALUES
    (1,  1),   -- Coldplay → Pop Rock
    (2,  2),   -- Eminem → Hip Hop
    (3,  3),   -- Daft Punk → Electronic
    (4,  4),   -- Ed Sheeran → Pop
    (5,  5),   -- Metallica → Metal
    (6,  6),   -- Adele → Soul
    (7,  7),   -- The Weeknd → R&B
    (8,  8),   -- Linkin Park → Rock
    (9,  9),   -- Billie Eilish → Indie Pop
    (10, 10);  -- Radiohead → Alternative

-- Listening_history
INSERT INTO listening_history
(user_id, track_id, played_at, session_duration, is_completed)
VALUES
(1, 1, '2026-07-01 08:30:00', 35, TRUE),
(1, 2, '2026-07-01 09:15:00', 20, TRUE),
(1, 5, '2026-07-01 14:45:00', 40, FALSE),
(1, 3, '2026-07-01 19:20:00', 50, TRUE),
(1, 8, '2026-07-02 07:50:00', 25, TRUE),
(1, 10,'2026-07-02 22:10:00', 60, TRUE);

-- Tracks
INSERT INTO tracks
(track_name, artist_id, duration_sec, release_year, popularity_score)
VALUES
('Yellow', 1, 269, 2000, 94.5),
('Fix You', 1, 295, 2005, 96.2),
('Viva La Vida', 1, 242, 2008, 97.8),

('Lose Yourself', 2, 326, 2002, 99.5),
('Without Me', 2, 290, 2002, 97.1),
('The Real Slim Shady', 2, 284, 2000, 96.5),

('One More Time', 3, 320, 2000, 95.4),
('Get Lucky', 3, 369, 2013, 98.2),

('Perfect', 4, 263, 2017, 98.0),
('Shape of You', 4, 233, 2017, 99.0),

('Nothing Else Matters', 5, 388, 1991, 96.4),
('Enter Sandman', 5, 331, 1991, 97.3),

('Hello', 6, 295, 2015, 98.8),
('Rolling in the Deep', 6, 228, 2010, 98.0),

('Blinding Lights', 7, 200, 2020, 99.8),
('Starboy', 7, 230, 2016, 98.6),

('Numb', 8, 187, 2003, 98.9),
('In the End', 8, 216, 2000, 99.2),

('Bad Guy', 9, 194, 2019, 98.5),
('Ocean Eyes', 9, 200, 2016, 95.0),

('Creep', 10, 239, 1992, 97.4),
('Karma Police', 10, 261, 1997, 96.1);

--User_moods
INSERT INTO user_moods
(play_id, mood_label)
VALUES
(1,'Morning Boost'),
(2,'Focused'),
(3,'Afternoon Focus'),
(4,'Evening Chill'),
(5,'Morning Boost'),
(6,'Night Owl');

-- Test user (password = 'test123' — use hashed in real app)
INSERT INTO users (username, email, password_hash) VALUES
    ('tunetrack_user', 'test@tunetrack.com', 'hashed_password_here');

SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM genres;
SELECT COUNT(*) FROM artist_genres;
SELECT COUNT(*) FROM tracks;
SELECT COUNT(*) FROM listening_history;
SELECT COUNT(*) FROM user_moods;

-- TEST RELATIONSHIP
SELECT
    t.track_name,
    a.artist_name
FROM tracks t
JOIN artists a
ON t.artist_id = a.artist_id;

-- ============================================================
--  USEFUL QUERIES 
-- ============================================================

-- Q1: Top 10 most played artists for user 1
SELECT
    a.artist_name,
    COUNT(*) AS play_count,
    COUNT(DISTINCT DATE(lh.played_at)) AS active_days
FROM listening_history lh
JOIN tracks t
    ON lh.track_id = t.track_id
JOIN artists a
    ON t.artist_id = a.artist_id
WHERE lh.user_id = 1
GROUP BY a.artist_name
ORDER BY play_count DESC
LIMIT 10;


-- Q2: Top genres for user 1
SELECT
    g.genre_name,
    COUNT(*) AS total_plays,
    COUNT(DISTINCT a.artist_id) AS unique_artists
FROM listening_history lh
JOIN tracks t
    ON lh.track_id = t.track_id
JOIN artists a
    ON t.artist_id = a.artist_id
JOIN artist_genres ag
    ON a.artist_id = ag.artist_id
JOIN genres g
    ON ag.genre_id = g.genre_id
WHERE lh.user_id = 1
GROUP BY g.genre_name
ORDER BY total_plays DESC
LIMIT 10;


-- Q3: Mood distribution for user 1
SELECT
    um.mood_label,
    COUNT(*) AS total
FROM user_moods um
JOIN listening_history lh
    ON um.play_id = lh.play_id
WHERE lh.user_id = 1
GROUP BY um.mood_label
ORDER BY total DESC;

-- Q4: Listening by hour of day (when does user 1 listen most?)
SELECT
    EXTRACT(HOUR FROM played_at) AS hour_of_day,
    COUNT(*) AS plays
FROM listening_history
WHERE user_id = 1
GROUP BY EXTRACT(HOUR FROM played_at)
ORDER BY hour_of_day;

-- Q5: Daily play count (for streak calendar)
SELECT
    DATE(played_at) AS play_date,
    COUNT(*)        AS plays
FROM listening_history
WHERE user_id = 1
GROUP BY play_date
ORDER BY play_date;


-- Q6: Overall summary stats for user 1
SELECT
    COUNT(*) AS total_plays,
    COUNT(DISTINCT t.artist_id) AS unique_artists,
    COUNT(DISTINCT lh.track_id) AS unique_tracks,
    COUNT(DISTINCT DATE(lh.played_at)) AS active_days
FROM listening_history lh
JOIN tracks t
    ON lh.track_id = t.track_id
WHERE lh.user_id = 1;


