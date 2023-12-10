from load_data_in_memory import Radovi

# Check if the script is being run as the main program
if __name__ == "__main__":
   
    """ Upotreba klasa i objekata """

    radovi = Radovi()
    radovi.UcitajScopus("e:\git\ExternalData\MedBio\Scopus\scopus_9.csv")
    radovi.UcitajPubMed("e:\git\ExternalData\MedBio\PubMed\pubmed-serbiaANDu-set(1).txt")
    print("Broj radova: ", len(radovi.kolekcija))
    # print(len(radovi.kolekcija))
    # print("Broj autora -1-tog rada: ")

    # Primer prolaska kroz sve autore
    for rad in radovi.kolekcija:
        for autor in rad.autori:
            print("{}, {}, {}, |{}|". format(autor.ime, autor.prezime, autor.institucija, autor.zemlja))

    # ako je potrebno dodatne obrade, mozda je pametno napraviti dataframe (pandas) od ove strukture u memoriji

    print("Done")
