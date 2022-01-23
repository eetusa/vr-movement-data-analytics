Readme

Kokonaisuus toimii lokaalilla palvelimella ja tietokannalla. Nettiin elämään saaminen saattaa vaatia muutoksia.

=================
0. 	a) Vaatimukset: asennettu npm, Node, MongoDB database
	b) Käynnissä oleva MongoDB-tietokanta
	c) Käytetyn Questin unique device ID vaihdettu server2-koodiin
	   (muuttuja devideID rivi 4)
	d) Käytetyn mongodb-tietokannan url vaihdettu rivillä 10

1. Asenna dependencyt > "npm install"

2. Aja palvelin ylös > "node server2"


server2.js
=================
Palvelin vastaanottaa dataa Questiltä, ja tallentaa sen MongoDB-tietokantaan. Palvelin vastaanottaa pyyntöjä Python-clientiltä ja lähettää dataa takaisin.


DataStatistics.js
=================
Apuluokka tiettyjen keskilukujen laskemiseen datasta, kuten keskihajonta, kvantiileja, min, max, keskiarvo


MongoDB
=================
0. Asenna mongoDB tietokoneelle lokaalisti
1. Käynnistä MongoDB tietokanta
2. Vaihda mongoDB:n tietokannan "url" server2.js-koodissa käynnissä olevan MongoDB-tietokannan urliin