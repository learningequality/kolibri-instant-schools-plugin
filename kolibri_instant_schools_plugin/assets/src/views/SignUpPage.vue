<template>

  <div class="signup-page">
    <form
      ref="form"
      class="signup-form"
      @submit.prevent="signUp"
    >
      <h1>{{ $tr('createAccount') }}</h1>

      <KTextbox
        id="name"
        ref="name"
        v-model="name"
        type="text"
        autocomplete="name"
        :label="$tr('name')"
        :maxlength="120"
        :autofocus="true"
        :invalid="nameIsInvalid"
        :invalidText="nameIsInvalidText"
        @blur="nameBlurred = true"
      />

      <KTextbox
        id="username"
        ref="username"
        v-model="username"
        type="tel"
        autocomplete="tel"
        :label="$tr('phoneNumberLabel')"
        :invalid="usernameIsInvalid"
        :invalidText="usernameIsInvalidText"
        :showInvalidText="usernameIsInvalid"
        @blur="usernameBlurred = true"
        @input="resetSignUpState"
      />

      <KTextbox
        id="password"
        ref="password"
        v-model="password"
        type="password"
        autocomplete="new-password"
        :label="$tr('password')"
        :invalid="passwordIsInvalid"
        :invalidText="passwordIsInvalidText"
        :showInvalidText="passwordIsInvalidText"
        @blur="passwordBlurred = true"
      />

      <KTextbox
        id="confirmed-password"
        ref="confirmedPassword"
        v-model="confirmedPassword"
        type="password"
        autocomplete="new-password"
        :label="$tr('reEnterPassword')"
        :invalid="confirmedPasswordIsInvalid"
        :invalidText="confirmedPasswordIsInvalidText"
        @blur="confirmedPasswordBlurred = true"
      />

      <p class="privacy-link">
        <KButton
          :text="$tr('viewTermsOfServicePrompt')"
          appearance="basic-link"
          @click="showTerms = true"
        />
      </p>

      <KCheckbox
        id="terms-agreement-checkbox"
        :class="['terms-agreement-checkbox', termsNotAgreed ? 'invalid' : '']"
        :checked="termsAgreed"
        :label="$tr('termsAgreementLabel')"
        @change="termsAgreed = $event"
        @blur="termsAgreementCheckboxBlurred = true"
      />

      <label
        v-if="termsNotAgreed"
        aria-live="polite"
        for="terms-agreement-checkbox"
        class="terms-agreement-error-box"
      >
        {{ termsNotAgreedText }}
      </label>

      <p>
        <KButton
          :disabled="busy"
          :primary="true"
          :text="$tr('finish')"
          type="submit"
          class="submit"
        />
      </p>
    </form>

    <div class="footer">
      <LanguageSwitcherFooter />
    </div>

    <KModal
      v-if="showTerms"
      :title="$tr('termsOfServiceModalHeader')"
      :size="'large'"
      @cancel="showTerms = false"
    >
      <iframe class="terms" src="/content/databases/about/tos.txt"></iframe>
      <KButton
        :text="$tr('close')"
        :primary="false"
        :disabled="false"
        @click="showTerms = false"
      />
    </KModal>
  </div>

</template>


