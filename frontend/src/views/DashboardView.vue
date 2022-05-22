<template>
  <v-card class="ma-15" height="70vh">
    <v-toolbar flat color="primaryDark" dark>
      <v-toolbar-title>Admin Dashboard</v-toolbar-title>
    </v-toolbar>
    <v-tabs vertical class="mt-10" color="secondary">
      <v-tab>
        <v-icon left> mdi-table </v-icon>
        Add clothing class
      </v-tab>
      <v-divider></v-divider>
      <v-tab>
        <v-icon left> mdi-tshirt-crew </v-icon>
        Add clothing
      </v-tab>
      <v-divider></v-divider>
      <v-tab>
        <v-icon left> mdi-truck-minus-outline </v-icon>
        Manage orders
      </v-tab>
      <v-tab-item><update-clothing-class /> </v-tab-item>
      <v-tab-item><add-clothing /> </v-tab-item>
      <v-tab-item>
        <manage-orders />
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import AddClothing from "@/components/adminDashboard/AddClothing.vue";
import UpdateClothingClass from "@/components/adminDashboard/UpdateClothingClass.vue";
import ManageOrders from "@/components/adminDashboard/ManageOrders.vue";

export default {
  name: "DashboardView",
  components: {
    AddClothing,
    UpdateClothingClass,
    ManageOrders,
  },

  data: () => ({ previewImage: false }),

  mounted() {},

  methods: {
    uploadPreview: function (files) {
      files.forEach((file, index) => {
        const reader = new FileReader();
        reader.addEventListener("load", (e) => {
          this.previewImage = e.target.result;
        });
        reader.addEventListener("error", () => {
          console.log("read image error", index);
        });
        reader.readAsDataURL(file);
      });
    },
  },
};
</script>
