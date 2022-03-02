<template>

  <KModal
    :title="currentTitle"
    @cancel="closeModal"
  >
    <div class="contents">
      <ResetPasswordModalStatus
        v-if="showStatus"
        :status="status"
        @close="handleClose"
      />
      <PhoneNumberForm
        v-else
        :disabled="disableForms"
        :phoneLookupFailed="phoneLookupFailed"
        @submit="submitTokenRequest"
        @close="closeModal"
      />
    </div>
  </KModal>

</template>


<script>

  import { RequestTokenStates as STATES } from '../../../constants';
  import { createResetToken } from './api';
  import ResetPasswordModalStatus from './ResetPasswordModalStatus';
  import PhoneNumberForm from './PhoneNumberForm';

  export default {
    name: 'ResetPasswordModal',
    components: {
      PhoneNumberForm,
      ResetPasswordModalStatus,
    },
    data() {
      return {
        disableForms: false,
        status: STATES.ENTER_PHONE_NUMBER,
      };
    },
    computed: {
      currentTitle() {
        switch (this.status) {
          case STATES.MESSAGE_SENT:
            return this.$tr('messageSent');
          case STATES.SMS_SERVICE_ERROR:
            return this.$tr('smsServiceError');
          default:
            return this.$tr('resetPassword');
        }
      },
      showStatus() {
        return this.status === STATES.MESSAGE_SENT || this.status === STATES.SMS_SERVICE_ERROR;
      },
      phoneLookupFailed() {
        return this.status === STATES.ACCOUNT_NOT_FOUND;
      },
    },
    methods: {
      submitTokenRequest(phoneNumber) {
        this.disableForms = true;
        createResetToken({ phoneNumber })
          .then(() => {
            this.status = STATES.MESSAGE_SENT;
          })
          .catch(err => {
            const { code } = err.status;
            if (code === 400) {
              this.status = STATES.ACCOUNT_NOT_FOUND;
            } else {
              this.status = STATES.SMS_SERVICE_ERROR;
            }
          })
          .then(() => {
            this.disableForms = false;
          });
      },
      resetState() {
        this.status = STATES.ENTER_PHONE_NUMBER;
      },
      closeModal() {
        // guard against closing until 'X' button can be removed
        if (!this.disableForms) {
          this.$emit('close');
        }
      },
      handleClose() {
        if (this.status === STATES.ACCOUNT_NOT_FOUND) {
          this.status = STATES.ENTER_PHONE_NUMBER;
        } else {
          this.closeModal();
        }
      },
    },
    $trs: {
      accountNotFound: 'Account not found',
      messageSent: 'Message sent',
      resetPassword: 'Reset password',
      smsServiceError: 'SMS service error',
    },
  };

</script>


<style lang="scss" scoped>

  .contents {
    margin: 1em 0;
  }

</style>
