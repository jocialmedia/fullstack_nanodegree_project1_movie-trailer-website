import webbrowser

class Movie():
    """ This class provides a way to store movie related information"""
    
    def __init__(self, name, year, runtime, myrating, id_imdb, id_trailer, url_wikipedia):
        	self.title = name
		self.year = year
		self.runtime = runtime
		self.myrating = myrating
		self.id_imdb = id_imdb
		self.id_trailer = id_trailer
		self.url_wikipedia = url_wikipedia
