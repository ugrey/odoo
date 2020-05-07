# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import api, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields):
        """ Method overridden in order to add an attachment containing the ISR
        to the draft message when opening the 'send by mail' wizard on an invoice.
        This attachment generation will only occur if all the required data are
        present on the invoice. Otherwise, no ISR attachment will be created, and
        the mail will only contain the invoice (as defined in the mother method).
        """
        result = super(MailTemplate, self).generate_email(res_ids, fields)
        if self.model != 'account.move':
            return result

        multi_mode = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi_mode = False

        if self.model == 'account.move':
            for record in self.env[self.model].browse(res_ids):
                if record.l10n_ch_isr_valid:
                    # We add an attachment containing the ISR
                    inv_print_name = self._render_field('report_name', record.ids, compute_lang=True)[record.id]

            if related_model._name == 'account.move':

                template = res_ids_to_templates[res_id]
                inv_print_name = self._render_template(template.report_name, template.model, res_id)
                new_attachments = []

                if related_model.l10n_ch_isr_valid:
                    # We add an attachment containing the ISR
                    isr_report_name = 'ISR-' + inv_print_name + '.pdf'
                    isr_pdf = self.env.ref('l10n_ch.l10n_ch_isr_report').render_qweb_pdf([res_id])[0]
                    isr_pdf = base64.b64encode(isr_pdf)
                    new_attachments.append((isr_report_name, isr_pdf))

                if related_model.can_generate_qr_bill():
                    # We add an attachment containing the QR-bill
                    qr_report_name = 'QR-bill-' + inv_print_name + '.pdf'
                    qr_pdf = self.env.ref('l10n_ch.l10n_ch_qr_report').render_qweb_pdf([res_id])[0]
                    qr_pdf = base64.b64encode(qr_pdf)
                    new_attachments.append((qr_report_name, qr_pdf))

                attachments_list = multi_mode and result[res_id].get('attachments', False) or result.get('attachments', False)
                if attachments_list:
                    attachments_list.extend(new_attachments)
                else:
                    record_dict['attachments'] =  new_attachments

        return result
