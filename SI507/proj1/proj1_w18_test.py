import unittest
import proj1_w18 as proj1
import json

class TestMedia(unittest.TestCase):

    def test_init(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince", "2000")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m1.release_year, "0000")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertNotIn("movie_length", dir(m1))
        self.assertNotIn("album", dir(m1))


    def test_str(self):
        m1 = proj1.Media("1999", "Prince", "2000")
        self.assertEqual(m1.__str__(), "1999 by Prince (2000)")

    def test_len(self):
        m1 = proj1.Media("1999", "Prince", "2000")
        self.assertEqual(m1.__len__(), 0)

class TestSong(unittest.TestCase):

    def test_init(self):
        m1 = proj1.Song()
        m2 = proj1.Song('Lose Your Self', 'Eminem', '2002', '8 mile', 'Hip Hop', 267)
        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.track_length, 0)
        self.assertEqual(m1.genre, "No Genre")
        self.assertEqual(m2.genre, "Hip Hop")
        self.assertEqual(m2.author, "Eminem")
        self.assertNotIn("movie_length", dir(m1))
        self.assertNotIn("rating", dir(m1))

    def test_str(self):
        m1 = proj1.Song('Lose Your Self', 'Eminem', '2002', '8 mile', 'Hip Hop', 267)
        self.assertEqual(m1.__str__(), "Lose Your Self by Eminem (2002)[Hip Hop]")

    def test_len(self):
        m1 = proj1.Song('Lose Your Self', 'Eminem', '2002', '8 mile', 'Hip Hop', 267)
        self.assertEqual(m1.__len__(), 267)

class TestMovie(unittest.TestCase):

    def test_init(self):
        m1 = proj1.Movie()
        m2 = proj1.Movie('Terminal', 'Steven', '2004', 'PG', 128)
        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.movie_length, 0)
        self.assertEqual(m2.title, "Terminal")
        self.assertEqual(m2.movie_length, 128)
        self.assertEqual(m2.rating, "PG")
        self.assertNotIn("genre", dir(m1))
        self.assertNotIn("album", dir(m1))

    def test_str(self):
        m1 = proj1.Movie('Terminal', 'Steven', '2004', 'PG', 128)
        self.assertEqual(m1.__str__(), "Terminal by Steven (2004)[PG]")

    def test_len(self):
        m1 = proj1.Movie('Terminal', 'Steven', '2004', 'PG', 128)
        self.assertEqual(m1.__len__(), 128)

class TestJson(unittest.TestCase):

    with open("sample_json.json", 'r') as file:
        sample = json.load(file)

    for i in sample:
        if 'kind' in i:
            if i["kind"] == "song":
                song_test = proj1.Song(json= i)
            elif i["kind"] == "feature-movie":
                movie_test = proj1.Movie(json= i)
        else:
            media_test = proj1.Media(json=i)

    def test_init(self):

        with open("sample_json.json", 'r') as file:
            sample = json.load(file)

        for i in sample:
            if 'kind' in i:
                if i["kind"] == "song":
                    self.song_test = proj1.Song(json=i)
                elif i["kind"] == "feature-movie":
                    self.movie_test = proj1.Movie(json=i)
            else:
                self.media_test = proj1.Media(json= i)

        self.assertEqual(self.media_test.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(self.media_test.author, "Helen Fielding")
        self.assertEqual(self.media_test.release_year, 2012)

        self.assertEqual(self.song_test.title, "Hey Jude")
        self.assertEqual(self.song_test.author, "The Beatles")
        self.assertEqual(self.song_test.release_year, 1968)
        self.assertEqual(self.song_test.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(self.song_test.genre, "Rock")

        self.assertEqual(self.movie_test.title, "Jaws")
        self.assertEqual(self.movie_test.author, "Steven Spielberg")
        self.assertEqual(self.movie_test.release_year, 1975)
        self.assertEqual(self.movie_test.rating, "PG")

    def test_string(self):

        self.assertEqual(self.media_test.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
        self.assertEqual(self.song_test.__str__(), "Hey Jude by The Beatles (1968)[Rock]")
        self.assertEqual(self.movie_test.__str__(), "Jaws by Steven Spielberg (1975)[PG]")

    def test_len(self):

        self.assertEqual(len(self.media_test), 0)
        self.assertEqual(len(self.song_test), 431)
        self.assertEqual(len(self.movie_test), 124)

class TestItunes(unittest.TestCase):

    def query(self, query):

        for result in proj1.getiTunes(query):
            if 'kind' in result:
                if result["kind"] == "song":
                    test = proj1.Song(result)
                elif result["kind"] == "feature-movie":
                    test = proj1.Movie(result)
            else:
                test = proj1.Media(result)

            self.assertIsNotNone(test.title)
            self.assertIsNotNone(test.author)
            self.assertIsNotNone(test.release_year)


            if type(test) is proj1.Song:
                self.assertIsNotNone(test.album)
                self.assertIsNotNone(test.genre)
                self.assertIsNotNone(test.track_length)

            if type(test) is proj1.Movie:
                self.assertIsNotNone(test.rating)
                self.assertIsNotNone(test.movie_length)

    def test_commonwords(self):
        self.query("baby")
        self.query("love")

    def test_uncommonwords(self):
        self.query("moana")
        self.query("helter skelter")

    def test_nonsensequeries(self):
        self.query("&@#!$")

    def test_blankquery(self):
        self.query("")




unittest.main()
