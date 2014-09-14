# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class AccountFiscalPosition(orm.Model):
    _inherit = 'account.fiscal.position'

    _columns = {
        # 'Use' domain to limit the number of fiscal positions to display:
        #   'sale':     applied to sale documents (sale order, customer invoice)
        #   'purchase': applied to purchase documents (purchase order, supplier invoice)
        #   'all':      applied to both sales and purchases
        'use': fields.selection([('sale', 'Sale'), ('purchase', 'Purchase'), ('all', 'All')], 'Position Application', required=True),
    }

    _defaults = {
        'use': 'all',
    }


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def onchange_fiscal_position(self, cr, uid, ids, position_id, invoice_type, invoice_line, context=None):
        """ Change accounts and taxes mapping when fiscal position is changed
        """
        result = {}
        context = context or {}
        prod_obj = self.pool.get('product.product')
        line_obj = self.pool.get('account.invoice.line')
        fpos_obj = self.pool.get('account.fiscal.position')
        position = position_id and fpos_obj.browse(cr, uid, position_id, context=context) or False

        for index, (op, id, line) in enumerate(invoice_line):
            if op in (2, 3, 5, 6):
                continue
            line = line or {}
            product_id = line.get('product_id') or (line_obj.browse(cr, uid, id, context=context).product_id.id if id else False)
            product = product_id and prod_obj.browse(cr, uid, product_id, context=context) or False
            if product:
                if invoice_type in ('out_invoice', 'out_refund'):
                    account_id = product.property_account_income.id if product.property_account_income else product.categ_id.property_account_income_categ.id
                    tax_id = product.taxes_id
                else:
                    account_id = product.property_account_expense.id if product.property_account_expense else product.categ_id.property_account_expense_categ.id
                    tax_id = product.supplier_taxes_id
                account_id = fpos_obj.map_account(cr, uid, position, account_id)
                tax_id = fpos_obj.map_tax(cr, uid, position, tax_id)
                line.update({'account_id': account_id, 'invoice_line_tax_id': [(6, 0, tax_id)]})
                invoice_line[index] = (1 if op == 4 else op, id, line)
        result.update(invoice_line=invoice_line)
        return {'value': result}


class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    _columns = {
        # Disable editing fiscal position if confirmed
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position', readonly=True,
                                           states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),
    }

    def onchange_fiscal_position(self, cr, uid, ids, position_id, order_line, context=None):
        """ Change taxes when fiscal position is changed
        """
        result = {}
        context = context or {}
        prod_obj = self.pool.get('product.product')
        line_obj = self.pool.get('sale.order.line')
        fpos_obj = self.pool.get('account.fiscal.position')
        position = position_id and fpos_obj.browse(cr, uid, position_id, context=context) or False

        for index, (op, id, line) in enumerate(order_line):
            if op in (2, 3, 5, 6):
                continue
            line = line or {}
            product_id = line.get('product_id') or (line_obj.browse(cr, uid, id, context=context).product_id.id if id else False)
            product = product_id and prod_obj.browse(cr, uid, product_id, context=context) or False
            if product:
                tax_id = fpos_obj.map_tax(cr, uid, position, product.taxes_id)
                line.update({'tax_id': [(6, 0, tax_id)]})
                order_line[index] = (1 if op == 4 else op, id, line)
        result.update(order_line=order_line)
        return {'value': result}


class PurchaseOrder(orm.Model):
    _inherit = 'purchase.order'

    def onchange_fiscal_position(self, cr, uid, ids, position_id, order_line, context=None):
        """ Change taxes when fiscal position is changed
        """
        result = {}
        context = context or {}
        prod_obj = self.pool.get('product.product')
        line_obj = self.pool.get('purchase.order.line')
        fpos_obj = self.pool.get('account.fiscal.position')
        position = position_id and fpos_obj.browse(cr, uid, position_id, context=context) or False

        for index, (op, id, line) in enumerate(order_line):
            if op in (2, 3, 5, 6):
                continue
            line = line or {}
            product_id = line.get('product_id') or (line_obj.browse(cr, uid, id, context=context).product_id.id if id else False)
            product = product_id and prod_obj.browse(cr, uid, product_id, context=context) or False
            if product:
                tax_id = fpos_obj.map_tax(cr, uid, position, product.supplier_taxes_id)
                line.update({'taxes_id': [(6, 0, tax_id)]})
                order_line[index] = (1 if op == 4 else op, id, line)
        result.update(order_line=order_line)
        return {'value': result}
