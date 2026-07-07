
from database.db import get_connection
import bcrypt
import time

# ─────────────────────────────────────────────────────────────
#  STYLING HELPERS
# ─────────────────────────────────────────────────────────────

def divider():
    print("\n" + "─" * 55)

def thick_divider():
    print("\n" + "═" * 55)

def section_header(title, emoji="🎵"):
    print("\n" + "═" * 55)
    print(f"   {emoji}  {title}")
    print("═" * 55)

def sub_header(title):
    print("\n" + "─" * 45)
    print(f"  {title}")
    print("─" * 45)

def success(msg):
    print(f"\n  ✅  {msg}")

def error(msg):
    print(f"\n  ❌  {msg}")

def info(msg):
    print(f"\n  ✦  {msg}")

def heartfelt(msg):
    print(f"\n  ♪  {msg}")

def slow_print(text, delay=0.03):
    """Prints text character by character for dramatic effect."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


# ─────────────────────────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────────────────────────

connection = get_connection()
if connection:
    cursor = connection.cursor()
else:
    print("\n  ❌  Could not connect to the database. Please check your settings.")
    exit()


# ─────────────────────────────────────────────────────────────
#  WELCOME SCREEN
# ─────────────────────────────────────────────────────────────

def show_welcome():
    print("\n")
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║                                                   ║")
    print("  ║        🎵   T U N E T R A C K   🎵               ║")
    print(" ║            D e c o d e  Y o u r                   ║")
    print(" ║              M u s i c a l  D N A                 ║")
    print("  ║                                                   ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print()
    slow_print("  Your music has been keeping a diary about you.", 0.02)
    slow_print("  It's time you read it. 🎧", 0.02)
    print()

show_welcome()


# ─────────────────────────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────────────────────────

def register_user():
    section_header("Create Your TuneTrack Account", "👤")
    heartfelt("Every great musical journey starts with one step.")
    heartfelt("Let's begin yours.\n")

    username = input("  Enter Username    : ").strip()
    email    = input("  Enter Email       : ").strip()
    password = input("  Enter Password    : ").strip()

    if not username or not email or not password:
        error("All fields are required.")
        return

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        connection.commit()

        divider()
        print(f"\n  ✅  Welcome to TuneTrack, {username}! 🎉")
        heartfelt("Your Musical DNA journey has officially begun.")
        heartfelt("Every song you log brings you closer to knowing yourself.")
        divider()

    except Exception as e:
        connection.rollback()
        error("Registration failed. This email or username may already exist.")


# ─────────────────────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────────────────────

def login_user():
    section_header("Welcome Back", "🔑")
    heartfelt("Your music missed you.\n")

    email    = input("  Enter Email    : ").strip()
    password = input("  Enter Password : ").strip()

    try:
        cursor.execute(
            "SELECT username, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if user:
            username        = user[0]
            stored_password = user[1]

            if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                print()
                slow_print(f"  🎉  Welcome back, {username}!", 0.03)
                heartfelt("Your story continued while you were away.")
                heartfelt("Let's see what your playlist has been saying about you.")
                time.sleep(0.5)
                user_dashboard(username)
            else:
                error("Incorrect password. Please try again.")
        else:
            error("No account found with this email.")

    except Exception as e:
        error("Login failed.")
        print(f"  {e}")


# ─────────────────────────────────────────────────────────────
#  ARTIST MANAGEMENT
# ─────────────────────────────────────────────────────────────

def add_artist():
    section_header("Add New Artist", "🎤")

    artist_name = input("  Artist Name : ").strip()
    country     = input("  Country     : ").strip()

    if not artist_name or not country:
        error("Artist name and country cannot be empty.")
        return

    try:
        cursor.execute(
            "INSERT INTO artists (artist_name, country) VALUES (%s, %s)",
            (artist_name, country)
        )
        connection.commit()
        success(f"'{artist_name}' has been added to TuneTrack! 🎸")
        heartfelt("Every artist you add is a part of your world.")

    except Exception as e:
        connection.rollback()
        error("Failed to add artist. They may already exist.")


def view_artists():
    section_header("All Artists", "🎤")

    try:
        cursor.execute(
            "SELECT artist_id, artist_name, country FROM artists ORDER BY artist_name"
        )
        artists = cursor.fetchall()

        if not artists:
            error("No artists found. Add some to begin your journey.")
            return

        print(f"\n  {'ID':<6}{'Artist Name':<28}{'Country'}")
        print("  " + "─" * 48)
        for a in artists:
            print(f"  {a[0]:<6}{a[1]:<28}{a[2]}")

        divider()
        info(f"{len(artists)} artist(s) in your TuneTrack universe.")

    except Exception as e:
        error("Failed to fetch artists.")


def update_artist():
    section_header("Update Artist", "✏️")
    view_artists()

    try:
        artist_id   = int(input("\n  Enter Artist ID to update : "))
        new_name    = input("  New Artist Name            : ").strip()
        new_country = input("  New Country                : ").strip()

        cursor.execute(
            "UPDATE artists SET artist_name = %s, country = %s WHERE artist_id = %s",
            (new_name, new_country, artist_id)
        )
        connection.commit()

        if cursor.rowcount == 0:
            error("Artist ID not found.")
        else:
            success("Artist updated successfully!")

    except Exception as e:
        connection.rollback()
        error("Failed to update artist.")


def delete_artist():
    section_header("Delete Artist", "🗑️")
    view_artists()

    try:
        artist_id = int(input("\n  Enter Artist ID to delete : "))
        confirm   = input("  Are you sure? (Y/N)        : ").strip().upper()

        if confirm != "Y":
            info("Deletion cancelled.")
            return

        cursor.execute("DELETE FROM artists WHERE artist_id = %s", (artist_id,))
        connection.commit()

        if cursor.rowcount == 0:
            error("Artist ID not found.")
        else:
            success("Artist removed from TuneTrack.")

    except Exception as e:
        connection.rollback()
        error("Failed to delete artist.")


# ─────────────────────────────────────────────────────────────
#  TRACK MANAGEMENT
# ─────────────────────────────────────────────────────────────

def add_track():
    section_header("Add New Track", "🎵")

    try:
        cursor.execute(
            "SELECT artist_id, artist_name FROM artists ORDER BY artist_name"
        )
        artists = cursor.fetchall()

        if not artists:
            error("No artists found. Please add an artist first.")
            return

        print(f"\n  {'ID':<6}{'Artist'}")
        print("  " + "─" * 30)
        for a in artists:
            print(f"  {a[0]:<6}{a[1]}")

        artist_id    = int(input("\n  Enter Artist ID         : "))
        track_name   = input("  Track Name              : ").strip()
        duration     = int(input("  Duration (seconds)      : "))
        release_year = int(input("  Release Year            : "))
        popularity   = float(input("  Popularity Score (0-100): "))

        # Auto-fetch artist_id validation
        cursor.execute("SELECT artist_id FROM artists WHERE artist_id = %s", (artist_id,))
        if not cursor.fetchone():
            error("Artist ID not found.")
            return

        cursor.execute(
            """INSERT INTO tracks (track_name, artist_id, duration_sec, release_year, popularity_score)
               VALUES (%s, %s, %s, %s, %s)""",
            (track_name, artist_id, duration, release_year, popularity)
        )
        connection.commit()

        success(f"'{track_name}' added to TuneTrack! 🎶")
        heartfelt("Every track you add is a chapter of your musical story.")

    except Exception as e:
        connection.rollback()
        error("Failed to add track.")
        print(f"  {e}")


def view_tracks():
    section_header("All Tracks", "🎵")

    try:
        cursor.execute("""
            SELECT t.track_id, t.track_name, a.artist_name,
                   t.release_year, t.duration_sec, t.popularity_score
            FROM tracks t
            JOIN artists a ON t.artist_id = a.artist_id
            ORDER BY t.track_name
        """)
        tracks = cursor.fetchall()

        if not tracks:
            error("No tracks found. Start adding your music!")
            return

        print(f"\n  {'ID':<5}{'Track':<26}{'Artist':<22}{'Year':<7}{'Dur(s)':<9}{'Pop'}")
        print("  " + "─" * 75)
        for t in tracks:
            print(f"  {t[0]:<5}{t[1]:<26}{t[2]:<22}{t[3]:<7}{t[4]:<9}{t[5]}")

        divider()
        info(f"{len(tracks)} track(s) in your TuneTrack collection.")

    except Exception as e:
        error("Failed to fetch tracks.")


def update_track():
    section_header("Update Track", "✏️")
    view_tracks()

    try:
        track_id = int(input("\n  Enter Track ID to update : "))

        cursor.execute(
            "SELECT artist_id, artist_name FROM artists ORDER BY artist_name"
        )
        artists = cursor.fetchall()
        print(f"\n  {'ID':<6}{'Artist'}")
        print("  " + "─" * 30)
        for a in artists:
            print(f"  {a[0]:<6}{a[1]}")

        artist_id    = int(input("\n  New Artist ID           : "))
        track_name   = input("  New Track Name          : ").strip()
        duration     = int(input("  New Duration (seconds)  : "))
        release_year = int(input("  New Release Year        : "))
        popularity   = float(input("  New Popularity Score    : "))

        cursor.execute(
            """UPDATE tracks SET track_name=%s, artist_id=%s, duration_sec=%s,
               release_year=%s, popularity_score=%s WHERE track_id=%s""",
            (track_name, artist_id, duration, release_year, popularity, track_id)
        )
        connection.commit()

        if cursor.rowcount == 0:
            error("Track ID not found.")
        else:
            success("Track updated successfully!")

    except Exception as e:
        connection.rollback()
        error("Failed to update track.")


def delete_track():
    section_header("Delete Track", "🗑️")
    view_tracks()

    try:
        track_id = int(input("\n  Enter Track ID to delete : "))
        confirm  = input("  Are you sure? (Y/N)       : ").strip().upper()

        if confirm != "Y":
            info("Deletion cancelled.")
            return

        cursor.execute("DELETE FROM tracks WHERE track_id = %s", (track_id,))
        connection.commit()

        if cursor.rowcount == 0:
            error("Track ID not found.")
        else:
            success("Track removed from TuneTrack.")

    except Exception as e:
        connection.rollback()
        error("Failed to delete track.")


# ─────────────────────────────────────────────────────────────
#  LISTENING HISTORY
# ─────────────────────────────────────────────────────────────

def listening_history_menu():
    while True:
        section_header("Listening History", "🎧")
        heartfelt("Every listen is a moment. Every moment tells your story.\n")
        print("   1.  Add Listening Record")
        print("   2.  View Listening History")
        print("   3.  Update Listening Record")
        print("   4.  Delete Listening Record")
        print("   5.  ← Back")

        choice = input("\n  Enter your choice : ").strip()

        if choice == "1":
            add_listening_history()
        elif choice == "2":
            view_listening_history()
        elif choice == "3":
            update_listening_history()
        elif choice == "4":
            delete_listening_history()
        elif choice == "5":
            break
        else:
            error("Invalid choice. Please enter 1-5.")


def add_listening_history():
    section_header("Log a Listening Session", "🎧")
    heartfelt("What were you listening to?\n")

    try:
        cursor.execute("SELECT user_id, username FROM users ORDER BY username")
        users = cursor.fetchall()

        if not users:
            error("No users found.")
            return

        print(f"  {'ID':<6}{'Username'}")
        print("  " + "─" * 25)
        for u in users:
            print(f"  {u[0]:<6}{u[1]}")

        user_id = int(input("\n  Enter User ID : "))

        cursor.execute("""
            SELECT t.track_id, t.track_name, a.artist_name
            FROM tracks t JOIN artists a ON t.artist_id = a.artist_id
            ORDER BY t.track_name
        """)
        tracks = cursor.fetchall()

        if not tracks:
            error("No tracks found. Please add tracks first.")
            return

        print(f"\n  {'ID':<6}{'Track':<28}{'Artist'}")
        print("  " + "─" * 55)
        for t in tracks:
            print(f"  {t[0]:<6}{t[1]:<28}{t[2]}")

        track_id         = int(input("\n  Enter Track ID              : "))
        session_duration = int(input("  Session Duration (seconds)  : "))
        completed        = input("  Did you complete the song? (Y/N): ").strip().upper()
        is_completed     = completed == "Y"

        # Auto-fetch artist_id from track
        cursor.execute("SELECT artist_id FROM tracks WHERE track_id = %s", (track_id,))
        track_row = cursor.fetchone()
        if not track_row:
            error("Track ID not found.")
            return
        artist_id = track_row[0]

        cursor.execute(
            """INSERT INTO listening_history
               (user_id, track_id, session_duration, is_completed)
               VALUES (%s, %s, %s, %s)""",
            (user_id, track_id, session_duration, is_completed)
        )
        connection.commit()

        success("Listening record added! 🎵")
        if is_completed:
            heartfelt("You listened to the whole song. That song meant something to you.")
        else:
            heartfelt("Even a few seconds with a song leaves a mark.")

    except Exception as e:
        connection.rollback()
        error("Failed to add listening record.")
        print(f"  {e}")


def view_listening_history():
    section_header("Your Listening History", "🎧")

    try:
        cursor.execute("""
            SELECT lh.play_id, u.username, t.track_name, a.artist_name,
                   lh.played_at, lh.session_duration, lh.is_completed
            FROM listening_history lh
            JOIN users u   ON lh.user_id   = u.user_id
            JOIN tracks t  ON lh.track_id  = t.track_id
            JOIN artists a ON t.artist_id   = a.artist_id
            ORDER BY lh.played_at DESC
        """)
        records = cursor.fetchall()

        if not records:
            error("No listening history found yet.")
            heartfelt("Start logging your music — your story is waiting to be written.")
            return

        print(f"\n  {'ID':<5}{'User':<14}{'Track':<24}{'Artist':<20}{'Played At':<22}{'Dur(s)':<8}{'Done'}")
        print("  " + "─" * 100)
        for r in records:
            status = "✅" if r[6] else "⏸"
            print(f"  {r[0]:<5}{r[1]:<14}{r[2]:<24}{r[3]:<20}{str(r[4]):<22}{r[5]:<8}{status}")

        divider()
        info(f"{len(records)} listening record(s) found.")

    except Exception as e:
        error("Failed to fetch listening history.")


def update_listening_history():
    section_header("Update Listening Record", "✏️")
    view_listening_history()

    try:
        play_id = int(input("\n  Enter Play ID to update : "))

        cursor.execute("SELECT user_id, username FROM users ORDER BY username")
        users = cursor.fetchall()
        print(f"\n  {'ID':<6}{'Username'}")
        for u in users:
            print(f"  {u[0]:<6}{u[1]}")
        user_id = int(input("\n  New User ID : "))

        cursor.execute("""
            SELECT t.track_id, t.track_name, a.artist_name
            FROM tracks t JOIN artists a ON t.artist_id = a.artist_id
            ORDER BY t.track_name
        """)
        tracks = cursor.fetchall()
        print(f"\n  {'ID':<6}{'Track':<28}{'Artist'}")
        for t in tracks:
            print(f"  {t[0]:<6}{t[1]:<28}{t[2]}")
        track_id         = int(input("\n  New Track ID               : "))
        session_duration = int(input("  New Session Duration (sec) : "))
        completed        = input("  Completed? (Y/N)            : ").strip().upper()
        is_completed     = completed == "Y"

        cursor.execute("""
        UPDATE listening_history
        SET user_id=%s, 
            track_id=%s, 
            session_duration=%s, 
            is_completed=%s
        WHERE play_id=%s""",
        (user_id, track_id, session_duration, is_completed, play_id)
        )
        connection.commit()

        if cursor.rowcount == 0:
            error("Play ID not found.")
        else:
            success("Listening record updated successfully!")

    except Exception as e:
        connection.rollback()
        error("Failed to update listening record.")


def delete_listening_history():
    section_header("Delete Listening Record", "🗑️")
    view_listening_history()

    try:
        play_id = int(input("\n  Enter Play ID to delete : "))
        confirm = input("  Are you sure? (Y/N)      : ").strip().upper()

        if confirm != "Y":
            info("Deletion cancelled.")
            return

        cursor.execute("DELETE FROM listening_history WHERE play_id = %s", (play_id,))
        connection.commit()

        if cursor.rowcount == 0:
            error("Play ID not found.")
        else:
            success("Listening record deleted.")

    except Exception as e:
        connection.rollback()
        error("Failed to delete listening record.")


# ─────────────────────────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────────────────────────

def analytics_menu():
    while True:
        section_header("TuneTrack Analytics", "📊")
        heartfelt("Numbers don't lie. Your music tells the truth.\n")
        print("   1.  Total Users")
        print("   2.  Total Artists")
        print("   3.  Total Tracks")
        print("   4.  Total Listening Records")
        print("   5.  Most Played Artist")
        print("   6.  Most Played Track")
        print("   7.  Total Listening Time")
        print("   8.  Completion Rate")
        print("   9.  ← Back")

        choice = input("\n  Enter your choice : ").strip()

        if choice == "1":
            total_users()
        elif choice == "2":
            total_artists()
        elif choice == "3":
            total_tracks()
        elif choice == "4":
            total_listening_records()
        elif choice == "5":
            most_played_artist()
        elif choice == "6":
            most_played_track()
        elif choice == "7":
            total_listening_time()
        elif choice == "8":
            completion_rate()
        elif choice == "9":
            break
        else:
            error("Invalid choice. Please enter 1-9.")


def total_users():
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        divider()
        print(f"\n  👤  Total Registered Users : {total}")
        heartfelt(f"{total} people are decoding their Musical DNA right now.")
    except Exception as e:
        error("Failed to fetch total users.")


def total_artists():
    try:
        cursor.execute("SELECT COUNT(*) FROM artists")
        total = cursor.fetchone()[0]
        divider()
        print(f"\n  🎤  Total Artists : {total}")
        heartfelt(f"{total} voices. Each one someone's reason to press play.")
    except Exception as e:
        error("Failed to fetch total artists.")


def total_tracks():
    try:
        cursor.execute("SELECT COUNT(*) FROM tracks")
        total = cursor.fetchone()[0]
        divider()
        print(f"\n  🎵  Total Tracks : {total}")
        heartfelt(f"{total} songs. That's {total} stories waiting to be felt.")
    except Exception as e:
        error("Failed to fetch total tracks.")


def total_listening_records():
    try:
        cursor.execute("SELECT COUNT(*) FROM listening_history")
        total = cursor.fetchone()[0]
        divider()
        print(f"\n  🎧  Total Listening Records : {total}")
        heartfelt(f"{total} moments where music was the answer.")
    except Exception as e:
        error("Failed to fetch total listening records.")


def most_played_artist():
    try:
        cursor.execute("""
            SELECT a.artist_name, COUNT(*) AS total_plays
            FROM listening_history lh
            JOIN tracks t  ON lh.track_id  = t.track_id
            JOIN artists a ON t.artist_id   = a.artist_id
            GROUP BY a.artist_name
            ORDER BY total_plays DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        divider()
        if result:
            print(f"\n  🏆  Most Played Artist : {result[0]}")
            print(f"  🎧  Total Plays        : {result[1]}")
            heartfelt(f"'{result[0]}' — the voice TuneTrack loves the most right now.")
        else:
            error("No listening history found yet.")
    except Exception as e:
        error("Failed to fetch most played artist.")


