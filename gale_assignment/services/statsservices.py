from gale_assignment import app, pg_conn

class StatsService():
    def execute_query(self, sql):
        print(sql)
        cur = pg_conn.cursor()
        sql = sql
        try:
            cur.execute(sql)
            data = cur.fetchall()
            pg_conn.commit()
        except Exception as e:
            print(str(e))
        data_list = []
        data_dict = {}
        print(data, len(data))
        if len(data) == 1:
            for x in data:
                print(len(x))
                if len(x) == 1:
                    for d in x:
                        data_dict = {'value': d}
                else:
                    data_dict = dict(data)
        else:
            data_dict = dict(data)
        data_list.append(data_dict)
        return data_list

    def get_status(self, value=''):
        res = {"status": 0, "top_4_teams": {}, "most_win_toss_team": {}, "max_player_of_match": {}, "most_win_team": {}, "location_win_top_team": {}, "toss_winning_team_choosing_bat": {}, "venue": {}, "team_win_by_highest_margin": {}, "team_win_by_highest_wicket": {}, "team_won_toss_and_match": {}, "most_runs_in_match": {}, "most_catches": {}, "err": ""}
        try:
            # cur = pg_conn.cursor()
            sql = '''select winner, count(winner) from matches m where season = {} group by winner order by count(winner) desc limit(4);'''.format(value)
            data = self.execute_query(sql)
            res['top_4_teams'] = data

            sql = '''SELECT TOSS_WINNER, COUNT(TOSS_WINNER) FROM MATCHES WHERE SEASON = {}
                        GROUP BY TOSS_WINNER HAVING COUNT (TOSS_WINNER) = (SELECT MAX(TOSS_WIN_COUNT) 
                        FROM (SELECT TOSS_WINNER, COUNT(TOSS_WINNER) TOSS_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} GROUP BY TOSS_WINNER) AS RESULTS);'''.format(value, value)
            data = self.execute_query(sql)
            res['most_win_toss_team'] = data

            sql = '''SELECT PLAYER_OF_MATCH, COUNT(PLAYER_OF_MATCH) FROM MATCHES WHERE SEASON = {} 
                        GROUP BY PLAYER_OF_MATCH HAVING COUNT (PLAYER_OF_MATCH) = (SELECT MAX(PLAYER_WIN_COUNT) 
                        FROM (SELECT PLAYER_OF_MATCH, COUNT(PLAYER_OF_MATCH) PLAYER_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} GROUP BY PLAYER_OF_MATCH) AS RESULTS);'''.format(value, value)
            data = self.execute_query(sql)
            res['max_player_of_match'] = data

            sql = '''SELECT WINNER, COUNT(WINNER) FROM MATCHES WHERE SEASON = {} 
                        GROUP BY WINNER HAVING COUNT (WINNER) = (SELECT MAX(MATCH_WIN_COUNT) 
                        FROM (SELECT WINNER, COUNT(WINNER) MATCH_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} GROUP BY WINNER) AS RESULTS);
                        '''.format(value, value)
            data = self.execute_query(sql)
            res['most_win_team'] = data

            sql = '''SELECT WINNER, VENUE FROM MATCHES WHERE SEASON = {} AND WINNER IN(SELECT WINNER FROM MATCHES WHERE SEASON = {}
                        GROUP BY WINNER HAVING COUNT (WINNER) = (SELECT MAX(MATCH_WIN_COUNT) 
                        FROM (SELECT WINNER, COUNT(WINNER) MATCH_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} GROUP BY WINNER) AS RESULTS)) 
                        GROUP BY VENUE,WINNER ORDER BY COUNT(WINNER) DESC
                        LIMIT (SELECT COUNT(*) FROM (SELECT WINNER FROM MATCHES WHERE SEASON = {}
                        GROUP BY WINNER HAVING COUNT (WINNER) = (SELECT MAX(MATCH_WIN_COUNT) 
                        FROM (SELECT WINNER, COUNT(WINNER) MATCH_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} GROUP BY WINNER) AS RESULTS)) AS FINALDATA);
                        '''.format(value, value, value, value, value)
            data = self.execute_query(sql)
            res['location_win_top_team'] = data

            sql = '''SELECT CONCAT(ROUND((
                        ((CAST((SELECT COUNT(*) FROM MATCHES WHERE TOSS_DECISION = 'bat' AND SEASON = {}) AS DECIMAL(7,2))) /
                        (CAST((SELECT COUNT(*) FROM MATCHES WHERE SEASON = {}) AS DECIMAL(7,2)))) * 100),2),'%') AS PERCENTAGE;'''.format(value, value)
            data = self.execute_query(sql)
            res['toss_winning_team_choosing_bat'] = data

            sql = '''SELECT VENUE, COUNT(VENUE) FROM MATCHES WHERE SEASON = {} 
                        GROUP BY VENUE HAVING COUNT (VENUE) IN (SELECT DISTINCT COUNT(VENUE) VENUE_WIN_COUNT 
                        FROM MATCHES WHERE SEASON = {} AND VENUE IS NOT NULL GROUP BY VENUE ORDER BY COUNT(VENUE) 
                        DESC LIMIT 1) ORDER BY COUNT(VENUE) DESC;'''.format(value, value)
            data = self.execute_query(sql)
            res['venue'] = data

            sql = '''SELECT WINNER FROM MATCHES WHERE SEASON = {} AND WIN_BY_RUNS IN 
                        (SELECT MAX(WIN_BY_RUNS) FROM MATCHES WHERE SEASON = {}) GROUP BY WINNER;'''.format(value, value)
            data = self.execute_query(sql)
            res['team_win_by_highest_margin'] = data

            sql = '''SELECT WINNER FROM MATCHES WHERE SEASON = {} AND WIN_BY_WICKETS IN 
                        (SELECT MAX(WIN_BY_WICKETS) FROM MATCHES WHERE SEASON = {}) GROUP BY WINNER;'''.format(value, value)
            data = self.execute_query(sql)
            res['team_win_by_highest_wicket'] = data

            sql = '''SELECT COUNT(*) FROM MATCHES WHERE TOSS_WINNER = WINNER AND SEASON = {};'''.format(value)
            data = self.execute_query(sql)
            res['team_won_toss_and_match'] = data

            sql = '''SELECT BATSMAN, COUNT(BATSMAN_RUNS) FROM DELIVERIES D1
                        INNER JOIN MATCHES M1 ON D1.MATCH_ID = M1.ID
                        WHERE DISMISSAL_KIND = 'caught' AND M1.SEASON = {}
                        GROUP BY BATSMAN HAVING COUNT (BATSMAN_RUNS) IN (SELECT DISTINCT COUNT(BATSMAN_RUNS) RUN_COUNT 
                        FROM DELIVERIES D2 INNER JOIN MATCHES M2 ON D2.MATCH_ID = M2.ID 
                        WHERE DISMISSAL_KIND = 'caught' AND M2.SEASON = {} AND BATSMAN IS NOT NULL 
                        GROUP BY BATSMAN ORDER BY COUNT(BATSMAN_RUNS) DESC LIMIT 1) 
                        '''.format(value, value)
            data = self.execute_query(sql)
            res['most_runs_in_match'] = data

            sql = '''SELECT FIELDER, COUNT(FIELDER) FROM DELIVERIES D1
                        INNER JOIN MATCHES M1 ON D1.MATCH_ID = M1.ID
                        WHERE DISMISSAL_KIND = 'caught' AND M1.SEASON = {}
                        GROUP BY FIELDER HAVING COUNT (FIELDER) IN (SELECT DISTINCT COUNT(FIELDER) CATCHES_COUNT 
                        FROM DELIVERIES D2 INNER JOIN MATCHES M2 ON D2.MATCH_ID = M2.ID 
                        WHERE DISMISSAL_KIND = 'caught' AND M2.SEASON = {} AND FIELDER IS NOT NULL 
                        GROUP BY FIELDER ORDER BY COUNT(FIELDER) DESC LIMIT 1) 
                        '''.format(value, value)
            data = self.execute_query(sql)
            res['most_catches'] = data
            
            res['status'] = 1

        except Exception as e:
            res['err'] = str(e)
        return res