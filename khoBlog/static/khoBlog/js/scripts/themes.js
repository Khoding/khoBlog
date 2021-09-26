/* jshint esversion: 6 */

(function (exports) {
    const themeChanger = {
        settings: {
            wrapper: $('.wrapper'),
            buttons: $('.controls .controls')
        },

        init: function () {
            const _self = this;
            this.settings.buttons.on('click', function () {
                const $node = $(this);
                const theme = $node.data('theme');
                _self.settings.wrapper.removeClass().addClass('wrapper ' + theme);
                _self.settings.buttons.removeClass('disabled');
                $node.toggleClass('disabled');
            });
        }
    };

    themeChanger.init();
})(window);
