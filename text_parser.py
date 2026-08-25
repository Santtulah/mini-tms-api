
import re
from database import get_db_connection

def extract_delivery_info(message: str):
    """
    Perkaa tekstistä Regexin avulla rekisterinumeron, postinumeron ja hinnan.
    """
    plate_match =  re.search(r"[a-zA-ZåäöÅÄÖ]{2,3}-\d{1,3}", message)
    postal_match = re.search(r"\b\d{5}\b", message)
    price_match = re.search(r"(\d+)\s*(e|E|€|eur|euroa)", message)

    return {
        "license_plate": plate_match.group(0).upper() if plate_match else None,
        "postal_code": postal_match.group(0) if postal_match else None,
        "price": float(price_match.group(1)) if price_match else None,
        "raw_message": message
    }
def process_and_save_message(message: str):
    clean_message = extract_delivery_info(message)

    if not clean_message.get("license_plate") or not clean_message.get("postal_code"):
        return False
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        # Määritellään dictionary-kursori
        cursor = conn.cursor(dictionary=True)

        sql = 'SELECT id FROM vehicles WHERE license_plate = %s'
        license_plate = (clean_message.get('license_plate'),)

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
        delivery_values = (vehicle_id, "Tuntematon osoite", clean_message.get("postal_code"), clean_message.get("price"), clean_message.get("raw_message"),)

        cursor.execute(insert_delivery_sql, delivery_values)
        conn.commit()
    
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






if __name__ == "__main__":
    message = "Uusi pikakeikka: Jääkaappi osoitteeseen Vapaudenkatu 1, 40100 Jyväskylä. Autoksi ABC-123. Hinta 150e."
    process_and_save_message(message)



