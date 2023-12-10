import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List
import re


""" Definicija klasa i objekata """
@dataclass
class Autor:
    """ Autor """
    ime: str
    prezime: str
    institucija: str

@dataclass
class Rad:
    """ Rad """
    id: str
    naziv: str
    autori: List[Autor] = field(default_factory=list)

    def dodaj_autora(self, autor: Autor):
        self.autori.append(autor)

def parse_prezime_zarez_ime(tekst: str):
    pattern = r"(.+?),(.+)"

    # Use re.match to find matches in the input string
    match = re.match(pattern, tekst)

    ime = ""
    prezime = ""

    # Check if there is a match
    if match:
        # Extract values from the matched groups
        ime = match.group(2).strip()
        prezime = match.group(1).strip()
    else:
        prezime = tekst

    return ime, prezime

def parse_pubmed_liniju(pub_med_red:str):
    key = ""
    value = ""
    key = pub_med_red[:6]
    value = pub_med_red[6:]
    return key, value

def ucitaj_rad_iz_pubmed_sekcije(pub_med_linije: list):
    recnik = {}
    last_key = ""
    last_value = ""

    rad = Rad("", "")

    autor_ime = ""
    autor_prezime = ""
    institucija = ""
    for linija in pub_med_linije:
        key, value = parse_pubmed_liniju(linija)

        if (key.strip() != ""):
            # dosli smo do nekog kljuca
            # sad mozemo da |prethodni| kljuc proverimo i vidimo da li predstavlja autora ili naslov
            # provera autor

            # Odredjujemo naslov
            if (last_key == "TI  - "):
                rad.naziv = last_value.replace("\n", "")

            # Odredjujemo autora
            if (last_key == "FAU - "):
                # resetuj vrednosti jer naziv autora ide uvek prvi
                institucija = ""
                autor_ime = ""
                autor_prezime = ""
                autor_ime, autor_prezime = parse_prezime_zarez_ime(last_value)

            # dva faksa
            #if (last_key == "AD  - ") and (key == "AD  - "):
                # situacija kad jedan autor ima dva fakuleta
                # desava se da se AD - i AD - dese red za redom. Jedan autor dva fakulteta
                # "Azouaghe, Soufian" i to u situaciji kad bi drugi trebalo da bude prazan
                # ne radi nista za sad ali ovde mozes da detektujes ovu situaciju

            # Ako smo dosli do polja AD (institucija) 
            if (last_key == "AD  - "):
                # kad god je prethodni kljuc institucija, dodaj na institucija vrednost.
                institucija = institucija + last_value
                if (autor_prezime != ""):
                    # Ovime se proverava da li je autor iskoriscen do sada.
                    # Prakticno se ovime za jednog autora uzima samo prva institucija
                    
                    autor = Autor(autor_ime, autor_prezime, institucija.replace("\n", ""))
                    rad.dodaj_autora(autor)

                # Resetuj vrednosti
                institucija = ""
                autor_ime = ""
                autor_prezime = ""

            #
            last_value = value
            last_key = key
        else:
            # dodaj na last_value vrednost 
            # ako je sada prazan kljuc (odgovara starom), last_value ce dobiti dodatnu vrednost
            last_value = last_value + value

    return rad

@dataclass
class Radovi:
    """ Radovi """
    kolekcija: List[Rad] = field(default_factory=list)

    def obrisiSve(self):
        self.kolekcija.clear()
        return

    """ Ucitaj PubMed podatke """
    def UcitajPubMed(self, pubmedPath: str):
        # Read lines from the file into an array
        rad_linije = []
        with open(pubmedPath, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line  # Remove leading and trailing whitespaces
                if not line.strip():  # Break if an empty line is encountered
                    self.kolekcija.append(ucitaj_rad_iz_pubmed_sekcije(rad_linije))
                    rad_linije = []

                rad_linije.append(line)

        # Poslednja sekcija rada (proveri da li smo stigli do kraja kada je ostala poslednja sekcija da se obradi)
        if (rad_linije != []):
            self.kolekcija.append(ucitaj_rad_iz_pubmed_sekcije(rad_linije))
            rad_linije = []

    """ Ucitaj i dodaj scopus fajl na trenutnu kolekciju radova"""
    def UcitajScopus(self, scopusPath: str):

        # Read the CSV file into a DataFrame
        df = pd.read_csv(scopusPath)
        greske_broj = 0

        # za svaki red napravi novi rad u memoriji
        for index, row in df.iterrows():
            rad = Rad(row['EID'], row['Source title'])

            # delimiter ili razdvajac je ;
            if (pd.isnull(row["Author full names"])):
                continue

            # razdvoji autore
            autori = row["Author full names"].split(";")

            # odvojeni ;
            # todo: rename institucije -> institucije_sa_autorom
            if (pd.isnull(row["Authors with affiliations"])):
                continue
            
            institucije_sa_autorom = row["Authors with affiliations"].split(";")

            # proveri da li je broj autora jednak broju institucija
            if (len(autori) != len(institucije_sa_autorom)):
                #print(autori)
                print(index)
                print(len(autori))
                #print(institucije_sa_autorom)
                print(len(institucije_sa_autorom))
                print("Broj autora nije jednak broju institucija")
                greske_broj = greske_broj + 1
                print(str(greske_broj) + " ------------------------------------------------------------------------------------")
                continue

            for idxAutor in range(len(autori)):
                krataknaziv_autor_institucija = institucije_sa_autorom[idxAutor]
                naziv_institucije = ""
                # parsiraj instituciju 
                # Autor P., <sve ostalo institucija sa sve zarezima i razmacima"
                # Define a regular expression pattern for the specified format
                pattern = r"(.+?),(.+)"

                # Use re.match to find matches in the input string
                match = re.match(pattern, krataknaziv_autor_institucija)

                # Check if there is a match
                if match:
                    # Extract values from the matched groups
                    naziv_institucije = match.group(2).strip()
                else:
                    #TODO ovo znaci da je institucija prazna
                    continue
                    # raise Exception("Autor Institucija polje nije dobro: |" + krataknaziv_autor_institucija)


                # parsiraj autora 
                # Karthigesu, Kandeepan (57224781451)
                # ime,  prezime (ID)
                # Define a regular expression pattern for the specified format
                pattern = r"(.+?), (.+?) \((\w+)\)"
                # pattern = r"^(.*?),?\s*([\w\s\.]+) \((\w+)\)$"

                # Use re.match to find matches in the input string
                match = re.match(pattern, autori[idxAutor])

                # Check if there is a match
                if match:
                    # Extract values from the matched groups
                    name = match.group(1).strip()
                    surname = match.group(2).strip()
                    ID = match.group(3).strip()

                    rad.dodaj_autora(Autor(name, surname, naziv_institucije))
                else:
                    match = re.match("(.+?) \((\w+)\)", autori[idxAutor])
                    if match:
                        # Extract values from the matched groups
                        name = ""
                        surname = match.group(1).strip()
                        ID = match.group(2).strip()
                        rad.dodaj_autora(Autor(name, surname, naziv_institucije))
                    else:
                        raise Exception("Format autora nije dobar: |" + autori[idxAutor])
                
            self.kolekcija.append(rad)

        return
        

