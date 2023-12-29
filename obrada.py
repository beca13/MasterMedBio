import pandas as pd
from load_data_in_memory import Radovi

# Check if the script is being run as the main program
if __name__ == "__main__":
   
    """ Upotreba klasa i objekata """

    radovi = Radovi()
    radovi.UcitajScopus("e:\git\ExternalData\MedBio\Scopus\scopus_6.csv")
    radovi.UcitajPubMed("e:\git\ExternalData\MedBio\PubMed\pubmed-serbiaANDu-set(1).txt")
    print("Broj radova: ", len(radovi.kolekcija))
    # print(len(radovi.kolekcija))
    # print("Broj autora -1-tog rada: ")


    # Primer prolaska kroz sve autore
    rad_br = 0
    redovi_niz = []
    for rad in radovi.kolekcija:
        rad_br = rad_br + 1
        for autor in rad.autori:
            print("{}. {}, {}, {}, {}, {}, {},|{}|". format(rad_br, autor.ime, autor.prezime, autor.institucija, autor.zemlja, autor.grad, autor.uni, autor.medbio))
            
            # ako je potrebno dodatne obrade, mozda je pametno napraviti dataframe (pandas) od ove strukture u memoriji
            new_row = {'Ime': autor.ime,
                        'Prezime': autor.prezime,
                        'Institucija': autor.institucija,
                        'Zemlja': autor.zemlja,
                        'Grad': autor.grad,
                        'Univerzitet': autor.uni,
                        'Medbio': autor.medbio,
                        'Rad': rad.naziv,
                        'RadId': rad.id}

            # Append the new row to the list (this is faster than directly changing dataframe)
            redovi_niz.append(new_row)


# Napravi dataframe od niza recnika (najbrze resenje)            
df = pd.DataFrame(redovi_niz)
df.to_csv("e:\git\ExternalData\MedBio\sviradovi002.csv", encoding='utf-8', index=False)
#df = pd.read_csv('e:\git\ExternalData\MedBio\sviradovi001.csv', encoding='utf-8')
print("Done")

print(df)