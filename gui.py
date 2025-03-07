import filmdatabase as fd
from tkinter import *
from tkinter import messagebox, simpledialog
import requests
from PIL import Image, ImageTk
from io import BytesIO
import json

# Oppretter hovedvinduet
root = Tk()
root.title("Filmdatabase")
root.geometry("275x300")

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
    def legg_til():
        tittel = entry_tittel.get()
        regissor = entry_regissor.get()
        produsent = entry_produsent.get()
        try:
            ar = int(entry_ar.get())
        except ValueError:
            messagebox.showerror("Feil", "År må være et tall!")
            return
        sjanger = entry_sjanger.get()
        
        if tittel and regissor and produsent and sjanger:
            fd.legg_til_film(tittel, regissor, produsent, ar, sjanger.split(","))
            messagebox.showinfo("Suksess", "Filmen ble lagt til!")
            popup.destroy()
        else:
            messagebox.showerror("Feil", "Alle felt må fylles ut!")

    popup = Toplevel()
    popup.title("Legg til film")
    
    Label(popup, text="Film tittel:").grid(row=0, column=0)
    entry_tittel = Entry(popup)
    entry_tittel.grid(row=0, column=1)
    
    Label(popup, text="Regissør:").grid(row=1, column=0)
    entry_regissor = Entry(popup)
    entry_regissor.grid(row=1, column=1)
    
    Label(popup, text="Produsent:").grid(row=2, column=0)
    entry_produsent = Entry(popup)
    entry_produsent.grid(row=2, column=1)
    
    Label(popup, text="År:").grid(row=3, column=0)
    entry_ar = Entry(popup)
    entry_ar.grid(row=3, column=1)
    
    Label(popup, text="Sjangere (kommaseparert):").grid(row=4, column=0)
    entry_sjanger = Entry(popup)
    entry_sjanger.grid(row=4, column=1)
    
    Button(popup, text="Legg til", command=legg_til).grid(row=5, column=0, columnspan=2)
    
    popup.mainloop()

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

def legg_til_film_via_OMDb_gui():
    def hent_film():
        tittel = entry_tittel.get()
        if not tittel:
            messagebox.showerror("Feil", "Du må skrive inn en tittel!")
            return
        
        try:
            # Hent data fra OMDb API
            response = requests.get(f"https://www.omdbapi.com/?apikey={fd.API_KEY}&t={tittel}")
            film_data = json.loads(response.text)
            
            if film_data["Response"] == "False":
                messagebox.showerror("Feil", "Fant ikke filmen.")
                return
            
            poster_url = film_data["Poster"]
            vis_filmvalg(film_data, poster_url)

        except Exception as e:
            messagebox.showerror("Feil", f"En feil oppstod: {e}")

    def vis_filmvalg(film_data, poster_url):
        # Lukk input-vinduet
        popup.destroy()

        # Opprett nytt vindu for bekreftelse
        bekreft_vindu = Toplevel()
        bekreft_vindu.title("Bekreft film")

        Label(bekreft_vindu, text="Er dette filmen du vil legge til?", font=("Arial", 14)).pack(pady=10)

        # Hent og vis filmplakat
        response = requests.get(poster_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((200, 300), Image.Resampling.LANCZOS)  # Skaler bildet
        photo = ImageTk.PhotoImage(img)

        label_img = Label(bekreft_vindu, image=photo)
        label_img.image = photo  # Behold referanse til bildet
        label_img.pack(pady=10)

        # Funksjon for å legge til filmen i databasen
        def bekreft():
            fd.legg_til_film(
                tittel=film_data["Title"],
                regissør=film_data["Director"],
                produsent=film_data["Production"],
                år=film_data["Released"][-4:],
                sjanger=film_data["Genre"].split(", ")
            )
            messagebox.showinfo("Suksess", "Filmen ble lagt til i databasen!")
            bekreft_vindu.destroy()

        # Knappene for bekreftelse
        Button(bekreft_vindu, text="Ja", command=bekreft).pack(side=LEFT, padx=20, pady=10)
        Button(bekreft_vindu, text="Nei", command=bekreft_vindu.destroy).pack(side=RIGHT, padx=20, pady=10)

        bekreft_vindu.mainloop()

    # Opprett popup for filminput
    popup = Toplevel()
    popup.title("Legg til film via OMDb")

    Label(popup, text="Skriv inn filmtittel:").pack(pady=5)
    entry_tittel = Entry(popup)
    entry_tittel.pack(pady=5)

    Button(popup, text="Søk", command=hent_film).pack(pady=5)
    popup.mainloop()

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
Button(root, text="Legg til film via OMDb", command=legg_til_film_via_OMDb_gui).pack(pady=5)
Button(root, text="Sorter filmer", command=sorter_filmer_gui).pack(pady=5)
Button(root, text="Lagre og avslutt", command=lagre_og_avslutt).pack(pady=5)

# Kjører Tkinter-hovedløkken
root.mainloop()
