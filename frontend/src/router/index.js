import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ShoppingView from "@/views/ShoppingView.vue";
import DashboardView from "@/views/DashboardView.vue";
import ClothingDetailView from "@/views/ClothingDetailView.vue";
import CartView from "@/views/CartView.vue";
import PersonalOrderView from "@/views/PersonalOrderView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/shop",
    name: "shop",
    component: ShoppingView,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
  },
  {
    path: "/clothing/:id",
    name: "clothing_detail",
    component: ClothingDetailView,
  },
  {
    path: "/cart",
    name: "cart",
    component: CartView,
  },
  {
    path: "/personal_order",
    name: "personal_order",
    component: PersonalOrderView,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
