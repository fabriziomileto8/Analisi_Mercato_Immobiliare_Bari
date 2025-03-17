import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from sklearn.linear_model import LinearRegression

#    Calcola statistiche descrittive sui prezzi al mq per zona.
def calcola_statistiche(df: DataFrame) -> DataFrame:
    statistiche: DataFrame = df.groupby("Zona")["Prezzo_mq_vendita"].agg(["mean", "median", "std"])
    statistiche.columns = ["Media Prezzo", "Mediana Prezzo", "Deviazione Standard"]
    return statistiche

#    Crea un grafico a barre con i prezzi medi di vendita per ogni zona.
def visualizza_prezzi_medi(df: DataFrame) -> None:
    media_prezzi: DataFrame = df.groupby("Zona")["Prezzo_mq_vendita"].mean()

    plt.figure(figsize=(12, 6))
    plt.bar(media_prezzi.index, media_prezzi.values)
    plt.xlabel("Zona")
    plt.ylabel("Prezzo medio al mq (€)")
    plt.title("Prezzo medio al mq per zona a Bari")
    plt.xticks(rotation=45)
    plt.show()

#    Crea un grafico della variazione dei prezzi nel tempo per una o tutte le zone.
def visualizza_trend_prezzi(df: DataFrame, zona: str | None = None) -> None:
    plt.figure(figsize=(10, 5))

    if zona:
        df_zona = df[df["Zona"] == zona]
        trend = df_zona.groupby("Data")["Prezzo_mq_vendita"].mean()
        plt.plot(trend.index, trend.values, marker="o", linestyle="-", label=f"{zona}")
    else:
        for quartiere in df["Zona"].unique():
            df_quartiere = df[df["Zona"] == quartiere]
            trend = df_quartiere.groupby("Data")["Prezzo_mq_vendita"].mean()
            plt.plot(trend.index, trend.values, marker="o", linestyle="-", label=quartiere)

    plt.xlabel("Anno")
    plt.ylabel("Prezzo medio al mq (€)")
    plt.title("Andamento dei prezzi al mq nel tempo")
    plt.legend()
    plt.grid()
    plt.show()

#    Stima la crescita futura dei prezzi per una o tutte le zone usando regressione lineare. Se `zona` è None, genera un grafico separato per ciascuna zona.
def predizione_prezzi(df: DataFrame, zona: str | None = None, anni: int = 3) -> None:
    if zona:
        quartieri: list[str] = [zona]
    else:
        quartieri: list[str] = df["Zona"].unique()

    for quartiere in quartieri:
        df_zona = df[df["Zona"] == quartiere]
        df_zona = df_zona.groupby("Data")["Prezzo_mq_vendita"].mean().reset_index()

        X = df_zona["Data"].dt.year.values.reshape(-1, 1)
        y = df_zona["Prezzo_mq_vendita"].values

        modello: LinearRegression = LinearRegression()
        modello.fit(X, y)

        anni_futuri = np.array(range(X[-1][0] + 1, X[-1][0] + anni + 1)).reshape(-1, 1)
        prezzi_previsti = modello.predict(anni_futuri)

        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, color="blue", label="Dati Storici")
        plt.plot(anni_futuri, prezzi_previsti, color="red", linestyle="--", label="Previsione")
        plt.xlabel("Anno")
        plt.ylabel("Prezzo medio al mq (€)")
        plt.title(f"Previsione Prezzi - {quartiere}")
        plt.legend()
        plt.grid()
        plt.show()