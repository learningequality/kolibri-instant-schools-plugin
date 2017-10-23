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
          <mat-svg
            category="social"
            name="person"
            class="person-icon"
          />
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
    padding: 1.5em 1em
    cursor: pointer
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.19), 0 1px 1px rgba(0, 0, 0, 0.23)

  .profile-icon
    display: inline-block
    padding: 0 0.5em

  .profile-name
    display: inline-block
    vertical-align: super

</style>
