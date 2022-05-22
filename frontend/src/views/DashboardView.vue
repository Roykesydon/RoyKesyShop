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
      <v-divider></v-divider>
      <v-tab>
        <v-icon left> mdi-text-box-multiple-outline </v-icon>
        Update clothing
      </v-tab>
      <v-divider></v-divider>
      <v-tab>
        <v-icon left> mdi-account </v-icon>
        ban user
      </v-tab>

      <!-- Add clothing -->
      <v-tab-item><update-clothing-class /> </v-tab-item>
      <v-tab-item><add-clothing /> </v-tab-item>
      <v-tab-item>
        <manage-orders />
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <p>
              Morbi nec metus. Suspendisse faucibus, nunc et pellentesque
              egestas, lacus ante convallis tellus, vitae iaculis lacus elit id
              tortor. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam
              libero, non adipiscing dolor urna a orci. Curabitur ligula sapien,
              tincidunt non, euismod vitae, posuere imperdiet, leo. Nunc sed
              turpis.
            </p>

            <p>
              Suspendisse feugiat. Suspendisse faucibus, nunc et pellentesque
              egestas, lacus ante convallis tellus, vitae iaculis lacus elit id
              tortor. Proin viverra, ligula sit amet ultrices semper, ligula
              arcu tristique sapien, a accumsan nisi mauris ac eros. In hac
              habitasse platea dictumst. Fusce ac felis sit amet ligula pharetra
              condimentum.
            </p>

            <p>
              Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,
              quis gravida magna mi a libero. Nam commodo suscipit quam. In
              consectetuer turpis ut velit. Sed cursus turpis vitae tortor.
              Aliquam eu nunc.
            </p>

            <p>
              Etiam ut purus mattis mauris sodales aliquam. Ut varius tincidunt
              libero. Aenean viverra rhoncus pede. Duis leo. Fusce fermentum
              odio nec arcu.
            </p>

            <p class="mb-0">
              Donec venenatis vulputate lorem. Aenean viverra rhoncus pede. In
              dui magna, posuere eget, vestibulum et, tempor auctor, justo.
              Fusce commodo aliquam arcu. Suspendisse enim turpis, dictum sed,
              iaculis a, condimentum nec, nisi.
            </p>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <p>Ban users</p>
          </v-card-text>
        </v-card>
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
