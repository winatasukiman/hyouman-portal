from odoo import models, fields


class HolidaysRequestCustom(models.Model):
    _inherit = "hr.leave"
    
    delegate_employee_id = fields.Many2one('hr.employee', string='Delegate to', required=True)
    
    
    def _validate_leave_request(self):
        """ Override function """
        
        res = super()._validate_leave_request()
        self.notify_all_employee()
        
        return res
    
    
    def notify_all_employee(self):
        """ Email notification to all employees upon validated leave request """
        
        employees = self.env['hr.employee'].search([('work_email', '!=', False), ('active', '=', True)])
        if not employees:
            return
        
        # Get email template
        template = self.env.ref('custom_time_off.email_template_notify_all_employees_on_validated_leave_request')
        if not template:
            return
        
        # Send the email using the leave request record (self)
        for employee in employees:
            template.sudo().send_mail(self.id, email_values={'email_to': employee.work_email}, force_send=True)