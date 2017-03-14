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
        <a href="#" @click.prevent="openTermsModal" class="tos">{{$tr('termsAgreement')}}</a>
      </ui-checkbox>

      <ui-modal ref="termsModal" :title="$tr('termsOfService')" size="large">
        <div class="terms">
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc. </p>

          <p>Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. </p>

          <p>Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi a tellus consequat imperdiet. Vestibulum sapien. Proin quam. Etiam ultrices. Suspendisse in justo eu magna luctus suscipit. Sed lectus. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. </p>

          <p>Praesent blandit dolor. Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas et, augue. Vestibulum tincidunt malesuada tellus. Ut ultrices ultrices enim. Curabitur sit amet mauris. Morbi in dui quis est pulvinar ullamcorper. Nulla facilisi. Integer lacinia sollicitudin massa. </p>

          <p>Cras metus. Sed aliquet risus a tortor. Integer id quam. Morbi mi. Quisque nisl felis, venenatis tristique, dignissim in, ultrices sit amet, augue. Proin sodales libero eget ante. Nulla quam. Aenean laoreet. Vestibulum nisi lectus, commodo ac, facilisis ac, ultricies eu, pede. Ut orci risus, accumsan porttitor, cursus quis, aliquet eget, justo. Sed pretium blandit orci. Ut eu diam at pede suscipit sodales. Aenean lectus elit, fermentum non, convallis id, sagittis at, neque. </p>

          <p>Nullam mauris orci, aliquet et, iaculis et, viverra vitae, ligula. Nulla ut felis in purus aliquam imperdiet. Maecenas aliquet mollis lectus. Vivamus consectetuer risus et tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. </p>

          <p>Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. </p>

          <p>Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi a tellus consequat imperdiet. Vestibulum sapien. Proin quam. Etiam ultrices. </p>

          <p>Suspendisse in justo eu magna luctus suscipit. Sed lectus. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. Praesent blandit dolor. Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas et, augue. Vestibulum tincidunt malesuada tellus. </p>

          <p>Ut ultrices ultrices enim. Curabitur sit amet mauris. Morbi in dui quis est pulvinar ullamcorper. Nulla facilisi. Integer lacinia sollicitudin massa. Cras metus. Sed aliquet risus a tortor. Integer id quam. Morbi mi. Quisque nisl felis, venenatis tristique, dignissim in, ultrices sit amet, augue. Proin sodales libero eget ante. Nulla quam. Aenean laoreet. Vestibulum nisi lectus, commodo ac, facilisis ac, ultricies eu, pede. </p>


        </div>
      </ui-modal>

      <icon-button :disabled="busy" id="submit" :primary="true" text="Finish" type="submit" />

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
      'ui-modal': require('keen-ui/src/UiModal'),
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
        if (this.phoneNumberVisited) {
          const strippedPhoneNumber = this.phoneNumber.replace(/\D/g, '');
          return strippedPhoneNumber.length > 6;
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
      openTermsModal() {
        this.$refs.termsModal.open();
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


<style lang="stylus">

  #signup-page
    .ui-modal__
      &container
          max-height: 90vh
          max-width: 90vw

</style>


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
    font-size: smaller

</style>
