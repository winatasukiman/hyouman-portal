from odoo import http
from odoo.http import request


class GoalController(http.Controller):
    """ Controller for handling goal-related requests. """

    @http.route('/goal/graph', auth='user', type='json')
    def get_goal_graph(self):
        """ Returns a JSON representation of the goal graph. """
        return self._get_goal_graph()

    def _get_goal_graph(self):
        """ Helper method to construct the goal graph data. """
        goals = request.env['goal.goal'].sudo().search([])
        nodes = [{'id': goal.id, 'label': goal.name, 'type': 'parent' if goal.sub_goal_ids else 'sub'} for goal in goals]
        links = [{'source': p.id, 'target': c.id} for c in goals for p in c.parent_goal_ids]

        return {'nodes': nodes, 'links': links}
