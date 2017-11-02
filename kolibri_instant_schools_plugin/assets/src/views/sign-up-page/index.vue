<template>

  <div id="signup-page">

    <ui-toolbar type="colored" textColor="white">
      <template slot="icon">
        <ui-icon class="app-bar-icon"><logo/></ui-icon>
      </template>
      <template slot="brand">
        {{ $tr('appBarHeader') }}
      </template>
      <div slot="actions">
        <router-link id="signin" :to="signInPage">
          <span>{{ $tr('logIn') }}</span>
        </router-link>
      </div>
    </ui-toolbar>

    <form class="signup-form" ref="form" @submit.prevent="signUp">
      <ui-alert type="error" @dismiss="resetSignUpState" v-if="unknownError">
        {{errorMessage}}
      </ui-alert>

      <h1 class="signup-title">{{ $tr('createAccount') }}</h1>

      <k-textbox
        ref="name"
        id="name"
        type="text"
        autocomplete="name"
        :label="$tr('name')"
        :maxlength="120"
        :autofocus="true"
        :invalid="nameIsInvalid"
        :invalidText="nameIsInvalidText"
        @blur="nameBlurred = true"
        v-model="name"
      />

      <k-textbox
        ref="username"
        id="username"
        type="tel"
        autocomplete="tel"
        :label="$tr('phoneNumberLabel')"
        :invalid="usernameIsInvalid"
        :invalidText="usernameIsInvalidText"
        @blur="usernameBlurred = true"
        @input="resetSignUpState"
        v-model="username"
      />

      <k-textbox
        ref="password"
        id="password"
        type="password"
        autocomplete="new-password"
        :label="$tr('password')"
        :invalid="passwordIsInvalid"
        :invalidText="passwordIsInvalidText"
        @blur="passwordBlurred = true"
        v-model="password"
      />

      <k-textbox
        ref="confirmedPassword"
        id="confirmed-password"
        type="password"
        autocomplete="new-password"
        :label="$tr('reEnterPassword')"
        :invalid="confirmedPasswordIsInvalid"
        :invalidText="confirmedPasswordIsInvalidText"
        @blur="confirmedPasswordBlurred = true"
        v-model="confirmedPassword"
      />

      <ui-select
        :name="$tr('selectFacility')"
        :placeholder="$tr('selectFacility')"
        :label="$tr('facility')"
        :value="selectedFacility"
        :options="facilityList"
        :invalid="facilityIsInvalid"
        :error="facilityIsInvalidText"
        @blur="facilityBlurred = true"
        @input="updateSelection"
      />

      <!-- ToS modal only shows up if the box empty prior to clicking -->
      <!-- Using UI Checkbox for blur events and v-model -->
      <ui-checkbox
        id="terms-agreement-checkbox"
        :class="['terms-agreement-checkbox', termsNotAgreed ? 'invalid' : '']"
        v-model="termsAgreed"
        @change="showTerms = termsAgreed"
        @blur="termsAgreementCheckboxBlurred = true"
        :label="$tr('termsAgreementLabel')"
      />
      <label
        v-if="termsNotAgreed"
        for="terms-agreement-checkbox"
        class="terms-error-box"
      >
        {{ termsNotAgreedText }}
      </label>


      <k-button :disabled="busy" :primary="true" :text="$tr('finish')" type="submit" />

    </form>

    <core-modal
      v-if="showTerms"
      @cancel="showTerms = false"
      :title="$tr('termsOfServiceModalHeader')"
    >
      <iframe class="terms" src="/content/databases/tos.txt"></iframe>
    </core-modal>

    <div class="footer">
      <language-switcher :footer="true"/>
    </div>
  </div>

</template>


