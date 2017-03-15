<template>

  <div class="login-page">
    <div id="login-content">
      <img class="logo" src="../img/instant-school-logo.png" alt="logo">
      <h1 class="login-text title">{{ $tr('instantSchool') }}</h1>
      <form id="login-form" ref="form" @submit.prevent="signIn">
        <core-textbox
          :label="$tr('username')"
          id="username"
          type="tel"
          :placeholder="$tr('enterUsername')"
          :aria-label="$tr('username')"
          v-model="username"
          autocomplete="tel"
          required
          autofocus/>
        <core-textbox
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

        <a @click.prevent="showResetModal = true" role="link" href="#" id="password-reset">
          {{ $tr('resetPassword') }}
        </a>

      </form>
      <core-modal
        :title="$tr('resetPassword')"
        v-if="showResetModal"
        @cancel="showResetModal = false">
        <p>
          This is a test. If you need to change you're password, please call:
        </p>
        <a id="password-reset-phone-number" href="tel:+1111111111">(XXX)-XXX-XXXX</a>
      </core-modal>
      <div id="divid-line"></div>

      <h2 class="login-text no-account">{{ $tr('noAccount') }}</h2>
      <div id="btn-group">
        <router-link class="group-btn" :to="signUp">
          <icon-button id="signup-button" :text="$tr('createAccount')" :primary="true"></icon-button>
        </router-link>
        <a class="group-btn" href="/learn">
          <icon-button id="guest-access-button" :text="$tr('accessAsGuest')" :primary="false"></icon-button>
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
      'core-textbox': require('kolibri.coreVue.components.textbox'),
      'core-modal': require('kolibri.coreVue.components.coreModal'),
    },
    data: () => ({
      username: '',
      password: '',
      showResetModal: false,
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
      openPasswordResetModal() {
        this.$refs.passwordResetModal.open();
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


<style lang="stylus">

  $login-text = #D8D8D8
  $login-red = #f44336

  #login-content
    .ui-
      &textbox__
        &label-text
          color: $login-text
        &input
          border-bottom-color: $login-text
          color: $login-text
          &:autofill
            background-color: transparent
      &button
        background-color: $login-red

        &#guest-access-button
          background-color: transparent
          color: $login-text
          border: 2px solid $login-red

      &modal__
        &container
            max-height: 90vh
            max-width: 90vw

</style>


<style lang="stylus" scoped>

  $login-overlay = #201A21
  $login-text = #D8D8D8
  $login-section-margin = 25px
  $title-size = 1.3em

  // wrappers
  .login-page
    background-color: $login-overlay
    height: 100%
    background: url(../img/instant-background.jpg) no-repeat center center fixed
    background-size: cover
    overflow-y: auto

  #login-content
    display: block
    margin-top: $login-section-margin
    margin-left: auto
    margin-right: auto


  // Logo stuff
  .logo
    display: block
    margin: auto
    margin-top: 34px
    width: 30%
    height: auto
    max-width: 120px
    min-width: 45px
    margin-bottom: $login-section-margin

    // All text on screen (excluding buttons, fields)
  .login-text
    color: $login-text
  .title
    font-weight: 100
    font-size: $title-size
    letter-spacing: 0.1em
    text-align: center
    margin-top: 0
    margin-bottom: 30px

  // form
  #login-form
    width: 70%
    max-width: 300px
    margin-left: auto
    margin-right: auto
    margin-bottom: $login-section-margin

  #login-btn
    display: block
    margin: auto
    width: 100%
    margin-bottom: $login-section-margin

  #password-reset
    display: block
    text-align: center
    margin-right: auto
    margin-left: auto
    font-size: 0.8em
    color: $login-text
    margin-bottom: $login-section-margin
    &-phone-number
      display: block
      text-align: center

  // seperator between login and accountless options
  #divid-line
    width: 412px
    max-width: 90%
    height: 1px
    background-color: $core-text-annotation
    background-color: $login-text
    margin-left: auto
    margin-right: auto
    margin-bottom: $login-section-margin

  // accountless options
  .no-account
    text-align: center
    font-weight: normal
    font-size: $title-size * 0.8
    margin-top: 0
    margin-bottom: $login-section-margin
  #btn-group
    display: table
    margin-left: auto
    margin-right: auto
    margin-top: $login-section-margin
    text-align: center
  .group-btn
    padding: 5px
    display: inline-block
    text-decoration: none

  // error text
  .sign-in-error
    color: red

</style>
