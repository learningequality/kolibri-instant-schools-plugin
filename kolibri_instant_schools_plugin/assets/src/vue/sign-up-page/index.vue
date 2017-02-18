<template>

  <div class="signup-page">

    <form class="signup-form" ref="form" @submit.prevent="signUp">
      <ui-alert type="error" @dismiss="resetSignUpState" v-if="errorCode">
        {{errorMessage}}
      </ui-alert>

      <h1 class="signup-title">{{ $tr('createAccount') }}</h1>

      <ui-textbox
        :placeholder="$tr('enterName')"
        :label="$tr('name')"
        :aria-label="$tr('name')"
        v-model="name"
        autocomplete="name"
        autofocus
        required
        id="name"
        type="text" />

      <ui-textbox
        :placeholder="$tr('enterUsername')"
        :label="$tr('username')"
        :aria-label="$tr('username')"
        :invalid="usernameError"
        v-model="username"
        autocomplete="username"
        required
        id="username"
        type="text" />

      <ui-textbox
        id="password"
        type="password"
        :placeholder="$tr('enterPassword')"
        :aria-label="$tr('password')"
        :label="$tr('password')"
        v-model="password"
        autocomplete="new-password"
        required />

      <ui-textbox
        id="confirmed-password"
        type="password"
        :placeholder="$tr('confirmPassword')"
        :aria-label="$tr('confirmPassword')"
        :label="$tr('confirmPassword')"
        :invalid="!passwordsMatch"
        :error="passwordError "
        v-model="confirmed_password"
        autocomplete="new-password"
        required />

      <!-- Need terms of service thing -->

      <icon-button :disabled="canSubmit" id="submit" :primary="true" text="Finish" type="submit" />

    </form>

  </div>

</template>


<script>

  const actions = require('../../actions');

  module.exports = {
    name: 'Sign-Up-Page',
    $trNameSpace: 'signUpPage',
    $trs: {
      createAccount: 'Create an Account',
      name: 'Name',
      enterName: 'Enter Name',
      username: 'Username',
      enterUsername: 'Enter Username',
      password: 'Password',
      enterPassword: 'Enter Password',
      confirmPassword: 'Confirm Password',
      passwordMatchError: 'Passwords do not match',
      genericError: 'Something went wrong during sign up!',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-alert': require('keen-ui/src/UiAlert'),
      'ui-textbox': require('keen-ui/src/UiTextbox'),
    },
    computed: {
      passwordsMatch() {
        // make sure both fields are populated
        if (this.password && this.confirmed_password) {
          return this.password === this.confirmed_password;
        }
        return true;
      },
      passwordError() {
        if (this.passwordsMatch) {
          return '';
        }
        return this.$tr('passwordMatchError');
      },
      usernameError() {
        return this.errorCode === 400;
      },
      allFieldsPopulated() {
        return !(this.name && this.username && this.password && this.confirmed_password);
      },
      canSubmit() {
        return !!this.allFieldsPopulated || !!this.passwordError || this.busy;
      },
      errorMessage() {
        return this.backendErrorMessage || this.$tr('genericError');
      },
    },
    data: () => ({
      name: '',
      username: '',
      password: '',
      confirmed_password: '',
    }),
    methods: {
      signUp() {
        this.signUpAction({
          full_name: this.name,
          username: this.username,
          password: this.password,
        });
      },
    },
    vuex: {
      getters: {
        session: state => state.core.session,
        errorCode: state => state.pageState.errorCode,
        busy: state => state.pageState.busy,
        backendErrorMessage: state => state.pageState.errorMessage,
      },
      actions: {
        signUpAction: actions.signUp,
        resetSignUpState: actions.resetSignUpState,
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'
  $iphone-5-width = 320px
  .signup-page
    position: relative
    width: 100%
    height: 100%
    overflow-y: auto

  .signup-title
    text-align: center


  .signup-form
    position: absolute
    top: 50%
    left: 50%
    width: ($iphone-5-width - 20)px
    transform: translate(-50%, -50%)

  #submit
    width: 90%
    margin-left: auto
    margin-right: auto
    display: block
    margin-top: 4em

  .signup-error
    color: red

</style>
