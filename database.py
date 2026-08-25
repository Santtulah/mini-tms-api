import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Luo ja palauttaa yhteyden paikalliseen XAMPP-tietokantaan

    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='logiapp_db',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Virhe yhdistettäessä tietokantaan: {e}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()

    if conn and conn.is_connected():
        print(">>> Yhteys logiapp_db tietokantaan onnistui! <<<")
        conn.close()

    
