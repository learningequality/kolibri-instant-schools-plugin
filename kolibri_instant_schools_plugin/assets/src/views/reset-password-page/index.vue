<template>

  <div>
    <status
      v-if="showStatus"
      :status="status"
    />
    <new-password-form
      v-else
      @submit="submitNewPassword"
      :disable="disableForms"
    />
  </div>

</template>


<script>

  import { getTokenStatus } from '../../state/resetPasswordActions';
  import newPasswordForm from './new-password-form';
  import status from './status';

  const STATUSES = {
    ENTER_PASSWORD: 'ENTER_PASSWORD',
    CHECKING_TOKEN: 'CHECKING_TOKEN',
    SUCCESS: 'SUCCESS',
    LINK_EXPIRED: 'LINK_EXPIRED',
    OTHER_ERROR: 'OTHER_ERROR',
  };

  export default {
    components: {
      newPasswordForm,
      status,
    },
    data() {
      return {
        status: STATUSES.CHECKING_TOKEN,
        disableForms: false,
      };
    },
    computed: {
      showStatus() {
        return this.status !== STATUSES.ENTER_PASSWORD;
      },
    },
    methods: {
      submitNewPassword() {
        this.disableForms = true;
        setTimeout(() => {
          this.disableForms = false;
          this.status = 'SUCCESS';
        }, 1000);
      },
    },
    mounted() {
      this.getTokenStatus({
        token: this.token,
        phoneNumber: this.phone,
      })
        .then(() => {
          this.status = STATUSES.ENTER_PASSWORD;
        })
        .catch(response => {
          if (response.status.code === 400) {
            this.status = STATUSES.LINK_EXPIRED;
          } else {
            this.status = STATUSES.OTHER_ERROR;
          }
        });
    },
    vuex: {
      getters: {
        phone: ({ pageState }) => pageState.phone,
        token: ({ pageState }) => pageState.token,
      },
      actions: {
        getTokenStatus,
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


<style lang="stylus" scoped></style>
