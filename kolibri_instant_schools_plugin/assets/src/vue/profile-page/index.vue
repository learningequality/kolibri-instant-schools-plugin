<template>

  <div :style="fieldWidth" class="content">
    <div v-if="error" class="error ">
      {{errorMessage}}
    </div>
    <div v-if="success" class="success">
      {{$tr('success')}}
    </div>
    <!-- WRAP THE STRINGS -->
    <form @focus.capture="" @submit.prevent="submitEdits">

      <ui-textbox
        v-if="hasPrivilege('username')"
        class="input-field"
        :invalid="busy"
        :label="$tr('username')"
        v-model="username"
        autocomplete="username"
        id="username"
        type="text" />

      <ui-textbox
          v-if="hasPrivilege('name')"
          class="input-field"
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
      success: 'Changes successfully made',
      username: 'Username',
      name: 'Name',
      updateProfile: 'Update Profile',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-textbox': require('keen-ui/src/UiTextbox'),
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
        return {
          width: `${this.wideMult().submit * this.windowSize.width}px`,
        };
      },
      fieldWidth() {
        return {
          width: `${this.wideMult().field * this.windowSize.width}px`,
        };
      },
    },
    methods: {
      hasPrivilege(privilege) {
        return this.privileges[privilege];
      },
      passwordsMatch() {
        return this.password === this.confirm_password;
      },
      submitEdits() {
        // if (this.passwordsMatch()) {
        const edits = {
          username: this.username,
          full_name: this.full_name,
          password: this.password,
        };
        this.editProfile(edits, this.session);
        // }
      },
      wideMult() {
        const field = 0.33;
        const submit = field * 0.98;
        return {
          field,
          submit,
        };
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
    height: (4 * $ui-input-height)

  form
    height: 100%

  #submit
    margin-left: auto
    margin-right: auto
    display: block
    position: absolute
    bottom: $vertical-page-margin

  .advanced-option
    color: $core-action-light
    width: 100%
    display: inline-block
    font-size: 0.9em

  .error
    background-color: red
    font-size: 2em
    color: white
  .success
    background-color: green
    font-size: 2em
    color: white

</style>
