<template>
  <clothing-detail-card :clothing-id="$route.params.id" />
</template>

<script>
import ClothingDetailCard from "@/components/infoCard/ClothingDetailCard.vue";

export default {
  name: "ClothingDetailView",

  components: {
    ClothingDetailCard,
  },

  data: () => ({}),

  async mounted() {},

  methods: {},
};
</script>
