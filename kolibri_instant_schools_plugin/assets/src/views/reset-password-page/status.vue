<template>

  <div>
    <h1>{{ header }}</h1>
    <p>{{ explanation }}</h1>
  </div>

</template>


<script>

  export default {
    components: {},
    props: {
      status: {
        type: String,
        required: true,
      },
    },
    computed: {
      header() {},
    },
    methods: {},
    vuex: {
      getters: {},
      actions: {},
    },
  };

</script>


<style lang="stylus" scoped></style>
