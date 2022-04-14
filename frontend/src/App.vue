<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <h2>RoyKesyShop</h2>
      </div>

      <v-spacer></v-spacer>

      <dark-mode-toggle />

      <v-btn text>
        <v-icon>mdi-account</v-icon>
      </v-btn>
      <v-btn text>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn text>
        <v-icon>mdi-cart</v-icon>
        <span>({{ cartItemCount }})</span>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import DarkModeToggle from "./components/style/DarkModeToggle";

export default {
  name: "App",
  components: { DarkModeToggle },
  data() {
    return {};
  },
  computed: {
    cartItemCount: {
      get() {
        if (this.$cookies.get("cartItemCount") == null) return "0";
        else return this.$cookies.get("cartItemCount");
      },
    },
  },
};
</script>
