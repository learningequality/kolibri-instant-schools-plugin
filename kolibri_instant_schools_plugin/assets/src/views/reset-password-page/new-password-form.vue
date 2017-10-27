<template>

  <div>
    <h1>{{ $tr('resetPasswordHeader') }}</h1>

    <form @submit.prevent="submit">
      <k-textbox
        :autofocus="true"
        ref="newPw"
        type="password"
        :label="$tr('newPw')"
        :disabled="disable"
        :maxlength="120"
        :invalid="!newPwIsValid"
        :invalidText="$tr('required')"
        @blur="newPwBlurred = true"
        v-model="newPw"
      />
      <k-textbox
        ref="newPwConfirm"
        type="password"
        :label="$tr('newPwConfirm')"
        :disabled="disable"
        :maxlength="120"
        :invalid="!newPwConfirmIsValid"
        :invalidText="$tr('passwordsDoNotMatch')"
        @blur="newPwConfirmBlurred = true"
        v-model="newPwConfirm"
      />

      <k-button
        type="submit"
        :text="$tr('saveButton')"
        :disabled="disable"
        :primary="true"
      />
    </form>
  </div>

</template>


<script>

  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import kButton from 'kolibri.coreVue.components.kButton';

  export default {
    name: 'newPasswordForm',
    components: {
      kButton,
      kTextbox,
    },
    props: {
      disable: {
        type: Boolean,
        required: true,
      },
    },
    data() {
      return {
        formSubmitted: false,
        newPw: '',
        newPwConfirm: '',
        newPwBlurred: false,
        newPwConfirmBlurred: false,
      };
    },
    computed: {
      newPwIsValid() {
        if (this.newPwShouldValidate) {
          return this.newPw !== '';
        }
        return true;
      },
      newPwConfirmIsValid() {
        if (this.newPwConfirmShouldValidate) {
          return this.newPw === this.newPwConfirm;
        }
        return true;
      },
      newPwShouldValidate() {
        return this.newPwBlurred || this.formSubmitted;
      },
      newPwConfirmShouldValidate() {
        return (
          (this.newPw !== '' && this.newPwBlurred && this.newPwConfirm !== '') || this.formSubmitted
        );
      },
      formIsValid() {
        return this.newPwConfirmIsValid;
      },
    },
    methods: {
      submit() {
        this.formSubmitted = true;

        if (!this.newPwIsValid) {
          return this.$refs.newPw.focus();
        }

        if (!this.newPwConfirmIsValid) {
          return this.$refs.newPwConfirm.focus();
        }

        if (this.formIsValid) {
          return this.$emit('submit', this.newPw);
        }
      },
    },
    $trs: {
      newPw: 'New password',
      newPwConfirm: 'New password again',
      passwordsDoNotMatch: 'Passwords do not match',
      resetPasswordHeader: 'Reset password',
      required: 'Required',
      saveButton: 'Save',
    },
  };

</script>


<style lang="stylus" scoped>

  button[type='submit']
    margin-left: 0

</style>
