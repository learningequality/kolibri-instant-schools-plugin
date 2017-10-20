<template>

  <div>
    <core-base
      :navBarNeeded="true"
      :topLevelPageName="topLevelPageName"
      :appBarTitle="appBarTitle"
    >
      <component
        :is="currentPage"
        class="page"
      />
    </core-base>
  </div>

</template>


<script>

  import coreBase from 'kolibri.coreVue.components.coreBase';
  import { TopLevelPageNames } from 'kolibri.coreVue.vuex.constants';
  import { PageNames } from '../constants';
  import store from '../state/store';
  import aboutPage from './about-page';
  import faqPage from './faq-page';

  export default {
    $trs: { userProfileTitle: 'Profile' },
    name: 'userPlugin',
    components: {
      coreBase,
      aboutPage,
      faqPage,
    },
    computed: {
      appBarTitle() {
        if (this.pageName === PageNames.ABOUT) {
          return this.$tr('userProfileTitle');
        } else if (this.pageName === PageNames.FAQ) {
          return this.$tr('userProfileTitle');
        }
        return '';
      },

      topLevelPageName() {
        return TopLevelPageNames.ABOUT;
      },

      currentPage() {
        if (this.pageName === PageNames.ABOUT) {
          return 'about-page';
        } else if (this.pageName === PageNames.FAQ) {
          return 'faq-page';
        }
        return null;
      },
    },
    vuex: {
      getters: {
        pageName: state => state.pageName,
      },
    },
    store,
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  .page
    background-color: $core-bg-light
    padding: 16px

</style>