<script>

  import { signUp, resetSignUpState } from '../../state/actions';
  import { PageNames } from '../../constants';
  import { validateUsername } from 'kolibri.utils.validators';
  import kButton from 'kolibri.coreVue.components.kButton';
  import uiCheckbox from 'keen-ui/src/UiCheckbox';
  import coreModal from 'kolibri.coreVue.components.coreModal';
  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import uiToolbar from 'keen-ui/src/UiToolbar';
  import logo from 'kolibri.coreVue.components.logo';
  import uiIcon from 'keen-ui/src/UiIcon';
  import uiSelect from 'keen-ui/src/UiSelect';
  import languageSwitcher from 'kolibri.coreVue.components.languageSwitcher';

  export default {
    name: 'signUpPage',
    $trs: {
      createAccount: 'Create an account',
      name: 'Full name',
      phoneNumberLabel: 'Phone Number',
      password: 'Password',
      reEnterPassword: 'Re-enter password',
      passwordMatchError: 'Passwords do not match',
      genericError: 'Something went wrong during sign up!',
      phoneNumberInvalid: 'Please enter a valid phone number',
      accountAlreadyExistsError: 'An account with that phone number already exists',
      logIn: 'Sign in',
      termsAgreementLabel: 'I agree to the terms of service & privacy policy',
      termsOfServiceModalHeader: 'Terms of service & privacy policy',
      appBarHeader: 'Instant Schools',
      finish: 'Finish',
      facility: 'Facility',
      selectFacility: 'Select a facility',
      required: 'This field is required',
    },
    components: {
      kButton,
      kTextbox,
      uiToolbar,
      logo,
      uiIcon,
      uiSelect,
      languageSwitcher,
      coreModal,
      uiCheckbox,
    },
    data: () => ({
      name: '',
      username: '',
      password: '',
      confirmedPassword: '',
      selection: {},
      nameBlurred: false,
      usernameBlurred: false,
      passwordBlurred: false,
      confirmedPasswordBlurred: false,
      facilityBlurred: false,
      formSubmitted: false,
      showTerms: false,
      termsAgreed: false,
      termsAgreementCheckboxBlurred: false,
    }),
    computed: {
      signInPage() {
        return { name: PageNames.SIGN_IN };
      },
      facilityList() {
        return this.facilities.map(facility => ({
          label: facility.name,
          id: facility.id,
        }));
      },
      selectedFacility() {
        if (this.facilityList.length === 1) {
          return this.facilityList[0];
        }
        return this.selection;
      },
      nameIsInvalidText() {
        if (this.nameBlurred || this.formSubmitted) {
          if (this.name === '') {
            return this.$tr('required');
          }
        }
        return '';
      },
      nameIsInvalid() {
        return !!this.nameIsInvalidText;
      },
      usernameDoesNotExistYet() {
        if (this.errorCode === 400) {
          return false;
        }
        return true;
      },
      usernameIsInvalidText() {
        if (this.usernameBlurred || this.formSubmitted) {
          if (this.username === '') {
            return this.$tr('required');
          }
          if (!this.validatePhoneNumber(this.username)) {
            return this.$tr('phoneNumberInvalid');
          }
          if (!this.usernameDoesNotExistYet) {
            return this.$tr('accountAlreadyExistsError');
          }
        }
        return '';
      },
      usernameIsInvalid() {
        return !!this.usernameIsInvalidText;
      },
      passwordIsInvalidText() {
        if (this.passwordBlurred || this.formSubmitted) {
          if (this.password === '') {
            return this.$tr('required');
          }
        }
        return '';
      },
      passwordIsInvalid() {
        return !!this.passwordIsInvalidText;
      },
      confirmedPasswordIsInvalidText() {
        if (this.confirmedPasswordBlurred || this.formSubmitted) {
          if (this.confirmedPassword === '') {
            return this.$tr('required');
          }
          if (this.confirmedPassword !== this.password) {
            return this.$tr('passwordMatchError');
          }
        }
        return '';
      },
      confirmedPasswordIsInvalid() {
        return !!this.confirmedPasswordIsInvalidText;
      },
      termsNotAgreedText() {
        if ((this.termsAgreementCheckboxBlurred || this.formSubmitted) && !this.termsAgreed) {
          return this.$tr('required');
        }
        return '';
      },
      termsNotAgreed() {
        return !!this.termsNotAgreedText;
      },
      noFacilitySelected() {
        return !this.selectedFacility.id;
      },
      facilityIsInvalidText() {
        if (this.facilityBlurred || this.formSubmitted) {
          if (this.noFacilitySelected) {
            return this.$tr('required');
          }
        }
        return '';
      },
      facilityIsInvalid() {
        return !!this.facilityIsInvalidText;
      },
      formIsValid() {
        return (
          !this.nameIsInvalid &&
          !this.usernameIsInvalid &&
          !this.passwordIsInvalid &&
          !this.confirmedPasswordIsInvalid &&
          !this.facilityIsInvalid &&
          !this.termsNotAgreed
        );
      },
      unknownError() {
        if (this.errorCode) {
          return this.errorCode !== 400;
        }
        return false;
      },
      errorMessage() {
        return this.backendErrorMessage || this.$tr('genericError');
      },
    },
    methods: {
      updateSelection(selection) {
        this.selection = selection;
      },
      signUp() {
        this.formSubmitted = true;
        const canSubmit = this.formIsValid && !this.busy;
        if (canSubmit) {
          this.signUpAction({
            facility: this.selectedFacility.id,
            full_name: this.name,
            username: this.username,
            password: this.password,
          });
        } else {
          this.focusOnInvalidField();
        }
      },
      focusOnInvalidField() {
        if (this.nameIsInvalid) {
          this.$refs.name.focus();
        } else if (this.usernameIsInvalid) {
          this.$refs.username.focus();
        } else if (this.passwordIsInvalid) {
          this.$refs.password.focus();
        } else if (this.confirmedPasswordIsInvalid) {
          this.$refs.confirmedPassword.focus();
        }
      },
      validatePhoneNumber() {
        const strippedPhoneNumber = this.username.replace(/\D/g, '');
        return strippedPhoneNumber.length > 8;
      },
    },
    vuex: {
      getters: {
        session: state => state.core.session,
        errorCode: state => state.pageState.errorCode,
        busy: state => state.pageState.busy,
        backendErrorMessage: state => state.pageState.errorMessage,
        facilities: state => state.core.facilities,
      },
      actions: {
        signUpAction: signUp,
        resetSignUpState: resetSignUpState,
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
  $keen-invalid-md-red = #f44336

  // component, highest level
  #signup-page
    width: 100%
    height: 100%
    overflow-y: auto

  // Action Bar
  #logo
    // 1.63 * font height
    height: $logo-size
    display: inline-block
    margin-left: $logo-margin

  #signin
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
    height: 80vh
    width: 80vw
    &-agreement-checkbox
      text-decoration: underline
      &.invalid
        color: $keen-invalid-md-red
    &-error-box
      display: block
      color: $keen-invalid-md-red // same color as input error messages
      font-size: 14px // same as error messages from inputs

  .app-bar-icon
    font-size: 2.5em
    margin-left: 0.25em

  .footer
    margin: 36px
    margin-top: 96px

</style>
