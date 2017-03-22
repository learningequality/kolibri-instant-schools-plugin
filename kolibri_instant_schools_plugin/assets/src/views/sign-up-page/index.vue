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
        :placeholder="$tr('confirmPasswordPlaceholder')"
        :aria-label="$tr('confirmPassword')"
        :label="$tr('confirmPassword')"
        :invalid="!passwordsMatch"
        :error="passwordError "
        v-model="confirmed_password"
        autocomplete="new-password"
        required />

      <ui-checkbox v-model="termsAgreement" required>
        <a href="#" @click.prevent="showTerms = true" class="tos">{{$tr('termsAgreement')}}</a>
      </ui-checkbox>

      <core-modal v-if="showTerms" @cancel="showTerms = false" :title="$tr('termsOfService')">
        <iframe class="tos" src="/content/databases/tos.txt"></iframe>
      </core-modal>

      <icon-button :disabled="busy" id="submit" :primary="true" text="Finish" type="submit" />

    </form>

  </div>

</template>


<script>

  const actions = require('../../state/actions');
  const PageNames = require('../../constants').PageNames;

  module.exports = {
    name: 'Sign-Up-Page',
    $trNameSpace: 'signUpPage',
    $trs: {
      createAccount: 'Create an account',
      name: 'Name',
      enterName: 'Enter name',
      phoneNumber: 'Phone number',
      enterPhoneNumber: 'Enter phone number',
      phoneNumberInvalidError: 'Please enter a valid phone number',
      password: 'Password',
      enterPassword: 'Enter password',
      confirmPassword: 'Confirm password',
      confirmPasswordPlaceholder: 'Enter password again',
      passwordMatchError: 'Passwords do not match',
      genericError: 'Something went wrong during sign up',
      termsAgreement: 'I agree to the terms of service & privacy policy',
      termsOfService: 'Terms of service & privacy policy'
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-alert': require('keen-ui/src/UiAlert'),
      'core-textbox': require('kolibri.coreVue.components.textbox'),
      'ui-toolbar': require('keen-ui/src/UiToolbar'),
      'ui-checkbox': require('keen-ui/src/UiCheckbox'),
      'core-modal': require('kolibri.coreVue.components.coreModal'),
    },
    data: () => ({
      name: '',
      phoneNumber: '',
      password: '',
      phoneNumberVisited: false,
      confirmed_password: '',
      termsAgreement: false,
      showTerms: false,
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
        if (this.phoneNumberVisited) {
          const strippedPhoneNumber = this.phoneNumber.replace(/\D/g, '');
          return strippedPhoneNumber.length > 8;
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
      signUp() {
        const canSubmit =
          this.allFieldsPopulated
          && this.passwordsMatch
          && !this.busy
          && this.phoneNumberValid;
        if (canSubmit) {
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
  $vertical-page-margin = 40px
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
    color: $core-text-annotation

  #submit
    width: 90%
    display: block
    margin-left: auto
    margin-right: auto

    margin-top: $vertical-page-margin
    margin-bottom: $vertical-page-margin

  .tos
    width: 100%
    height: 50vh

</style>
