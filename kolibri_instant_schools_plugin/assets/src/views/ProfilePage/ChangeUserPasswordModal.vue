<template>

  <KModal
    :title="$tr('passwordChangeFormHeader')"
    size="medium"
    :submitText="$tr('updateButtonLabel')"
    :cancelText="$tr('cancelButtonLabel')"
    :submitDisabled="isBusy"
    @submit="submitForm"
    @cancel="$emit('cancel')"
  >
    {{ $tr('passwordChangeWarning') }}
    <KTextbox
      ref="newPassword"
      v-model="newPassword"
      type="password"
      :label="$tr('newPasswordFieldLabel')"
      :invalid="newPasswordIsInvalid"
      :invalidText="newPasswordInvalidErrorText"
      :autofocus="true"
      @blur="newPasswordBlurred = true"
    />
    <KTextbox
      ref="confirmedNewPassword"
      v-model="confirmedNewPassword"
      type="password"
      :label="$tr('confirmNewPasswordFieldLabel')"
      :invalid="confirmedNewPasswordIsInvalid"
      :invalidText="confirmedNewPasswordInvalidErrorText"
      @blur="confirmedNewPasswordBlurred = true"
    />
  </KModal>

</template>


<script>

  import { mapState, mapActions } from 'vuex';

  export default {
    name: 'ChangeUserPasswordModal',
    data() {
      return {
        newPassword: '',
        confirmedNewPassword: '',
        newPasswordBlurred: false,
        confirmedNewPasswordBlurred: false,
        submittedForm: false,
      };
    },
    computed: {
      ...mapState('profile', ['isBusy']),
      newPasswordInvalidErrorText() {
        if (this.newPasswordBlurred || this.submittedForm) {
          if (this.newPassword === '') {
            return this.$tr('required');
          }
        }
        return '';
      },
      newPasswordIsInvalid() {
        return Boolean(this.newPasswordInvalidErrorText);
      },
      confirmedNewPasswordInvalidErrorText() {
        if (this.confirmedNewPasswordBlurred || this.submittedForm) {
          if (this.confirmedNewPassword === '') {
            return this.$tr('required');
          }
          if (this.confirmedNewPassword !== this.newPassword) {
            return this.$tr('passwordMismatchErrorMessage');
          }
        }
        return '';
      },
      confirmedNewPasswordIsInvalid() {
        return Boolean(this.confirmedNewPasswordInvalidErrorText);
      },
      formIsValid() {
        return !this.newPasswordIsInvalid && !this.confirmedNewPasswordIsInvalid;
      },
    },
    methods: {
      ...mapActions('profile', ['updateUserProfilePassword']),
      submitForm() {
        this.submittedForm = true;
        if (this.formIsValid) {
          this.updateUserProfilePassword(this.newPassword);
        } else {
          if (this.newPasswordIsInvalid) {
            this.$refs.newPassword.focus();
          } else if (this.confirmedNewPasswordIsInvalid) {
            this.$refs.confirmedNewPassword.focus();
          }
        }
      },
    },
    $trs: {
      passwordChangeWarning: 'New password will be set for all users on this account',
      passwordChangeFormHeader: 'Change Password',
      newPasswordFieldLabel: 'Enter new password',
      confirmNewPasswordFieldLabel: 'Re-enter new password',
      passwordMismatchErrorMessage: 'New passwords do not match',
      required: 'This field is required',
      cancelButtonLabel: 'Cancel',
      updateButtonLabel: 'Update',
    },
  };

</script>


<style lang="scss" scoped></style>
