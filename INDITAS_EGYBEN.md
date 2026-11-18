# Blockchain Lab – javított közös indítás (Windows)

A felületen a Python blokklánc **és** a valódi Solidity okosszerződések együtt szerepelnek. A Solidity kódot a háttérben egy Ganache helyi Ethereum tesztlánc hajtja végre. Az app a tesztláncot automatikusan elindítja, amikor a Solidity indítógombjára kattintasz. Nem kell Remix és **nem kell safe-pysha3, py-evm vagy eth-tester**.

## Egyszeri előkészület

1. Telepítsd a Node.js LTS verzióját (csak egyszer a gépeden):

```powershell
winget install --id OpenJS.NodeJS.LTS -e
```

2. Zárd be, majd nyisd meg újra a VS Code-ot. A `blockchain_szakdolgozat` projektmappában:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-solidity.txt
npm install
```

Ha az előző próbálkozás után a `.venv` már létezik, az első parancs kihagyható.

## Indítás (ezután mindig csak ez kell)

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

A böngészőben nyisd meg: http://localhost:8501. A Solidity részben kattints a **Solidity szerződések indítása** gombra. Első alkalommal a Solidity 0.8.20 fordító letöltése miatt internet szükséges.

## Kipróbálás

- Regisztrálj egy `Igazolas-2026-001` tanúsítványt.
- Ellenőrizd ugyanezt: **regisztrálva**.
- Ellenőrizd az `Igazolas-2026-002` szöveget: **nincs regisztrálva**.
- A `TanusitvanyKezelo` szerződés meghívja a `TanusitvanyTarolo` szerződés `rogzit` függvényét.

A Node.js/Ganache csak háttérfolyamat; az egyetlen kezelőfelület továbbra is a Streamlit. A Ganache külön Ethereum helyi lánc, **nem** a Python demonstráció saját lánca. A regisztrációk tesztadatok, nem nyilvános Ethereum-tranzakciók.

## Gyakori hiba

- `npm is not recognized`: Node.js telepítés és VS Code újraindítása.
- `Ganache még nincs telepítve`: ellenőrizd, hogy `npm install` a projektmappában futott-e.
- `No module named eth_tester`: a régi alkalmazást futtatod. Ezt a verziót bontsd ki új mappába, és onnan indítsd.
