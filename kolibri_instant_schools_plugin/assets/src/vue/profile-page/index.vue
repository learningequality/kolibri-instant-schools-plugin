<template>

  <div class="content">
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
        label="Username"
        v-model.lazy="username"
        autocomplete="username"
        id="username"
        type="text" />

        <ui-textbox
            v-if="hasPrivilege('name')"
            class="input-field"
            label="Name"
            v-model.lazy="full_name"
            autocomplete="name"
            id="name"
            type="text" />

        <ui-button
          :disabled="busy"
          color="primary"
          type="primary"
          buttonType="submit"
          id="submit"
          class="input-field"
        >
          Update Profile
        </ui-button>

    </form>
  </div>

</template>


<script>

  const actions = require('../../actions');
  const responsiveElement = require('kolibri.coreVue.mixins.responsiveElement');

  module.exports = {
    name: 'profile-page',
    $trNameSpace: 'profile-page',
    $trs: {
      genericError: 'Something went wrong',
      success: 'Changes successfully made',
    },
    components: {
      'ui-textbox': require('keen-ui/src/UiTextbox'),
      'ui-button': require('keen-ui/src/UiButton'),
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
    mixins: [responsiveElement],
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  $content-width = 33%
  // taken from docs, assumes 1rem = 16px
  $ui-input-height = 68px

  .content
    margin-top: 100px
    width: $content-width
    margin-left: auto
    margin-right: auto
    height: (4 * $ui-input-height)

  form
    height: 100%

  #submit
    width: 98%
    margin-left: auto
    margin-right: auto
    display: block
    clear: both

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
