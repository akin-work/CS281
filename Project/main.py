from Database import Database


DATABASE_NAME = "esports_db"


def main():

   
    Database.create_database(DATABASE_NAME)

    # Create Database object
    db = Database(db_name=DATABASE_NAME)

    # Connect to database
    db.connect()

    # Setup tables and load data
    db.setup()

    # Create role
    db.execute_query("""
        CREATE ROLE esports_viewer
        LOGIN
        PASSWORD 'Project@520';
    """)

    # Create view
    db.execute_query("""
        CREATE OR REPLACE VIEW tournament_results_view AS
        SELECT
            m.match_id,
            t.tournament_name,
            g.game_name,
            tm.team_name AS winner,
            m.match_date
        FROM Matches m
        JOIN Tournaments t
            ON m.tournament_id = t.tournament_id
        JOIN Games g
            ON m.game_id = g.game_id
        JOIN Teams tm
            ON m.winner_team_id = tm.team_id;
    """)

    # Grant permissions to role
    db.execute_query("""
        GRANT SELECT
        ON tournament_results_view
        TO esports_viewer;
    """)


  
    print("\n--- SELECT FROM TEAMS ---")
    print(db.execute_query("""
        SELECT * FROM Teams;
    """))

    
    print("\n--- JOIN QUERY ---")
    print(db.execute_query("""
        SELECT
            t.tournament_name,
            tm.team_name,
            m.match_date
        FROM Matches m
        JOIN Tournaments t
            ON m.tournament_id = t.tournament_id
        JOIN Teams tm
            ON m.winner_team_id = tm.team_id;
    """))

    
    db.execute_query("""
        UPDATE Teams
        SET region = 'North America'
        WHERE team_id = 1;
    """)

    
    db.execute_query("""
        DELETE FROM Team_Participation
        WHERE participation_id = 6;
    """)

    
    print("\n--- AGGREGATE QUERY ---")
    print(db.execute_query("""
        SELECT
            COUNT(*) AS total_matches,
            AVG(prize_pool) AS average_prize_pool
        FROM Tournaments;
    """))

    
    db.close()

   

    role_db = Database(db_name=DATABASE_NAME)

    role_db.connect(
        username="esports_viewer",
        password="Project@520"
    )

    
    print("\n--- VIEW QUERY ---")
    print(role_db.execute_query("""
        SELECT * FROM tournament_results_view;
    """))

   
    role_db.close()


if __name__ == "__main__":
    main()