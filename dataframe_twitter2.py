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
tweets = extractor.user_timeline(screen_name="realDonaldTrump ", count=200)
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

# Sacamos la media de las longitudes:
mean = np.mean(data['longitud'])

print("La longitud media de los tweets: {}".format(mean))

# Sacamos el tweet con más "Me gusta" y el más retuiteado:
fav_max = np.max(data['Likes'])
rt_max  = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt  = data[data.RTs == rt_max].index[0]

# Tweet que más ha gustado:
print("El tweet con más <Me gusta> es: \n{}".format(data['Tweets'][fav]))
print("Número de <Me gusta>: {}".format(fav_max))
print("{} caracteres.\n".format(data['longitud'][fav]))

# Tweet más retuiteado:
print("El tweet más retuiteado es: \n{}".format(data['Tweets'][rt]))
print("Número de retweets: {}".format(rt_max))
print("{} caracteres.\n".format(data['longitud'][rt]))

# Creamos las series temporales de datos de los tweets:

tlen = pd.Series(data=data['longitud'].values, index=data['Fecha'])
tfav = pd.Series(data=data['Likes'].values, index=data['Fecha'])
tret = pd.Series(data=data['RTs'].values, index=data['Fecha'])

# Variación de las longitudes de tweets con el tiempo:
tlen.plot(figsize=(16,4), color='r');

# Visualización de Me gusta vs Retuits:
tfav.plot(figsize=(16,4), label="Me gusta", legend=True)
tret.plot(figsize=(16,4), label="Retuits", legend=True);

# Obtener todas las fuentes posibles:
fuentes = []
for fuente in data['Fuente']:
    if fuente not in fuentes:
        fuentes.append(fuente)

# Imprimir la lista de fuentes:
print("Creación de fuentes de contenido:")
for fuente in fuentes:
    print("* {}".format(fuente))
	
# Creamos un vector numpy mapeado a las etiquetas:
percent = np.zeros(len(fuentes))

for fuente in data['Fuente']:
    for indice in range(len(fuentes)):
        if fuente == fuentes[indice]:
            percent[indice] += 1
            pass

percent /= 100

# Gráfico de tarta:
tarta = pd.Series(percent, index=fuentes, name='Fuentes')
tarta.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));