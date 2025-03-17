from pandas import read_csv, DataFrame, to_datetime

#    Carica il dataset e converte la colonna Data in formato datetime.
def carica_dati(file_path: str) -> DataFrame:
    df: DataFrame = read_csv(file_path)
    df["Data"] = to_datetime(df["Data"])
    return df