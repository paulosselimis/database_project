import mysql.connector


def delete_data_from_tables():
    try:
            db = mysql.connector.connect(
                database='cooking_contest',
                host='localhost',
                user='root',
                passwd=''
            )
            cursor = db.cursor()

            # List of tables to delete data from
            tables = ['recipe_chef', 'rating', 'competitionparticipants', 'judges']

            # Iterate through each table and delete data
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                print(f"Data deleted from table: {table}")

            # Commit the transaction
            db.commit()

    except mysql.connector.Error as error:
        print("An error occurred: ", error)

    finally:
        
        cursor.close()
        db.close()
            



delete_data_from_tables()
