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
    filmer.append({"Tittel":tittel, "Regissør":regissør, "Produsent":produsent, "År":år, "Sjanger":sjanger})
    
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
