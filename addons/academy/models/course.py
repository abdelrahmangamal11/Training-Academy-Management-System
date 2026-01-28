import random
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError # ضفنا UserError هنا

class Course(models.Model):  
    _name="academy.course"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    ## Fields ##
    name = fields.Char(string='Course Name', required=True, tracking=True)
    ref=fields.Char(string='Reference', default='New',  required=True)
    code= fields.Char(string='Course Code', required=True, index=True)
    description = fields.Text(string='Course Description', tracking=True)
    instructor_id=fields.Many2one('res.partner')
    sale_order_ids=fields.One2many('sale.order', 'course_id', string='Sale Order')        
    category_id=fields.Many2one('academy.course.category', string='Category')
    product_id=fields.Many2one('product.product', string='Product')
    duration_hours=fields.Float(string='Duration (Hours)')
    max_students=fields.Integer(string='Maximum Students', default=20)
    state=fields.Selection([("draft","Draft"),
                            ("published","Published"),
                            ('in_progress','In_progress'),
                            ('done','Done'),
                            ('cancelled','Cancelled'),
                            ('closed','Closed')],default="draft",tracking=True)
    start_date=fields.Date(string='Start Date', tracking=True)
    expected_selling_date=fields.Date(string='Expected Selling Date', tracking=True)
    is_late=fields.Boolean(string='Is Late')
    end_date=fields.Date(string='End Date', tracking=True)
    enrollment_ids=fields.One2many("academy.enrollment","course_id",string="Enrollments")
    enrolled_count=fields.Integer(string='Number of Enrolled Students', compute='_compute_enrolled_count')
    available_seats=fields.Integer(string='Available Seats', compute='_compute_available_seats', store=True)
    sale_order_count=fields.Integer(string='Sale Order Line', compute='_compute_sale_order_count')
    is_full = fields.Boolean(string='Is Full', compute='_compute_is_full', store=True)
    instructor_name=fields.Char(string='Instructor Name', related='instructor_id.name', store=True)
    instructor_phone=fields.Char(string='Instructor Phone',related='instructor_id.vat', store=True)
    instructor_tax_id=fields.Char(string='Instructor Tax ID',related='instructor_id.phone', store=True)
    active=fields.Boolean(default=True)
    

    ## Constraints ##
    _sql_constraints=[('unique_course-code', 'UNIQUE(code)', 'code must be unique')]
 

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for course in self:
            if course.start_date and course.end_date:
             if course.end_date < course.start_date:
                raise ValidationError('End Date cannot be earlier than Start Date.')      

    @api.constrains('max_students')
    def _check_max_students(self):
        for course in self:
            if course.max_students <= 0:
                raise ValidationError('Maximum Students must be greater than zero.')

    # @api.constrains('product_ids')
    # def _check_product_list(self):
    #     for course in self:
    #         new_product=self.env['product.product'].search_count([('course_id','=',course.id)])
    #         if new_product> 1 :
    #             raise ValidationError('the course is connected to just one product.')

    # @api.constrains('code')
    # def _chack_uppercase_code(self):
    #     for rec in self:
    #         rec.code=rec.code.upper()      
                
    # Computation Methods ##

    @api.onchange('code')
    def _onchange_code_upper(self):
        for rec in self:
            print("the onchange excuted ")          

    @api.depends('enrollment_ids')
    def _compute_enrolled_count(self):
        for course in self:
            course.enrolled_count = len(course.enrollment_ids.filtered(lambda e: e.state == 'confirmed'))
            course.available_seats=5
            

    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for course in self:
            print(f"the record of @api.depends ${course}")
            course.available_seats =max(course.max_students - course.enrolled_count, 0)       
    
    @api.depends('available_seats')
    def _compute_is_full(self):
        for course in self:
            course.is_full = course.available_seats <= 0

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for course in self:
            course.sale_order_count = self.env['sale.order'].search_count([
                ('order_line.product_id.course_id', '=', course.id)
            ])

           
    ## Action Methods ##
    def action_publish(self):
        for rec in self:
            rec.state = 'published'
    
    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'   
    
    def action_complete(self):      
        
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled' 
    
    def action_set_draft(self):
        for rec in self:
            rec.state = 'draft' 
    
    def action_close(self):
        for rec in self:
            rec.state = 'closed' 

    def action_create_product(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("academy.action_academy_product_wizard")
        action["context"]={
            "default_course_id": self.id
        }
        return action
    
    def action_view_enrollments(self):
        return {
            'name': 'Enrollments',
            'type': 'ir.actions.act_window',
            'res_model': 'academy.enrollment',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {
                'default_course_id': self.id,
                'create': False,
            }
        }
    def action_view_sales_orders(self):
        return{
            'name': 'Sales Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('order_line.product_id.course_id', '=', self.id)],
            'context': {
                'default_course_ids': self.id,
                'create': True,
            }
        }
    
    def check_selling_date(self): # بتشاور على ال model نفسه مش ال recordset فهحتاج اعمل هنا loop معين او search لي set اشتغل عليها #
        course_ids=self.search([])
        for course in course_ids:
            if course.expected_selling_date and course.expected_selling_date < fields.Date.today():
                course.is_late = True   

    def action_print_report(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("academy.action_enrollment_report_wizard")
        return action
    
    def action(self):
        print("###########################################\n")
        print(self.env.user)
        print("###########################################\n")
        print(self.env.user.name)
        print("###########################################\n")
        print(self.env.user.partner_id.phone)
   
    @api.model
    def create(self,vals):
        res=super(Course,self).create(vals)
        if res.ref=='New':
            res.ref = self.env['ir.sequence'].next_by_code('academy_seq')
        return res


    def generate_test_data(self):
        # 1. تجهيز البيانات الأساسية
        partner = self.env['res.partner'].search([], limit=1)
        # مجلة المبيعات والمشتريات
        sale_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        purchase_journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        
        if not partner or not sale_journal or not purchase_journal:
            raise UserError("تأكد من وجود عميل واحد على الأقل وإعداد مجلات البيع والشراء في الحسابات!")

        # 2. توليد 30 فاتورة مبيعات (إيرادات)
        for i in range(30):
            invoice_date = datetime.now() - timedelta(days=random.randint(0, 60))
            self.env['account.move'].create({
                'move_type': 'out_invoice', # فاتورة عميل
                'partner_id': partner.id,
                'journal_id': sale_journal.id,
                'date': invoice_date.date(),
                'invoice_date': invoice_date.date(),
                'invoice_line_ids': [(0, 0, {
                    'name': f'كورس برمجة - {i}',
                    'quantity': 1,
                    'price_unit': random.uniform(500, 2000),
                })],
            }).action_post() # ترحيل عشان تظهر في التقارير

        # 3. توليد 20 فاتورة مشتريات (مصاريف)
        for j in range(20):
            bill_date = datetime.now() - timedelta(days=random.randint(0, 60))
            self.env['account.move'].create({
                'move_type': 'in_invoice', # فاتورة مورد
                'partner_id': partner.id, # ممكن تستخدم نفس الشريك للتجربة
                'journal_id': purchase_journal.id,
                'date': bill_date.date(),
                'invoice_date': bill_date.date(),
                'invoice_line_ids': [(0, 0, {
                    'name': f'مصاريف صيانة - {j}',
                    'quantity': 1,
                    'price_unit': random.uniform(100, 500),
                })],
            }).action_post()

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "تم ضخ 50 عملية مبيعات ومصاريف.. راجع تقاريرك الآن!",
                'type': 'rainbow_man',
            }
        }

            
    