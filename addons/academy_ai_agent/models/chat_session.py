from odoo import models, fields, api

class AcademyChatSession(models.Model):
    _name = 'academy.chat.session'
    _description = 'AI Chat Session'

    name = fields.Char(string="Session Name", default="New Chat")
    # دي اللي هتحفظ كل الرسايل القديمة وما تتمسحش
    history_ids = fields.One2many('academy.chat.command', 'session_id', string="History", readonly=True)
    # دي الخانة اللي بنكتب فيها (بتمسح نفسها بعد الإرسال)
    new_message = fields.Text(string="New Message")

    def action_send_and_notify(self):
        if not self.new_message:
            return
            
        command=self.env['academy.chat.command'].create({
            'session_id': self.id,
            'message': self.new_message,
            'response': "..."
        })

        command.process_command()
        
        self.new_message = False 
        
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
    