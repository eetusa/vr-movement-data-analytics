Unity VR setupattu käyttäen tutoriaalina
https://youtu.be/gGYtahQjmWQ?list=PLrk7hDwk64-a_gf7mBBduQb3PEBYnG4fU

======================
trackControllerData.cs
======================
Ei toimi siten, että se asetetaan kontrollerin gameobjektiin ja skripti seuraisi kyseistä ohjainta. Tuolla tapaa skripti voisi olla järkevämpi, mikäli sitä haluaa jatkokehittää. Skripti toimii globaalisti mistä objektista tahansa, ja tarkkailee (tällä hetkellä) vain vasemman ohjaimen dataa. Helposti muokattavissa haluttavaan muotoon sekä tarkkailemaan muita laitteita.

Huomaa: palvelimen URL on kovakoodattu trackControllerData.cs:n koodiin, ja se tulee tarpeen vaatiessa muuttaa.

Käytetty Unityn API VR-laitteita varten: UnityEngine.XR

======================
DataPacket.cs
======================
Luokka helpottamaan JSONin muodostamista tallennetusta datasta.