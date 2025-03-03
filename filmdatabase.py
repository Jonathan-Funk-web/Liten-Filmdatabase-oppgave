filmer = []

def legg_til_film(tittel: str = "Tittel Mangler", regissør: str ="Regissør Mangler", produsent: str ="Produsent Mangler", år: int = 0, sjanger: list[str] = ["Sjanger(e) Mangler"]) -> dict:
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
    filmer.append({"Tittel":tittel, "Regissør":regissør, "Produsent":produsent, "År":år, "Sjanger":sjanger})
    return 

print(filmer)
legg_til_film("Titeline","Regisman","Produsentus",2001,["Action","Drama"])
legg_til_film()
print(filmer[1])