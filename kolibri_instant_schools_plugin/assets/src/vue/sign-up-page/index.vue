<template>

  <div id="signup-page">

    <ui-toolbar type="colored" textColor="white">
      <template slot="icon">
        <img id="logo" src="../img/instant-school-logo.png" />
      </template>
      <template slot="brand">
        Instant Schools
      </template>
      <div slot="actions">
        <router-link id="login" :to="signInPage">
          <span>Log In</span>
        </router-link>
      </div>
    </ui-toolbar>

    <form class="signup-form" ref="form" @submit.prevent="signUp">
      <ui-alert type="error" @dismiss="resetSignUpState" v-if="errorCode">
        {{errorMessage}}
      </ui-alert>

      <h1 class="signup-title">{{ $tr('createAccount') }}</h1>

      <core-textbox
        :placeholder="$tr('enterName')"
        :label="$tr('name')"
        :aria-label="$tr('name')"
        v-model="name"
        autocomplete="name"
        autofocus
        required
        type="text" />

      <core-textbox
        :placeholder="$tr('enterPhoneNumber')"
        :label="$tr('phoneNumber')"
        :aria-label="$tr('phoneNumber')"
        @blur="phoneNumberVisited=true"
        :error="phoneNumberError"
        :invalid="!phoneNumberValid"
        v-model="phoneNumber"
        autocomplete="tel"
        required
        type="tel" />

      <core-textbox
        type="password"
        :placeholder="$tr('enterPassword')"
        :aria-label="$tr('password')"
        :label="$tr('password')"
        v-model="password"
        autocomplete="new-password"
        required />

      <core-textbox
        type="password"
        :placeholder="$tr('confirmPassword')"
        :aria-label="$tr('confirmPassword')"
        :label="$tr('confirmPassword')"
        :invalid="!passwordsMatch"
        :error="passwordError "
        v-model="confirmed_password"
        autocomplete="new-password"
        required />


      <div class="terms">
        <small>
          <p>
            1. Terms of Service: By accessing the application Kolibri you are
            agreeing to be bound by these terms of service, all applicable laws and
            regulations, and agree that you are responsible for compliance with any
            applicable local laws.
            <br>
            <em>
              Note: Complete Terms to follow preliminary testing period.
            </em>
          </p>
          <p>
            2. Privacy policy: By accessing the application Kolibri you acknowledge
            the use of this platform and how data are collected, used, and shared
            between Learning Equality and Vodafone Foundation.
            <br>
            <em>
              Note: Complete Privacy Notice to follow preliminary testing period.
            </em>
          </p>
        </small>
      </div>

      <ui-checkbox v-model="termsAgreement" required>
        {{$tr('termsAgreement')}}
      </ui-checkbox>

      <icon-button id="submit" :disabled="busy" :primary="true" text="Finish" type="submit" />

    </form>

  </div>

</template>


<script>

  const actions = require('../../actions');
  const PageNames = require('../../state/constants').PageNames;

  module.exports = {
    name: 'Sign-Up-Page',
    $trNameSpace: 'signUpPage',
    $trs: {
      createAccount: 'Create an account',
      name: 'Name',
      enterName: 'Enter name',
      phoneNumber: 'Phone number',
      enterPhoneNumber: 'Enter phone number',
      phoneNumberInvalidError: 'Please enter a valid 10-digit phone number',
      password: 'Password',
      enterPassword: 'Enter password',
      confirmPassword: 'Confirm password',
      passwordMatchError: 'Passwords do not match',
      genericError: 'Something went wrong during sign up',
      termsAgreement: 'I agree to the terms of service & privacy policy',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-alert': require('keen-ui/src/UiAlert'),
      'core-textbox': require('kolibri.coreVue.components.textbox'),
      'ui-toolbar': require('keen-ui/src/UiToolbar'),
      'ui-checkbox': require('keen-ui/src/UiCheckbox'),
    },
    data: () => ({
      name: '',
      phoneNumber: '',
      password: '',
      phoneNumberVisited: false,
      confirmed_password: '',
      termsAgreement: false,
    }),
    computed: {
      signInPage() {
        return { name: PageNames.SIGN_IN };
      },
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
      phoneNumberValid() {
        const fieldPopulated = this.phoneNumber !== '';
        const fieldVisited = this.phoneNumberVisited;
        const lengthCheck = () => {
          const strippedPhoneNumber = this.phoneNumber.replace(/\D/g, '');
          if (fieldVisited) {
            return strippedPhoneNumber.length === 10;
          }
          return strippedPhoneNumber.length <= 10;
        };
        if (fieldPopulated || fieldVisited) {
          // this avoids any octal, hex, negatives, etc interpretations
          const noBackendError = this.errorCode !== 400;
          const validLength = lengthCheck();
          return validLength && noBackendError;
        }
        // field hasn't been visited yet
        return true;
      },
      phoneNumberError() {
        if (this.phoneNumberValid) {
          return '';
        }
        return this.$tr('phoneNumberInvalidError');
      },
      allFieldsPopulated() {
        return !!(this.name && this.phoneNumber &&
          this.password && this.confirmed_password &&
          this.termsAgreement);
      },
      errorMessage() {
        return this.backendErrorMessage || this.$tr('genericError');
      },
    },
    methods: {
      canSubmit() {
        return this.allFieldsPopulated && this.passwordsMatch && !this.busy && this.phoneNumberValid;
      },
      signUp() {
        if (this.canSubmit()) {
          const userPayload = {
            full_name: this.name,
            username: this.phoneNumber,
            password: this.password,
          };
          this.signUpAction(userPayload);
        }
        // error should already be visible
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
  $vertical-page-margin = 100px
  $logo-size = (1.64 * 1.125)rem
  $logo-margin = (0.38 * $logo-size)rem

  // component, highest level
  #signup-page
    width: 100%
    height: 100%
    overflow-y: auto

  // Action Bar
  #logo
    // 1.63 * font height
    height: $logo-size
    width: auto
    display: inline-block
    margin-left: $logo-margin

  #login
    margin-right: 1em
    color: white
    text-decoration: none

  // Form
  .signup-title
    text-align: center

  .signup-form
    margin-top: $vertical-page-margin
    margin-left: auto
    margin-right: auto
    width: ($iphone-5-width - 20)px

  .terms
    background-color: $core-bg-light
    color: $core-text-annotation
    height: 6em
    overflow-y: scroll
    padding: 0.5em
    margin-bottom: 1em
    p
      margin-top: 0

  #submit
    width: 90%
    display: block
    margin-left: auto
    margin-right: auto

    margin-top: $vertical-page-margin
    margin-bottom: $vertical-page-margin

</style>
