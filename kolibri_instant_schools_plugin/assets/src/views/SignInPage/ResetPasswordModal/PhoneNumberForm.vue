<template>
  <div>
    <div class="instructions">
      {{ $tr('instructionsWillBeSent') }}
    </div>

    <UiAlert
      v-if="phoneLookupFailed && !disabled"
      class="alert"
      type="error"
      :dismissible="false"
    >
      {{ $tr('accountNotFound') }}
    </UiAlert>

    <form @submit.prevent="submitPhoneNumber">
      <KTextbox
        ref="phoneNumber"
        v-model="phoneNumber"
        :autofocus="true"
        :label="$tr('enterPhoneNumber')"
        :invalid="!phoneNumberIsValid"
        :invalidText="$tr('required')"
        :disabled="disabled"
      />
      <div class="buttons">
        <KButton
          :text="$tr('cancel')"
          :primary="false"
          :disabled="disabled"
          @click="$emit('close')"
        />
        <KButton
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

  import KTextbox from 'kolibri.coreVue.components.KTextbox';
  import KButton from 'kolibri.coreVue.components.KButton';
  import UiAlert from 'keen-ui/src/UiAlert';

  export default {
    name: 'PhoneNumberForm',
    components: {
      KButton,
      KTextbox,
      UiAlert,
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


<style lang="scss" scoped>

  .alert {
    text-align: left;
  }

  .instructions {
    margin: 1em 0;
    text-align: left;
  }

  .buttons {
    margin-top: 1em;
    text-align: right;
  }

  button[type='submit'] {
    margin-right: 0;
  }

</style>
