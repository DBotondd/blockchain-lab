# Solidity mini alkalmazás – tanúsítványok nyilvántartása

## Cél

A két együttműködő okosszerződés egy egyszerű tanúsítvány-ellenőrzési folyamatot mutat be.

- `TanusitvanyKezelo`: fogadja a szöveget, elkészíti a **Keccak-256** lenyomatát, és a másik szerződést hívja.
- `TanusitvanyTarolo`: tárolja, hogy mely lenyomatokat regisztrálták; csak a kezelőtől fogad új bejegyzést.

**Nem a teljes szöveget tároljuk a láncon.** A publikus blokkláncon a hash és a tranzakció adatai ugyanakkor megismerhetők. A bemenetet a tranzakció is tartalmazza, így a bemutató **nem alkalmas titkos vagy személyes adatok kezelésére**.

## Kipróbálás böngészőben (Remix)

1. Nyisd meg a https://remix.ethereum.org oldalt.
2. Hozz létre `Tanusitvanyok.sol` néven egy fájlt, és másold bele a mellékelt Solidity-kódot.
3. A **Solidity Compiler** fülön válassz 0.8.20 vagy frissebb kompatibilis 0.8.x verziót, majd **Compile**.
4. A **Deploy & Run Transactions** fülön válassz egy **Remix VM** környezetet (helyi böngészős tesztlánc).
5. A szerződésválasztó listában válaszd a `TanusitvanyKezelo` szerződést, majd kattints a **Deploy** gombra. A kezelő automatikusan létrehozza a tárolót is.
6. A **Deployed Contracts** alatt nyisd le a `TanusitvanyKezelo` szerződést.
7. A `regisztral` mezőben add meg: `Igazolas-2026-001`, majd küldd el a tranzakciót.
8. Az `ellenoriz` mezőben ugyanazzal a szöveggel `true` eredményt kapsz; `Igazolas-2026-002` szöveggel `false` eredményt.
9. A `regisztraciokSzama` függvénnyel ellenőrizd a regisztrációk számát; `lenyomat` függvénnyel nézd meg a 32 bájtos hash-t.
10. A `tarolo` függvény visszaadja a külön létrehozott tároló szerződés címét. Ha szeretnéd, ezt a címet a Remixben a `TanusitvanyTarolo` szerződéssel is hozzáadhatod (`At Address` / `Add Contract`).

## Mit bizonyít ez a példa?

- Két külön okosszerződés is együtt tud működni egy alkalmazáson belül.
- A kezelő meghívja a tároló `rogzit` és `letezik` függvényeit.
- A regisztrált szöveg módosítása megváltoztatja a hash-t, ezért az ellenőrzés elutasítja az új változatot.
- A tároló korlátozza, melyik másik szerződés módosíthatja a nyilvántartását.

## Kapcsolat a Python-alkalmazással

A Python/Streamlit modul **SHA-256**-ot használ a blokkok láncolásához, ez a Solidity-példa pedig **Keccak-256**-ot használ a tanúsítványok azonosításához. Ezek különböző hash-algoritmusok, tehát az azonos szöveg hash-e nem egyezik meg.

A Solidity-projekt külön fut a Remix VM-en: nincs közvetlen hálózati kapcsolat a Python oktatási blokklánca és a Remix tesztlánca között. Ez tudatosan egyszerű, könnyen bemutatható felépítés.

**Korlát:** ez egy demonstráció, nem hiteles tanúsítvány-kibocsátási rendszer. Bármely felhasználó regisztrálhat szöveget a kezelőn keresztül, nincs jogosultságvizsgálat vagy kibocsátóhitelesítés.
