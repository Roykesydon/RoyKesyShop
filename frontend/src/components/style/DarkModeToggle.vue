<template>
  <span>
    <dark-mode-switch :initial-state="darkMode" @switched="handleDarkMode" />
  </span>
</template>
<script>
import DarkModeSwitch from "vue-dark-mode-switch";
import "vue-dark-mode-switch/dist/vue-dark-mode-switch.css";

export default {
  name: "DarkModeToggle",

  components: { DarkModeSwitch },

  data() {
    return {
      // darkMode: false,
    };
  },
  computed: {
    darkMode: {
      get() {
        return localStorage.getItem("DarkMode") === "true";
      },
      set() {
        if (localStorage.getItem("DarkMode") === "true") {
          localStorage.setItem("DarkMode", false);
          this.$vuetify.theme.dark = false;
        } else {
          localStorage.setItem("DarkMode", true);
          this.$vuetify.theme.dark = true;
        }
      },
    },
  },

  mounted() {
    if (localStorage.getItem("DarkMode") === "true") {
      this.$vuetify.theme.dark = true;
    } else {
      this.$vuetify.theme.dark = false;
    }
  },
  methods: {
    handleDarkMode() {
      this.darkMode = !this.darkMode;
    },
  },
};
</script>
