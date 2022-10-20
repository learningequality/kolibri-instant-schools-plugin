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
      <KSelect
        v-model="selectedPrefix"
        :label="phonePrefixOptions.find(o => o.value == selectedPrefix)"
        :options="phonePrefixOptions"
        @change="s => selectedPrefix = s"
      />
      <KTextbox
        ref="phoneNumber"
        v-model="phoneNumber"
        :autofocus="true"
        :label="$tr('enterPhoneNumber')"
        :invalid="!phoneNumberIsValid"
        :invalidText="$tr('required')"
        :disabled="disabled"
      />
      <KButtonGroup style="float: right">
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
      </KButtonGroup>
    </form>
  </div>

</template>


<script>

  import UiAlert from 'keen-ui/src/UiAlert';
  import plugin_data from 'plugin_data';
  import { countryCodesAndPrefixes } from './country_phone_prefixes.js';

  /**
   * Here we get the JSON for all country codes and create a list of options
   * that are sorted so that this country's code is at the top, the other OpCos
   * follow and the rest of the country codes are available after that.
   */

  const OPCO_COUNTRY_CODES = ['DRC','TZ','GH','MZ'];

  const OPCO_PHONE_PREFIXES = countryCodesAndPrefixes.reduce((acc, val) => {
    var countryCode = val["code"];
    if (OPCO_COUNTRY_CODES.includes(countryCode)) {
      acc[countryCode] = val["dial_code"]
    }
    return acc;
  }, {})

  const CURRENT_COUNTRY_PREFIX = countryCodesAndPrefixes.find(o => o.code == plugin_data["COUNTRY_CODE"]).dial_code;

  // Sorted so that all of the OPCO codes sort to the top
  const PHONE_PREFIX_OPTIONS = countryCodesAndPrefixes.map(codeObj => {
    // create object that maps code (country code) to a pretty version for the select label
    var { dial_code, name, code } = codeObj;
    var label = `${dial_code} ${name} (${code})`;
    return { label, value: dial_code };
  }).sort((a,b) => { // Then custom on top of that
    if(a.value === CURRENT_COUNTRY_PREFIX) {
        // The current country's code is always #1
        return -1;
      } else if(Object.values(OPCO_PHONE_PREFIXES).includes(a.value) && b.value !== CURRENT_COUNTRY_PREFIX) {
        // Other proper OPCO codes are next
        return -1;
      }
      return 0;
    }
  )

  export default {
    name: 'PhoneNumberForm',
    components: {
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
        selectedPrefix: PHONE_PREFIX_OPTIONS[0]
      };
    },
    computed: {
      phoneNumberIsValid() {
        if (this.phoneNumberShouldValidate) {
          return this.phoneNumber !== '';
        }
        return true;
      },
      phonePrefixOptions() {
        return PHONE_PREFIX_OPTIONS;
      }
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
          this.$emit('submit', { phoneNumber: this.phoneNumber, phonePrefix: this.selectedPrefix.value });
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

</style>
