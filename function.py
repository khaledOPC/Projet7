import nltk
import string
import os
import requests
from constant import GOOGLE_PLACES_URL
from constant import stop_words
from nltk.tokenize import word_tokenize


nltk.download("stopwords")
nltk.download("punkt")


def clean_search(search):
    
    # Créer une variable avec l'esemble de la ponctuation
    punctuation = set(string.punctuation)
    # Concatenner les elements de search et return les elements sans ponctuation
    search = "".join(letter for letter in search if letter not in punctuation)
    # Utiliser la fonction word_tokenize sur search
    tokenize_words = word_tokenize(search)
    # Ajouter chaque mot qui sont pas dans la stop_words liste et qui sont tokenize
    tokenize_words_without_stop_words = [
        word for word in tokenize_words if word not in stop_words
    ]
    search = " ".join(tokenize_words_without_stop_words)
    return search


class GoogleSearch:

    def search_google(self, place):
        url = GOOGLE_PLACES_URL.format(place=place, api_key=os.environ['API_KEY'])
        response = requests.request("GET", url)
        try:
            response = requests.request("GET", url)
            if response.ok:
                response_json = response.json()
                first_result = response_json["candidates"][0]
                adresse = first_result["formatted_address"]
                lat = first_result["geometry"]["location"]["lat"]
                lng = first_result["geometry"]["location"]["lng"]
                return (lat, lng, adresse)
            else:
                return None
        except Exception as e:
            print(e)
            return None


class WikiSearch:

    def search_wikipedia(self, lat, lng):
        wiki_url = "https://fr.wikipedia.org/w/api.php"
        payload = {
            "format": "json",
            "action": "query",
            "prop": "extracts",
            "exsentences": "2",
            "explaintext": "True",
            "generator": "geosearch",
            "ggsradius": "100",
            "ggscoord": f"{lat}|{lng}",
            "ggslimit": "2",
        }
        try:
            wiki_response = requests.get(wiki_url, params=payload).json()
            wiki_pages = wiki_response["query"]["pages"]
            wiki_page = None
            for key, value in wiki_pages.items():
                wiki_page = value
                break
            wiki_message = wiki_page["extract"]
            return wiki_message
        except:
            return "Oups !.. Je n'ai aucune information à ce sujet essayez autres choses !"
