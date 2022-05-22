<template>
  <v-card class="pa-10 ma-15" height="70vh">
    <!-- Add clothing -->
    <v-row>
      <loading
        :active.sync="isLoading"
        :can-cancel="false"
        :is-full-page="false"
        :color="$vuetify.theme.currentTheme.primary"
        :background-color="$vuetify.theme.currentTheme.customBackground"
      ></loading>
      <v-col cols="6" class="pr-5">
        <v-card height="100%" class="grey darken-3 pa-5">
          <v-card flat style="overflow: auto; height: 50vh" class="pa-5">
            <div class="text-h4 font-weight-thin mb-4">Order List</div>
            <v-divider class="mb-5"></v-divider>
            <div v-for="(item, i) in items" :key="i">
              <div
                v-show="
                  !(
                    (item.status != 'done' &&
                      item.isDeleted != 1 &&
                      inProgress != true) ||
                    (item.isDeleted == 1 && deleted != true) ||
                    (item.status == 'done' &&
                      item.isDeleted != 1 &&
                      done != true)
                  )
                "
              >
                <v-layout justify-space-between>
                  <div class="text-h5 font-weight-thin" style="width: 10vw">
                    {{ item.order_id }}
                  </div>
                  <div class="text-h5 font-weight-thin" style="width: 10vw">
                    {{ item.status }}
                  </div>
                  <div style="width: 15vw" class="white--text">
                    <v-layout justify-space-between align-center>
                      <div
                        v-if="item.status != 'done' && item.isDeleted != 1"
                        class="info text-center"
                        style="width: 7vw; height: 1.5em; border-radius: 0.25em"
                      >
                        Processing
                      </div>
                      <div
                        v-if="item.status == 'done' && item.isDeleted != 1"
                        class="success text-center"
                        style="width: 7vw; height: 1.5em; border-radius: 0.25em"
                      >
                        Complete
                      </div>
                      <div
                        v-if="item.isDeleted == 1"
                        class="error text-center"
                        style="width: 7vw; height: 1.5em; border-radius: 0.25em"
                      >
                        Deleted
                      </div>
                      <v-btn color="secondary" text @click="openDetail(i)">
                        Detail
                      </v-btn>
                    </v-layout>
                  </div>
                </v-layout>
                <div>
                  <v-divider class="my-3"></v-divider>
                </div>
              </div>
            </div>
          </v-card>
        </v-card>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col cols="6" class="pl-5" style="overflow: auto; height: 60vh">
        <v-card width="50vw" height="70vh" class="pa-10" elevation="0">
          <loading
            :active.sync="detailLoading"
            :can-cancel="false"
            :is-full-page="false"
            :color="$vuetify.theme.currentTheme.primary"
            :background-color="$vuetify.theme.currentTheme.customBackground"
          ></loading>
          <v-layout align-center>
            <span class="text-h3 font-weight-thin mr-5">
              Order {{ detail.order_id }}
            </span>
            <span v-if="Object.keys(detail).length != 0" class="white--text">
              <v-chip
                v-if="detail.status != 'done' && detail.isDeleted != 1"
                class="info"
              >
                Processing
              </v-chip>
              <v-chip
                v-if="detail.status == 'done' && detail.isDeleted != 1"
                class="success"
              >
                Complete
              </v-chip>
              <v-chip v-if="detail.isDeleted == 1" class="error">
                Deleted
              </v-chip>
            </span>
          </v-layout>
          <v-divider class="my-5"></v-divider>
          <div v-if="Object.keys(detail).length != 0">
            <v-row align="center">
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Status</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  :
                  <span class="primary--text text-h4">{{
                    statusMapping(detail.status)
                  }}</span>
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Address</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  :
                  {{ detail.address }}
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Name</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  :
                  {{ detail.name }}
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Phone</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  :
                  {{ detail.phone }}
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Cost</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  : $&nbsp;{{ detail.cost }}
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Status</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">
                  :
                  {{ detail.status }}
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="text-h5 font-weight-thin">Clothing</div>
              </v-col>
              <v-col cols="9">
                <div class="text-h5 font-weight-thin">:</div>
                <div class="pa-5">
                  <div v-for="(item, index) in detail.clothing" :key="index">
                    <v-row align="center" justify="center">
                      <v-col cols="2">
                        <v-layout align-center>
                          <v-img
                            :src="item.imageSrc"
                            height="10vh"
                            width="10vh"
                          ></v-img>
                        </v-layout>
                      </v-col>
                      <v-col cols="10">
                        <div class="text-h5 font-weight-thin">
                          {{ item.parentClass }}/{{ item.subClass }}/{{
                            item.title
                          }}
                        </div>
                        <div class="text-h5 font-weight-thin">
                          $ &nbsp;
                          {{ item.cost }}
                        </div>
                        <div class="text-h5 font-weight-thin">
                          Size: {{ item.size }}
                        </div>
                        <div class="text-h5 font-weight-thin">
                          Count: {{ item.count }}
                        </div>
                      </v-col>
                    </v-row>
                    <v-divider class="my-2"></v-divider>
                  </div>
                </div>
              </v-col>
            </v-row>
            <v-row v-if="needNextStepButton()" justify="end">
              <v-btn
                outlined
                elevation="0"
                x-large
                color="secondary"
                @click="updateOrder()"
              >
                {{ statusButtonMessage(detail.status) }}
              </v-btn>
            </v-row>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";
