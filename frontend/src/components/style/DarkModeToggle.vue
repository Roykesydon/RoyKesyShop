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
    return {};
  },
  computed: {
    darkMode: {
      get() {
        return this.$cookies.get("DarkMode") == true;
      },
      set() {
        if (this.$cookies.get("DarkMode") == true) {
          this.$cookies.set("DarkMode", false);
          this.$vuetify.theme.dark = false;
        } else {
          this.$cookies.set("DarkMode", true);
          this.$vuetify.theme.dark = true;
        }
      },
    },
  },

  mounted() {
    if (this.$cookies.get("DarkMode") == true) {
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
