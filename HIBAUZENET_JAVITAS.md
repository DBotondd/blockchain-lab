# Rövidebb regisztrációs hibaüzenet

A `solidity_lab.py` `register()` függvénye a `verify()` hívással a tranzakció előtt ellenőrzi, hogy az adott szöveg lenyomata már szerepel-e a szerződésben. Ha igen, `CertificateAlreadyExistsError` kivételt dob. Az `app.py` a nyers EVM-hibát nem írja ki: helyette a következő rövid visszajelzés jelenik meg:

> Ez a tanúsítvány már regisztrálva van.

Üres bemenetnél az eredeti, közérthető `ValueError` szöveg jelenik meg. Váratlan hibáknál a részletek a szerver naplójába kerülnek, a felület általános hibát mutat.

**Fontos:** a Solidity `require` ellenőrzése változatlanul szükséges, mert két felhasználó között a tranzakció előtti ellenőrzés és az írás közben versenyhelyzet léphet fel. A régebbi, hosszú hibaüzeneteket csak az új kód futtatása után kerüljük el. A program újraindítása: `python -m streamlit run app.py`.
