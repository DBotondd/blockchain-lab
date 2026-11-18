# Blockchain Lab: teljes online telepítés (Render)

## Mi van ebben a mappában?

Ez a korábban működő Blockchain Lab kódjának **online futtatásra előkészített másolata**.
A Python-blokklánc, a Streamlit-felület, a két Solidity-szerződés és a Ganache is jelen van.
A helyi projektedet **ne írd felül** ezzel; ezt külön tárhelyre töltsd fel.

### A szükséges módosítások

- `Dockerfile`: Python 3.13, Node.js, Ganache és a teljes alkalmazás Docker-környezete.
- `render.yaml`: a Render ingyenes webszerverének beállítása.
- `requirements-online.txt`: a korábban ellenőrzött könyvtárverziók.
- `package.json`: Ganache 7.9.2 mellett `solc` 0.8.20; a Solidity fordítása build során történik.
- `compile_for_cloud.js`: a két szerződés ABI-ját és bytecode-ját előállítja, forrás-ellenőrző SHA-256-tal.
- `solidity_lab.py`: **a felhős példányban a már lefordított szerződést tölti be**, így a kis memóriájú Render Free csomagon nem kell minden kattintásra fordítani; helyben továbbra is működik a py-solc-x.
- `app.py`: opcionális belépési jelszó, ha a Render `APP_PASSWORD` környezeti változó be van állítva.

## Első telepítés – Windowsról

1. A ZIP-et csomagold ki, és **ebben a mappában** legyen az `app.py`, `Dockerfile`, `render.yaml` és `package.json`.
2. Hozz létre egy új, üres **GitHub / GitLab / Bitbucket** repót, például `blockchain-lab-online`. Ez csak a forrás tárolására kell: a kész weboldal **nem a GitHubon**, hanem a Renderen fut.
3. A VS Code-ban nyiss terminált ebben a mappában:

```powershell
git init
git add .
git commit -m "Blockchain Lab online Render verzio"
git branch -M main
git remote add origin https://github.com/FELHASZNALONEV/blockchain-lab-online.git
git push -u origin main
```

4. Nyisd meg a https://dashboard.render.com/ oldalt, jelentkezz be, és válaszd **New > Blueprint**. Kapcsold össze a tárolót a Renderrel.
5. Render beolvassa a `render.yaml`-t: `blockchain-lab-demo`, `Docker`, `Free`, healthcheck.
6. Ha az oldal APP_PASSWORD értéket kér: adj meg **saját erős jelszót**, és az oktatónak külön add meg. Soha ne tedd a jelszót a GitHub forrásfájljaiba. Ha nem akarod jelszóval védeni, a Dashboardban ellenőrizd, hogy APP_PASSWORD ne legyen beállítva.
7. Kattints **Apply** vagy **Deploy**. A Render létrehozza az image-et, és kiad egy nyilvános `*.onrender.com` webcímet. Az URL-t a Render Dashboardból másold ki; nem lehet előre biztosan kitalálni.
8. Próbáld ki: 1) Blokklánc / új blokk; 2) SHA-256 labor; 3) Adatmanipuláció; 4) PoW mérések; 5) **Solidity szerződések indítása**; 6) regisztráció és ellenőrzés.

**Alternatíva:** Render **New > Web Service**, Git repo kiválasztása, Language = Docker, Instance Type = Free. `Dockerfile` és port (`PORT=10000`) beállítás alapértelmezésben automatikus; az APP_PASSWORD-öt a **Environment** lapon add meg, ha szeretnél jelszót.

## Fontos korlátok

- A Free Render szolgáltatás **15 perc tétlenség után leáll**, de a webcím állandó marad, látogatásra újraindulhat (kb. 1 perc). Az otthoni számítógéped kikapcsolható.
- A Free csomag **512 MB memóriát ad**. A teljes Streamlit + Ganache + Web3.py rendszerhez ez szűk lehet. A szerződések előrefordítása segít, de **a teljes Solidity-funkciók működése élő Render teszt nélkül nem garantálható**. Ha `Out of memory`, `Exited with status 137`, `Killed` jelenik meg a Logsban, nagyobb RAM-ú kiszolgáló vagy külön Ganache szolgáltatás kell.
- A Ganache lánca a futó Docker-példányhoz kötött. Leállításkor / újraindításkor a tanúsítványok nem maradnak meg. A Python-blokkok és Streamlit munkamenetek sem tartósak. Ez **bemutató**, nem produkciós tanúsítvány-nyilvántartás.
- Az EVM RPC **csak** `127.0.0.1:18545` címen figyel a konténeren belül, nem lesz közvetlenül internetre kitéve. A jelszó nélküli weboldal ettől még nyilvánosan használható, ezért nagy PoW-terhelést és spam műveleteket okozhat.
- Az alkalmazás saját Solidity-telepítése minden friss Streamlit munkamenetben új szerződéseket hoz létre ugyanazon helyi Ganache folyamaton. A felhasználók nem közös tanúsítvány-nyilvántartást használnak.
- Docker/Python/Node telepítése az otthoni gépeden nem szükséges a Renderhez; csak a kód feltöltéséhez kell Git.

## Hibaelhárítás

- **Build failed / npm:** a Render Build Logs végén keresd az npm hibáját; ellenőrizd az `npm install` lépést.
- **Build failed / requirements-online.txt:** ellenőrizd, hogy a megadott verziók elérhetők-e a csomagindexen és Python 3.13 alatt.
- **Build failed / Solidity:** `compile_for_cloud.js` megmutatja a pontos Solidity-fordítási hibát.
- **Deploy failed / no open ports:** ellenőrizd, hogy a Streamlit a `${PORT:-10000}` porton és a `0.0.0.0` címen figyel.
- **Solidity sikertelen / Ganache:** nézd meg a Render `Logs` lapját; a `npm`-modulok telepítve vannak-e és a memória elfogyott-e.
- **A Solidity után a weboldal eltűnik:** valószínű RAM-limit; a 512 MB korlát miatt nem biztos, hogy a teljes modul elfér.

## Tesztek

A Docker build a `python -m unittest -q test_blockchain test_reszletes` parancsot is futtatja. A Python-rész helyben, Docker nélkül is tesztelhető ezzel.

## Ha valóban folyamatosan futó, ingyenes szervert szeretnél

Az **Oracle Cloud Always Free Ampere A1** több RAM-ot és folyamatos VM-et adhat, de regisztrációhoz bankkártya-ellenőrzés kellhet, a szabad kapacitás nem garantált, és az inaktív gépeket visszavehetik. A Docker-csomagot egy ilyen Linux VM-re is fel lehet telepíteni, de külön HTTPS/proxy és tűzfal szükséges. A Render-szintű egyszerű webcímet így saját magadnak kell beállítanod.
