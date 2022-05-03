/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    darkMode: "class",
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        "../templates/**/*.html",

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        "../../templates/**/*.html",

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        "../../**/templates/**/*.html",

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                jumbo: {
                    DEFAULT: "#78767F",
                    50: "#D5D5D8",
                    100: "#CBCACE",
                    200: "#B6B5BA",
                    300: "#A1A0A7",
                    400: "#8C8A93",
                    500: "#78767F",
                    600: "#615F67",
                    700: "#4B4950",
                    800: "#343338",
                    900: "#1E1D20",
                },
                flamingo: {
                    DEFAULT: "#EF4444",
                    50: "#FDEDED",
                    100: "#FCDADA",
                    200: "#F9B5B5",
                    300: "#F58F8F",
                    400: "#F26A6A",
                    500: "#EF4444",
                    600: "#E71414",
                    700: "#B30F0F",
                    800: "#800B0B",
                    900: "#4C0707",
                },
                cornflower: {
                    DEFAULT: "#8B5CF6",
                    50: "#EBE3FD",
                    100: "#DED0FC",
                    200: "#C2A9FA",
                    300: "#A783F8",
                    400: "#8B5CF6",
                    500: "#6527F3",
                    600: "#4A0CD6",
                    700: "#3709A1",
                    800: "#25066C",
                    900: "#130336",
                },
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/line-clamp"),
        require("@tailwindcss/aspect-ratio"),
    ],
};
