import mysql.connector
from mysql.connector import errorcode

def crear_base_datos_mariadb():
    try:
        # Conectar a MariaDB (ajusta el host, usuario y contraseña si es necesario)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS nanda_diagnosticos")
        conn.database = "nanda_diagnosticos"

        # Crear la tabla 'diagnosticos' if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            codigo VARCHAR(10),
            nombre VARCHAR(255),
            sintomas TEXT,
            intervenciones_nic TEXT,
            resultados_noc TEXT
        )
        ''')

        # Lista de diagnósticos
        nanda_diagnosticos = [
            {
                "codigo": "00292",
                "nombre": "Disposición para mejorar la autogestión de la salud",
                "sintomas": ["interés en aprender", "voluntad de cambiar hábitos", "confianza en las habilidades", "preocupación por el bienestar"],
                "intervenciones_nic": [
                    "Fomentar la autoeducación sobre la autogestión.",
                    "Establecer metas de salud específicas y alcanzables.",
                    "Brindar recursos educativos sobre autocuidado.",
                    "Proporcionar apoyo continuo para motivar la autogestión."
                ],
                "resultados_noc": [
                    "Autogestión de la salud",
                    "Conocimiento sobre la salud"
                ]
            },
            # ... (se han omitido los demás para brevedad, pero en el script real se incluirían todos)
        ]
        
        # Nota: He insertado los datos manualmente vía SQL, 
        # pero aquí dejo la estructura por si quieres re-ejecutarlo.
        
        # Guardar cambios
        conn.commit()
        print("Base de datos y tabla creadas exitosamente en MariaDB.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(err)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    crear_base_datos_mariadb()
