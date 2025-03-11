import filmdatabase as fd
from tkinter import *
from tkinter import messagebox, simpledialog
import requests
from PIL import Image, ImageTk
from io import BytesIO
import json, os

API_KEY = os.getenv("OMDb_API_KEY")

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
    root = Toplevel()
    root.title("Legg til film via OMDb")
    root.geometry("500x675")
    
    page = 1
    default_poster_url = "https://placehold.co/100x150?text=No+Poster+Available"
    
    def hent_filmer(page_num):
        nonlocal page
        page = page_num
        tittel = entry_tittel.get()
        if not tittel:
            messagebox.showerror("Feil", "Du må skrive inn en tittel!")
            return
        
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&s={tittel}&page={page}"
        print(f"Calling the URL: {url}")
        response = requests.get(url)
        film_data = json.loads(response.text)
        
        if film_data["Response"] == "False":
            messagebox.showerror("Feil", "Fant ingen filmer.")
            return
        
        vis_filmer(film_data["Search"])
        
        # Oppdater knappene for navigering
        forrige_side_btn["state"] = NORMAL if page > 1 else DISABLED
        neste_side_btn["state"] = NORMAL if len(film_data["Search"]) == 10 else DISABLED
    
    def vis_filmer(filmer):
        for widget in resultat_frame.winfo_children():
            widget.destroy()
        
        for film in filmer:
            frame = Frame(resultat_frame)
            frame.pack(pady=5)
            
            poster_url = film["Poster"] if film["Poster"] != "N/A" else default_poster_url
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)
            
            try:
                img = Image.open(img_data)
            except Exception:
                img = Image.new("RGB", (100, 150), color=(200, 200, 200))  # Grå bilde hvis feil
            
            img = img.resize((100, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            btn = Button(frame, image=photo, command=lambda f=film: velg_film(f))
            btn.image = photo
            btn.pack(side=LEFT, padx=5)
            
            Label(frame, text=f"{film['Title']} ({film['Year']})", font=("Arial", 12)).pack(side=LEFT)
    
    def velg_film(film):
        imdb_id = film["imdbID"]
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&i={imdbID}"
        response = requests.get(url)
        film_data = json.loads(response.text)
        
        fd.legg_til_film(
            tittel=film_data["Title"],
            regissør=film_data["Director"],
            produsent=film_data["Production"],
            år=film_data["Released"][-4:],
            sjanger=film_data["Genre"].split(", ")
        )
        messagebox.showinfo("Suksess", f"{film_data['Title']} ble lagt til i databasen!")
        root.destroy()
    
    Label(root, text="Skriv inn filmtittel:", font=("Arial", 12)).pack(pady=5)
    
    entry_tittel = Entry(root, font=("Arial", 12), width=40)
    entry_tittel.pack(pady=5)
    
    Button(root, text="Søk", font=("Arial", 12), command=lambda: hent_filmer(1)).pack(pady=5)
    
    resultat_frame = Frame(root)
    resultat_frame.pack(pady=10)
    
    navigasjon_frame = Frame(root)
    navigasjon_frame.pack(pady=5)
    
    forrige_side_btn = Button(navigasjon_frame, text="Forrige side", command=lambda: hent_filmer(page-1), state=DISABLED)
    forrige_side_btn.pack(side=LEFT, padx=10)
    
    neste_side_btn = Button(navigasjon_frame, text="Neste side", command=lambda: hent_filmer(page+1), state=DISABLED)
    neste_side_btn.pack(side=LEFT, padx=10)
    
    root.mainloop()


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
