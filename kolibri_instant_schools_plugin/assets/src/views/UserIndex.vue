<template>
  <CoreBase
    :immersivePage="pageName === PageNames.SIGN_UP"
    immersivePagePrimary
    :immersivePageRoute="{ name: PageNames.SIGN_IN }"
    :appBarTitle="appBarTitle"
    :fullScreen="pageName === PageNames.SIGN_IN"
  >
    <component :is="currentPage" />
  </CoreBase>
</template>


<script>

  import { mapState } from 'vuex';
  import CoreBase from 'kolibri.coreVue.components.CoreBase';
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
      CoreBase,
    },
    computed: {
      ...mapState(['pageName']),
      appBarTitle() {
        if (this.pageName === PageNames.PROFILE) {
          return this.$tr('userProfileTitle');
        } else if (this.pageName === PageNames.SIGN_UP) {
          return translator.$tr('createAccount');
        } else if (this.pageName == PageNames.SELECT_PROFILE) {
          return 'Instant Schools';
        }
        return this.$tr('userSignInTitle');
      },
      currentPage() {
        return pageNameComponentMap[this.pageName] || null;
      },
      PageNames() {
        return PageNames;
      },
    },
    $trs: {
      userProfileTitle: 'Profile',
      userSignInTitle: 'Sign in',
      about: 'About',
    },
  };

</script>


<style lang="scss" scoped></style>
