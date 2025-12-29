from odoo import fields, models

class AcademyProduct(models.TransientModel):
    _name="academy.product"

    name=fields.Char(string="Name", required=True)
    price = fields.Float(string="Price", required=True)
    course_id =fields.Many2one('academy.course', string='Course', required=True, readonly=True)

    def action_create_product(self):
        self.ensure_one()
        new_product=self.env['product.template'].create({
            'name': self.name,
            'type':'service',
            'list_price': self.price,
            'course_id': self.course_id.id,  
        })
        self.course_id.product_id=new_product.product_variant_id.id 
