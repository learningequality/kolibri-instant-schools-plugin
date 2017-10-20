<template>

  <div>
    <h1>{{ resetPasswordHeader }}</h1>

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
    computed: {
    },
    methods: {
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


<style lang="stylus" scoped></style>
