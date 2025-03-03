import json
filmer = []

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
    
    #TODO: Jeg kan legge til noe kode som gjør at denne funksjonen sier ifra hvis det er noen av argumentene som mangler.
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

def lagre_til_fil(filnavn: str) -> None:
    """Lagrer listen `filmer` til en JSON fil.

    Args:
        filnavn (str): Navnet til JSON filen.
    """
    #TODO: Legg til en check for at filen faktisk ble lagret.
    #TODO: Skjekk hvis `filnavn` ender med `.json`, hvis den gjør det, ikke legg till `.json`.
    
    with open(filnavn +".json", "w", encoding="utf8") as json_file:
        json.dump(filmer,json_file,ensure_ascii=False)

def last_inn_fra_fil(filnavn: str) -> None:
    """Laster in filmer fra en JSON fil.

    Args:
        filnavn (str): Navnet til JSON filen.
    """
    #TODO: Skjekk hvis `filnavn` ender med `.json`, hvis den gjør det, ikke legg till `.json`.
    
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

last_inn_fra_fil("Filmer")
vis_filmer()