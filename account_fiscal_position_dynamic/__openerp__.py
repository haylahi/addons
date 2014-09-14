##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 Vadim (<http://based.at>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Dynamic Fiscal Position',
    'version': '0.1',
    'depends': ['account', 'sale', 'purchase'],
    'author': 'Vadim',
    'website': 'http://based.at',
    'category': 'Accounting',
    'description': """
Dynamic Fiscal Position
=======================
Dynamically re-map accounts and taxes if fiscal_position is changed. Adds "on_change" handler to fiscal_position field.
Re-maps account and taxes of already entered invoice, purchase order and sales order lines.
    """,
    "data": [
        'fiscal_position_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
