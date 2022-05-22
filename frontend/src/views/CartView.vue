<template>
  <div>
    <loading
      :active.sync="isLoading"
      :can-cancel="false"
      :is-full-page="true"
      :color="$vuetify.theme.currentTheme.primary"
      :background-color="$vuetify.theme.currentTheme.customBackground"
    ></loading>
    <v-layout align-center justify-center>
      <v-card class="my-15 pa-0 pb-10" style="width: 75vw">
        <div class="pa-5 text-h4 secondary white--text font-weight-thin">
          Clothing In Cart
        </div>

        <v-row class="mt-2 pa-5 pb-0">
          <v-col
            cols="1"
            class="text-h5 font-weight-thin d-flex align-center justify-end"
          >
            Image
          </v-col>
          <v-col
            cols="3"
            class="pl-7 text-h5 font-weight-thin d-flex align-center"
          >
            Title
          </v-col>

          <v-col
            cols="4"
            class="text-h5 font-weight-thin d-flex align-center justify-end"
          >
            <span
              class="text-h5 font-weight-thin d-flex align-center justify-end pr-10"
            >
              Size
            </span>
          </v-col>

          <v-col cols="1" class="text-h5 font-weight-thin d-flex align-center">
            Count
          </v-col>
          <v-col cols="1" class="text-h5 font-weight-thin d-flex align-center">
            <span>Single Cost</span>
          </v-col>
          <v-col cols="1" class="text-h5 font-weight-thin d-flex align-center">
            <span>Total Cost</span>
          </v-col>
          <v-col cols="1" class="text-h5 font-weight-thin d-flex align-center">
            Delete
          </v-col>
        </v-row>

        <div style="min-height: 10vh">
          <div v-for="(value, key, index) in items" :key="index" class="mx-10">
            <v-divider v-if="index" class="my-5"></v-divider>
            <v-row>
              <v-col cols="1">
                <v-img
                  :src="value.src"
                  height="10vh"
                  aspect-ratio="1.0"
                  class="white"
                ></v-img>
              </v-col>
              <v-col cols="3" class="d-flex align-center">
                <span class="text-h4 text-truncate font-weight-thin">
                  {{ value.title }}
                </span>
              </v-col>
              <v-col cols="4" class="d-flex align-center font-weight-thin">
                <v-spacer></v-spacer>
                <span class="ml-5 text-h4 font-weight-thin px-10"
                  >{{ value.size }}
                </span>
              </v-col>
              <!-- <v-spacer></v-spacer> -->
              <v-col cols="1" class="d-flex align-center pa-5">
                <v-text-field
                  v-model="value.count"
                  single-line
                  :rules="[rules.required, rules.buyCount]"
                  type="number"
                  style="width: 10vw"
                  min="1"
                  max="500"
                  @change="updateCookie()"
                />
              </v-col>
              <v-col cols="1" class="d-flex align-center text-truncate">
                <span>$ {{ value.cost }}</span>
              </v-col>
              <v-col cols="1" class="d-flex align-center text-truncate">
                <span
                  >$ {{ parseFloat(value.cost * value.count).toFixed(2) }}</span
                >
              </v-col>
              <v-col cols="1" class="d-flex align-center justify-center">
                <v-btn icon color="red" @click="removeItem(key)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-card>
    </v-layout>
    <v-layout align-center justify-center>
      <v-card class="my-15 mt-0 pa-0 pb-10" style="width: 75vw">
        <div class="pa-5 text-h4 secondary white--text font-weight-thin">
          Checkout
        </div>
        <div class="pa-10 text-h4 font-weight-thin">
          <v-row>
            <v-col cols="6">
              <v-form ref="receiveForm" v-model="receiveValid" lazy-validation>
                <div class="pa-10">
                  <div class="d-flex">
                    <v-layout align-center>
                      <span> Name : </span>
                      <v-spacer></v-spacer>
                      <span style="width: 15vw">
                        <v-text-field
                          v-model="receiverName"
                          single-line
                          :rules="[rules.required, rules.name]"
                          min="1"
                          max="500"
                        />
                      </span>
                    </v-layout>
                  </div>
                  <div class="d-flex">
                    <v-layout align-center>
                      <span> Address : </span>
                      <v-spacer></v-spacer>
                      <span style="width: 15vw">
                        <v-text-field
                          v-model="address"
                          single-line
                          :rules="[rules.required, rules.address]"
                          min="1"
                          max="500"
                        />
                      </span>
                    </v-layout>
                  </div>
                  <div class="d-flex">
                    <v-layout align-center>
                      <span> phoneNumber : </span>
                      <v-spacer></v-spacer>
                      <span style="width: 15vw">
                        <v-text-field
                          v-model="phoneNumber"
                          single-line
                          :rules="[rules.required, rules.phone]"
                          min="1"
                          max="500"
                        />
                      </span>
                    </v-layout>
                  </div>
                </div>
              </v-form>
            </v-col>

            <v-col cols="6">
              <div class="pa-15">
                <div class="mb-auto">
                  <v-layout align-center>
                    <span>Total Cost: </span>
                    <v-spacer></v-spacer>
                    <div>$ {{ totalCost }}</div>
                  </v-layout>
                </div>
                <div class="d-flex justify-end">
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    x-large
                    outlined
                    style="position: absolute; bottom: 12vh"
                    :disabled="isZeroItem"
                    @click="requestOrder()"
                  >
                    Submit
                  </v-btn>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-card>
    </v-layout>
  </div>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";
