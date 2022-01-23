Kansiossa eri osiot VR-data-analytiikka -kokonaisuudesta. Jokaisessa kansiossa on oma readme-tiedostonsa.


======================== Python-appi =============================

Python työpöytä-applikaatio ei toimi Pythonin 3.8.5:ttä uudemmilla versiolla. Kyseinen sovellus vaatii paljon eri kirjastoja, joista osa ei toimi uudemmilla versioilla. Voit kokeilla sitä muillakin Pythonin versiolla, kuin 3.8.5, tai asentaa version 3.8.5. Helpointa on käyttää kirjastojen asentamiseen virtuaaliympäristöä (virtual enviroment).

Uuden virtual enviromentin luonti (samaan sijaintiin, jossa  requirements.txt tiedosto) ja käyttö:

0) Käytä terminaalia, kuten PowerShell tai Windows Terminal, tms.
1) Navigoi tähän sijaintiin
2) virtualenv VENVIN_NIMI --python=python3.8.5
	- huom. vaatii 3.8.5 asennettuna tietokoneelle

Luodun venvin aktivointi:
3) .\VENVIN_NIMI\Scripts\activate

Dependencyjen asentaminen (samassa kansiossa edelleen):
4) pip install -r requirements.txt

Mikäli kirjastojen asennus heittää erroria, varmista, että Pythonin versio on oikea.

==================================================================