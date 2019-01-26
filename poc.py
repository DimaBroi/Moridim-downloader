from imdb import IMDb
from pprint import pprint
# create an instance of the IMDb class
ia = IMDb()
# get a movie
#print((ia.get_movie('0133093')['directors']))
#pprint(vars((ia.search_movie('the blacklist')[0])))
movie = ia.get_movie('2741602')
print(movie['kind'])
ia.update(movie, 'main')
pprint(vars(movie))