import { apiAddress } from "@/config.js";

import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "CartView",

  components: { Loading },

  data: () => ({
    isLoading: false,

    items: {
      // name: {
      // _id
      // title
      // cost
      // imageExtension
      // size
      // src
      // count
      // }
    },
    rules: rules,

    address: "",
    receiverName: "",
    phoneNumber: "",

    receiveValid: false,
  }),

  computed: {
    totalCost: {
      get() {
        let sum = 0;
        for (let key of Object.keys(this.items))
          sum += this.items[key].cost * this.items[key].count;

        return parseFloat(sum).toFixed(2);
      },
    },
    isZeroItem: {
      get() {
        if (Object.keys(this.items).length == 0) return true;
        else return false;
      },
    },
  },

  async mounted() {
    if (
      this.$cookies.isKey("cartItems") != false &&
      this.$cookies.get("cartItems") != ""
    ) {
      let clothing = this.$cookies.get("cartItems").split(",");
      let items = {};
      console.log(clothing);
      for (let item of clothing) {
        console.log(item.split("-")[2]);
        let clothingAndSize = item.split("-")[0] + "-" + item.split("-")[1];

        let _id = item.split("-")[0];
        let size = item.split("-")[1];
        let title = "";
        let cost = parseFloat(0).toFixed(2);
        let imageExtension = "";
        let src = "";

        await sendNormalRequest(
          this,
          "get",
          "/clothing/" + _id,
          {},
          {},
          false,
          "",
          "data"
        ).then((data) => {
          title = data[1];

          cost = data[2];
          cost = parseFloat(cost).toFixed(2);

          imageExtension = data[3];

          src =
            apiAddress +
            "/clothing/image/" +
            String(_id) +
            "." +
            imageExtension;
        });

        items[clothingAndSize] = {
          _id: _id,
          size: size,
          title: title,
          cost: cost,
          imageExtension: imageExtension,
          src: src,
          count: item.split("-")[2],
        };
      }
      this.items = items;
    }
  },

  methods: {
    requestOrder: async function () {
      if (this.$refs.receiveForm.validate() == false) return;

      this.isLoading = true;
      await sendNormalRequest(
        this,
        "post",
        "/order/",
        {
          name: this.receiverName,
          address: this.address,
          phoneNumber: this.phoneNumber,
          clothing: this.$cookies.get("cartItems"),
        },
        {},
        true,
        "Successfully add order!",
        "success"
      )
        .then(() => {
          this.items = [];
          this.$cookies.remove("cartItems");
        })
        .catch((error) => {
          console.log(error);
        });
      this.isLoading = false;
    },

    removeItem: function (keyName) {
      this.$delete(this.items, keyName);
      this.updateCookie();
    },

    updateCookie: function () {
      let newCookie = "";

      for (let clothingAndSize in this.items) {
        let item = clothingAndSize + "-" + this.items[clothingAndSize].count;

        if (newCookie == null || newCookie == "") newCookie = item;
        else newCookie += "," + item;
      }
      this.$cookies.set("cartItems", newCookie);
    },
  },
};
</script>
