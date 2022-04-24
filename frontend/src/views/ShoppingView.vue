<template>
  <div>
    <v-row class="mb-0">
      <v-col cols="3"> </v-col>
      <v-divider vertical></v-divider>
      <v-col cols="9" class="mb-0">
        <div class="ma-0 pa-5">
          <v-row class="ma-15">
            <v-col v-for="(item, i) in items" :key="i" cols="3" class="pa-5"
              ><div>
                <v-card
                  class="ma-10 mx-auto my-0"
                  elevation="20"
                  height="40vh"
                  max-width="25vh"
                >
                  <v-img
                    :src="item.src[0]"
                    aspect-ratio="2.0"
                    class="my-auto"
                    height="30vh"
                  ></v-img>
                  <v-row>
                    <v-col cols="7">
                      <span>
                        <div class="text-h6 ma-3 mb-0 text-truncate">
                          {{ item.title }}
                        </div>
                        <div
                          class="text-h7 ma-3 mt-0 grey--text text--lighten-1"
                        >
                          {{ item.cost }} 元/月
                        </div>
                      </span>
                    </v-col>
                    <v-col cols="5" class="my-auto mx-auto text-right">
                      <v-btn class="ma-2 pr-5 mr-5" outlined color="secondary">
                        查看詳情
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card>
              </div></v-col
            >
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "ShoppingView",

  data: () => ({
    items: [
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
      {
        title: "test",
        cost: "12345",
        src: ["https://picsum.photos/510/300?random"],
      },
    ],
  }),

  mounted() {},
};
</script>
