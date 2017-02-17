<template>

  <div class="login">
    <div id="login-container">
      <img class="logo" src="../img/instant-school-logo.png" alt="logo">
      <h1 class="login-text title">{{ $tr('instantSchool') }}</h1>
      <form id="login-form" ref="form" @submit.prevent="signIn">
        <ui-autocomplete
          :label="$tr('username')"
          id="username"
          type="text"
          :placeholder="$tr('enterUsername')"
          :aria-label="$tr('username')"
          v-model="username"
          autocomplete="username"
          required
          autofocus/>
        <ui-autocomplete
          :label="$tr('password')"
          id="password"
          type="password"
          :placeholder="$tr('enterPassword')"
          :aria-label="$tr('password')"
          v-model="password"
          autocomplete="current-password"
          required/>
        <icon-button id="login-btn" :text="$tr('signIn')" :primary="true" type="submit"></icon-button>

        <p v-if="loginError" class="sign-in-error">{{ $tr('signInError') }}</p>
      </form>
      <router-link class="login-text" id="password-reset" :to="signUp">{{ $tr('resetPassword') }}</router-link>
      <div id="divid-line"></div>

      <p class="login-text no-account">{{ $tr('noAccount') }}</p>
      <div id="btn-group">
        <router-link class="group-btn" :to="signUp">
          <icon-button :text="$tr('createAccount')" :primary="true"></icon-button>
        </router-link>
        <a class="group-btn" href="/">
          <icon-button :text="$tr('accessAsGuest')" :primary="false"></icon-button>
        </a>
      </div>
    </div>
  </div>

</template>


<script>

  const actions = require('kolibri.coreVue.vuex.actions');
  const PageNames = require('../../state/constants').PageNames;

  module.exports = {
    $trNameSpace: 'signInPage',
    $trs: {
      instantSchool: 'INSTANT SCHOOLS',
      signIn: 'Log In',
      username: 'Phone Number',
      enterUsername: 'Enter phone number',
      password: 'Password',
      enterPassword: 'Enter Password',
      noAccount: `Don't have an account?`,
      createAccount: 'Create Account',
      accessAsGuest: 'Access as Guest',
      signInError: 'Incorrect username or password',
      resetPassword: 'Reset your password',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-autocomplete': require('keen-ui/src/UiAutocomplete'),
    },
    data: () => ({
      username: '',
      password: '',
    }),
    computed: {
      signUp() {
        return { name: PageNames.SIGN_UP };
      },
    },
    methods: {
      signIn() {
        this.kolibriLogin({
          username: this.username,
          password: this.password,
        });
      },
    },
    vuex: {
      getters: {
        loginError: state => state.core.loginError === 401,
      },
      actions: {
        kolibriLogin: actions.kolibriLogin,
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '../../styles/theme.styl'

  .login
    background-color: $login-overlay
    height: 100%
    background: url(../img/instant-background.jpg) no-repeat center center fixed
    background-size: cover
    overflow-y: auto
    overflow-x: hidden

  #login-container
    display: block
    margin: auto

  .logo
    position: relative
    display: block
    margin: auto
    margin-top: 34px
    width: 30%
    max-width: 120px
    min-width: 60px

  .login-text
    color: $login-text

  .title
    font-weight: 100
    font-size: 1.3em
    letter-spacing: 0.1em
    text-align: center

  #login-form
    width: 70%
    max-width: 300px
    margin: auto
    margin-top: 30px

  #password
    margin-top: 30px

  #login-btn
    display: block
    margin: auto
    margin-top: 38px
    width: 100%

  #btn-group
    display: table
    margin: auto
    margin-top: 28px
    margin-bottom: 20px

  .group-btn
    padding: 5px

  #password-reset
    display: block
    text-align: center
    margin: auto
    margin-top: 26px
    font-size: 0.8em

  #divid-line
    width: 412px
    height: 1px
    background-color: $core-text-annotation
    margin: auto
    margin-top: 16px

  .no-account
    text-align: center

  .sign-in-error
    color: red

</style>
