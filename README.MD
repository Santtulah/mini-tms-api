# Mini-TMS API (Transport Management System)

This is a lightweight Transport Management System (TMS) and vehicle telematics API implemented with Python and FastAPI.

The project was built as a portfolio piece to demonstrate my proficiency with modern REST APIs, clean software architecture, and relational databases.

## Features and Solved Problems

The project simulates the backend system of logistics software and addresses two typical challenges:

1. **Parsing Messy Data:** The system often receives orders as free-form text. The API includes a Regex-based parser that extracts essential variables (license plates, postal codes, and prices) from the text and saves them in a structured format into a relational database.
2. **Telematics Ingestion (IoT / GPS):** Vehicles can send continuous location data to the API. The data is stored in the database and automatically linked to the correct vehicle using Foreign Keys.

## Architecture (Separation of Concerns)

The code is divided into three distinct layers to ensure maintainability and testability:

- **`api.py` (Controller):** Handles HTTP requests, Pydantic model validation, and error management (HTTP Exceptions).
- **`text_parser.py` (Service):** Contains the business logic and Regex rules for data cleaning. It does not interact with databases or network traffic.
- **`database.py` (Repository):** Manages all communication with the MySQL/MariaDB database securely using parameterized queries (preventing SQL injections).

## Technologies

- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Database:** MySQL / MariaDB
- **Other Tools:** Built-in `re` (Regex) for text analysis, `mysql-connector-python` for database connections.

## Endpoints

FastAPI generates automatic OpenAPI/Swagger documentation for the application. When the server is running, the graphical user interface is available at: `http://127.0.0.1:8000/docs`

- `GET /api/deliveries` - Lists all deliveries saved in the system from newest to oldest, combining order and vehicle data (SQL JOIN).
- `POST /api/deliveries/parse-text` - Receives free-form text, parses the order details, and saves them to the database.
- `POST /api/telematics/ping` - Receives and stores the GPS location sent by a vehicle.

## Installation and Usage (Local Testing)

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR-GITHUB-USERNAME]/mini-tms-api.git

2. **Create and activate a virtual environment (recommended):**

python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
---

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
