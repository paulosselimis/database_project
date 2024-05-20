def query1(cursor):
    cursor.execute('''
       -- Query for average rating per chef
SELECT c.chef_id, c.first_name, c.last_name, AVG(r.rating) AS average_rating
FROM competitionparticipants cp
JOIN rating r ON cp.participant_id = r.participant_id
JOIN chef c ON cp.chef_id = c.chef_id
GROUP BY c.chef_id, c.first_name, c.last_name;
    ''')
    result = cursor.fetchall()
    print("Query 1 results for chefs:")
    print("chef_id | first_name | last_name | average_rating")
    for row in result:
        print(row)

    cursor.execute('''
       -- Query for average rating per cuisine
SELECT cu.cuisine_id, cu.name AS cuisine_name, AVG(ra.rating) AS average_rating
FROM recipe r
JOIN cuisines cu ON r.cuisine_id = cu.cuisine_id
JOIN competitionparticipants cp ON r.recipe_id = cp.recipe_id
JOIN rating ra ON cp.participant_id = ra.participant_id
GROUP BY cu.cuisine_id, cu.name;

    ''')
    result = cursor.fetchall()
    print("\nQuery 1 results for cuisines:")
    print("cuisine_id | cuisine_name | average_rating")
    for row in result:
        print(row)


def query2(cursor, cuisine_name, specific_year):
    cursor.execute('''
-- Query to find chefs for a specific cuisine
WITH ChefsInCuisine AS (
    SELECT c.chef_id, c.first_name, c.last_name, c.age
    FROM chef c
    JOIN chef_cuisines cc ON c.chef_id = cc.chef_id
    JOIN cuisines cu ON cc.cuisine_id = cu.cuisine_id
    WHERE cu.name = %s
),

-- Query to find chefs who participated in episodes during a specific year
ChefsInYear AS (
    SELECT DISTINCT c.chef_id, c.first_name
    FROM chef c
    JOIN competitionparticipants cp ON c.chef_id = cp.chef_id
    JOIN episode e ON cp.episode_id = e.episode_id
    WHERE YEAR(e.date) = %s
)

-- Combine results from both queries
SELECT ci.chef_id, ci.first_name, ci.last_name, ci.age
FROM ChefsInCuisine ci
JOIN ChefsInYear cy ON ci.chef_id = cy.chef_id;''', (cuisine_name, specific_year))
    result = cursor.fetchall()
    if not result:
        print("Incorrect input.")
    else:
        print("chef_id | first_name | last_name | age")
        for row in result:
            print(row)

def query3(cursor):
    cursor.execute('''
SELECT c.chef_id, c.first_name, c.last_name, c.age, COUNT(rc.recipe_id) AS recipe_count
FROM chef c
JOIN recipe_chef rc ON c.chef_id = rc.chef_id
WHERE c.age < 30
GROUP BY c.chef_id, c.first_name, c.last_name, c.age
ORDER BY recipe_count DESC;''')
    result = cursor.fetchall()
    print("chef_id | first_name | last_name | age | recipe_count")
    for row in result:
        print(row)


def query4(cursor):
    cursor.execute('''
SELECT c.chef_id, c.first_name, c.last_name
FROM chef c
WHERE c.chef_id NOT IN (
    SELECT cp.chef_id
    FROM competitionparticipants cp
    WHERE cp.is_judge = 1
);'''
)
    result = cursor.fetchall()
    print("chef_id | first_name | last_name")
    for row in result:
        print(row)

def query5(cursor, specific_year):
    cursor.execute('''
SELECT judge_name, judge_id, episode_count
FROM (
    SELECT c.first_name AS judge_name, cp.judge_id, COUNT(DISTINCT cp.episode_id) AS episode_count
    FROM competitionparticipants cp
    JOIN episode e ON cp.episode_id = e.episode_id
    JOIN chef c ON cp.chef_id = c.chef_id
    WHERE cp.is_judge = 1 AND YEAR(e.date) = %s
    GROUP BY cp.judge_id, c.first_name
    HAVING episode_count > 3
) AS subquery
GROUP BY episode_count, judge_name, judge_id;''', (specific_year,))
    result = cursor.fetchall()
    if not result:
        print(f"No judges have participated more than 3 times during the year: {specific_year}")
    else:
        print("judge_name | judge_id | episode_count")
        for row in result:
            print(row)


