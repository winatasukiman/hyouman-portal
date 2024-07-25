from odoo import models, fields


class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    # Override field to set False as the default value
    purchase_ok = fields.Boolean('Can be Purchased', default=False)

    # Override field to set 'service' as the default value
    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
