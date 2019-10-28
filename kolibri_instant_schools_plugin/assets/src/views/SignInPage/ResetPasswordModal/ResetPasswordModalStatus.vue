<template>
  <div>
    <div class="message">
      {{ message }}
    </div>
    <div class="buttons">
      <KButton
        :text="$tr('close')"
        :primary="true"
        @click="$emit('close')"
      />
    </div>
  </div>
</template>


<script>

  import KButton from 'kolibri.coreVue.components.KButton';
  import { RequestTokenStates as STATES } from '../../../constants';

  export default {
    name: 'ResetPasswordModalStatus',
    components: {
      KButton,
    },
    props: {
      status: {
        type: String,
        required: true,
      },
    },
    computed: {
      message() {
        switch (this.status) {
          case STATES.MESSAGE_SENT:
            return this.$tr('messageSent');
          case STATES.SMS_SERVICE_ERROR:
            return this.$tr('smsServiceUnavailable');
          default:
            return '';
        }
      },
    },
    $trs: {
      close: 'Close',
      goBack: 'Go back',
      messageSent:
        'A text message (SMS) has been sent to your phone with instructions to reset your password.',
      smsServiceUnavailable: 'The text message (SMS) service is not currently available',
    },
  };

</script>


<style lang="scss" scoped>

  .message {
    text-align: left;
  }

  .buttons {
    margin-top: 1em;
    text-align: right;
  }
  button {
    margin-right: 0;
  }

</style>
