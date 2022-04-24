<template>
  <div>
    <div
      class="pa-7"
      style="
        position: absolute;
        top: 25%;
        left: 5%;
        float: left;
        border-width: thin;
        border: solid;
      "
    >
      <div class="font-weight-thin" style="font-size: 4em">
        <div style="font-size: 2em">Expensive</div>
        But
        <span style="font-size: 2em">worth</span>
        the money
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",

  data: () => ({
    items: [
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
      },
    ],
  }),

  mounted() {},
};
</script>
