<template>
  <v-card
    class="ma-10 mx-auto my-0"
    elevation="0"
    height="40vh"
    max-width="25vh"
    color="transparent"
  >
    <v-hover v-slot="{ hover }">
      <v-img
        :src="item.src"
        aspect-ratio="2.0"
        class="my-auto align-center"
        height="30vh"
      >
        <v-overlay :absolute="true" :value="hover" opacity="0.8">
          <v-layout justify-center stlye="" class="pa-5">
            <v-icon
              :class="{ 'show-btns': hover }"
              :color="transparent"
              @click="$router.push({ path: '/clothing/' + item['_ID'] })"
            >
              mdi-magnify
            </v-icon>
            <v-icon class="ml-5" @click="addToCart(item['_ID'])">
              mdi-cart
            </v-icon>
          </v-layout>
        </v-overlay>
      </v-img>
    </v-hover>
    <span>
      <div
        class="text-h7 ma-3 mt-4 mb-0 pb-0 text-truncate d-flex justify-center"
      >
        {{ item.title }}
      </div>
      <div
        class="text-h7 ma-3 mb-0 mt-0 pt-0 text--lighten-1 secondary--text d-flex justify-center"
      >
        $ {{ item.cost }}
      </div>
    </span>
  </v-card>
</template>

<script>
export default {
  name: "ClothingDetailCard",

  props: {
    item: {
      type: Object,
      default: function () {
        let item = {
          _ID: "",
          title: "",
          cost: "",
          imageExtension: "",
          sizes: "",
          stc: "",
        };

        return item;
      },
    },
  },

  data() {
    return { transparent: "rgba(255, 255, 255, 0)" };
  },

  mounted() {},
  methods: {
    addToCart: function (_ID) {
      // console.log(JSON.parse(this.$cookies.get("cartItems")));
      if (this.$cookies.isKey("cartItems") == false)
        this.$cookies.set("cartItems", String(_ID));
      else {
        this.$cookies.set(
          "cartItems",
          this.$cookies.get("cartItems") + "," + String(_ID)
        );
      }
    },
  },
};
</script>

<style scoped>
.lower-opacity {
  opacity: 0.6;
  background-color: black;
}

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>
