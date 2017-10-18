<template>

  <core-modal v-if="show" :title="currentTitle">
    <confirmation v-if="confirmation" :type="confirmation" @close="handleClose" />
    <phone-number-form v-else @submit="submitTokenRequest" />
  </core-modal>

</template>


<script>

  import coreModal from 'kolibri.coreVue.components.coreModal';
  import confirmation from './confirmation';
  import phoneNumberForm from './phone-number-form';
  import { requestResetToken } from '../../state/resetPasswordActions';

  export default {
    name: 'resetPasswordModal',
    components: {
      confirmation,
      coreModal,
      phoneNumberForm,
    },
    props: {
      show: {
        type: Boolean,
        required: true,
      },
    },
    data() {
      return {
        confirmation: null,
      };
    },
    computed: {
      currentTitle() {
        return 'Reset password';
      },
    },
    methods: {
      submitTokenRequest(phoneNumber) {
        this.requestResetToken({ phoneNumber })
          .then(() => {
            this.confirmation = 'success';
          })
          .catch(err => {
            console.log(err);
            this.confirmation = 'accountNotFound';
          });
      },
    },
    vuex: {
      getters: {
        resetPwModalIsOpen: () => true,
      },
      actions: {
        requestResetToken,
      },
    },
    $trs: {
      accountNotFound: 'Account not found',
      resetPassword: 'Reset password',
      smsServiceError: 'SMS service error',
    },
  };

</script>


<style lang="stylus" scoped></style>
