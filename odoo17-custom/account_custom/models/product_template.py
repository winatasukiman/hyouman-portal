from odoo import models, fields


class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    # Override field to set default=False
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
