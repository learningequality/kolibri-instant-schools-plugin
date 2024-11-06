<template>

  <component
    :is="currentPage"
    :title="appBarTitle"
  />

</template>


<script>

  import { mapState } from 'vuex';
  import AppBarPage from 'kolibri.coreVue.components.AppBarPage';
  import { crossComponentTranslator } from 'kolibri.utils.i18n';
  import { PageNames } from '../constants';
  import SignInPage from './SignInPage';
  import SignUpPage from './SignUpPage';
  import ProfilePage from './ProfilePage';
  import ResetPasswordPage from './ResetPasswordPage';
  import SelectProfilePage from './SelectProfilePage';

  const translator = crossComponentTranslator(SignUpPage);

  const pageNameComponentMap = {
    [PageNames.SIGN_IN]: SignInPage,
    [PageNames.SIGN_UP]: SignUpPage,
    [PageNames.PROFILE]: ProfilePage,
    [PageNames.SELECT_PROFILE]: SelectProfilePage,
    [PageNames.RESET_PASSWORD]: ResetPasswordPage,
  };

  export default {
    name: 'UserIndex',
    components: {
      AppBarPage,
    },
    computed: {
      ...mapState(['pageName']),
      appBarTitle() {
        if (this.pageName === PageNames.PROFILE) {
          return this.$tr('userProfileTitle');
        } else if (this.pageName === PageNames.SIGN_UP) {
          // eslint-disable-next-line kolibri/vue-no-undefined-string-uses
          return translator.$tr('createAccount');
        } else if (this.pageName == PageNames.SELECT_PROFILE) {
          return 'Instant Schools';
        }
        return this.$tr('userSignInTitle');
      },
      currentPage() {
        return pageNameComponentMap[this.pageName] || null;
      },
    },
    $trs: {
      userProfileTitle: 'Account',
      userSignInTitle: 'Sign in',
    },
  };

</script>


<style lang="scss" scoped></style>
