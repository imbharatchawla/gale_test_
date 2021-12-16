import psycopg2

conn = psycopg2.connect(database="galetest",
                            user="galetest",
                            password="bharat",
                            host="localhost",
                            port="5432")

conn.autocommit=True
cursor = conn.cursor()

def create_table_with_data():
    try:

        sql = '''CREATE TABLE DELIVERIES(match_id int,\
            inning int,\
                batting_team varchar(30),\
                    bowling_team varchar(30),\
                        over int, ball int, batsman varchar(30), non_striker varchar(30),
                        bowler varchar(30), is_super_over int, wide_runs int, bye_runs int, legbye_runs int,
                        noball_runs int, penalty_runs int, batsman_runs int, extra_runs int, total_runs int, 
                        player_dismissed varchar(30), dismissal_kind varchar(30), fielder varchar(30));'''
        
        sql2 = '''COPY deliveries(match_id,\
            inning,\
                batting_team,\
                    bowling_team,\
                        over, ball, batsman, non_striker,
                        bowler, is_super_over, wide_runs, bye_runs, legbye_runs,
                        noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, 
                        player_dismissed, dismissal_kind, fielder)
                FROM '/home/guddu/gale/gale_assignment/scripts/deliveries.csv'
                DELIMITER ','
                CSV HEADER;'''
        
        sql3 = '''CREATE TABLE MATCHES(id int,\
            season int,\
                city varchar(30),\
                    date date,\
                        team1 varchar(30), team2 varchar(30), toss_winner varchar(30), toss_decision varchar(30),
                        result varchar(30), dl_applied int, winner varchar(30), win_by_runs int, win_by_wickets int,
                        player_of_match varchar(30), venue varchar(90), umpire1 varchar(30),
                        umpire2 varchar(30), umpire3 varchar(30));'''

        sql4 = '''COPY matches(id,\
            season,\
                city,\
                    date,\
                        team1, team2, toss_winner, toss_decision,
                        result, dl_applied, winner, win_by_runs, win_by_wickets,
                        player_of_match, venue, umpire1, umpire2, umpire3)
                FROM '/home/guddu/gale/gale_assignment/scripts/matches.csv'
                DELIMITER ','
                CSV HEADER;'''

        cursor.execute(sql4)
        conn.commit()

    except Exception as e:
        print(e)    

if __name__ == "__main__":
    create_table_with_data()


