<template>

  <div :style="fieldWidth" class="content">
    <ui-alert type="success" @dismiss="resetProfileState" v-if="success">
      {{$tr('success')}}
    </ui-alert>
    <form @submit.prevent="submitEdits">

      <ui-textbox
        v-if="hasPrivilege('username')"
        class="input-field"
        :invalid="error"
        :error="errorMessage"
        :label="$tr('username')"
        :disabled="busy"
        v-model="username"
        autocomplete="username"
        id="username"
        type="text" />

      <ui-textbox
        v-if="hasPrivilege('name')"
        class="input-field"
        :disabled="busy"
        :label="$tr('name')"
        v-model="full_name"
        autocomplete="name"
        id="name"
        type="text" />

      <icon-button
        :style="submitWidth"
        :disabled="busy"
        :primary="true"
        :text="$tr('updateProfile')"
        id="submit"
        type="submit" />
    </form>
  </div>

</template>


<script>

  const actions = require('../../actions');
  const responsiveWindow = require('kolibri.coreVue.mixins.responsiveWindow');

  module.exports = {
    name: 'profile-page',
    $trNameSpace: 'profile-page',
    $trs: {
      genericError: 'Something went wrong',
      success: 'Profile details updated!',
      username: 'Username',
      name: 'Name',
      updateProfile: 'Update Profile',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-textbox': require('keen-ui/src/UiTextbox'),
      'ui-alert': require('keen-ui/src/UiAlert'),
    },
    data() {
      return {
        username: this.session.username,
        full_name: this.session.full_name,
      };
    },
    computed: {
      errorMessage() {
        if (this.error) {
          if (this.backendErrorMessage) {
            return this.backendErrorMessage;
          }
          return this.$tr('genericError');
        }
        return '';
      },
      submitWidth() {
        const width = this.widthMultiplier.submit * this.windowSize.width;
        const fieldWidth = this.widthMultiplier.field * this.windowSize.width;
        const margins = (fieldWidth - width) / 2;
        return {
          width: `${width}px`,
          margin: `0 ${margins}px 0 ${margins}px`,
        };
      },
      fieldWidth() {
        return {
          width: `${this.widthMultiplier.field * this.windowSize.width}px`,
        };
      },
      widthMultiplier() {
        const wideMult = () => {
          const field = 0.33;
          const submit = field * 0.95;
          return {
            field,
            submit,
          };
        };
        const mobileMult = () => ({
          field: 0.85,
          submit: 0.85,
        });

        if (this.windowSize.breakpoint <= 2) {
          return mobileMult();
        }
        return wideMult();
      },
    },
    methods: {
      hasPrivilege(privilege) {
        return this.privileges[privilege];
      },
      submitEdits() {
        const edits = {
          username: this.username,
          full_name: this.full_name,
          password: this.password,
        };
        this.editProfile(edits, this.session);
      },
    },
    vuex: {
      getters: {
        privileges: state => state.core.learnerPrivileges,
        session: state => state.core.session,
        error: state => state.pageState.error,
        success: state => state.pageState.success,
        busy: state => state.pageState.busy,
        backendErrorMessage: state => state.pageState.errorMessage,
      },
      actions: {
        editProfile: actions.editProfile,
        resetProfileState: actions.resetProfileState,
      },
    },
    mixins: [responsiveWindow],
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  // taken from docs, assumes 1rem = 16px
  $ui-input-height = 68px
  $vertical-page-margin = 100px

  .content
    margin-top: $vertical-page-margin
    margin-left: auto
    margin-right: auto

  #submit
    display: block
    position: absolute
    bottom: $vertical-page-margin

  .advanced-option
    color: $core-action-light
    width: 100%
    display: inline-block
    font-size: 0.9em

</style>
