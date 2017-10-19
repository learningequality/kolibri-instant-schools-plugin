<template>

  <div>
    <div>
      {{ $tr('instructionsWillBeSent') }}
    </div>

    <form @submit.prevent="$emit('submit', phoneNumber)">
      <k-textbox
        :label="$tr('enterPhoneNumber')"
        v-model="phoneNumber"
      />
      <div class="buttons">
        <k-button
          :text="$tr('cancel')"
          @click="$emit('close')"
          :primary="false"
        />
        <k-button
          type="submit"
          :text="$tr('send')"
          :primary="true"
        />
      </div>
    </form>
  </div>

</template>


<script>

  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import kButton from 'kolibri.coreVue.components.kButton';

  export default {
    name: 'phoneNumberForm',
    components: {
      kButton,
      kTextbox,
    },
    data() {
      return {
        phoneNumber: '',
      };
    },
    computed: {},
    methods: {},
    vuex: {
      getters: {},
      actions: {},
    },
    $trs: {
      cancel: 'Cancel',
      enterPhoneNumber: 'Enter your phone number',
      instructionsWillBeSent: 'Instructions will be sent to your phone.',
      send: 'Send',
    },
  };

</script>


<style lang="stylus" scoped>

  .buttons
    text-align: right
    margin-top: 1em

  button[type='submit']
    margin-right: 0

</style>
