<template>

  <div class="login">
    <div id="login-container">
      <br>
      <br>
      <img class="logo" src="../img/instant-school-logo.png" alt="logo">
      <h1 class="login-text title">{{ $tr('instantSchool') }}</h1>
      <br>
      <form ref="form" @submit.prevent="signIn">
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
        <br>
        <ui-autocomplete
          :label="$tr('password')"
          id="password"
          type="password"
          :placeholder="$tr('enterPassword')"
          :aria-label="$tr('password')"
          v-model="password"
          autocomplete="current-password"
          required/>
        <br>
        <icon-button id="login-btn" :text="$tr('signIn')" :primary="true" type="submit"></icon-button>

        <p v-if="loginError" class="sign-in-error">{{ $tr('signInError') }}</p>
      </form>
      <br>
      <router-link class="login-text" id="password-reset" :to="signUp">{{ $tr('resetPassword') }}</router-link>
      <br>
      <div id="divid-line"></div>

      <p class="login-text">{{ $tr('noAccount') }}</p>
      <br>
      <div id="btn-group">
        <router-link class="group-btn" :to="signUp">
          <icon-button :text="$tr('createAccount')" :primary="true"></icon-button>
        </router-link>
        <a class="group-btn" href="/">
          <icon-button :text="$tr('accessAsGuest')" :primary="false"></icon-button>
        </a>
      </div>
      <br>
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
    height: 100vh
    background: url(../img/instant-background.jpg) no-repeat center center fixed
    -webkit-background-size: cover
    -moz-background-size: cover
    -o-background-size: cover
    background-size: cover
    overflow-y: auto
    overflow-x: hidden

  #login-container
    display: block
    margin: auto

  .login-text
    color: $login-text

  .title
    font-weight: 100

  #login-btn
    display:block
    margin: auto
    width: 100%

  #btn-group
    display:table
    margin: auto

  .group-btn
    padding: 5px

  #password-reset
    display: table
    margin: auto
    font-size: 0.8em

  #divid-line
    width: 412px
    height: 1px
    background-color: $core-text-annotation
    margin: auto

  h1
    font-size: 1.3em
    letter-spacing: 0.1em

  h1, p
    text-align: center

  img
    position: relative
    display: block
    margin: auto
    width: 16vh

  form
    width: 70%;
    max-width: 300px;
    margin: auto

  .sign-in-error
    color: red


</style>
