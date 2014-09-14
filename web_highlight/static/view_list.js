/*---------------------------------------------------------
 * One2ManyList: highlights clicked row
 *---------------------------------------------------------*/

openerp.web_highlight = function(instance) {

    instance.web.form.One2ManyList = instance.web.form.One2ManyList.extend({
        init: function() {
            this._super.apply(this,arguments);
            this.$current
                .on('click', 'tr', function (e) {
                    $(e.currentTarget)
                        .parent()
                        .find('tr.oe_row_selected')
                        .removeClass('oe_row_selected');
                    $(e.currentTarget)
                        .addClass('oe_row_selected');
                })
        }
    });

};
