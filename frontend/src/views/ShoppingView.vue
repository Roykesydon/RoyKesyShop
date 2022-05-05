<template>
  <div style="overflow: hidden">
    <v-row class="mb-0 my-auto">
      <v-col cols="2" class="my-auto">
        <v-card class="ml-5 pa-5" style="height: 80vh" elevation="6">
          <div
            class="font-weight-thin text-h4 pa-3 mb-0 mt-0 pt-0 text--lighten-1 d-flex justify-start"
          >
            Search
          </div>
          <v-text-field
            v-model="searchInput"
            class="pa-3"
            prepend-icon="mdi-magnify"
          ></v-text-field>
          <div class="d-flex">
            <v-btn
              dark
              x-large
              text
              color="secondary"
              @click="filterClothingWithNothing()"
              >Clear</v-btn
            >
            <v-spacer></v-spacer>
            <v-btn
              dark
              x-large
              text
              color="primary"
              @click="filterWithKeyword()"
              >Search</v-btn
            >
          </div>
          <div class="pa-3" style="overflow: auto; height: 55vh">
            <v-divider></v-divider>
            <div v-for="(value, name, index) in existedClasses" :key="index">
              <div class="py-4">
                <v-layout align-center>
                  <span
                    class="font-weight-thin text-h5"
                    style="cursor: pointer; user-select: none"
                    @click="toggleMenu(index)"
                    >{{ name }}</span
                  >
                  <v-spacer></v-spacer>
                  <v-btn
                    icon
                    x-large
                    color="primary"
                    @click="filterClothingWithClass(name)"
                  >
                    <v-icon> mdi-arrow-right </v-icon>
                  </v-btn>
                </v-layout>
              </div>
              <div v-if="classExpandFlag[index]">
                <div
                  v-for="(smallClass, smallIndex) in value"
                  :key="name + smallIndex"
                >
                  <v-btn
                    class="font-weight-thin text-h5 mb-3 ml-3"
                    text
                    @click="filterClothingWithClass(name, smallClass)"
                  >
                    {{ smallClass }}
                  </v-btn>
                </div>
              </div>
              <v-divider></v-divider>
            </div>
          </div>
        </v-card>
      </v-col>

      <v-col cols="10" class="mb-0" style="overflow: auto; height: 90vh">
        <div class="ma-0 pa-5">
          <v-row class="ma-15 mt-5">
            <v-col v-for="(item, i) in items" :key="i" cols="3" class="pa-5">
              <clothing-summary-card :item="item" />
            </v-col>
          </v-row>
        </div>
        <mugen-scroll :handler="fetchData" :should-handle="!isLoading">
          <div class="text-center ma-10">
            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="primary"
            ></v-progress-circular></div
        ></mugen-scroll>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Vue from "vue";
import MugenScroll from "vue-mugen-scroll";
import ClothingSummaryCard from "@/components/infoCard/ClothingSummaryCard.vue";
import { sendNormalRequest } from "@/jsLibrary/request.js";
import { apiAddress } from "@/config.js";

export default {
  name: "ShoppingView",

  components: {
    MugenScroll,
    ClothingSummaryCard,
  },

  data: () => ({
    isLoading: false,
    items: [
      // _ID
      // title
      // cost
      // imageExtension
      // sizes
      // src
    ],
    loadBatchIndex: 0,
    noMoreDataCanGet: false,
    searchInput: "",
    existedClasses: {},
    classExpandFlag: [],
    fetchUrl: "/clothing/",
  }),

  async mounted() {
    await sendNormalRequest(
      this,
      "get",
      "/clothing_class/",
      {},
      {},
      false,
      "",
      "data"
    ).then((data) => {
      this.existedClasses = data;
    });
    this.classExpandFlag = new Array(
      Object.keys(this.existedClasses).length
    ).fill(false);
  },

  methods: {
    fetchData: async function () {
      if (this.noMoreDataCanGet) return;
      this.isLoading = true;
      await sendNormalRequest(
        this,
        "get",
        this.fetchUrl,
        {},
        {
          batch: this.loadBatchIndex++,
        },
        false,
        "",
        "data"
      ).then((data) => {
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

          this.items.push(clothing);
        }
        if (data.length == 0) {
          this.noMoreDataCanGet = true;
        }
      });
      this.loadBatchIndex += 1;
      this.isLoading = false;
    },

    toggleMenu: function (index) {
      Vue.set(this.classExpandFlag, index, !this.classExpandFlag[index]);
      console.log(this.classExpandFlag);
    },

    filterWithKeyword: async function () {
      this.items = [];
      this.noMoreDataCanGet = false;
      this.loadBatchIndex = 0;

      if (this.searchInput != "")
        this.fetchUrl = "/clothing/search/" + this.searchInput;
      else this.fetchUrl = "/clothing/";

      this.isLoading = true;
      await this.fetchData();
      this.isLoading = false;
    },

    filterClothingWithNothing: async function () {
      this.items = [];
      this.noMoreDataCanGet = false;
      this.loadBatchIndex = 0;
      this.fetchUrl = "/clothing/";
      this.isLoading = true;
      await this.fetchData();
      this.isLoading = false;
    },

    filterClothingWithClass: async function (parentClass, subClass = "") {
      this.items = [];
      this.noMoreDataCanGet = false;
      this.loadBatchIndex = 0;

      let api_url = "/clothing_class/" + parentClass;
      if (subClass != "") api_url += "/" + subClass;

      this.fetchUrl = api_url;

      this.isLoading = true;
      await this.fetchData();
      this.isLoading = false;
    },
  },
};
</script>
