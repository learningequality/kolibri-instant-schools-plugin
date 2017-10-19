<template>

  <core-modal
    :title="currentTitle"
    @cancel="closeModal"
  >
    <div class="contents">
      <status
        v-if="showStatus"
        :status="status"
        @close="closeModal"
        @goback="resetState"
      />
      <phone-number-form
        v-else
        @submit="submitTokenRequest"
        @close="closeModal"
        :disabled="disableForms"
      />
    </div>
  </core-modal>

</template>


<script>

  import coreModal from 'kolibri.coreVue.components.coreModal';
  import status from './status';
  import phoneNumberForm from './phone-number-form';
  import { createResetToken } from '../../state/resetPasswordActions';
  import { STATUSES } from './constants';

  export default {
    name: 'resetPasswordModal',
    components: {
      status,
      coreModal,
      phoneNumberForm,
    },
    props: {},
    data() {
      return {
        disableForms: false,
        status: STATUSES.ENTER_PHONE_NUMBER,
      };
    },
    computed: {
      currentTitle() {
        switch (this.status) {
          case STATUSES.ACCOUNT_NOT_FOUND:
            return this.$tr('accountNotFound');
          case STATUSES.MESSAGE_SENT:
            return this.$tr('messageSent');
          case STATUSES.SMS_SERVICE_ERROR:
            return this.$tr('smsServiceError');
          default:
            return this.$tr('resetPassword');
        }
      },
      showStatus() {
        return this.status !== STATUSES.ENTER_PHONE_NUMBER;
      },
    },
    methods: {
      submitTokenRequest(phoneNumber) {
        this.disableForms = true;
        this.createResetToken({ phoneNumber })
          .then(() => {
            this.status = STATUSES.MESSAGE_SENT;
          })
          .catch(err => {
            const { code } = err.status;
            if (code === 400) {
              this.status = STATUSES.ACCOUNT_NOT_FOUND;
            } else if (code === 500) {
              this.status = STATUSES.SMS_SERVICE_ERROR;
            }
          })
          .then(() => {
            this.disableForms = false;
          });
      },
      resetState() {
        this.status = STATUSES.ENTER_PHONE_NUMBER;
      },
      closeModal() {
        // guard against closing until 'X' button can be removed
        if (!this.disableForms) {
          this.$emit('close');
        }
      },
    },
    vuex: {
      getters: {},
      actions: {
        createResetToken,
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


<style lang="stylus" scoped>

  .contents
    margin: 1em 0

</style>
