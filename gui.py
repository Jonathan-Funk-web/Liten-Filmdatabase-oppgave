import filmdatabase as fd
from tkinter import *
from tkinter import messagebox, simpledialog

# Oppretter hovedvinduet
root = Tk()
root.title("Filmdatabase")
root.geometry("400x400")

# Funksjon for å vise filmer i et popup-vindu
def vis_filmer_gui():
    filmer = fd.vis_filmer()
    if filmer == 0:
        messagebox.showinfo("Filmer", "Det er ingen filmer i databasen.")
    else:
        film_tekst = "\n".join([f"{film['tittel']} ({film['år']}) - {', '.join(film['sjanger'])}" for film in fd.filmer])
        messagebox.showinfo("Filmer i databasen", film_tekst)

# Funksjon for å legge til en film
def legg_til_film_gui():
    tittel = simpledialog.askstring("Legg til film", "Film tittel:")
    regissør = simpledialog.askstring("Legg til film", "Regissør:")
    produsent = simpledialog.askstring("Legg til film", "Produsent:")
    år = simpledialog.askinteger("Legg til film", "År:")
    sjanger = simpledialog.askstring("Legg til film", "Sjangere (kommaseparert):")
    
    if tittel and regissør and produsent and år and sjanger:
        fd.legg_til_film(tittel, regissør, produsent, år, sjanger.split(","))
        messagebox.showinfo("Suksess", "Filmen ble lagt til!")
    else:
        messagebox.showerror("Feil", "Alle felt må fylles ut!")

# Funksjon for å søke etter en film
def søk_film_gui():
    tittel = simpledialog.askstring("Søk etter film", "Tittel på filmen:")
    if tittel:
        resultater = [film for film in fd.filmer if tittel.lower() in film['tittel'].lower()]
        if resultater:
            film_tekst = "\n".join([f"{film['tittel']} ({film['år']})" for film in resultater])
            messagebox.showinfo("Søkeresultat", film_tekst)
        else:
            messagebox.showinfo("Ingen treff", "Fant ingen filmer med den tittelen.")
    else:
        messagebox.showerror("Feil", "Du må skrive inn en tittel!")

# Funksjon for å sortere filmer
def sorter_filmer_gui():
    kriterium = simpledialog.askstring("Sorter filmer", "Sorteringskriterie (tittel, regissør, produsent, år):")
    if kriterium in ["tittel", "regissør", "produsent", "år"]:
        fd.sorter_filmer(kriterium)
        messagebox.showinfo("Suksess", f"Filmer sortert etter {kriterium}.")
    else:
        messagebox.showerror("Feil", "Ugyldig sorteringskriterie!")

# Funksjon for å lagre filmene til fil og avslutte programmet
def lagre_og_avslutt():
    fd.lagre_til_fil("Filmer")
    messagebox.showinfo("Lagring", "Filmer lagret. Programmet avsluttes.")
    root.quit()

# GUI-komponenter
Label(root, text="Filmdatabase", font=("Arial", 16)).pack(pady=10)
Button(root, text="Vis alle filmer", command=vis_filmer_gui).pack(pady=5)
Button(root, text="Legg til ny film", command=legg_til_film_gui).pack(pady=5)
Button(root, text="Søk etter film", command=søk_film_gui).pack(pady=5)
Button(root, text="Sorter filmer", command=sorter_filmer_gui).pack(pady=5)
Button(root, text="Lagre og avslutt", command=lagre_og_avslutt).pack(pady=5)

# Kjører Tkinter-hovedløkken
root.mainloop()
