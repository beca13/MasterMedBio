from load_data_in_memory import Radovi

# Check if the script is being run as the main program
if __name__ == "__main__":
   
    """ Upotreba klasa i objekata """

    radovi = Radovi()
    radovi.UcitajScopus("d:\data\Beca\src\MasterMedBioLocal\data\Scopus\scopus_9.csv")
    radovi.UcitajPubMed("d:\data\Beca\src\MasterMedBioLocal\data\PubMed\\full.txt")
    print("Broj radova: ", len(radovi.kolekcija))
    # print(len(radovi.kolekcija))
    # print("Broj autora -1-tog rada: ")

    # Primer prolaska kroz sve autore
    # for rad in radovi.kolekcija:
    #     for autor in rad.autori:
    #         print("{}, {}, {}". format(autor.ime, autor.prezime, autor.institucija))

    print("Done")
