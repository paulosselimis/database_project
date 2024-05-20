import mysql.connector
import subprocess
from queries import query1, query2, query3, query4, query5, query6, query7, query8, query9, query10, query11, query12, query13, query14, query15
import random
db = mysql.connector.connect(
    database = 'cooking_contest',
    host = 'localhost',
    user = 'root',
    passwd = ''

)

cursor = db.cursor()

def login(username, password):
    # Query the database to check if the user exists
    cursor.execute("SELECT user_id, is_admin FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        # Check if the user is an admin
        cursor.execute("SELECT * FROM admin WHERE user_id=%s", (user[0],))
        is_admin = cursor.fetchone()
        

        if is_admin:
            print("Welcome, admin!")
            return "admin", None, None
        else:
            cursor.execute("SELECT chef_id FROM chef WHERE user_id=%s", (user[0],))
            chef_id_result = cursor.fetchone()
            chef_id = chef_id_result[0]
            user_id = user[0]
            print("Welcome, user%s!" % user[0])
            print("Your chef id is %s." % chef_id)
            print("Your user_id is %s." % user_id)

            return "user", chef_id, user_id
    else:
        print("Invalid username or password.")
        return None, None, None
    
def fetch_and_display_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    if records:
        column_names = [i[0] for i in cursor.description]
        print(f"\n{table_name} Table Data:")
        print(", ".join(column_names))
        for record in records:
            print(record)
    else:
        print(f"No records found in {table_name} table.")

def add_new_recipe(cursor):
    try:
        # Insert into recipe table
        name = input("Enter recipe name: ")
        difficulty = input("Enter difficulty from 1 to 5: ")
        description = input("Enter description for the new recipe: ")
        fetch_and_display_table_data(cursor, "ingredients")
        base_id = input("Enter the id of the basic ingredient: ")
        recipe_type = input("Enter <cooking> or <pastry> :")
        fetch_and_display_table_data(cursor, "cuisines")
        cuisine_id = input("Enter the id of the cuisine: ")
        image_id = input("Enter the id of the image: ")
        fetch_and_display_table_data(cursor, "time")
        time_id = input("Enter the id of the time: ")


        cursor.execute("INSERT INTO recipe (name, difficulty, description, base_id, recipe_type, cuisine_id, image_id, time_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (name, difficulty, description, base_id, recipe_type, cuisine_id, image_id if image_id else None, time_id))
        db.commit()

        # Get the last inserted recipe_id
        recipe_id = cursor.lastrowid

        # Insert into recipe_equipment table
        fetch_and_display_table_data(cursor, "equipment")
        while True:
            equipment_id = input("Enter equipment ID (or 'done' to finish): ")
            if equipment_id.lower() == 'done':
                break
            cursor.execute("INSERT INTO recipe_equipment (recipe_id, equipment_id) VALUES (%s, %s)", 
                           (recipe_id, equipment_id))
            db.commit()

        # Insert into recipe_ingredient table
        fetch_and_display_table_data(cursor, "ingredients")
        while True:
            ingredient_id = input("Enter ingredient ID (or 'done' to finish): ")
            if ingredient_id.lower() == 'done':
                break
            quantity = input("Enter quantity: ")
            cursor.execute("INSERT INTO recipe_ingredient (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)", 
                           (recipe_id, ingredient_id, quantity))
            db.commit()

        # Insert into recipe_label table
        fetch_and_display_table_data(cursor, "label")
        while True:
            label_id = input("Enter label ID (or 'done' to finish): ")
            if label_id.lower() == 'done':
                break
            cursor.execute("INSERT INTO recipe_label (recipe_id, label_id) VALUES (%s, %s)", 
                           (recipe_id, label_id))
            db.commit()

        # Insert into recipe_meal_type table
        fetch_and_display_table_data(cursor, "meal_type")
        while True:
            meal_type_id = input("Enter meal type ID (or 'done' to finish): ")
            if meal_type_id.lower() == 'done':
                break
            cursor.execute("INSERT INTO recipe_meal_type (recipe_id, meal_type_id) VALUES (%s, %s)", 
                           (recipe_id, meal_type_id))
            db.commit()

        # Insert into recipe_section table
        fetch_and_display_table_data(cursor, "sections")
        while True:
            section_id = input("Enter section id (or 'done' to finish): ")
            if section_id.lower() == 'done':
                break
            cursor.execute("INSERT INTO recipe_section (recipe_id, section_id) VALUES (%s, %s)", 
                           (recipe_id, section_id))
            db.commit()

        # Insert into recipe_tips table
        fetch_and_display_table_data(cursor, "tips")
        while True:
            tips_id = input("Enter tip id (or 'done' to finish): ")
            if tips_id.lower() == 'done':
                break
            cursor.execute("INSERT INTO recipe_tips (recipe_id, tips_id) VALUES (%s, %s)", 
                           (recipe_id, tips_id))
            db.commit()

         # Insert into steps table
        fetch_and_display_table_data(cursor, "equipment")
        amount = input("Enter the amount (portions) of the recipe after all the steps are done: ")
        while True:
            sequence_order = input("Enter sequence order (or 'done' to finish): ")
            if sequence_order.lower() == 'done':
                break
            step_description = input("Enter step description: ")
            equipment_id = input("Enter equipment ID for this step: ")
            image_id = input("Enter image ID (optional, press Enter to skip): ")

            cursor.execute(
                "INSERT INTO steps (recipe_id, equipment_id, sequence_order, step_description, amount, image_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (recipe_id, equipment_id, sequence_order, step_description, amount, image_id if image_id else None)
            )
            db.commit()

            # Insert into nutritional_info table
            fat_per_serving = random.randint(5, 70)  # Example range for fat_per_serving
            protein_per_serving = random.randint(5, 70)  # Example range for protein_per_serving
            carbs_per_serving = random.randint(10, 170)  # Example range for carbs_per_serving

            cursor.execute("INSERT INTO nutritional_info (recipe_id, fat_per_serving, protein_per_serving, carbs_per_serving) VALUES (%s, %s, %s, %s)",
                        (recipe_id, fat_per_serving, protein_per_serving, carbs_per_serving))
            db.commit()

        print("New recipe added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_user_recipe(cursor, chef_id):
    try:
        # Prompt the user to input the recipe ID
        fetch_and_display_table_data(cursor, "recipe")
        recipe_id = input("Enter the recipe ID of the recipe you want to edit: ")

        # Check if the recipe ID belongs to the user
        cursor.execute("SELECT * FROM recipe_chef WHERE recipe_id = %s AND chef_id = %s", (recipe_id, chef_id))
        assigned_recipe = cursor.fetchone()

        if assigned_recipe:
            # Allow the user to update the recipe details
            name = input("Enter new recipe name (press Enter to keep current value): ")
            difficulty = input("Enter new difficulty from 1 to 5 (press Enter to keep current value): ")
            description = input("Enter new description for the new recipe (press Enter to keep current value): ")
            fetch_and_display_table_data(cursor, "ingredients")
            base_id = input("Enter the new id of the basic ingredient (press Enter to keep current value): ")
            recipe_type = input("Enter <cooking> or <pastry> (press Enter to keep current value):")
            fetch_and_display_table_data(cursor, "cuisines")
            cuisine_id = input("Enter the new id of the cuisine (press Enter to keep current value): ")
            image_id = input("Enter the new id of the image (press Enter to keep current value): ")
            fetch_and_display_table_data(cursor, "time")
            time_id = input("Enter the new id of the time (press Enter to keep current value): ")

            # Generate UPDATE query based on user input
            update_query = "UPDATE recipe SET "
            update_values = []

            if name:
                update_query += "name = %s, "
                update_values.append(name)
            if difficulty:
                update_query += "difficulty = %s, "
                update_values.append(difficulty)
            if description:
                update_query += "description = %s, "
                update_values.append(description)
            if base_id:
                update_query += "base_id = %s, "
                update_values.append(base_id)
            if recipe_type:
                update_query += "recipe_type = %s, "
                update_values.append(recipe_type)
            if cuisine_id:
                update_query += "cuisine_id = %s, "
                update_values.append(cuisine_id)
            if image_id:
                update_query += "image_id = %s, "
                update_values.append(image_id)
            if time_id:
                update_query += "time_id = %s, "
                update_values.append(time_id)

            if not any([name, difficulty, description, base_id, recipe_type, cuisine_id, image_id, time_id]):
                print("No changes made in the recipe table.")
            else:
                # Remove the trailing comma and space from the query
                update_query = update_query.rstrip(", ")

                # Add WHERE clause to restrict updates to the specific recipe ID
                update_query += " WHERE recipe_id = %s"
                update_values.append(recipe_id)

                # Execute the UPDATE query
                cursor.execute(update_query, update_values)
                db.commit()
            fetch_and_display_table_data(cursor, "equipment")
            equipment_ids = input("Enter new equipment IDs separated by commas (press Enter to keep the same equipment): ").split(",")
            if any(equipment_ids):
                
                
                delete_query = "DELETE FROM recipe_equipment WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for equipment_id in equipment_ids:
                    insert_query = "INSERT INTO recipe_equipment (recipe_id, equipment_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (recipe_id, equipment_id.strip()))

                db.commit()
                print("Equipment updated successfully.")
            else:
                print("No changes made for the equipment of the recipe")

            fetch_and_display_table_data(cursor, "ingredients")
            ingredients_input = input("Enter new ingredient IDs and quantities separated by commas (format: id:quantity, id:quantity, ...), press Enter to keep the same ingredients: ")
            if ingredients_input.strip():
                ingredients = [item.split(":") for item in ingredients_input.split(",") if ":" in item]
                delete_query = "DELETE FROM recipe_ingredient WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for ingredient_id, quantity in ingredients:
                    insert_query = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (recipe_id, int(ingredient_id.strip()), float(quantity.strip())))

                db.commit()
                print("Ingredients updated successfully.")
            else:
                print("No changes made for the ingredients of the recipe")

            fetch_and_display_table_data(cursor, "label")
            label_ids = input("Enter new label IDs separated by commas (press Enter to keep the same equipment): ").split(",")
            if any(label_ids):
                
                
                delete_query = "DELETE FROM recipe_label WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for label_id in label_ids:
                    insert_query = "INSERT INTO recipe_label (recipe_id, label_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (recipe_id, label_id.strip()))

                db.commit()
                print("Labels updated successfully.")
            else:
                print("No changes made for the labels of the recipe")

            fetch_and_display_table_data(cursor, "meal_type")
            meal_type_ids = input("Enter new meal type IDs separated by commas (press Enter to keep the same equipment): ").split(",")
            if any(meal_type_ids):
                
                
                delete_query = "DELETE FROM recipe_meal_type WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for meal_type_id in meal_type_ids:
                    insert_query = "INSERT INTO recipe_meal_type (recipe_id, meal_type_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (recipe_id, meal_type_id.strip()))

                db.commit()
                print("Meal types updated successfully.")
            else:
                print("No changes made for the meal types of the recipe")

            fetch_and_display_table_data(cursor, "sections")
            section_ids = input("Enter new section IDs separated by commas (press Enter to keep the same equipment): ").split(",")
            if any(section_ids):
                
                
                delete_query = "DELETE FROM recipe_section WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for section_id in section_ids:
                    insert_query = "INSERT INTO recipe_section (recipe_id, section_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (recipe_id, section_id.strip()))

                db.commit()
                print("Sections updated successfully.")
            else:
                print("No changes made for the sections of the recipe")

            fetch_and_display_table_data(cursor, "tips")
            tip_ids = input("Enter new tip IDs separated by commas (press Enter to keep the same equipment): ").split(",")
            if any(tip_ids):
                
                
                delete_query = "DELETE FROM recipe_tips WHERE recipe_id = %s"
                cursor.execute(delete_query, (recipe_id,))
                for tip_id in tip_ids:
                    insert_query = "INSERT INTO recipe_tips (recipe_id, tips_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (recipe_id, tip_id.strip()))

                db.commit()
                print("Tips updated successfully.")
            else:
                print("No changes made for the tips of the recipe")

            cursor.execute("SELECT fat_per_serving, protein_per_serving, carbs_per_serving, calories_per_serving FROM nutritional_info WHERE recipe_id = %s", (recipe_id,))
            nutritional_info = cursor.fetchone()

            if nutritional_info:
                print(f"Current nutritional info for recipe {recipe_id}:")
                print(f"Fat per serving: {nutritional_info[0]}")
                print(f"Protein per serving: {nutritional_info[1]}")
                print(f"Carbs per serving: {nutritional_info[2]}")
                print(f"Calories per serving: {nutritional_info[3]}")

            # Get new nutritional info from user
            new_fat = input("Enter new fat per serving (press Enter to keep the same): ")
            new_protein = input("Enter new protein per serving (press Enter to keep the same): ")
            new_carbs = input("Enter new carbs per serving (press Enter to keep the same): ")

            # Generate update query and values
            update_values = []
            update_query = "UPDATE nutritional_info SET "

            if new_fat.strip():
                update_query += "fat_per_serving = %s, "
                update_values.append(float(new_fat.strip()))
            
            if new_protein.strip():
                update_query += "protein_per_serving = %s, "
                update_values.append(float(new_protein.strip()))
            
            if new_carbs.strip():
                update_query += "carbs_per_serving = %s, "
                update_values.append(float(new_carbs.strip()))

            # Only proceed if there are values to update
            if update_values:
                # Remove the trailing comma and space
                update_query = update_query.rstrip(", ")
                update_query += " WHERE recipe_id = %s"
                update_values.append(recipe_id)

                # Execute the update query
                cursor.execute(update_query, update_values)
                db.commit()
                print("Nutritional info updated successfully.")
            else:
                print("No changes made for the nutritional info of the recipe")

            # Fetch existing steps for the recipe
            cursor.execute("SELECT * FROM steps WHERE recipe_id = %s ORDER BY sequence_order", (recipe_id,))
            existing_steps = cursor.fetchall()
            fetch_and_display_table_data(cursor, "equipment")
            print("Existing steps for the recipe:")
            for step in existing_steps:
                print(f"Step ID: {step[0]}, Equipment ID: {step[2]}, Sequence Order: {step[3]}, Description: {step[4]}, Amount: {step[5]}, Image ID: {step[6]}")

            

            steps_input = input("Enter new steps (format: sequence_order:equipment_id:description:amount:image_id, ..., press Enter to keep the same steps): ")
            
            if steps_input.strip():
                # Parse the new steps input
                new_steps = [item.split(":") for item in steps_input.split(",") if len(item.split(":")) == 5]
                # Validate input
                valid_input = all(len(item) == 5 and item[0].strip().isdigit() and item[1].strip().isdigit() for item in new_steps)
                if not valid_input:
                    print("Invalid input format. No changes made.")
                    
                
                # Delete existing steps
                else:
                    delete_query = "DELETE FROM steps WHERE recipe_id = %s"
                    cursor.execute(delete_query, (recipe_id,))
                
                    # Insert new steps
                    for step in new_steps:
                            sequence_order, equipment_id, description, amount, image_id = step
                            if image_id.strip().upper() == "NULL":
                                image_id = None
        
                            insert_query = "INSERT INTO steps (recipe_id, equipment_id, sequence_order, step_description, amount, image_id) VALUES (%s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (recipe_id, equipment_id.strip(), sequence_order.strip(), description.strip(), amount.strip(), image_id))
                    
                    db.commit()
                    print("Steps updated successfully.")
            else:
                print("No changes made for the steps of the recipe.")

            print("Recipe edited successfully.")
        else:
            print("You are not assigned to this recipe or the recipe does not exist.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_user_info(cursor, user_id):
    try:
        # Ask the user which field they want to update
        print("What do you want to update?")
        print("1. Username")
        print("2. Password")
        choice = input("Enter your choice: ")

        if choice == "1":
            new_username = input("Enter your new username: ")
            if new_username:
                cursor.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, user_id))
                db.commit()
                print("Username updated successfully.")
            else:
                print("Username cannot be empty.")
        
        elif choice == "2":
            new_password = input("Enter your new password: ")
            if new_password:
                cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_password, user_id))
                db.commit()
                print("Password updated successfully.")
            else:
                print("Password cannot be empty.")
        
        
        
        else:
            print("Invalid choice. Please enter a valid option.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def insert_into_table(cursor):

    try:
        table = input("Enter the table name: ")
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()

        values = []
        for column in columns:
            value = input(f"Enter value for {column[0]} ({column[1]}): ")
            if value.upper() == 'NULL':
                values.append(None)
            else:
                values.append(value)

        columns_names = ", ".join([column[0] for column in columns])
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({columns_names}) VALUES ({placeholders})"
        
        cursor.execute(query, values)
        db.commit()  # Don't forget to commit the transaction
        
        print("Record inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def delete_from_table(cursor):
    try:
        table = input("Enter the table name: ")
        cursor.execute(f"DESCRIBE {table}")
        columns = [column[0] for column in cursor.fetchall()]
        print("Column Names:", ", ".join(columns))
        column_name = input("Enter the column name for condition: ")
        value = input(f"Enter the value for {column_name}: ")
        
        query = f"DELETE FROM {table} WHERE {column_name} = %s"
        
        cursor.execute(query, (value,))
        db.commit()  # Don't forget to commit the transaction
        
        print("Record(s) deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def retrieve_from_table(cursor):
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            print("No tables found in the database.")
            return
        table = input("Enter the table name: ")
        cursor.execute(f"DESCRIBE {table}")
        columns = [column[0] for column in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()

        if records:
            print("Column Names:", ", ".join(columns))
            print("Records:")
            for record in records:
                print(record)
        else:
            print("No records found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_table(cursor):
    try:
        table = input("Enter the table name: ")
        cursor.execute(f"DESCRIBE {table}")
        columns = [column[0] for column in cursor.fetchall()]
        print("Column Names:", ", ".join(columns))
        id_column = input("Enter the name of the ID column: ")
        record_id = input(f"Enter the {id_column} of the record to update: ")

        
        update_values = {}
        for column in columns:
            if column != id_column:
                new_value = input(f"Enter new value for {column} (press Enter to keep current value): ")
                if new_value:
                    update_values[column] = new_value

        if update_values:
            set_clause = ", ".join([f"{column} = %s" for column in update_values.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"

            values = list(update_values.values())
            values.append(record_id)

            cursor.execute(query, values)
            db.commit()
            print("Record updated successfully.")
        else:
            print("No changes made.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_calories_per_serving(cursor):
    try:
        query = """
UPDATE nutritional_info ni
JOIN (
    SELECT 
        ri.recipe_id,
        SUM(ri.quantity * i.calories / 100) AS total_calories
    FROM 
        recipe_ingredient ri
    JOIN 
        ingredients i ON ri.ingredient_id = i.ingredient_id
    GROUP BY 
        ri.recipe_id
) AS calculated_calories ON ni.recipe_id = calculated_calories.recipe_id
SET ni.calories_per_serving = calculated_calories.total_calories;
        """
        
        cursor.execute(query)
        db.commit()
        print("Calories per serving updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Prompt the user for their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

user_type, chef_id, user_id = login(username, password)
if user_type == "user" or user_type == "admin":
    while True:
            
            print("Available actions:")
            print("1. Execute queries")
            print("2. Exit")
            print("3. Edit database")
            choice = input("Enter your choice: ")

            if choice == "1":
                query_name = input("Enter the name of the query function to execute (e.g., query1): ")
                if query_name == "query1":
                    query1(cursor)
                elif query_name == "query2":
                    cuisine_name = input("Enter cuisine name (e.g., Italian Cuisine): ")
                    specific_year = input("Enter specific year: ")
                    query2(cursor, cuisine_name, specific_year)
                elif query_name == "query3":
                    query3(cursor)
                elif query_name == "query4":
                    query4(cursor)
                elif query_name == "query5":
                    specific_year = input("Enter specific year: ")
                    query5(cursor, specific_year)
                elif query_name == "query6":
                    query6(cursor)
                elif query_name == "query7":
                    query7(cursor)
                elif query_name == "query8":
                    query8(cursor)
                elif query_name == "query9":
                    query9(cursor)
                elif query_name == "query10":
                    print("Enter 2 consecutive years")
                    year1 = input("Enter the first year: ")
                    year2 = input("Enter the second year: ")
                    query10(cursor, year1, year2)
                elif query_name == "query11":
                    chef_id = input("Enter chef ID(1781 - 1828 and 1909 - 1930): ")
                    query11(cursor, chef_id)
                elif query_name == "query12":
                    query12(cursor) 
                elif query_name == "query13":
                    query13(cursor)
                elif query_name == "query14":
                    query14(cursor)
                elif query_name == "query15":
                    query15(cursor)
                else:
                    print("Invalid query name")

            elif choice == "2":
                break

            elif choice == "3":
                if user_type == "user":
                    #user privileges
                    print("1. Insert new recipe")
                    print("2. Edit username/password")
                    print("3. Edit recipe assigned to you")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        add_new_recipe(cursor)
                              

                    elif choice == "2":
                        update_user_info(cursor, user_id)

                    elif choice == "3":
                        update_user_recipe(cursor, chef_id)

                    else:
                        print("Invalid choice. Please enter a valid option.")
                    

                elif user_type == "admin":
                    #admin privileges
                    print("1. Backup database")
                    print("2. Restore database")
                    print("3. Insert Data")
                    print("4. Delete Data")
                    print("5. View Data")
                    print("6. Update Data")
                    print("7. Update calories per serving for each recipe")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        try:
                                    # Run mysqldump command to create backup
                            mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"        
                            subprocess.run([mysqldump_path, '-u', 'root', '-p', 'cooking_contest', '>', 'backup.sql'], shell=True, check=True)
                            print("Backup completed successfully.")
                        except subprocess.CalledProcessError as e:
                            print("Error occurred during backup:", e)

                    elif choice == "2":
                        try:
                            subprocess.run([r"C:\xampp\mysql\bin\mysql.exe", '-u', 'root', '-p', 'cooking_contest', '<', 'backup.sql'], shell=True, check=True)
                            print("Restore completed successfully.")
                        except subprocess.CalledProcessError as e:
                            print("Error occurred during restore:", e)

                    elif choice == "3":
                        insert_into_table(cursor)

                    elif choice == "4":
                        delete_from_table(cursor)

                    elif choice == "5":
                        retrieve_from_table(cursor)  

                    elif choice == "6":
                        update_table(cursor)

                    elif choice == "7":
                        update_calories_per_serving(cursor)

                    else:
                        print("Invalid choice. Please enter a valid option.")

                   
            else:
                print("Invalid choice. Please enter a valid option.")




cursor.close()
db.close()