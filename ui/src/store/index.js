import { createStore } from 'vuex'
import camelCase from 'lodash/camelCase';

const requireModule = require.context('@/store/modules', false, /\.js$/);
const module = {};
requireModule.keys().forEach(filename => {
  const isIndexJsFile = filename === './index.js';
  if (!isIndexJsFile) {
    const moduleName = camelCase(filename.replace(/(\.\/|\.js)/g, ''));
    module[moduleName] = requireModule(filename).default;
  }
});

export default createStore({
  modules: module
})