import { apiAddress } from "@/config.js";
import { statusMapping } from "@/jsLibrary/textTransform.js";

import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "PersonalOrderView",

  components: {
    Loading,
  },

  data: () => ({
    previewImage: "",

    email: "",
    recentCount: 150,

    inProgress: true,
    done: true,
    deleted: true,

    items: [],

    rules: rules,

    orderFormValid: false,
    isLoading: false,
    detailLoading: false,

    detail: {},
  }),

  async mounted() {
    this.isLoading = true;
    await this.getListWithEmail();
    this.isLoading = false;
  },

  methods: {
    updateOrder: async function () {
      await sendNormalRequest(
        this,
        "put",
        "/order/status",
        {
          order_id: this.detail.order_id,
        },
        {},
        true,
        "Successfully update order status",
        "data"
      ).then((data) => {
        this.detail.status = data.new_status;
        this.items[this.detail.index].status = data.new_status;
      });
    },

    statusButtonMessage: function (status) {
      let returnMsg = "can't decode status";
      if (status == "delivering") {
        returnMsg = "Package received";
      }
      return returnMsg;
    },

    needNextStepButton: function () {
      if (this.detail.isDeleted) return false;
      let items = ["wait pay"];
      for (let item of items) {
        if (this.detail.status == item) return true;
      }
      return false;
    },

    statusMapping: function (input) {
      return statusMapping(input);
    },

    openDetail: async function (index) {
      this.detail = Object.assign({}, this.items[index]);
      this.detail.clothing = this.detail.clothing.split(",");
      this.detail.index = index;
      for (let i = 0; i < this.detail.clothing.length; i++) {
        let result = this.detail.clothing[i].split("-");
        let clothingId = result[0];
        let size = result[1];
        let count = result[2];
        await sendNormalRequest(
          this,
          "get",
          "/clothing/" + clothingId,
          {},
          {},
          false,
          "",
          "data"
        ).then((data) => {
          this.detail.clothing[i] = {};

          this.detail.clothing[i].title = data[1];

          this.detail.clothing[i].cost = data[2];
          this.detail.clothing[i].cost = parseFloat(
            this.detail.clothing[i].cost
          ).toFixed(2);

          this.detail.clothing[i].clothingId = clothingId;
          this.detail.clothing[i].imageExtension = data[3];
          this.detail.clothing[i].supportSizes = data[4].split(",");
          this.detail.clothing[i].parentClass = data[5];
          this.detail.clothing[i].subClass = data[6];
          this.detail.clothing[i].description = data[7];

          this.detail.clothing[i].imageSrc =
            apiAddress +
            "/clothing/image/" +
            String(this.detail.clothing[i].clothingId) +
            "." +
            this.detail.clothing[i].imageExtension;

          this.detail.clothing[i].size = size;
          this.detail.clothing[i].count = count;
        });
        this.detail = Object.assign({}, this.detail);
      }
      this.detailLoading = false;
    },

    getListWithEmail: async function () {
      await sendNormalRequest(
        this,
        "post",
        "/order/with_email",
        {
          recentCount: 1000,
        },
        {},
        true,
        "",
        "data"
      )
        .then((result) => {
          this.items = result;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