def query6(cursor):
    cursor.execute('''
SELECT
    CONCAT(LEAST(rl1.label_id, rl2.label_id), '-', GREATEST(rl1.label_id, rl2.label_id)) AS label_pair,
    COUNT(*) AS pair_count
FROM
    recipe_label rl1
JOIN
    recipe_label rl2 ON rl1.recipe_id = rl2.recipe_id AND rl1.label_id < rl2.label_id
JOIN
    competitionparticipants cp ON rl1.recipe_id = cp.recipe_id
GROUP BY
    label_pair
ORDER BY
    pair_count DESC
LIMIT 3;''')
    result = cursor.fetchall()
    print("label_pair | pair_count")
    for row in result:
        print(row)

def query7(cursor):
    cursor.execute('''
SELECT c.chef_id, c.first_name, c.last_name, COUNT(cp.episode_id) AS appearance_count
FROM chef c
JOIN competitionparticipants cp ON c.chef_id = cp.chef_id
GROUP BY c.chef_id, c.first_name, c.last_name
HAVING appearance_count <= (
    SELECT MAX(appearance_count) - 5
    FROM (
        SELECT COUNT(*) AS appearance_count
        FROM competitionparticipants
        GROUP BY chef_id
    ) AS subquery
);
''')
    result = cursor.fetchall()
    print("chef_id | first_name | last_name | appearance_count")
    for row in result:
        print(row)


def query8(cursor):
    cursor.execute('''
SELECT 
    e.episode_number,
    cp.episode_id,
    COUNT(re.recipe_id) AS equipment_count
FROM 
    competitionparticipants cp
JOIN 
    episode e ON cp.episode_id = e.episode_id
JOIN 
    recipe_equipment re ON cp.recipe_id = re.recipe_id
GROUP BY 
    cp.episode_id
ORDER BY 
    equipment_count DESC
LIMIT 1;''')
    result = cursor.fetchall()
    print("episode_number | episode_id | equipment_count")
    for row in result:
        print(row)

def query9(cursor):
    cursor.execute('''
SELECT YEAR(e.date) AS competition_year, AVG(ni.carbs_per_serving) AS average_carbohydrates
FROM competitionparticipants cp
JOIN episode e ON cp.episode_id = e.episode_id
JOIN nutritional_info ni ON cp.recipe_id = ni.recipe_id
GROUP BY competition_year;
''')
    result = cursor.fetchall()
    print("competition_year | average_carbohydrates")
    for row in result:
        print(row)


def query10(cursor, year1, year2):
    cursor.execute(f'''
            SELECT 
                r.cuisine_id,
                c.name AS cuisine_name,
                SUM(CASE WHEN YEAR(ep.date) = {year1} THEN 1 ELSE 0 END) AS participation_count_{year1},
                SUM(CASE WHEN YEAR(ep.date) = {year2} THEN 1 ELSE 0 END) AS participation_count_{year2},
                SUM(CASE WHEN YEAR(ep.date) = {year1} THEN 1 ELSE 0 END) + SUM(CASE WHEN YEAR(ep.date) = {year2} THEN 1 ELSE 0 END) AS total_participation_count
            FROM 
                recipe r
            JOIN 
                competitionparticipants cp ON r.recipe_id = cp.recipe_id
            JOIN 
                episode ep ON cp.episode_id = ep.episode_id
            JOIN 
                cuisines c ON r.cuisine_id = c.cuisine_id
            WHERE 
                YEAR(ep.date) IN ({year1}, {year2})
            GROUP BY 
                r.cuisine_id,
                c.name
            HAVING 
                SUM(CASE WHEN YEAR(ep.date) = {year1} THEN 1 ELSE 0 END) >= 3
                AND SUM(CASE WHEN YEAR(ep.date) = {year2} THEN 1 ELSE 0 END) >= 3
            ORDER BY 
                total_participation_count;
        ''')
    result = cursor.fetchall()
    if result:
            print(f"cuisine_id | cuisine_name | participation_count_{year1} | participation_count_{year2} | total_participation_count")
            for row in result:
                print(row)
    else:
            print("Not enonugh participation counts found for the given years.")

def query11(cursor, chef_id):
    cursor.execute("SELECT CONCAT(first_name, ' ', last_name) FROM chef WHERE chef_id = %s", (chef_id,))
    chef_name_result = cursor.fetchone()

