# Mini-TMS API (Transport Management System)

Tämä on Pythonilla ja FastAPI:lla toteutettu kevyt kuljetusten hallinnan (TMS) ja ajoneuvotelematiikan rajapinta.

Projekti on rakennettu työnäytteenä osoittamaan osaamistani modernien REST API -rajapintojen, puhtaan ohjelmistoarkkitehtuurin ja relaatiotietokantojen parissa.

## Ominaisuudet ja ratkaistut ongelmat

Projekti simuloi logistiikka-alan ohjelmiston taustajärjestelmää ja ratkoo kahta tyypillistä haastetta:

1. **Sotkuisen datan jäsentäminen (Data Parsing):** Järjestelmään saapuu usein tilauksia vapaamuotoisena tekstinä. API sisältää Regex-pohjaisen parserin, joka eristää vapaasta tekstistä tärkeät muuttujat (rekisterinumerot, postinumerot ja hinnat) ja tallentaa ne strukturoituna relaatiotietokantaan.
2. **Telematiikan vastaanotto (IoT / GPS):** Ajoneuvot voivat lähettää jatkuvaa sijaintidataa rajapintaan. Data tallennetaan tietokantaan siten, että se linkittyy automaattisesti oikeaan ajoneuvoon viiteavainten (Foreign Key) avulla.

## Arkkitehtuuri (Separation of Concerns)

Koodi on jaettu kolmeen selkeään kerrokseen ylläpidettävyyden ja testattavuuden takaamiseksi:

- **`api.py` (Controller):** Vastaa HTTP-pyynnöistä, Pydantic-mallien validoinnista ja virheiden (HTTP Exceptions) hallinnasta.
- **`text_parser.py` (Service):** Sisältää liiketoimintalogiikan ja Regex-säännöt datan siivoamiseen. Ei ota kantaa tietokantoihin tai nettiliikenteeseen.
- **`database.py` (Repository):** Hoitaa kaiken kommunikaation MySQL/MariaDB-tietokannan kanssa turvallisesti parametrisoiduilla kyselyillä (SQL-injektioiden esto).

## Teknologiat

- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Tietokanta:** MySQL / MariaDB
- **Muut työkalut:** Sisäänrakennettu `re` (Regex) tekstin analysointiin, `mysql-connector-python` tietokantayhteyksiin.

## Rajapinnat (Endpoints)

FastAPI generoi sovellukselle automaattisen OpenAPI/Swagger-dokumentaation. Kun palvelin on käynnissä, graafinen käyttöliittymä löytyy osoitteesta: `http://127.0.0.1:8000/docs`

- `GET /api/deliveries` - Listaa kaikki järjestelmään tallennetut kuljetukset uusimmasta vanhimpaan, yhdistäen tilaus- ja ajoneuvotiedot (SQL JOIN).
- `POST /api/deliveries/parse-text` - Ottaa vastaan vapaamuotoisen tekstin, parsii tilauksen tiedot ja tallentaa kantaan.
- `POST /api/telematics/ping` - Vastaanottaa ja tallentaa ajoneuvon lähettämän GPS-sijainnin.

## Asennus- ja käyttöohjeet (Paikallinen testaus)

1. **Kloonaa repositorio:**

   ```bash
   git clone [https://github.com/](https://github.com/)[SINUN-GITHUB-TUNNUKSESI]/mini-tms-api.git
   ''

   ```

2. **Luo ja aktivoi virtuaaliympäristö (suositeltu):**

   ```bash
   python -m venv .venv

   # Windows:
   .venv\Scripts\activate

   # Mac/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```
