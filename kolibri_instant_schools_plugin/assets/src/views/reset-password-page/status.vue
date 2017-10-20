<template>

  <div>
    Status
    {{ status }}
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
    computed: {},
    methods: {},
    vuex: {
      getters: {},
      actions: {},
    },
  };

</script>


<style lang="stylus" scoped></style>
