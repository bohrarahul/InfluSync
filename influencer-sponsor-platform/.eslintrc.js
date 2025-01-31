module.exports = {
    parserOptions: {
      parser: 'babel-eslint',
    },
    extends: [
      'plugin:vue/vue3-recommended',
      'eslint:recommended',
    ],
    globals: {
      module: 'readonly', // define 'module' as a global
      require: 'readonly', // define 'require' as a global
    },
    rules: {
      'vue/multi-word-component-names': ['error', {
        'ignores': ['Home', 'Login', 'Register'],
      }],
      'no-unused-vars': ['warn'], // Optionally change to 'warn' instead of 'error' to see unused vars more leniently
    },
  };
  