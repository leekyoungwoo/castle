module.exports = {
  devServer: {
    port: 3001,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/exec': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/fdata': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  },
  chainWebpack: config => {
    const path = require('path');
    if (process.env.NODE_ENV !== 'production') {
      // config.devtool('eval');
      config.devtool('source-map');
      config.module
        .rule('istanbul')
        .test(/\.(js|vue)$/)
        .enforce('post')
        .include.add(path.resolve(__dirname, '/src'))
        .end()
        .use('istanbul-instrumenter-loader')
        .loader('istanbul-instrumenter-loader')
        .options({ esModules: true });
    }
  }
};
