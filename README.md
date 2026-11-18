## Online verzió – kiegészítő módosítások

A Blockchain Lab eredetileg a szakdolgozatom gyakorlati részeként készült, helyi futtatásra. A projekt később egy online változattal is kibővült, hogy a program böngészőből, külön telepítés nélkül is kipróbálható legyen.

**Fontos megjegyezni, hogy az online működéshez szükséges módosítások utólag készültek, és nem képezik a szakdolgozat eredeti gyakorlati feladatának részét.**

### Az online működéshez elvégzett változtatások

- Docker-alapú futtatási környezetet készítettem a programhoz.
- Hozzáadtam a Render szolgáltatáshoz szükséges telepítési beállításokat.
- Átalakítottam az indítási folyamatot, hogy a Streamlit és a Ganache felhős környezetben is működhessen.
- A Solidity-szerződések fordítását előre elvégezhetővé tettem, hogy csökkenjen a futás közbeni erőforrásigény.
- Bevezettem egy opcionális jelszavas belépési lehetőséget az online alkalmazáshoz.
- Elvégeztem néhány, a felhős futtatáshoz szükséges konfigurációs és környezeti módosítást.

### Mi maradt változatlan?

A szakdolgozatban bemutatott alapvető funkciókat nem módosítottam:

- a Pythonban megvalósított blokklánc működését;
- a blokkok létrehozását, hash-elését és ellenőrzését;
- a Proof of Work algoritmust;
- az adatmanipuláció és a SHA-256 működésének bemutatását;
- a két Solidity-okosszerződés alapvető működését és együttműködését.

### Elhatárolás a szakdolgozattól

Az online változat nem egy új szakdolgozati fejlesztés, hanem a már elkészült program utólagos, könnyebb hozzáférhetőséget szolgáló kiegészítése.

A szakdolgozatban dokumentált implementáció, tesztelés és mérési eredmények az eredeti, helyi környezetben működő programhoz tartoznak. Az online telepítéshez hozzáadott fájlok és módosítások kizárólag azt szolgálják, hogy az alkalmazás interneten keresztül is bemutatható és kipróbálható legyen.
