<template>

  <div>
    <template v-for="profile in profiles">
      <div
        class="profile-card"
        :key="profile.username"
        role="button"
        @click="selectProfile(profile)"
      >
        <div class="profile-icon">
          Icon
        </div>
        <div class="profile-name">
          {{ profile.full_name }}
        </div>
      </div>
    </template>
  </div>

</template>


<script>

  export default {
    name: 'profilesList',
    props: {
      profiles: {
        type: Array,
        required: true,
      },
    },
    methods: {
      selectProfile(profile) {
        return this.$emit('selectprofile', profile);
      },
    },
  };

</script>


<style lang="stylus" scoped>

  .profile-card
    padding: 0.5em
    cursor: pointer
    // copied from kolibri card carousel
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23)

</style>
