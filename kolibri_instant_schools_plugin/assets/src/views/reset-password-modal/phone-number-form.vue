<template>

  <div>
    <div class="instructions">
      {{ $tr('instructionsWillBeSent') }}
    </div>

    <form @submit.prevent="submitPhoneNumber">
      <k-textbox
        :label="$tr('enterPhoneNumber')"
        v-model="phoneNumber"
        :invalid="!phoneNumberIsValid"
        :invalidText="$tr('required')"
        :disabled="disabled"
      />
      <div class="buttons">
        <k-button
          :text="$tr('cancel')"
          @click="$emit('close')"
          :primary="false"
          :disabled="disabled"
        />
        <k-button
          type="submit"
          :text="$tr('send')"
          :primary="true"
          :disabled="disabled"
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
    props: {
      disabled: {
        type: Boolean,
        required: true,
      },
    },
    data() {
      return {
        phoneNumber: '',
        phoneNumberShouldValidate: false,
      };
    },
    computed: {
      phoneNumberIsValid() {
        if (this.phoneNumberShouldValidate) {
          return this.phoneNumber.trim() !== '';
        }
        return true;
      },
    },
    methods: {
      submitPhoneNumber() {
        this.phoneNumberShouldValidate = true;
        if (this.phoneNumberIsValid) {
          this.$emit('submit', this.phoneNumber);
        }
      },
    },
    vuex: {
      getters: {},
      actions: {},
    },
    $trs: {
      cancel: 'Cancel',
      enterPhoneNumber: 'Enter your phone number',
      instructionsWillBeSent: 'Instructions will be sent to your phone.',
      required: 'Required',
      send: 'Send',
    },
  };

</script>


<style lang="stylus" scoped>

  .instructions
    margin: 1em 0

  .buttons
    text-align: right
    margin-top: 1em

  button[type='submit']
    margin-right: 0

</style>
