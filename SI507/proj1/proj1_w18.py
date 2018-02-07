import json
import requests
import webbrowser

class Media:
    name = 'Media'
    def __init__(self, title="No Title", author="No Author", release_year = "0000", json= None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
        else:
            if 'kind' in json:
                self.title = json['trackName']

            elif json['wrapperType'] == 'audiobook':
                self.title = json['collectionName']

            self.author = json["artistName"]
            self.release_year = int(json["releaseDate"][:4])
            if 'trackViewUrl' in json:
                self.url = json["trackViewUrl"]
            elif 'collectionViewUrl' in json:
                self.url = json["collectionViewUrl"]
            else:
                self.url = None

    def __str__(self):
        s = "{0} by {1} ({2})".format(self.title, self.author, self.release_year)
        return s

    def __len__(self):
        return 0

class Song(Media):
    name = "Song"
    def __init__(self, title="No Title", author="No Author", release_year = "No Year", album= "No Album", genre= "No Genre", track_length = 0, json= None):
        if json is None:
            super().__init__(title, author, release_year, json)
            self.album = album
            self.genre = genre
            self.track_length = track_length

        else:
            super().__init__(title, author, release_year, json)
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = round(int(json["trackTimeMillis"]) / 1000)

    def __str__(self):
        return super().__str__() + "[{0}]".format(self.genre)

    def __len__(self):
        return self.track_length


class Movie(Media):
    name="Movie"
    def __init__(self, title="No Title", author="No Author", release_year = "No Year", rating = "No Rating", movie_length = 0, json=None):
        if json is None:
            super().__init__(title, author, release_year, json)
            self.rating = rating
            self.movie_length = movie_length
        else:
            super().__init__(title, author, release_year, json)
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = round(int(json["trackTimeMillis"])/1000/60)

    def __str__(self):
        return super().__str__() + "[{0}]".format(self.rating)

    def __len__(self):
        return round(self.movie_length)

def getiTunes(term, mx=20):
    baseurl = "https://itunes.apple.com/search"
    params = {}
    params['term'] = term
    params['limit'] = mx
    return requests.get(baseurl, params).json()["results"]

def store_results(results):
    storage_dict = {'Media': [], "Songs": [], "Movies": []}
    for i in results:
        if 'kind' in i:
            if i['kind'] == 'song':
                storage_dict['Songs'].append(Song(json=i))
            elif i['kind'] == "feature-movie":
                storage_dict['Movies'].append(Movie(json=i))
        else:
            storage_dict['Media'].append(Media(json=i))
    return storage_dict['Media'] + storage_dict['Songs'] + storage_dict['Movies']

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False




if __name__ == "__main__":
    word = input("Enter a search term or \"exit\" to quit: ")
    while word != "exit":
        results = store_results(getiTunes(word, 50))
        counter = 1
        current_type = None
        newsearch = True
        if len(results) > 0:
            for result in results:
                if type(result) != current_type:
                    current_type = type(result)
                    print(str(result.name))
                print(str(counter) + " - " + result.__str__())
                counter += 1
                newsearch = False
        else:
            print("No results found for " + word)
            word = input("Enter a search term or \"exit\" to quit: ")
            if word == "exit":
                break
            newsearch = True
        while not newsearch:
            word = input("Enter a number for more info, or another search term, or \"exit\": ")
            if word == "exit":
                break
            if isInt(word) and (int(word) >= 1 and int(word) < len(results)+1):
                # make sure this media has a url we can use
                if results[int(word)-1].url != None:
                    print("Launching: " + results[int(word)-1].url + "\nin web browser")
                    webbrowser.open(results[int(word)-1].url)
                else:
                    print("No URL")
            elif isInt(word) and (int(word) < 1 or int(word) >= len(results)+1):
                print("{} is an invalid selection.)".format(word))
            else:
                newsearch = True
