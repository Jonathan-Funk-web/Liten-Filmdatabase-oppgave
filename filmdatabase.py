import requests
import json
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path

filmer = []

load_dotenv(Path(".env"))
API_KEY = os.getenv("OMDb_API_KEY")


def legg_til_film(tittel: str = "Tittel Mangler", regissør: str ="Regissør Mangler", produsent: str ="Produsent Mangler", år: int = 0, sjanger: list[str] = ["Sjanger(e) Mangler"]) -> None:
    """Tar de forselige detaljene til filmen og lagrer de som en ordbok i `filmer` listen.
    Args:
        tittel (str, optional): Tittelen til filmen. Hvis ingen verdi er oppgit så er standardverdien `"Tittel Mangler"`.
        regissør (str, optional): Regissøren til filmen. Hvis ingen verdi er oppgit så er standardverdien `"Regissøren Mangler"`.
        produsent (str, optional): Produsenten til filmen. Hvis ingen verdi er oppgit så er standardverdien `"Produsent Mangler"`.
        år (str, optional): Året filmen ble utgitt. Hvis ingen verdi er oppgit så er standardverdien `0`.
        sjanger (list[str], optional): Sjangeren(e) til filmen. Hvis ingen verdi er oppgit så er standardverdien `["Sjanger(e) Mangler"]`.
    Returns:
        dict: Slår sammen all infoen in til en ordbok.
    """
    
    filmer.append({"tittel":tittel, "regissør":regissør, "produsent":produsent, "år":år, "sjanger":sjanger})
    
    print("Film lagt til i `filmer` listen.")
    
    return None

def vis_filmer() -> list[dict] | int:
    """Denne funksjonen skriver ut alle filmene i databasen, enn sålenge så er det bare `filmer` listen.

    Returns:
        list[dict]: Den lille film databasen vår.
        int: Verdien er `0` hvis databasen er tom, ellers så er verdien hvor mange filmer som er i databasen.
    """
    if len(filmer) == 0:
        print("Det er ingen filmer i databasen.")
        return 0
    
    for film in filmer:
        print(film)
    
    return len(filmer)

def søk_film(tittel: str) -> list[dict]:
    """Søker gjennom databasen (`filmer`) etter filmer som ineholder tittelen `tittel`. Den printer (og returner) så de filmene som en liste av ordbøker.
    Args:
        tittel (str): Tittelen til filmen.
    Returns:
        list[dict]: Filmene som har tittlen.
    """
    #TODO: Legg till et argument til, dette argumentet bestemmer hva man søker etter, sånn man kan søke etter regissører, produsenter etc.
    tittler = [film["tittel"] for film in filmer] #Tittlene til alle filmene i databasen.
    print([navn for navn in tittler if tittel.lower() in navn.lower()]) #`.lower()` er for å gjøre det case insensitive.
    return

def lagre_til_fil(filnavn: str = "Filmer" ) -> None:
    """Lagrer listen `filmer` til en JSON fil.

    Args:
        filnavn (str): Navnet til JSON filen.
    """    
    with open(filnavn +".json", "w", encoding="utf8") as json_file:
        json.dump(filmer,json_file,ensure_ascii=False)

def last_inn_fra_fil(filnavn: str = "Filmer") -> None:
    """Laster in filmer fra en JSON fil.

    Args:
        filnavn (str): Navnet til JSON filen.
    """    
    global filmer
    with open(filnavn + ".json", "r", encoding="utf8") as json_file:
        filmer = json.load(json_file)

def sorter_filmer(kirterium: str, økende: bool = True) -> list[dict]:
    """Viser og sorterer filmene i databasen etter en spesifik rekkefølge.

    Args:
        kirterium (str): Hvordan databasen skal sorteres, mulige verdier: `tittel` som sorterer etter film tittlene i alfabetisk rekkefølge (A → Å), `regissør` som sorterer etter filmenes regissører navn i alfabetisk rekkefølge (A → Å), `produsent` som sorterer etter filmenes produsentens navn i alfabetisk rekkefølge (A → Å), `år` som sorterer filmene etter år i økende rekkefølge (1→9).
        økende (bool): Hvis `True` sorterer ting i en økende rekkefølge, for alfaberisk sortering så går det fra A til Å, og for tall sortering så går det fra lavt tall til stort tall. Hvis `False` så gjør den det motsatte.
    Returns:
        list[dict]: filmene, sortert.
    """
    global filmer
    filmer = sorted(filmer, key = lambda k: k[kirterium.lower()], reverse=not økende)

def meny() -> None:
    """
    En konsollbasert meny, som virker via en while-løkke.
    """
    last_inn_fra_fil("Filmer")
    while True:
        print("\nMeny\n"
            " [1] Legg til ny film i databasen\n"
            " [2] Vis alle filmer i databasen\n"
            " [3] Søk etter filmer\n"
            " [4] Sortere databasen\n"
            " [5] Legg til film via OMDb\n"
            " [6] Lagre og avslutt programmet")
        
        try:
            meny_valg = int(input("Velg menyvalg (1-6): "))
            meny_valg in range(0,7)
        except ValueError:
            print("Ugyldig input! Vennligst skriv et tall mellom 1 og 6.")
            continue
        
        if meny_valg == 1:
            tittel = input("Film tittel: ")
            regissør = input("Film regissør: ")
            produsent = input("Film produsent: ")
            år = input("Året filmen kom ut: ")
            
            sjangere = []
            while True:
                sjanger = input("Film sjanger (trykk enter for å avslutte): ")
                if sjanger == "":
                    break
                sjangere.append(sjanger)

            legg_til_film(tittel, regissør, produsent, år, sjangere)
        elif meny_valg == 2:
            vis_filmer()
        elif meny_valg == 3:
            søk_film(input("Film navn: "))
        elif meny_valg == 4:
            sorter_filmer(input("Sorteringskriterie: "))
        elif meny_valg == 5:
            legg_til_film_via_OMDb(input("Film navn: "))
        elif meny_valg == 6:
            lagre_til_fil("Filmer")
            print("Programmet avsluttes...")
            break  # Avslutter løkken og dermed programmet
        else:
            print("\nUgyldig valg, prøv igjen!")

def legg_til_film_via_OMDb(tittel: str = None) -> json:
    response = requests.get("https://www.omdbapi.com/?apikey=" + API_KEY + "&t=" + tittel)
    response_text = json.loads(response.text)
    legg_til_film(tittel = response_text["Title"],regissør = response_text["Director"],produsent=response_text["Production"],år=response_text["Released"][-4:], sjanger=response_text["Genre"])
    return response_text["Poster"]


if not os.path.exists("Filmer.json"):
    with open("Filmer.json", "w", encoding="utf8") as file:
        json.dump([], file, ensure_ascii=False)

meny()