<template>

  <div>


    <div>

    </div>
    <div class="buttons">
      <k-button v-if="atAccountNotFound" :text="$tr('goBack')" @click="$emit('goback')" />
      <k-button v-else :text="$tr('close')" @click="$emit('closemodal')" />
    </div>
  </div>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';

  export default {
    name: 'resetPasswordConfirmation',
    components: {
      kButton,
    },
    props: {
      type: {
        type: String,
        required: true,
      },
    },
    computed: {
      atAccountNotFound() {
        return this.type === 'accountNotFound';
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

  .buttons
    text-align: right

</style>
