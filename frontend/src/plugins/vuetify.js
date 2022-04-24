import Vue from "vue";
import Vuetify from "vuetify/lib";
import colors from "vuetify/lib/util/colors";
import VueCookies from "vue-cookies-reactive";
import Toast from "vue-toastification";

import "vue-toastification/dist/index.css";

Vue.use(Vuetify);

Vue.use(VueCookies);
Vue.$cookies.config("3d");

Vue.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
});

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#039BE5",
        primaryDark: "#039BE5",
        secondary: "#9575CD",
        accent: colors.shades.black,
        error: colors.red.accent3,
        customBackground: "#F5F5F5",
      },
      dark: {
        primary: "#9575CD",
        primaryDark: "#5E35B1",
        secondary: "#039BE5",
        customBackground: "#212121",
      },
    },
  },
});
