<template>
  <v-app>
    <v-app-bar app :class="barColorMode" dark>
      <a>
        <div class="d-flex align-center">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
            transition="scale-transition"
            width="40"
          />

          <span class="font-weight-thin text-h5 white--text">RoyKesyShop</span>
        </div>
      </a>

      <v-spacer></v-spacer>

      <dark-mode-toggle class="mr-2" />

      <v-dialog
        v-if="!isLogin"
        v-model="signInUpInterface"
        persistent
        max-width="30vw"
      >
        <template #activator="{ on, attrs }">
          <v-btn text class="mx-1" v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <sign-in-up-interface
          @closeSignInUpInterface="signInUpInterface = false"
        />
      </v-dialog>
      <v-btn v-if="isLogin" text class="mx-1">
        <v-icon>mdi-account</v-icon>
      </v-btn>
      <v-btn text class="mx-1">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn text class="mx-1">
        <v-icon>mdi-cart</v-icon>
        <span>({{ cartItemCount }})</span>
      </v-btn>
      <v-btn v-if="isLogin" @click="signOut" text class="mx-1">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main :class="backgroundColorMode">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import DarkModeToggle from "@/components/style/DarkModeToggle";
import SignInUpInterface from "@/components/combinedForm/SignInUpInterface.vue";

export default {
  name: "App",
  components: { DarkModeToggle, SignInUpInterface },
  data() {
    return { signInUpInterface: false };
  },
  computed: {
    cartItemCount: {
      get() {
        if (this.$cookies.get("cartItemCount") == null) return "0";
        else return this.$cookies.get("cartItemCount");
      },
    },
    barColorMode: {
      get() {
        if (this.$cookies.get("DarkMode") == true) {
          return "dark-bar";
        } else {
          return "light-bar";
        }
      },
    },
    backgroundColorMode: {
      get() {
        if (this.$cookies.get("DarkMode") == true) {
          return "dark-background";
        } else {
          return "light-background";
        }
      },
    },
    isLogin: {
      get() {
        if (this.$cookies.get("token") == null) return false;
        else return true;
      },
    },
  },
  methods: {
    signOut: function () {
      this.$cookies.remove("token");
      this.$toast.info("Successfully logged out", {
        position: "top-center",
        timeout: 2000,
      });
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles/app-bar/light-bar.css";
@import "@/assets/styles/app-bar/dark-bar.css";

@import "@/assets/styles/background/light-background.css";
@import "@/assets/styles/background/dark-background.css";
</style>
