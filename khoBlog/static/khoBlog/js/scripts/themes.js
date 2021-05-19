(function (exports) {
    var themeChanger = {
        settings: {
            wrapper: $('.wrapper'),
            buttons: $('.controls .controls')
        },

        init: function () {
            var _self = this;
            this.settings.buttons.on('click', function () {
                var $node = $(this),
                    theme = $node.data('theme');
                _self.settings.wrapper.removeClass().addClass('wrapper ' + theme);
                _self.settings.buttons.removeClass('disabled');
                $node.toggleClass('disabled');
            });
        }
    };

    themeChanger.init();
})(window);