<script>

  import { mapState, mapActions, mapGetters, mapMutations } from 'vuex';
  import { ERROR_CONSTANTS } from 'kolibri.coreVue.vuex.constants';
  import getUrlParameter from './getUrlParameter';
  import LanguageSwitcherFooter from './LanguageSwitcherFooter';

  export default {
    name: 'SignUpPage',
    metaInfo() {
      return {
        title: this.$tr('documentTitle'),
      };
    },
    components: {
      LanguageSwitcherFooter,
    },
    data: () => ({
      name: '',
      username: '',
      password: '',
      confirmedPassword: '',
      selectedFacility: {},
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
      ...mapGetters(['facilities']),
      ...mapState('signUp', ['errors', 'busy']),
      currentFacility() {
        return this.$store.getters.currentFacilityId;
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
        return Boolean(this.nameIsInvalidText);
      },
      usernameDoesNotExistYet() {
        if (this.errors.includes(ERROR_CONSTANTS.INVALID)) {
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
            return this.$tr('usernameAlreadyExistsError');
          }
        }
        return '';
      },
      usernameIsInvalid() {
        return Boolean(this.usernameIsInvalidText);
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
        return Boolean(this.passwordIsInvalidText);
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
        return Boolean(this.confirmedPasswordIsInvalidText);
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
      formIsValid() {
        return (
          !this.nameIsInvalid &&
          !this.usernameIsInvalid &&
          !this.passwordIsInvalid &&
          !this.confirmedPasswordIsInvalid &&
          !this.termsNotAgreed
        );
      },
      nextParam() {
        // query is after hash
        if (this.$route.query.next) {
          return this.$route.query.next;
        }
        // query is before hash
        return getUrlParameter('next');
      },
    },
    methods: {
      ...mapActions('signUp', ['signUpNewUser']),
      ...mapMutations('signUp', {
        resetSignUpState: 'RESET_STATE',
      }),
      signUp() {
        this.formSubmitted = true;
        const canSubmit = this.formIsValid && !this.busy;
        if (canSubmit) {
          const payload = {
            facility: this.currentFacility.id,
            full_name: this.name,
            username: this.username,
            password: this.password,
          };
          if (global.oidcProviderEnabled) {
            payload['next'] = this.nextParam;
          }
          this.signUpNewUser(payload);
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
    $trs: {
      createAccount: 'Create an account',
      name: 'Full name',
      phoneNumberLabel: 'Phone Number',
      password: 'Password',
      reEnterPassword: 'Re-enter password',
      passwordMatchError: 'Passwords do not match',
      finish: 'Finish',
      facility: 'Facility',
      required: 'This field is required',
      documentTitle: 'User Sign Up',
      privacyLink: 'Usage and privacy in Kolibri',
      genericError: 'Something went wrong during sign up!',
      phoneNumberInvalid: 'A valid phone number has at least 9 digits',
      usernameAlreadyExistsError: 'An account with that phone number already exists',
      logIn: 'Sign in',
      termsAgreementLabel: 'I agree to the terms of service & privacy policy',
      termsOfServiceModalHeader: 'Terms of service & privacy policy',
      viewTermsOfServicePrompt: 'View terms of service & privacy policy',
      appBarHeader: 'Instant Schools',
      close: 'Close',
    },
  };

</script>


<style lang="scss" scoped>

  $iphone-5-width: 320px;
  $vertical-page-margin: 100px;

  // Form
  .signup-form {
    max-width: $iphone-5-width - 20;
    margin-right: auto;
    margin-left: auto;
  }

  .footer {
    margin: 36px;
    margin-top: 48px;
  }

  .privacy-link {
    margin-top: 24px;
  }

  .submit {
    margin-left: 0;
  }

  .terms {
    width: 80vw;
    height: 80vh;
    border: none;
    &-agreement {
      $height-of-prompt: 18px + 16px;
      $height-of-checkbox: 48px + 16px;
      $k-textbox-text-distance: 24px; // distance from top of text to its label container
      $height-of-error: 16px;

      display: inline-block;
      max-width: 100%;
      height: $height-of-prompt + $height-of-checkbox + $height-of-error;
      margin-top: $k-textbox-text-distance;
      // margin-bottom: $form-item-spacing; // margin defined for k-textbox
      &-view-prompt {
        // end dupe

        display: block;
        max-width: 100%;
        padding: 0;
        // margin-bottom: $form-item-spacing;
        overflow: hidden;

        // duplicating styles from `<a>` in core theme
        // color: $core-action-normal;
        text-decoration: underline;
        text-overflow: ellipsis;
        white-space: nowrap;
        // transition: color $core-time ease-out;
        // &:hover {
        //   color: $core-action-dark;
        // }
        &:hover:focus,
        &:focus {
          // outline: $core-outline;
        }
      }
      &-checkbox {
        margin-top: 0;
        // margin-bottom: $form-item-spacing;
        &.invalid {
          // color: $keen-invalid-md-red;
        }
      }
      &-error-box {
        display: block;
        font-size: 14px; // same as error messages from inputs
        // color: $keen-invalid-md-red; // same color as input error messages
      }
    }
  }

</style>
