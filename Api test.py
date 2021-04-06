from imdb import IMDb
API = IMDb()

#deze functie vraagt aan de user welke titel de API moet opzoeken
#daarna checkt de functie of de titel legitiem is, zoniet dan wordt er weer aan de user gevraagt voor een titel
def get_first_movie():
    movie_name = input("Geef alstublieft de naam van een film op.\n")
    movies = API.search_movie(movie_name)

    if len(movies) > 0 and movies[0].movieID != '':
        return movies[0]
    else:
        print('De opgegeven film is niet gevonden')
        get_first_movie()

#deze fucnties zijn voor configurariteit zodat de user kan bepalen welke informatie er wordt getoond
def get_directors():
    try:
        print('Directors:')
        for director in movie_details['directors']:
            print(director['name'])
    except:
        print("Deze film heeft geen directors.")

def get_writers():
    try:
        print('writers:')
        for director in movie_details['writers']:
            print(writers)
    except:
        print("Deze film heeft geen writers.")

def get_genres():
    try:
        print('Genres:')
        for genre in movie_details['genres']:
            print(genre)
    except:
        print("Deze film heeft geen genres.")

def get_cast():
    try:
        print('cast:')
        for cast in movie_details['cast']:
            print(cast)
    except:
        print("Deze film heeft geen cast.")


def get_user_input():
    user_input = input("Wil je de directors zien? y/n")
    print('\n')
    if user_input == 'y':
        get_directors()
    elif user_input != 'n' and user_input != '':
        print('het opgegeven woord is niet herkend')
        get_user_input()


first_movie = get_first_movie()
movie_details = API.get_movie(first_movie.movieID)
get_user_input()

