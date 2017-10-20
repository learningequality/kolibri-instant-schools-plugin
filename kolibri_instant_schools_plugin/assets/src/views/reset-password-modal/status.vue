<template>

  <div>
    <div class="message">
      {{ message }}
    </div>
    <div class="buttons">
      <k-button
        :text="buttonText"
        @click="$emit('close')"
        :primary="true"
      />
    </div>
  </div>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';
  import { STATUSES } from './constants';

  export default {
    name: 'resetPasswordStatus',
    components: {
      kButton,
    },
    props: {
      status: {
        type: String,
        required: true,
      },
    },
    computed: {
      buttonText() {
        if (this.status === STATUSES.ACCOUNT_NOT_FOUND) {
          return this.$tr('goBack');
        }
        return this.$tr('close');
      },
      message() {
        switch (this.status) {
          case STATUSES.ACCOUNT_NOT_FOUND:
            return this.$tr('accountNotFound');
          case STATUSES.MESSAGE_SENT:
            return this.$tr('messageSent');
          case STATUSES.SMS_SERVICE_ERROR:
            return this.$tr('smsServiceUnavailable');
          default:
            return '';
        }
      },
    },
    methods: {},
    $trs: {
      accountNotFound:
        'No account was found under this phone number. Check to see if your phone number was entered correctly.',
      close: 'Close',
      goBack: 'Go back',
      messageSent:
        'A text message (SMS) has been sent to your phone with instructions to reset your password.',
      smsServiceUnavailable: 'The text message (SMS) service is not currently available',
    },
  };

</script>


<style lang="stylus" scoped>

  .message
    text-align: left

  .buttons
    text-align: right
    margin-top: 1em

  button
    margin-right: 0

</style>
