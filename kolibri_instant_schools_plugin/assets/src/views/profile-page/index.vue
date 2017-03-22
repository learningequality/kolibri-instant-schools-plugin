<template>

  <div class="content">
    <ui-alert type="success" @dismiss="resetProfileState" v-if="success">
      {{$tr('success')}}
    </ui-alert>
    <form @submit.prevent="submitEdits">

      <core-textbox
        class="input-field"
        :disabled="true"
        :label="$tr('name')"
        :value="fullName"
        type="text" />
      <core-textbox
        class="input-field"
        :disabled="busy"
        :label="$tr('newPassword')"
        :placeholder="$tr('enterNewPassword')"
        v-model="newPassword"
        type="password" />
      <core-textbox
        class="input-field"
        :disabled="busy"
        :label="$tr('confirmNewPassword')"
        :invalid="!passwordsMatch"
        :error="$tr('passwordsDoNotMatch')"
        :placeholder="$tr('reenterNewPassword')"
        @blur="passwordConfirmVisited = true"
        v-model="newPasswordConfirm"
        type="password" />

      <icon-button
        :disabled="busy"
        :primary="true"
        :text="$tr('updateProfile')"
        id="submit"
        type="submit" />
    </form>
  </div>

</template>


<script>

  const actions = require('../../state/actions');
  const responsiveWindow = require('kolibri.coreVue.mixins.responsiveWindow');

  module.exports = {
    name: 'profile-page',
    $trNameSpace: 'profile-page',
    $trs: {
      genericError: 'Something went wrong',
      success: 'Profile details updated!',
      name: 'Name',
      updateProfile: 'Update profile',
      newPassword: 'New password',
      enterNewPassword: 'Enter new password',
      confirmNewPassword: 'Confirm new password',
      reenterNewPassword: 'Re-enter new password',
      passwordsDoNotMatch: 'Password entered does not match new password',

    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'core-textbox': require('kolibri.coreVue.components.textbox'),
      'ui-alert': require('keen-ui/src/UiAlert'),
    },
    data() {
      return {
        fullName: this.fullName,
        newPassword: '',
        newPasswordConfirm: '',
        passwordConfirmVisited: false,
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
      passwordsMatch() {
        if (this.passwordConfirmVisited) {
          const passwordsMatch = this.newPassword === this.newPasswordConfirm;
          this.setProfileError(!passwordsMatch);
          return passwordsMatch;
        }
        return true;
      },
    },
    methods: {
      hasPrivilege(privilege) {
        return this.privileges[privilege];
      },
      submitEdits() {
        if (this.passwordsMatch) {
          const edits = {
            password: this.newPassword,
          };
          this.editProfile(edits);
        }
      },
    },
    vuex: {
      getters: {
        privileges: state => state.core.learnerPrivileges,
        fullName: state => state.core.session.full_name,
        error: state => state.pageState.error,
        success: state => state.pageState.success,
        busy: state => state.pageState.busy,
        backendErrorMessage: state => state.pageState.errorMessage,
      },
      actions: {
        editProfile: actions.editProfile,
        setProfileError: actions.setProfileError,
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
  $iphone-width = 320

  .content
    padding-top: $vertical-page-margin
    margin-left: auto
    margin-right: auto
    overflow-y: auto
    width: ($iphone-width - 20)px

  #submit
    margin-left: auto
    margin-right: auto
    display: block
    margin-top: $vertical-page-margin
    width: 98%

  .advanced-option
    color: $core-action-light
    width: 100%
    display: inline-block
    font-size: 0.9em

</style>
