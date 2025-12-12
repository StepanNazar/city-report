const API_TARGET = "http://api:5000";

module.exports = {
  "/api": {
    target: API_TARGET,
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
            API_TARGET,
            "http://localhost:4200/api"
          );
        }
      });
    }
  },
  "/uploads": {
    target: API_TARGET,
    secure: false,
    changeOrigin: true,
    logLevel: "debug"
  }
};
