Aja ohjelmaa tästä kansiosta terminaalsita "python data-analysis-application.py". 

Huomaa, että riippuvuuksien on oltava asennettuja. Helpointa on ajaa ohjelmaa virtuaaliympäristöstä. (ks. yläkansio, readme & requirements). 

Huomaa, että saadaksesi jotakin dataa näkyviin ohjelmassa, sinulla pitää olla palvelin päällä sekä siihen liittyvä tietokanta. (..\node_server)

Kansiosta löytyy myös example.jpg, joka tarjoaa näkymän siihen, miltä ohjelma näyttää datan kanssa.

========================================================================

"Pääohjelma" on data-analysis-applications.py -tiedostossa. Appi käyttää hyödykseen PyQt5 GUI:n ja verkkoliikenteen mahdollistamisessa. Pääohjelma kutsuu kahta moduulia datan käsittelyyn sekä piirtämiseen.

threedeeplot on 2D sekä 3D graafien mahdollistava moduuli. Hyödyksi käytetään numpyä, matplotlibbiä, pyqtgraphia sekä OpenGL.GL. Koodi on hyvin purkkaviritys sen johdosta, että ohjelmaan haluttiin lisätä tuki n määrälle kuvaajia (tällä hetkellä 6).

DataHandlerin avulla tallennetaan palvelimelta saatuja datoja, ja seurataan, ettei jo ladattua dataa tarvitse ladata uudestaan.

loginDialog on pop-up dialog, joka ei tällä hetkellä ole enabloituna ohjelmassa.

serverConnection.ui on tiedosto, jota PyQt5 käyttää UI:n rakentamisen apuna. Tätä voi muokata käyttäen Qt Designeria (ilmainen).

Ohjelma kommunikoi palvelimen kanssa, sekä sisäisesti käsittelee dataa, käyttäen datasetin tunnisteina aikaa (millisekunnit 1.1.1970 lähtien).

Kokonaisuus on hankala, ja vaatii vähintään PyQt5:n tutustumista, sekä ylipäätänsä runsasta koodiin tutustumista, mikäli sille haluaa tehdä jotain.