import Vue from "vue";
import Vuetify from "vuetify/lib";
import colors from "vuetify/lib/util/colors";
import VueCookies from "vue-cookies-reactive";
import VueToast from "vue-toast-notification";

import "vue-toast-notification/dist/theme-sugar.css";

Vue.use(Vuetify);
Vue.use(VueCookies);
Vue.use(VueToast);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#5E35B1",
        primaryDark: "#5E35B1",
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        error: colors.red.accent3,
        background: colors.indigo.lighten5,
      },
      dark: {
        primary: "#9575CD",
        primaryDark: "#5E35B1",
        secondary: "#039BE5",
        background: colors.indigo.lighten5,
      },
    },
  },
});
