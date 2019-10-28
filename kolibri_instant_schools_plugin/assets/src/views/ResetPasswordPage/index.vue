<template>
  <div>
    <ResetPasswordPageStatus
      v-if="showStatus"
      :status="status"
      @close="goToHomePage"
    />
    <NewPasswordForm
      v-else
      :disable="disableForms"
      @submit="submitNewPassword"
    />
  </div>
</template>


<script>

  import { mapState } from 'vuex';
  import { PageNames, ResetPasswordStates as STATES } from '../../constants';
  import { getTokenStatus, updatePassword } from './api';
  import NewPasswordForm from './NewPasswordForm';
  import ResetPasswordPageStatus from './ResetPasswordPageStatus';

  export default {
    name: 'ResetPasswordPage',
    components: {
      NewPasswordForm,
      ResetPasswordPageStatus,
    },
    data() {
      return {
        status: STATES.CHECKING_TOKEN,
        disableForms: false,
      };
    },
    computed: {
      ...mapState('signIn', ['token', 'phone']),
      showStatus() {
        return this.status !== STATES.ENTER_PASSWORD;
      },
    },
    mounted() {
      getTokenStatus({
        token: this.token,
        phoneNumber: this.phone,
      })
        .then(() => {
          this.status = STATES.ENTER_PASSWORD;
        })
        .catch(response => {
          if (response.status.code === 400) {
            this.status = STATES.LINK_EXPIRED;
          } else {
            this.status = STATES.OTHER_ERROR;
          }
        });
    },
    methods: {
      submitNewPassword(newPw) {
        this.disableForms = true;
        return updatePassword({
          password: newPw,
          token: this.token,
          phone: this.phone,
        })
          .then(() => {
            this.status = STATES.PASSWORD_CHANGED;
          })
          .catch(() => {
            this.status = STATES.OTHER_ERROR;
          })
          .then(() => {
            this.disableForms = false;
          });
      },
      goToHomePage() {
        this.$router.replace({ name: PageNames.SIGN_IN });
      },
    },
    $trs: {
      newPw: 'New password',
      newPwConfirm: 'New password again',
      passwordsDoNotMatch: 'Passwords do not match',
      resetPasswordHeader: 'Reset password',
      saveButton: 'Save',
    },
  };

</script>


<style lang="scss" scoped></style>
