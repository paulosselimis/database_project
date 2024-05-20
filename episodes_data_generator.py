import mysql.connector
import random

history = []
def insert_episode_data(cursor, episode_id):
    try: 
        global history
        while True:
            selected_cuisine_ids = random.sample(range(1, 16), 10)
            if all(history.count(num) < 3 for num in selected_cuisine_ids):
                history.extend(selected_cuisine_ids)
                for x in range(1, 16):
                    if x not in selected_cuisine_ids:
                        history = [y for y in history if y != x]
                break

        # Initialize a set to store selected chef IDs
        selected_chef_ids = []

        # Select a random chef ID for each selected cuisine
        for cuisine_id in selected_cuisine_ids:
            # Select chef IDs associated with the current cuisine from chef_cuisines table
            cursor.execute("SELECT chef_id FROM chef_cuisines WHERE cuisine_id = %s", (cuisine_id,))
            chefs_for_cuisine = [row[0] for row in cursor.fetchall()]

            # Randomly select one chef ID from the list
            selected_chef_id = random.choice(chefs_for_cuisine)

            # Check if the selected chef has already been selected for another cuisine
            while selected_chef_id in selected_chef_ids:
                selected_chef_id = random.choice(chefs_for_cuisine)

            # Add the selected chef ID to the set
            selected_chef_ids.append(selected_chef_id)

        # Select 1 recipe for each selected cuisine_id
        selected_recipes = []
        for cuisine_id in selected_cuisine_ids:
            cursor.execute("SELECT recipe_id FROM recipe WHERE cuisine_id = %s ORDER BY RAND() LIMIT 1", (cuisine_id,))
            recipe = cursor.fetchone()
            selected_recipes.append(recipe[0])

        # Insert selected data into the recipe_chef table
        for chef_id, recipe_id in zip(selected_chef_ids, selected_recipes):
            cursor.execute("INSERT INTO recipe_chef (chef_id, recipe_id) VALUES (%s, %s)",
                        (chef_id, recipe_id))
            db.commit()

        # Select 3 random judges (chefs) who are not already selected as chefs
        cursor.execute("SELECT chef_id FROM chef WHERE chef_id NOT IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ORDER BY RAND() LIMIT 3", tuple(selected_chef_ids))
        selected_judge_ids = [row[0] for row in cursor.fetchall()]

        # Insert selected judge IDs into the judges table
        for judge_id in selected_judge_ids:
            cursor.execute("INSERT INTO judges (chef_id, episode_id) VALUES (%s, %s)", (judge_id, episode_id))
            db.commit()

            # Retrieve the generated judge_ids
        cursor.execute("SELECT judge_id FROM judges WHERE chef_id IN (%s) AND episode_id = %s"  % (','.join(map(str, selected_judge_ids)), episode_id))
        generated_judge_ids = [row[0] for row in cursor.fetchall()]

        # Retrieve the corresponding chef_id for each judge_id
        cursor.execute("SELECT chef_id FROM judges WHERE judge_id IN (%s)" % ','.join(map(str, generated_judge_ids)))
        generated_chef_ids = [row[0] for row in cursor.fetchall()]

    
        

            # Insert chef and recipe data for the current episode
        for chef_id, recipe_id in zip(selected_chef_ids, selected_recipes):
            cursor.execute("INSERT INTO competitionparticipants (episode_id, chef_id, recipe_id) VALUES (%s, %s, %s)",
                            (episode_id, chef_id, recipe_id))
            db.commit()

            # Insert the judge and chef IDs into the competitionparticipants table
        for judge_id, chef_id in zip(generated_judge_ids, generated_chef_ids):
            cursor.execute("INSERT INTO competitionparticipants (episode_id, judge_id, chef_id, is_judge) VALUES (%s, %s, %s, 1)",
                            (episode_id, judge_id, chef_id))
            db.commit()


        # Insert ratings for each judge for each chef
        for judge_id in generated_judge_ids:
            for chef_id in selected_chef_ids:
                # Generate a random rating between 1 and 5
                rating = random.randint(1, 5)
                
                # Get the participant ID of the chef from the competitionparticipants table
                cursor.execute("SELECT participant_id FROM competitionparticipants WHERE chef_id = %s AND episode_id = %s", (chef_id, episode_id))
                participant_id = cursor.fetchone()[0]
                

                # Insert the rating into the ratings table
                cursor.execute("INSERT INTO rating (judge_id, participant_id, rating) VALUES (%s, %s, %s)",
                            (judge_id, participant_id, rating))
                db.commit()


        print("Selected Cuisine IDs:", selected_cuisine_ids)
        print("Associated Chef IDs:", selected_chef_ids)
        print("Selected Recipe IDs:", selected_recipes)
        print("Selected Chef IDs for Judges:", selected_judge_ids)
        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print("Error inserting data:", error)

# Connect to your MySQL database
try:
    db = mysql.connector.connect(
        database='cooking_contest',
        host='localhost',
        user='root',
        passwd=''
    )
    cursor = db.cursor()

    

    # Loop over 60 episodes
    for episode_id in range(1, 61):

        insert_episode_data(cursor, episode_id)
        

except mysql.connector.Error as error:
    print("Error connecting to MySQL:", error)

finally:
    # Close the cursor and database connection
    
    cursor.close()
    db.close()
