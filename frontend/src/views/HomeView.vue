<template>
  <div>
    <div
      class="pa-7"
      style="
        position: absolute;
        top: 25%;
        left: 5%;
        float: left;
        border-width: thin;
        border: solid;
      "
    >
      <div class="font-weight-thin" style="font-size: 4em">
        <div style="font-size: 2em">Expensive</div>
        But
        <span style="font-size: 2em">worth</span>
        the money
      </div>
    </div>
    <div style="overflow: hidden">
      <v-row align="center" justify="end" style="height: 100vh" class="pa-10">
        <v-card
          width="15vw"
          elevation="5"
          class="rounded-0"
          style="z-index: 3; right: 23vw; position: absolute"
        >
          <v-overlay
            :absolute="true"
            :value="true"
            :opacity="opacityWithLightOrNot(0.5, 0.9)"
            :color="colorWithLightOrNot()"
          ></v-overlay>
          <v-img :src="items[4].src" height="35vh" aspect-ratio="0.5"> </v-img>
        </v-card>

        <v-card
          width="15vw"
          elevation="10"
          class="rounded-0"
          style="z-index: 4; right: 20vw; position: absolute"
        >
          <v-overlay
            :absolute="true"
            :value="true"
            :opacity="opacityWithLightOrNot(0.4, 0.7)"
            :color="colorWithLightOrNot()"
          ></v-overlay>
          <v-img :src="items[1].src" height="50vh" aspect-ratio="0.5"> </v-img>
        </v-card>

        <v-card
          width="15vw"
          elevation="20"
          class="rounded-0"
          style="z-index: 10; right: 15vw; position: absolute"
        >
          <v-img :src="items[0].src" height="70vh" aspect-ratio="0.5"> </v-img>
        </v-card>

        <v-card
          width="15vw"
          elevation="10"
          class="rounded-0"
          style="z-index: 4; right: 10vw; position: absolute"
        >
          <v-overlay
            :absolute="true"
            :value="true"
            :opacity="opacityWithLightOrNot(0.4, 0.7)"
            :color="colorWithLightOrNot()"
          ></v-overlay>
          <v-img :src="items[2].src" height="50vh" aspect-ratio="0.5"> </v-img>
        </v-card>

        <v-card
          width="15vw"
          elevation="5"
          class="rounded-0"
          style="z-index: 3; right: 7vw; position: absolute"
        >
          <v-overlay
            :absolute="true"
            :value="true"
            :opacity="opacityWithLightOrNot(0.5, 0.9)"
            :color="colorWithLightOrNot()"
          ></v-overlay>
          <v-img :src="items[3].src" height="35vh" aspect-ratio="0.5"> </v-img>
        </v-card>
      </v-row>
    </div>
  </div>
</template>

<script>
import { apiAddress } from "@/config.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";

export default {
  name: "HomeView",

  data: () => ({
    icons: ["mdi-facebook", "mdi-twitter", "mdi-linkedin", "mdi-instagram"],
    items: [],
  }),

  async created() {
    for (let i = 0; i < 5; i++) this.items.push({ src: "" });
    console.log(this.items);
    await sendNormalRequest(
      this,
      "get",
      "/clothing/",
      {},
      {
        batch: 0,
      },
      false,
      "",
      "data"
    ).then((data) => {
      let index = 0;
      for (let item of data) {
        let clothing = {};

        clothing["_ID"] = item[0];
        clothing["title"] = item[1];
        clothing["cost"] = item[2];
        clothing["cost"] = parseFloat(clothing["cost"]).toFixed(2);
        clothing["imageExtension"] = item[3];
        clothing["sizes"] = item[4];

        clothing["src"] =
          apiAddress +
          "/clothing/image/" +
          String(clothing["_ID"]) +
          "." +
          clothing["imageExtension"];

        if (index < 5) this.$set(this.items, index, clothing);
        else if (index >= 5) this.items.push(clothing);
        index++;
      }
      if (data.length == 0) {
        this.noMoreDataCanGet = true;
      }
    });
  },

  methods: {
    colorWithLightOrNot: function () {
      if (this.$cookies.get("DarkMode")) return "#232323";
      return "#cfcfcf";
    },
    opacityWithLightOrNot: function (lightOpacity, darkOpacity) {
      if (this.$cookies.get("DarkMode")) return darkOpacity;
      return lightOpacity;
    },
  },
};
</script>