def most_played_track():
    try:
        cursor.execute("""
            SELECT t.track_name, COUNT(*) AS total_plays
            FROM listening_history lh
            JOIN tracks t ON lh.track_id = t.track_id
            GROUP BY t.track_name
            ORDER BY total_plays DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        divider()
        if result:
            print(f"\n  🎵  Most Played Track : {result[0]}")
            print(f"  🎧  Total Plays       : {result[1]}")
            heartfelt(f"'{result[0]}' — played {result[1]} times and counting.")
            heartfelt("Some songs just understand us better than words ever could.")
        else:
            error("No listening history found yet.")
    except Exception as e:
        error("Failed to fetch most played track.")


def total_listening_time():
    try:
        cursor.execute("SELECT SUM(session_duration) FROM listening_history")
        result = cursor.fetchone()

        if not result or result[0] is None:
            error("No listening history found yet.")
            return

        total_seconds = result[0]
        hours         = total_seconds // 3600
        minutes       = (total_seconds % 3600) // 60
        seconds       = total_seconds % 60

        divider()
        print(f"\n  ⏱️   Total Listening Time")
        print(f"\n       {hours}h  {minutes}m  {seconds}s")
        heartfelt(f"That's {hours} hours of letting music take over.")
        heartfelt("Every second you listened, you were exactly where you needed to be.")

    except Exception as e:
        error("Failed to calculate total listening time.")


def completion_rate():
    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_plays,
                   SUM(CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END) AS completed_plays
            FROM listening_history
        """)
        result = cursor.fetchone()

        total_plays     = result[0]
        completed_plays = result[1] or 0

        if total_plays == 0:
            error("No listening history found yet.")
            return

        rate = (completed_plays / total_plays) * 100

        divider()
        print(f"\n  📊  Completion Rate")
        print(f"\n       Completed Plays : {completed_plays}")
        print(f"       Total Plays     : {total_plays}")
        print(f"       Rate            : {rate:.2f}%")

        if rate >= 90:
            heartfelt("You don't skip songs. You feel every single one. That's rare.")
        elif rate >= 70:
            heartfelt("You give most songs the time they deserve. That's respect.")
        elif rate >= 50:
            heartfelt("You're selective. You know exactly what you want.")
        else:
            heartfelt("Quick sampler — always searching for the perfect sound.")

    except Exception as e:
        error("Failed to calculate completion rate.")


