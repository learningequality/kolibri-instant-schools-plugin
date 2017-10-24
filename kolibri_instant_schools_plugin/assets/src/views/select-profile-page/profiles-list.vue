<template>

  <div>
    <div
      v-for="profile in profiles"
      class="profile-card"
      :class="{ 'profile-card-disabled': disabled }"
      :key="profile.username"
      role="button"
      @click="submitLogin(profile)"
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
      disabled: {
        type: Boolean,
        required: true,
      },
    },
    methods: {
      submitLogin(profile) {
        if (!this.disabled) {
          return this.$emit('selectprofile', profile);
        }
      },
    },
  };

</script>


<style lang="stylus" scoped>

  .profile-card
    padding: 1.5em 1em
    cursor: pointer
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.19), 0 1px 1px rgba(0, 0, 0, 0.23)
    margin-bottom: 1em
    &-disabled
      opacity: 0.5
      cursor: default

  .profile-icon
    display: inline-block
    padding: 0 0.5em

  .profile-name
    display: inline-block
    vertical-align: super

</style>
