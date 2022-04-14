import Vue from "vue";
import Vuetify from "vuetify/lib";
import colors from "vuetify/lib/util/colors";
import VueCookies from "vue-cookies-reactive";

Vue.use(Vuetify);
Vue.use(VueCookies);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#5E35B1",
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        error: colors.red.accent3,
        background: colors.indigo.lighten5,
      },
      dark: {
        primary: "#5E35B1",
        background: colors.indigo.lighten5,
      },
    },
  },
});
