<template>
  <v-layout justify-center>
    <v-card flat class="pa-10" style="height: 70vh; width: 50vw">
      <loading
        :active.sync="isLoading"
        :can-cancel="false"
        :is-full-page="false"
        :color="$vuetify.theme.currentTheme.primary"
        :background-color="$vuetify.theme.currentTheme.customBackground"
      ></loading>

      <v-dialog v-model="sumbitCheckInterface" max-width="290">
        <v-card class="pa-5">
          <h3>
            Are you sure the information of clothing class is correct, and want
            to add this class?
          </h3>
          <v-layout justify-center>
            <h2 class="ma-3 mx-auto primary--text">
              {{ submitParentClass }} - {{ submitSubClass }}
            </h2>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="primary" text @click="addClothingClass()">
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

      <div class="font-weight-thin text-h4 mb-3">Add Clothing Class</div>
      <v-form
        ref="addClothingClassWithNewParentForm"
        v-model="addClothingClassWithNewParent"
        lazy-validation
      >
        <h3 class="font-weight-thin mb-2">With New Parent Class</h3>
        <div class="d-flex">
          <v-text-field
            v-model="newParentClass"
            :rules="[rules.required, rules.parentClass]"
            class="mr-5"
            outlined
          ></v-text-field>
          <v-text-field
            v-model="newSubClass"
            :rules="[rules.required, rules.subClass]"
            class="mr-2"
            outlined
          ></v-text-field>
          <v-btn
            dark
            x-large
            text
            color="secondary"
            @click="wantToSubmit(newParentClass, newSubClass)"
            >Add</v-btn
          >
        </div>
      </v-form>
      <v-form
        ref="addClothingClassWithExistedParentForm"
        v-model="addClothingClassWithExistedParent"
        lazy-validation
      >
        <h3 class="font-weight-thin mb-2">With Existed Parent Class</h3>
        <div class="d-flex">
          <v-select
            v-model="selectParentClass"
            :items="Object.keys(existedClasses)"
            :rules="[rules.required]"
            label="Parent Class"
            class="mr-5"
            outlined
          ></v-select>
          <v-text-field
            v-model="newSubClass"
            :rules="[rules.required, rules.subClass]"
            class="mr-2"
            outlined
          ></v-text-field>
          <v-btn
            dark
            x-large
            text
            color="secondary"
            @click="wantToSubmit(selectParentClass, newSubClass, false)"
            >Add</v-btn
          >
        </div>
      </v-form>
    </v-card>
  </v-layout>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { sendNormalRequest } from "@/jsLibrary/request.js";

import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "UpdateClothingClass",

  components: {
    Loading,
  },

  data: () => ({
    rules: rules,
    sumbitCheckInterface: false,
    addClothingClassValid: false,
    isLoading: false,

    submitParentClass: "",
    submitSubClass: "",

    addClothingClassWithNewParent: "",
    addClothingClassWithExistedParent: "",

    newParentClass: "",
    newSubClass: "",
    selectParentClass: "",

    existedClasses: {},
    // existedClasses: {
    //   Tops: ["T-Shirts", "Shirts", "Sweat", "Parka", "Others"],
    //   Jacket: ["Coat", "Nylon", "Others"],
    //   Pants: ["Denim", "Short Pants", "Others"],
    //   Bag: ["Lunch Bag", "Backpack", "Others"],
    // },
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

    wantToSubmit: function (parentClass, subClass, withNewParent = true) {
      if (
        withNewParent &&
        this.$refs.addClothingClassWithNewParentForm.validate() == false
      )
        return;
      if (
        !withNewParent &&
        this.$refs.addClothingClassWithExistedParentForm.validate() == false
      )
        return;
      this.submitParentClass = parentClass;
      this.submitSubClass = subClass;
      this.sumbitCheckInterface = true;
    },

    addClothingClass: async function () {
      this.sumbitCheckInterface = false;
      this.isLoading = true;

      await sendNormalRequest(
        this,
        "post",
        "/clothing_class/",
        {
          parentClass: this.submitParentClass,
          subClass: this.submitSubClass,
        },
        {},
        true,
        "Successfully add clothing class!",
        ""
      )
        .then(async () => {
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
        })
        .catch((error) => {
          console.log(error);
        });

      this.isLoading = false;
    },
  },
};
</script>
