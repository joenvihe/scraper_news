
import psycopg2
import os

# selecciona las noticias por la BD
def get_noticias():
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(
        dbname= os.environ["HEROKU_DATABASE"],
        user= os.environ["HEROKU_USER"],
        password= os.environ["HEROKU_PASSWORD"],
        host= os.environ["HEROKU_HOST"],  # o la dirección del servidor
        port="5432"  # el puerto de PostgreSQL
    )

    # Crear un cursor
    cursor = conn.cursor()

    # Definir la consulta SQL
    query = """
    SELECT DISTINCT periodico,_id,contenido  FROM public.noticias WHERE contenido IS NOT NULL
    AND EXTRACT(YEAR FROM TO_DATE(display_date, 'YYYY-MM-dd')) = 2023
    AND EXTRACT(MONTH FROM TO_DATE(display_date, 'YYYY-MM-dd')) = 8
    """

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados en una lista de arreglos
    resultados = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()
    
    return resultados


#####################################################################################
# MAIN PRINCIPAL
#####################################################################################
if __name__ == '__main__':
    ln = get_noticias()
    print(ln)

# generar langchain
# guardar la data actualizada

