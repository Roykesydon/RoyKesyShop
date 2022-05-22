<template>
  <v-layout justify-center class="mt-10">
    <div style="width: 60vw">
      <v-card flat class="pa-10" style="height: 70vh">
        <v-row>
          <loading
            :active.sync="isLoading"
            :can-cancel="false"
            :is-full-page="false"
            :color="$vuetify.theme.currentTheme.primary"
            :background-color="$vuetify.theme.currentTheme.customBackground"
          ></loading>
          <v-col cols="6" class="pr-5">
            <v-img
              id="output"
              contain
              :src="imageSrc"
              height="60vh"
              class="grey darken-3"
            >
            </v-img>
          </v-col>
          <v-divider vertical></v-divider>

          <v-col cols="6" class="pl-5" style="overflow: auto; height: 60vh">
            <v-form
              ref="addClothingForm"
              v-model="addClothingValid"
              lazy-validation
            >
              <div class="font-weight-thin text-h3 mt-15">
                {{ title }}
              </div>
              <div class="my-1 secondary--text mb-10">
                <span>{{ parentClass }}</span>
                <span> / </span>
                <span>{{ subClass }}</span>
              </div>

              <v-row class="pa-5">
                <v-layout align-center justify-start>
                  <div>
                    <span class="font-weight-thin text-h5">Cost: </span>
                  </div>
                </v-layout>
                <v-layout align-center justify-start>
                  <div cols="10">
                    <span class="font-weight-thin text-h4">{{ cost }}</span>
                  </div>
                </v-layout>
              </v-row>

              <v-row class="pa-5">
                <v-layout align-center justify-start>
                  <div>
                    <span class="font-weight-thin text-h5">Sizes: </span>
                  </div>
                </v-layout>
                <v-layout align-center justify-start>
                  <div cols="10" class="d-flex">
                    <span v-for="size in sizes" :key="size" class="mx-3"
                      ><v-checkbox
                        v-model="supportSizes"
                        :label="size"
                        :value="size"
                        :rules="[supportSizes.length > 0]"
                        disabled="disabled"
                      ></v-checkbox
                    ></span>
                  </div>
                </v-layout>
              </v-row>

              <v-form ref="buyForm" v-model="buyFormValue" lazy-validation>
                <v-row class="pa-5">
                  <v-layout align-center justify-start>
                    <div>
                      <span class="font-weight-thin text-h5">Select: </span>
                    </div>
                  </v-layout>
                  <v-layout align-center justify-start>
                    <div cols="10">
                      <v-select
                        v-model="selectSize"
                        :items="supportSizes"
                        :rules="[rules.required]"
                        :hide-details="true"
                        label="Select Size"
                        style="width: 10vw"
                      ></v-select>
                    </div>
                  </v-layout>
                </v-row>

                <v-row class="pa-5">
                  <v-layout align-center justify-start>
                    <div>
                      <span class="font-weight-thin text-h5">Number: </span>
                    </div>
                  </v-layout>
                  <v-layout align-center justify-start>
                    <div cols="10">
                      <v-text-field
                        v-model="buyCount"
                        single-line
                        :rules="[rules.required, rules.buyCount]"
                        type="number"
                        style="width: 10vw"
                        min="0"
                        max="500"
                      />
                    </div>
                  </v-layout>
                </v-row>
              </v-form>

              <div class="d-flex justify-end pa-5 mt-15">
                <v-btn
                  outlined
                  color="secondary"
                  class="mr-5"
                  @click="
                    () => {
                      addToCart();
                      $router.push({ path: '/cart' });
                    }
                  "
                >
                  Buy now
                </v-btn>
                <v-btn outlined color="primary" @click="addToCart()">
                  Add to Cart
                </v-btn>
              </div>
            </v-form>
          </v-col>
        </v-row>
      </v-card>
      <v-card flat class="my-10 pa-10"
        ><h1 class="font-weight-thin mb-5">Description</h1>
        <div
          style="min-height: 5vh; white-space: pre"
          class="font-weight-thin text-h5"
        >
          {{ description }}
        </div>
      </v-card>
    </div>
  </v-layout>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";
import { apiAddress } from "@/config.js";

import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "ClothingDetailCard",

  components: {
    Loading,
  },
  props: { clothingId: { type: String, required: true, default: -1 } },

  data: () => ({
    previewImage: "",

    title: "Title",
    cost: "0.00",
    description: "",
    sizes: ["XS", "S", "M", "L", "XL", "XXL"],
    supportSizes: ["M", "L"],
    imageExtension: "",
    parentClass: "Parent Class",
    subClass: "Sub Class",
    imageSrc: "",

    buyCount: 0,
    selectSize: null,

    buyFormValue: false,

    rules: rules,
    sumbitCheckInterface: false,
    addClothingValid: false,

    isLoading: false,
    existedClasses: {},
  }),

  async mounted() {
    await sendNormalRequest(
      this,
      "get",
      "/clothing/" + this.clothingId,
      {},
      {},
      false,
      "",
      "data"
    ).then((data) => {
      console.log(data);
      this.title = data[1];

      this.cost = data[2];
      this.cost = parseFloat(this.cost).toFixed(2);

      this.imageExtension = data[3];
      this.supportSizes = data[4].split(",");
      this.parentClass = data[5];
      this.subClass = data[6];
      this.description = data[7];

      console.log(this.description);

      this.imageSrc =
        apiAddress +
        "/clothing/image/" +
        String(this.clothingId) +
        "." +
        this.imageExtension;
    });
  },

  methods: {
    addToCart: function () {
      if (this.$refs.buyForm.validate() == false) return;

      let item =
        String(this.clothingId) + "-" + this.selectSize + "-" + this.buyCount;

      if (
        this.$cookies.isKey("cartItems") == false ||
        this.$cookies.get("cartItems") == ""
      )
        this.$cookies.set("cartItems", item);
      else {
        let oldCart = this.$cookies.get("cartItems").split(",");
        let newCookie = item;
        for (let oldItem of oldCart)
          if (!oldItem.includes(this.clothingId + "-" + this.selectSize))
            newCookie += "," + oldItem;

        this.$cookies.set("cartItems", newCookie);
      }

      this.$toast.success("Successfully adding to cart!", {
        position: "top-center",
        timeout: 2000,
      });
    },
  },
};
</script>
