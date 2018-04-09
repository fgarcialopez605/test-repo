import tweepy

# General:
import tweepy           # Para consumir la API de Tweeter
import pandas as pd     # Para análisis de datos
import numpy as np      # Para cálculo numérico

# Para visualización con gráficos:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# Importamos nuestras claves de acceso:
from credentials import *    # Esto nos permite usar las claves como variables

# Configuración de la API:
def twitter_setup():
    """
    Función de utilidad para configurar la API de Twitter
    con nuestras claves de acceso.
    """
    # Autenticación y acceso usando claves:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Retornar API con autenticación:
    api = tweepy.API(auth)
    return api
	
# Creamos un objeto extractor:
extractor = twitter_setup()

# Creamos una lista de tweets:
tweets = extractor.user_timeline(screen_name="machinelearnbot", count=200)
print("Número de tweets extraidos: {}.\n".format(len(tweets)))

# Imprimimos los 5 tweets más recientes:
print("5 tweets más recientes:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print()
	
# Creamos una dataframe de pandas:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# Dibujamos los 10 primeros elementos del dataframe:
display(data.head(10))

# Métodos internos de un objeto tweet:
print(dir(tweets[0]))

# Imprimimos la información del primer tweet:
print(tweets[0].id)
print(tweets[0].created_at)
print(tweets[0].source)
print(tweets[0].favorite_count)
print(tweets[0].retweet_count)
print(tweets[0].geo)
print(tweets[0].coordinates)
print(tweets[0].entities)

# Añadimos los datos relevantes:
data['longitud']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Fecha'] = np.array([tweet.created_at for tweet in tweets])
data['Fuente'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])

# Mostramos los 10 primeros elementos del dataframe:
display(data.head(10))