# ─────────────────────────────────────────────────────────────
#  MUSICAL DNA  ←  The heart of TuneTrack
# ─────────────────────────────────────────────────────────────

def musical_dna(username):

    print("\n")
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║                                                   ║")
    print("  ║           🧬  YOUR MUSICAL DNA  🧬               ║")
    print("  ║                                                   ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print()
    slow_print(f"  Decoding the musical identity of  →  {username}", 0.03)
    slow_print("  You've been listening your whole life.", 0.02)
    slow_print("  Now — for the first time — your music listens back.", 0.02)
    print()
    time.sleep(0.4)

    rate = 0  # default for personality calculation

    # ── SOUL ARTIST ──────────────────────────────────────────
    try:
        cursor.execute("""
            SELECT a.artist_name, COUNT(*) AS total_plays
            FROM listening_history lh
            JOIN users u   ON lh.user_id  = u.user_id
            JOIN tracks t  ON lh.track_id = t.track_id
            JOIN artists a ON t.artist_id  = a.artist_id
            WHERE u.username = %s
            GROUP BY a.artist_name
            ORDER BY total_plays DESC
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()

        divider()
        if result:
            print(f"\n  🎤  Soul Artist    :  {result[0]}  ({result[1]} plays)")
            heartfelt(f"'{result[0]}' isn't just your top artist.")
            heartfelt("This is the voice that understood you when nobody else did.")
        else:
            print("  🎤  Soul Artist    :  Not enough data yet")
            heartfelt("Start logging your music — your soul artist is waiting to be discovered.")
    except Exception as e:
        error("Could not fetch Soul Artist.")

    # ── FAVOURITE TRACK ───────────────────────────────────────
    try:
        cursor.execute("""
            SELECT t.track_name, COUNT(*) AS total_plays
            FROM listening_history lh
            JOIN users u  ON lh.user_id  = u.user_id
            JOIN tracks t ON lh.track_id = t.track_id
            WHERE u.username = %s
            GROUP BY t.track_name
            ORDER BY total_plays DESC
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()

        divider()
        if result:
            print(f"\n  🎵  Favourite Track :  {result[0]}  ({result[1]} plays)")
            heartfelt(f"You didn't just listen to '{result[0]}'.")
            heartfelt("You needed it. Again and again. That's not a song — that's a feeling.")
        else:
            print("  🎵  Favourite Track :  Not enough data yet")
    except Exception as e:
        error("Could not fetch Favourite Track.")

    # ── TOTAL PLAYS ───────────────────────────────────────────
    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM listening_history lh
            JOIN users u ON lh.user_id = u.user_id
            WHERE u.username = %s
        """, (username,))
        result = cursor.fetchone()
        total_plays = result[0]

        divider()
        print(f"\n  🎧  Total Plays    :  {total_plays}")
        heartfelt(f"{total_plays} moments where music was the answer.")

    except Exception as e:
        error("Could not fetch Total Plays.")

    # ── TOTAL LISTENING TIME ──────────────────────────────────
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(session_duration), 0)
            FROM listening_history lh
            JOIN users u ON lh.user_id = u.user_id
            WHERE u.username = %s
        """, (username,))
        result       = cursor.fetchone()
        total_secs   = result[0]
        total_mins   = round(total_secs / 60, 1)
        total_hours  = round(total_secs / 3600, 1)

        divider()
        print(f"\n  ⏱️   Listening Time :  {total_mins} minutes  ({total_hours} hours)")
        heartfelt(f"{total_hours} hours of letting music take over completely.")

    except Exception as e:
        error("Could not fetch Listening Time.")

    # ── COMPLETION RATE ───────────────────────────────────────
    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_plays,
                   SUM(CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END) AS completed_plays
            FROM listening_history lh
            JOIN users u ON lh.user_id = u.user_id
            WHERE u.username = %s
        """, (username,))
        result          = cursor.fetchone()
        total_plays     = result[0]
        completed_plays = result[1] or 0

        if total_plays > 0:
            rate = (completed_plays / total_plays) * 100
        else:
            rate = 0

        divider()
        print(f"\n  📊  Completion Rate :  {rate:.1f}%")

    except Exception as e:
        error("Could not fetch Completion Rate.")

    # ── MUSIC PERSONALITY ─────────────────────────────────────
    divider()
    try:
        if rate >= 90:
            personality = "🎯  Loyal Listener"
            description = "You don't skip. You don't rush. You feel every song completely.\n  That kind of loyalty to music is rare and beautiful."
        elif rate >= 70:
            personality = "🎶  Music Explorer"
            description = "You're always searching — for the next emotion, the next story.\n  Your playlist is never the same twice."
        elif rate >= 50:
            personality = "🎧  Casual Listener"
            description = "You pick your moments. When you listen, you truly listen.\n  Quality over quantity — that's your style."
        else:
            personality = "⚡  Quick Sampler"
            description = "You're always hunting for something that hits perfectly.\n  When you find it — you'll know and you'll play it forever."

        print(f"\n  🎭  Music Personality :  {personality}")
        print()
        heartfelt(description)

    except Exception as e:
        error("Could not generate Music Personality.")

    # ── CLOSING ───────────────────────────────────────────────
    print()
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║                                                   ║")
    print("  ║   Most people go their whole lives never knowing  ║")
    print("  ║   what their music says about them.               ║")
    print("  ║                                                   ║")
    print("  ║              You do now.  🎵                      ║")
    print("  ║                                                   ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print()
    heartfelt("Come back tomorrow — your Musical DNA is still evolving.")
    heartfelt("Every song you play is one more piece of you, discovered.")
    print()


# ─────────────────────────────────────────────────────────────
#  USER DASHBOARD
# ─────────────────────────────────────────────────────────────

def user_dashboard(username):
    while True:
        print("\n")
        print("  ╔═══════════════════════════════════════════════════╗")
        print(f" ║   🎵  TuneTrack Dashboard                          ║")
        print(f" ║   👋  Hey, {username:<40}                          ║")
        print("  ╚═══════════════════════════════════════════════════╝")
        heartfelt("Your story continued while you were away.")
        print()
        print("   1.  🎤  Artist Management")
        print("   2.  🎵  Track Management")
        print("   3.  🎧  Listening History")
        print("   4.  🧬  Musical DNA")
        print("   5.  📊  Analytics")
        print("   6.  🚪  Logout")

        choice = input("\n  Enter your choice : ").strip()

        if choice == "1":
            while True:
                section_header("Artist Management", "🎤")
                print("   1.  Add Artist")
                print("   2.  View Artists")
                print("   3.  Update Artist")
                print("   4.  Delete Artist")
                print("   5.  ← Back")
                c = input("\n  Enter your choice : ").strip()
                if c == "1":   add_artist()
                elif c == "2": view_artists()
                elif c == "3": update_artist()
                elif c == "4": delete_artist()
                elif c == "5": break
                else:          error("Invalid choice.")

        elif choice == "2":
            while True:
                section_header("Track Management", "🎵")
                print("   1.  Add Track")
                print("   2.  View Tracks")
                print("   3.  Update Track")
                print("   4.  Delete Track")
                print("   5.  ← Back")
                c = input("\n  Enter your choice : ").strip()
                if c == "1":   add_track()
                elif c == "2": view_tracks()
                elif c == "3": update_track()
                elif c == "4": delete_track()
                elif c == "5": break
                else:          error("Invalid choice.")

        elif choice == "3":
            listening_history_menu()

        elif choice == "4":
            musical_dna(username)

        elif choice == "5":
            analytics_menu()

        elif choice == "6":
            print()
            print("  ╔═══════════════════════════════════════════════════╗")
            print(f" ║     👋  See you soon, {username:<33}              ║")
            print("  ║                                                    ║")
            print("  ║   Your Musical DNA is still evolving.              ║")
            print("  ║   Come back — there's more of your story           ║")
            print("  ║   left to discover. 🎵                            ║")
            print("  ╚═══════════════════════════════════════════════════╝")
            print()
            break

        else:
            error("Invalid choice. Please enter 1-6.")


# ─────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────

while True:
    print("\n")
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │                  MAIN  MENU                     │")
    print("  ├─────────────────────────────────────────────────┤")
    print("  │   1.  Register  — Start your musical journey    │")
    print("  │   2.  Login     — Continue your story           │")
    print("  │   3.  Exit      — Until next time               │")
    print("  └─────────────────────────────────────────────────┘")

    choice = input("\n  Enter your choice : ").strip()

    if choice == "1":
        register_user()

    elif choice == "2":
        login_user()

    elif choice == "3":
        print()
        print("  ╔═══════════════════════════════════════════════════╗")
        print("  ║                                                   ║")
        print("  ║   🎵  Thank you for using TuneTrack.              ║")
        print("  ║                                                   ║")
        print("  ║   Because sometimes the best way to understand    ║")
        print("  ║   ourselves is the music we never skip.           ║")
        print("  ║                                                   ║")
        print("  ║              See you on the other side. 🎧        ║")
        print("  ╚═══════════════════════════════════════════════════╝")
        print()
        connection.close()
        break

    else:
        error("Invalid choice. Please enter 1, 2, or 3.")