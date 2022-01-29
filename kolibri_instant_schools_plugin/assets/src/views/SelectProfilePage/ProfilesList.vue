<template>
  <table class="table">
    <tr v-for="profile in profiles" :key="profile.username">
      <td class="name-wrapper">
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
        <KButton
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

  export default {
    name: 'ProfilesList',
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


<style lang="scss" scoped>

  .name-wrapper {
    width: 100%;
    white-space: nowrap;
    vertical-align: middle;
    padding-bottom: 16px;
  }
  .profile-icon {
    display: inline-block;
    padding: 0 0.5em;
    vertical-align: middle;
  }

  .profile-name {
    display: inline-block;
    max-width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .table {
    width: 100%;
  }

</style>
