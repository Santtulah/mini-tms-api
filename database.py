import mysql.connector
from mysql.connector import Error


def get_db_connection():
    """
    Luo ja palauttaa yhteyden paikalliseen XAMPP-tietokantaan

    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='mini_tms_db',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Virhe yhdistettäessä tietokantaan: {e}")
        return None

def save_message(message: dict):
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        # Määritellään dictionary-kursori
        cursor = conn.cursor(dictionary=True)

        sql = 'SELECT id FROM vehicles WHERE license_plate = %s'
        license_plate = (message.get('license_plate'),)

        cursor.execute(sql, license_plate)
        result = cursor.fetchone()

        if result is not None:
            # Luetaan ID sanakirjasta sarakkeen nimellä ('id')
            vehicle_id = result['id']
            print(f"Auto löytyi tietokannasta, ID on: {vehicle_id}")
        else:
            insert_vehicle_sql = 'INSERT INTO vehicles (license_plate) VALUES (%s)'
            cursor.execute(insert_vehicle_sql, license_plate)
            conn.commit() 
            vehicle_id = cursor.lastrowid
            print(f"Uusi auto lisätty, ID on: {vehicle_id}")

        insert_delivery_sql = 'INSERT INTO deliveries (vehicle_id, destination_address, postal_code, price, raw_message) VALUES (%s, %s, %s, %s, %s)'
        delivery_values = (vehicle_id, "Tuntematon osoite", message.get("postal_code"), message.get("price"), message.get("raw_message"))

        cursor.execute(insert_delivery_sql, delivery_values)
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Tietokantavirhe: {e}")
        if conn:
            conn.rollback() # perutaan muutokset virhetilanteessa
        return False
        
    finally:
        # Varmistetaan, että resurssit vapautetaan aina
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_deliveries():
    """
    Hakee kaikki kuljetustilaukset tietokannasta ja palauttaa ne listana.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT d.id, d.destination_address, d.postal_code, d.price, d.status, d.created_at," \
        " v.license_plate FROM deliveries d JOIN vehicles v ON d.vehicle_id = v.id ORDER BY d.created_at DESC;")
        deliveries = cursor.fetchall()
        return deliveries
    except Exception as e:
        print(f"Tietokantavirhe: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_telematics_ping(license_plate: str, latitude: float, longitude: float):
    """
    Tallentaa telematiikkapingin tietokantaan.
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id FROM vehicles WHERE license_plate = %s', (license_plate,))
        result = cursor.fetchone()
        vehicle_id = result.get('id') if result else None

        if vehicle_id:
            cursor.execute('INSERT INTO telematics_logs (vehicle_id, latitude, longitude) VALUES (%s, %s, %s)', 
                           (vehicle_id, latitude, longitude))
            conn.commit()
            return True
    except Exception as e:
        print(f"Tietokantavirhe: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        


        


# if __name__ == "__main__":
#     conn = get_db_connection()

#     if conn and conn.is_connected():
#         print(">>> Yhteys logiapp_db tietokantaan onnistui! <<<")
#         conn.close()
    
