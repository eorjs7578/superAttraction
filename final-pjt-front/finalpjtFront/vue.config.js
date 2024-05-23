// vite.config.js
export default {
    server: {
      proxy: {
        '/api': {
          target: 'https://finlife.fss.or.kr',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, '')
        }
      }
    }
  }