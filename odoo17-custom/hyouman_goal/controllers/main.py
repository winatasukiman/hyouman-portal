from odoo import http
from odoo.http import request


class GoalController(http.Controller):
    """ Controller for handling goal-related requests. """

    @http.route('/goal/graph', auth='user', type='json')
    def get_goal_graph(self, team_name):
        """ Returns a JSON representation of the goal graph. """
        goals = request.env['goal.goal'].sudo().search([('accountable_team', '=', team_name)])
        nodes = [{'id': goal.id, 'label': goal.name, 'type': 'parent' if goal.sub_goal_ids else 'sub'} for goal in goals]
        links = [{'source': p.id, 'target': c.id} for c in goals for p in c.parent_goal_ids]

        return {'nodes': nodes, 'links': links}
    
    @http.route('/goal/team_list', auth='user', type='json')
    def get_goal_team(self):
        """ Returns a JSON representation of the goal graph. """
        goals = request.env['goal.goal'].sudo().search([])
        team_data = []
        for index, goal in enumerate(goals):
            team = goal.accountable_team
            if team and team not in [t['name'] for t in team_data]:
                team_data.append({
                    'id': index,
                    'name': team,
                })
               
        return team_data
