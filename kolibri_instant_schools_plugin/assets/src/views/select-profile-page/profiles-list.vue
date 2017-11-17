<template>

  <table class="table">
    <tr v-for="profile in profiles" :key="profile.username">
      <!--
        Adding click on this table cell as a convenience.
        Accessibility is not affected because it's redundant with
        the 'select' button in the next table cell.
      -->
      <td @click="selectProfile(profile)" class="name-wrapper">
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
      </td>
      <td>
        <k-button
          :text="$tr('select')"
          :primary="true"
          :disabled="disabled"
          @click="selectProfile(profile)"
        />
      </td>
    </tr>
  </table>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';

  export default {
    name: 'profilesList',
    components: {
      kButton,
    },
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
      selectProfile(profile) {
        if (!this.disabled) {
          return this.$emit('selectprofile', profile);
        }
      },
    },
    $trs: {
      select: 'Select',
    },
  };

</script>


<style lang="stylus" scoped>

  .name-wrapper
    vertical-align: middle
    white-space: nowrap
    width: 100%

  .profile-icon
    display: inline-block
    vertical-align: middle
    padding: 0 0.5em

  .profile-name
    display: inline-block
    max-width: 150px
    overflow: hidden
    text-overflow: ellipsis

  .table
    width: 100%

</style>
