<template>

  <div>
    <div class="instructions">
      {{ $tr('instructionsWillBeSent') }}
    </div>

    <ui-alert
      class="alert"
      v-if="phoneLookupFailed && !disabled"
      type="error"
      :dismissible="false"
    >
      {{ $tr('accountNotFound') }}
    </ui-alert>

    <form @submit.prevent="submitPhoneNumber">
      <k-textbox
        ref="phoneNumber"
        :autofocus="true"
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
  import uiAlert from 'keen-ui/src/UiAlert';

  export default {
    name: 'phoneNumberForm',
    components: {
      kButton,
      kTextbox,
      uiAlert,
    },
    props: {
      disabled: {
        type: Boolean,
        required: true,
      },
      phoneLookupFailed: {
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
          return this.phoneNumber !== '';
        }
        return true;
      },
    },
    watch: {
      phoneLookupFailed(val) {
        if (val) {
          this.$nextTick(() => {
            this.focusTextbox();
          });
        }
      },
    },
    methods: {
      submitPhoneNumber() {
        this.phoneNumberShouldValidate = true;
        if (this.phoneNumberIsValid) {
          this.$emit('submit', this.phoneNumber);
        } else {
          this.focusTextbox();
        }
      },
      focusTextbox() {
        this.$refs.phoneNumber.focus();
      },
    },
    $trs: {
      accountNotFound: 'No account was found for this phone number. Please try again.',
      cancel: 'Cancel',
      enterPhoneNumber: 'Enter your phone number',
      instructionsWillBeSent: 'Instructions will be sent to your phone.',
      required: 'Required',
      send: 'Send',
    },
  };

</script>


<style lang="stylus" scoped>

  .alert
    text-align: left

  .instructions
    text-align: left
    margin: 1em 0

  .buttons
    text-align: right
    margin-top: 1em

  button[type='submit']
    margin-right: 0

</style>
