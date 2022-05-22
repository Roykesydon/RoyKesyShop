const { defineConfig } = require("@vue/cli-service");
var path = require("path");
module.exports = defineConfig({
  transpileDependencies: ["vuetify"],
  configureWebpack: {
    resolve: {
      alias: {
        src: path.resolve(__dirname, "src"),
      },
    },
  },
  devServer: {
    allowedHosts: "all",
  },
});