# Check if a result is obtained
    if chef_name_result:
        chef_name = chef_name_result[0]  # Extract chef_name from the result tuple
    else:
        print("Chef with the given ID not found.")
        return
    cursor.execute('''
SELECT 
    result.chef_name,
    result.judge_name,
    result.rating,
    total_rating.total_rating
FROM 
    (
        SELECT 
            %s AS chef_name,
            CONCAT(chef_judge.first_name, ' ', chef_judge.last_name) AS judge_name,
            rating.rating
        FROM 
            rating
        JOIN 
            judges ON rating.judge_id = judges.judge_id
        JOIN 
            competitionparticipants ON rating.participant_id = competitionparticipants.participant_id
        JOIN 
            chef AS chef_judge ON judges.chef_id = chef_judge.chef_id
        WHERE 
            competitionparticipants.chef_id = %s
        ORDER BY 
            rating.rating DESC
        LIMIT 5
    ) AS result
JOIN 
    (
        SELECT 
            SUM(rating) AS total_rating
        FROM 
            (
                SELECT 
                    rating.rating
                FROM 
                    rating
                JOIN 
                    judges ON rating.judge_id = judges.judge_id
                JOIN 
                    competitionparticipants ON rating.participant_id = competitionparticipants.participant_id
                WHERE 
                    competitionparticipants.chef_id = %s
                ORDER BY 
                    rating.rating DESC
                LIMIT 5
            ) AS top_ratings
    ) AS total_rating ON 1=1;
''', (chef_name, chef_id, chef_id))
    result = cursor.fetchall()
    if result:
            print("chef_name | judge_name | rating | total_rating")
            for row in result:
                print(row)
    else:
            print("No ratings found for the given chef ID.")


def query12(cursor):
    cursor.execute('''
WITH EpisodeDifficulty AS (
    SELECT YEAR(ep.date) AS year,
           ep.episode_id,
           ep.date,
           ep.episode_number,
           AVG(r.difficulty) AS avg_difficulty
    FROM competitionparticipants cp
    JOIN episode ep ON cp.episode_id = ep.episode_id
    JOIN recipe r ON cp.recipe_id = r.recipe_id
    GROUP BY YEAR(ep.date), ep.episode_id, ep.date, ep.episode_number
),
MaxDifficultyPerYear AS (
    SELECT YEAR(date) AS year,
           MAX(avg_difficulty) AS max_avg_difficulty
    FROM EpisodeDifficulty
    GROUP BY year
)
SELECT e.year,
       e.episode_number,
       e.avg_difficulty
FROM EpisodeDifficulty e
JOIN MaxDifficultyPerYear max_diff ON e.year = max_diff.year AND e.avg_difficulty = max_diff.max_avg_difficulty;'''
)
    result = cursor.fetchall()
    print("year | episode_number | avg_difficulty")
    for row in result:
        print(row)

def query13(cursor):
    cursor.execute('''
SELECT 
    ep.episode_number,
    AVG(
        CASE ch.prof_certification
            WHEN 'First_chef' THEN 3
            WHEN 'Second_chef' THEN 2
            WHEN 'Third_chef' THEN 1
            WHEN 'Assistant_head_chef' THEN 4
            WHEN 'Head_chef' THEN 5
            ELSE 0  -- Handle other cases if any
        END
    ) AS avg_certification_score
FROM competitionparticipants cp
JOIN chef ch ON cp.chef_id = ch.chef_id
JOIN episode ep ON cp.episode_id = ep.episode_id
GROUP BY ep.episode_number
ORDER BY avg_certification_score
LIMIT 1;''')
    result = cursor.fetchall()
    print("episode_number | avg_certification_score")
    for row in result:
        print(row)


def query14(cursor):
    cursor.execute('''
SELECT s.name AS theme_category, COUNT(*) AS appearance_count
FROM competitionparticipants cp
JOIN recipe_section rs ON cp.recipe_id = rs.recipe_id
JOIN sections s ON rs.section_id = s.section_id
GROUP BY s.name
ORDER BY appearance_count DESC
LIMIT 1;''')
    result = cursor.fetchall()
    print("theme_category | appearance_count")
    for row in result:
        print(row)

def query15(cursor):
    cursor.execute('''
SELECT fc.name AS food_category
FROM food_category fc
WHERE NOT EXISTS (
    SELECT 1
    FROM recipe_ingredient ri
    JOIN competitionparticipants cp ON ri.recipe_id = cp.recipe_id
    JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    WHERE i.food_category_id = fc.food_category_id
)
GROUP BY fc.name;
''')
    result = cursor.fetchall()
    print("food_category")
    for row in result:
        print(row)



