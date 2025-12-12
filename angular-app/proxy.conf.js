module.exports = {
  "/api": {
    target: "http://localhost:5000",
    secure: false,
    changeOrigin: true,
    logLevel: "debug",
    cookiePathRewrite: {
      "/auth/refresh": "/api/auth/refresh"
    },
    pathRewrite: {
      "^/api": ""
    },
    configure: (proxy, options) => {
      proxy.on("proxyRes", (proxyRes, req, res) => {
        if (proxyRes.headers.location) {
          proxyRes.headers.location = proxyRes.headers.location.replace(
            "http://localhost:5000",
            "http://localhost:4200/api"
          );
        }
      });
    }
  },
  "/uploads": {
    target: "http://localhost:5000",
    secure: false,
    changeOrigin: true,
    logLevel: "debug"
  }
};
