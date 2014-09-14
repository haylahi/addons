openerp.web_returnkey = function(instance) {

    /**
     * Set focus to the next visible input field
     * Credits to: http://stackoverflow.com/a/292005
     *
     * @param {Object} input
     */
    var go_next = function (input) {
        $(':input:visible:eq(' + ($(':input:visible').index(input) + 1) + ')').focus();
    };

    instance.web.FormView.include({
        start: function() {
            this.$el.keypress(function (e) {
                if (e.which === $.ui.keyCode.ENTER) {
                    go_next(e.target);
                }
            });
            return this._super.apply(this,arguments);
        }
    });

    instance.web.form.FieldSelection.include({
        initialize_content: function() {
            this._super.apply(this,arguments);
            this.$("select").keypress(function(e) {
                if (e.which === $.ui.keyCode.ENTER && !e.shiftKey) {
                    e.preventDefault();
                    go_next(e.target);
                }
            });
        }
    });

    instance.web.form.FieldText.include({
        initialize_content: function() {
            this._super.apply(this,arguments);
            this.$("textarea").keydown(function(e) {
                if (e.which === $.ui.keyCode.ENTER && !e.shiftKey) {
                    e.preventDefault();
                    go_next(e.target);
                }
            });
        }
    });

    instance.web.form.FieldMany2ManyTags.include({
        initialize_content: function() {
            this._super.apply(this,arguments);
            var self = this;
            this.$("textarea").keydown(function(e) {
                if (e.which === $.ui.keyCode.TAB && self._drop_shown) {
                    self.$text.textext()[0].autocomplete().selectFromDropdown();
                }
                if (e.which === $.ui.keyCode.ENTER && !self._drop_shown) {
                    go_next(e.target);
                }
            });
        }
    });

};