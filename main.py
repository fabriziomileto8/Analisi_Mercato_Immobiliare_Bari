from pandas import DataFrame
from utils.data_loader import carica_dati
from utils.analysis import calcola_statistiche, visualizza_prezzi_medi, visualizza_trend_prezzi, predizione_prezzi

# Caricamento dei dati
df: DataFrame = carica_dati("prezzi_immobiliari_bari_storico.csv")

# Esecuzione delle analisi
dati_statistici: DataFrame = calcola_statistiche(df)
visualizza_prezzi_medi(df)
visualizza_trend_prezzi(df)
predizione_prezzi(df)