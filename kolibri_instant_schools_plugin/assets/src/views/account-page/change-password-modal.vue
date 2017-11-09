<template>

  <core-modal :title="$tr('changePassword')" @cancel="showPasswordModal(false)">
    <p>{{ $tr('passwordChangeWarning') }}</p>

    <form @submit.prevent="submitForm">
      <ui-alert
        v-if="passwordError"
        type="error"
        :dismissible="false"
      >
        {{ passwordErrorMessage || $tr('genericError') }}
      </ui-alert>

      <k-textbox
        ref="password"
        type="password"
        :label="$tr('password')"
        :maxlength="120"
        :invalid="passwordIsInvalid"
        :invalidText="passwordIsInvalidText"
        :autofocus="true"
        @blur="passwordBlurred = true"
        v-model="password"
      />
      <k-textbox
        ref="passwordConfirmation"
        type="password"
        :label="$tr('passwordConfirmation')"
        :maxlength="120"
        :invalid="passwordConfirmationIsInvalid"
        :invalidText="passwordConfirmationInvalidText"
        @blur="passwordConfirmationBlurred = true"
        v-model="passwordConfirmation"
      />

      <div class="ta-r">
        <k-button
          :text="$tr('cancel')"
          :primary="false"
          :raised="false"
          @click="showPasswordModal(false)"
        />
        <k-button
          type="submit"
          :text="$tr('save')"
          :primary="true"
          :raised="true"
          :disabled="passwordBusy"
        />
      </div>

    </form>
  </core-modal>

</template>


<script>

  import { changePassword, showPasswordModal } from '../../state/actions';
  import coreModal from 'kolibri.coreVue.components.coreModal';
  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import kButton from 'kolibri.coreVue.components.kButton';
  import uiAlert from 'keen-ui/src/UiAlert';

  export default {
    name: 'changePasswordModal',
    components: {
      coreModal,
      kTextbox,
      kButton,
      uiAlert,
    },
    data() {
      return {
        password: '',
        passwordConfirmation: '',
        passwordBlurred: false,
        passwordConfirmationBlurred: false,
        formSubmitted: false,
      };
    },
    computed: {
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
      passwordConfirmationInvalidText() {
        if (this.passwordConfirmationBlurred || this.formSubmitted) {
          if (this.passwordConfirmation === '') {
            return this.$tr('required');
          }
          if (this.passwordConfirmation !== this.password) {
            return this.$tr('passwordsDoNotMatch');
          }
        }
        return '';
      },
      passwordConfirmationIsInvalid() {
        return !!this.passwordConfirmationInvalidText;
      },
    },
    methods: {
      submitForm() {
        this.formSubmitted = true;

        if (this.passwordIsInvalid) {
          return this.$refs.password.focus();
        }
        if (this.passwordConfirmationIsInvalid) {
          return this.$refs.passwordConfirmation.focus();
        }
        this.changePassword(this.password).then(() => this.showPasswordModal(false));
      },
    },
    vuex: {
      actions: {
        changePassword,
        showPasswordModal,
      },
      getters: {
        passwordBusy: state => state.pageState.passwordBusy,
        passwordError: state => state.pageState.passwordError,
        passwordErrorMessage: state => state.pageState.passwordErrorMessage,
      },
    },
    $trs: {
      changePassword: 'Change account password',
      passwordChangeWarning: 'New password will be set for all users on this account',
      password: 'New password',
      passwordConfirmation: 'New password again',
      required: 'This field is required',
      passwordsDoNotMatch: 'Passwords do not match',
      cancel: 'Cancel',
      save: 'Save',
      genericError: 'Something went wrong',
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  .ta-r
    text-align: right

  .alert
    max-width: 400px

  button[type=submit]
    margin-right: 0

</style>
