<template>

  <div>
    <h1>{{ $tr('resetPasswordHeader') }}</h1>

    <form @submit.prevent="submit">
      <!-- Duplicated in Profile Page -->
      <k-textbox
        ref="newPw"
        type="password"
        :label="$tr('newPw')"
        :disabled="busy"
        :maxlength="120"
        :invalid="!newPwIsValid"
        @blur="newPwBlurred = true"
        v-model="newPw"
      />
      <k-textbox
        ref="newPwConfirm"
        type="password"
        :label="$tr('newPwConfirm')"
        :disabled="busy"
        :maxlength="120"
        :invalid="!newPwConfirmIsValid"
        :invalidText="$tr('passwordsDoNotMatch')"
        @blur="newPwConfirmBlurred = true"
        v-model="newPwConfirm"
      />

      <k-button
        type="submit"
        :text="$tr('saveButton')"
        :primary="true"
      />
    </form>
  </div>

</template>


<script>

  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import kButton from 'kolibri.coreVue.components.kButton';

  export default {
    components: {
      kButton,
      kTextbox,
    },
    data() {
      return {
        newPw: '',
        newPwConfirm: '',
        newPwBlurred: false,
        newPwConfirmBlurred: false,
        busy: false,
      };
    },
    computed: {
      newPwIsValid() {
        return false;
      },
      newPwConfirmIsValid() {
        return false;
      },
      newPwShouldValidate() {},
      newPwConfirmShouldValidate() {},
    },
    methods: {
      submit() {},
    },
    vuex: {
      getters: {},
      actions: {},
    },
    $trs: {
      newPw: 'New password',
      newPwConfirm: 'New password again',
      passwordsDoNotMatch: 'Passwords do not match',
      resetPasswordHeader: 'Reset password',
      saveButton: 'Save',
    },
  };

</script>


<style lang="stylus" scoped>

  button[type='submit']
    margin-left: 0

</style>
