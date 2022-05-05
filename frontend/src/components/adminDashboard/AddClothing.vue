<template>
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
          :src="previewImage"
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
          <h3 class="font-weight-thin">Title</h3>
          <v-text-field
            v-model="title"
            outlined
            :rules="[rules.required, rules.title]"
            counter="50"
            label="Title"
          ></v-text-field>

          <div class="d-flex">
            <v-select
              v-model="selectParentClass"
              :items="Object.keys(existedClasses)"
              :rules="[rules.required]"
              label="Parent Class"
              class="mr-5"
              outlined
            ></v-select>

            <v-select
              v-model="selectSubClass"
              :items="existedClasses[selectParentClass]"
              :rules="[rules.required]"
              label="Sub Class"
              class="mr-5"
              outlined
            ></v-select>
          </div>

          <h3 class="font-weight-thin">Cost</h3>
          <v-text-field
            v-model="cost"
            outlined
            :rules="[rules.required, rules.cost]"
            counter="10"
            label="Cost"
          ></v-text-field>

          <h3 class="font-weight-thin">Description</h3>
          <v-textarea
            v-model="description"
            :rules="[rules.description]"
            outlined
            counter="500"
          ></v-textarea>

          <v-row>
            <v-col v-for="size in sizes" :key="size" cosl="2"
              ><v-checkbox
                v-model="selectedSize"
                :label="size"
                :value="size"
                :rules="[selectedSize.length > 0]"
              ></v-checkbox
            ></v-col>
          </v-row>

          <h3 class="font-weight-thin">Upload Image</h3>
          <v-file-input
            accept="image/png, image/jpeg"
            placeholder="Pick an avatar"
            prepend-icon="mdi-camera"
            label="Image"
            :rules="[rules.required]"
            @change="uploadPreview"
          ></v-file-input>

          <div class="d-flex justify-end">
            <v-dialog v-model="sumbitCheckInterface" max-width="290">
              <v-card class="pa-5">
                <h3>
                  Are you sure the information of product is correct, and want
                  to add this product?
                </h3>
                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn color="primary" text @click="sendAddClothingRequest()">
                    Submit
                  </v-btn>

                  <v-btn
                    color="grey darken-1"
                    text
                    @click="sumbitCheckInterface = false"
                  >
                    close
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-btn outlined color="primary" @click="wantToSubmit()">
              Submit
            </v-btn>
          </div>
        </v-form>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";

import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "AddClothing",

  components: {
    Loading,
  },

  data: () => ({
    previewImage: "",

    title: "",
    cost: "",
    description: "",
    sizes: ["XS", "S", "M", "L", "XL", "XXL"],
    selectedSize: ["M", "L"],
    selectParentClass: "",
    selectSubClass: "",

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
      "/clothing_class/",
      {},
      {},
      false,
      "",
      "data"
    ).then((data) => {
      this.existedClasses = data;
    });
  },

  methods: {
    uploadPreview: function (file) {
      const reader = new FileReader();
      reader.addEventListener("load", (e) => {
        this.previewImage = e.target.result;
      });
      reader.addEventListener("error", () => {
        this.$toast.error("Uplaod image error", {
          position: "top-center",
          timeout: 2000,
        });
      });
      reader.readAsDataURL(file);
    },

    wantToSubmit: function () {
      if (this.$refs.addClothingForm.validate() == false) return;

      this.sumbitCheckInterface = true;
    },

    sendAddClothingRequest: async function () {
      this.sumbitCheckInterface = false;
      this.isLoading = true;
      await sendNormalRequest(
        this,
        "post",
        "/clothing/",
        {
          title: this.title,
          cost: this.cost,
          description: this.description,
          selectedSize: this.selectedSize,
          image: this.previewImage,
          selectParentClass: this.selectParentClass,
          selectSubClass: this.selectSubClass,
        },
        {},
        true,
        "Successfully add clothing!",
        "success"
      ).catch((error) => {
        console.log(error);
      });
      this.isLoading = false;
    },
  },
};
</script>
