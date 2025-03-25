import filmdatabase as fd
from tkinter import *
from tkinter import messagebox, simpledialog
import requests
from PIL import Image, ImageTk
from io import BytesIO
import json, os


def submit():
    user_input = entry.get()
    if fd.setup_API_key(user_input):
        messagebox.showinfo("Key setup", "Success! Key set up correctly.")
    else:
        messagebox.showinfo("Key setup", "Failure! Key was not set up.")
    popup.destroy()
    
if not os.path.exists(".env"):
    popup = Tk()
    popup.title("Input Required")
    popup.geometry("300x150")
    
    label = Label(popup, text="OMDb API key:")
    label.pack(pady=5)
    
    entry = Entry(popup)
    entry.pack(pady=5)
    
    submit_button = Button(popup, text="Submit", command=submit)
    submit_button.pack(pady=5)

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

page = 1
def legg_til_film_via_OMDb_gui():
    root = Toplevel()
    root.title("Legg til film via OMDb")
    root.geometry("500x675")
    
    default_poster_url = "https://placehold.co/100x150?text=No+Poster+Available"
    
    def hent_filmer(page_num=None):
        global page
        if page_num is None:
            page_num = page  # Bruker eksisterende side hvis ingen er angitt

        if page_num < 1:
            return  # Hindrer negative sidetall

        page = page_num
        tittel = entry_tittel.get()
        if not tittel:
            messagebox.showerror("Feil", "Du må skrive inn en tittel!")
            return
        
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&s={tittel}&page={page}"
        response = requests.get(url)
        film_data = json.loads(response.text)
        
        if film_data["Response"] == "False":
            messagebox.showerror("Feil", "Fant ingen filmer.")
            return
        
        vis_filmer(film_data["Search"])
        
        # Oppdater knappene for navigering
        forrige_side_btn["state"] = NORMAL if page > 1 else DISABLED
        neste_side_btn["state"] = NORMAL if len(film_data["Search"]) == 10 else DISABLED
    
    def vis_filmer(filmer=None):
        for widget in resultat_frame.winfo_children():
            widget.destroy()  # Fjerner gamle widgets

        row = 0  # Radindeks for grid

        for film in filmer:
            frame = Frame(resultat_frame)
            frame.grid(row=row, column=0, pady=5, sticky="w")  # Venstrejustering

            # Hent bilde-URL, bruk placeholder hvis ikke tilgjengelig
            poster_url = film["Poster"] if film["Poster"] != "N/A" else default_poster_url
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)

            try:
                img = Image.open(img_data)
            except Exception:
                img = Image.new("RGB", (100, 150), color=(200, 200, 200))  # Grå bilde ved feil
            
            img = img.resize((100, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            # **Bildeknapp**
            btn = Button(frame, image=photo, command=lambda f=film: velg_film(f))
            btn.image = photo
            btn.grid(row=0, column=0, padx=10)  # Legger bildet til venstre

            # **Filmtittel**
            label = Label(frame, text=f"{film['Title']} ({film['Year']})", font=("Arial", 12), anchor="w", justify=LEFT)
            label.grid(row=0, column=1, padx=10, sticky="w")  # Plasserer tittelen til høyre for bildet

            row += 1  # Flytt til neste rad
        # Oppdater canvas scroll-region
        resultat_canvas.update_idletasks()
        resultat_canvas.config(scrollregion=resultat_canvas.bbox("all"))

    def velg_film(film):
        imdb_id = film["imdbID"]
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}&plot=full"
        response = requests.get(url)
        film_data = json.loads(response.text)
        
        fd.legg_til_film(
            tittel=film_data["Title"],
            regissør=film_data["Director"],
            produsent=film_data["Production"],
            år=film_data["Released"][-4:],
            sjanger=film_data["Genre"].split(", "),
            plot=film_data["Plot"]
        )
        messagebox.showinfo("Suksess", f"{film_data['Title']} ble lagt til i databasen!")
        root.destroy()
    
    Label(root, text="Skriv inn filmtittel:", font=("Arial", 12)).pack(pady=5)

    entry_tittel = Entry(root, font=("Arial", 12), width=40)
    entry_tittel.pack(pady=5)

    Button(root, text="Søk", font=("Arial", 12), command=hent_filmer).pack(pady=5)

    # Opprett en canvas med scrollbar
    frame_container = Frame(root)
    frame_container.pack(pady=10, fill=BOTH, expand=True)

    resultat_canvas = Canvas(frame_container)
    scrollbar = Scrollbar(frame_container, orient=VERTICAL, command=resultat_canvas.yview)
    resultat_frame = Frame(resultat_canvas)

    resultat_frame.bind("<Configure>", lambda e: resultat_canvas.configure(scrollregion=resultat_canvas.bbox("all")))

    resultat_canvas.create_window((0, 0), window=resultat_frame, anchor="nw")
    resultat_canvas.configure(yscrollcommand=scrollbar.set)

    resultat_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Knappene for sidebytte
    knapp_frame = Frame(root)
    knapp_frame.pack(pady=5)

    forrige_side_btn = Button(knapp_frame, text="Forrige side", command=lambda: hent_filmer(page-1))
    forrige_side_btn.grid(row=0, column=0, padx=5)

    neste_side_btn = Button(knapp_frame, text="Neste side", command=lambda: hent_filmer(page+1))
    neste_side_btn.grid(row=0, column=1, padx=5)

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
