#deze library wordt gebruikt om de films op te halen via de IMDB API
import smtplib
#deze library wordt gebruikt om een veilige connectie op te zetten met de mailservers van google
import ssl
#deze library wordt gebruikt om het config.json bestand uit te lezen
import json
#deze library wordt gebruikt om het relatieve pad op te halen
import os
from imdb import IMDb
API = IMDb()
mailed_content = {}

#deze functie vraagt aan de user welke titel de API moet opzoeken
#daarna checkt de functie of de titel legitiem is, zo niet dan wordt er weer aan de user gevraagt voor een titel
def get_first_movie():
    movie_name = input("Geef alstublieft de naam van een film op.\n")
    movies = API.search_movie(movie_name)

    if len(movies) > 0 and movies[0].movieID != '':
        return movies[0]
    else:
        print('De opgegeven film is niet gevonden')
        get_first_movie()

#deze functie vraagt aan de user welke informatie moet worden getoond
def get_user_input():
    valid_input = False
    categories = ["cast", "directors", "producers", "writers"]
    user_input = input("Welke informatie over de film wil je zien?\nKies uit: Cast, Directors, Producers, Writers\n")
    for categorie in categories:
        if user_input.lower() == categorie:
            valid_input = True
            get_movie_information(categorie)
    if not valid_input:
        print("Dit is geen geldige optie, probeer het opnieuw.\n")
        get_user_input()
    confimation_loop("Wil je nog meer informatie ophalen? (ja/nee)\n", get_user_input)

#deze functie wordt gebruikt om de meegegeven funties uit te voeren.
#dit is nodig zodat dezelfde functie meerdere keren gebruikt kan worden en configureerbaar is.
def perform(fun, *args):
    fun(*args)

#deze configureerbare functie vraagt een ja/nee vraag aan de user en gebaseerd daarop gaat het programma verder of niet
def confimation_loop(input_text, function_yes):
    continue_to_loop = True
    while continue_to_loop:
        response = input(input_text)
        if response.lower() == "ja":
            continue_to_loop = False
            perform(function_yes)
        elif response.lower() == "nee":
            continue_to_loop = False
        else:
            print("Het opgegeven antwoord is niet geldig.\n")


#deze functie krijgt een categorie binnen die wordt opgezocht in de movie_details object
#daarna wordt de gevonden informatie in de dictionary mailed_content gezet onder dezelfde naam als de categorie
def get_movie_information(informatie_naam):
    try:
        print(informatie_naam + ':')
        mailed_content[informatie_naam] = ""
        for naam in movie_details[informatie_naam]:
            try:
                mailed_content[informatie_naam] += naam["name"] + "\n"
                print(naam)
            except:
                continue
        print("\n")
    except:
        print("Deze film heeft geen " + informatie_naam + ".")


#Deze functie legt eerst een connectie met de mailservers van google via het SMTP protocol
#Daarna stuurt het alle data die in de dictionary mailed_content staat naar het mailadres
#het mailadres wordt gelezen uit een json bestand in dezelfde map
#de functie checkt ook of de user input geldig is
def mail_information_to_user():
    port = 465
    password = input("Voer hier het wachtwoord in van het mailaccount die de mail verzend (Dit is te vinden in het bestand): Applicatie Documentatie Joep van der Sanden\n")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login("pythontestjvds@gmail.com", password)

            dirname = os.getcwd()
            f = open(dirname + '/config.json')
            data = json.load(f)
            email = data["mail"]
            f.close()

            #hier wordt de data in de dictionary omgezet naar een fstring
            data_to_send = "Subject: IMDB API zoekmachine resultaten: "
            for key in mailed_content:
                data_to_send += f"\n\n{key} : \n{mailed_content[key]}"
            server.sendmail("pythontestjvds@gmail.com", email, data_to_send.encode('utf-8').strip())
        except:
            print("De email kon niet worden verzonden")

first_movie = get_first_movie()
movie_details = API.get_movie(first_movie.movieID)
get_user_input()
confimation_loop("Wil je de opgehaalde informatie naar een mailadres sturen? (ja/nee)\n", mail_information_to_user)
