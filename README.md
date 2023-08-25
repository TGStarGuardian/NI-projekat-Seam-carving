# Projekat za kurs: Naučno izračunavanje

# Tema: Seam carving algoritam

# Autor:
+ Uroš Ševkušić 1011/2022

# Problem:

+ U ovom projektu obrađeni su sledeći algoritmi:
  + seam carving algoritam za skraćivanje slike
  + seam carving algoritam za uvećavanje slike
  + ubrzani seam carving algoritam za skraćivanje slike

+ Skup podataka: slike nad kojima smo primenili algoritam nalaze se u folderu **assets**, a rezultujuće slike smo smestili u folder **rezultati**. U potfolderima foldera **rezultati** su rezultati primene svakog od gornjih algoritama, sa različitim ulaznim parametrima.

+ Literatura:
  + za prva dva algoritma korišćen je rad **Seam Carving for Content-Aware Image Resizing** od autora **Shai Avidan** i **Ariel Shamir**
  + za treći algoritam korišćen je rad **Accelerated seam carving for image retargeting** od autora **Diptiben Patel** i **Shanmuganathan Raman**, objavljen u **IET Image Processing**

+ Napomena vezano za literaturu: Smatram da se u radu **Accelerated seam carving for image retargeting** nalazi greška kod izračunavanja trake najmanje energije, pa sam njihove jednačine za taj korak zamenio svojima.

+ Sadržaj projekta:
  + jupyter sveske - prezentacija rada algoritma na određenoj slici
  + fajlovi 1.py, 2.py, 3.py, 4.py, 5.py kojima su generisane slike u folderu **rezultati**, u njima je samo sabran ceo algoritam iz sveske
  + fajl poredjenja.odp je prezentacija u kojoj su poređeni algoritmi

+ Pokretanje jupyter-notebook datoteka:
Datoteke se pokreću na standardan način run all cells komandom unutar Jupyter-Notebook okruženja

+ Potrebni alati:
  + jupyter notebook
  + Python biblioteke:
    + numpy
    + matplotlib
    + scipy
    + PIL
   
