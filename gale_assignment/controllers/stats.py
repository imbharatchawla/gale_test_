from flask_restful import Resource, reqparse
from gale_assignment.services.statsservices import StatsService
# from gale_assignment import pg_conn
class Stats(Resource):
    def get(self):
        try:
            basis = ''
            season_dict = {
                "1": "2008",
                "2": "2009",
                "3": "2010",
                "4": "2011",
                "5": "2012",
                "6": "2013",
                "7": "2014",
                "8": "2015",
                "9": "2016",
                "10": "2017"
            }
            parser = reqparse.RequestParser()
            parser.add_argument('year', type=int, help='Year should be in string format (YYYY)')
            parser.add_argument('season', type=int, help='Season should be in Integer format as 1 or 2 etc')
            args = parser.parse_args()
            print(args['year'], args['season'])
            if args['year'] is not None:
                basis = args['year']
                data = StatsService().get_status(basis)

            elif args['season'] is not None:
                basis = args['season']
                max_value = max(season_dict, key=int)
                if basis > int(max_value):
                    data = {'err': "Invalid season value passed", "status": 0}
                for k,v in season_dict.items():
                    if str(basis) in k:
                        print(basis, v)
                        data = StatsService().get_status(v)

        except Exception as e:
            data = {'err': str(e)}
        
        return data
            