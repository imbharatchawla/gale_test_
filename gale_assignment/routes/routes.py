from gale_assignment.controllers.stats import Stats
from gale_assignment import api
api.add_resource(Stats, '/stats/')