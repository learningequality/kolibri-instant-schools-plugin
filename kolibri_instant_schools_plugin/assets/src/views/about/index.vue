<template>

  <AppBarPage
    :navBarNeeded="true"
    :appBarTitle="appBarTitle"
  >
    <component :is="currentPage" />
  </AppBarPage>

</template>


<script>

  import { mapState } from 'vuex';
  import AppBarPage from 'kolibri.coreVue.components.AppBarPage';
  import { PageNames } from '../../constants';
  import AboutPage from './AboutPage';
  import FAQPage from './FAQPage';

  const pageNameComponentMap = {
    [PageNames.ABOUT]: AboutPage,
    [PageNames.FAQ]: FAQPage,
  };

  export default {
    // eslint-disable-next-line kolibri/vue-filename-and-component-name-match
    name: 'About',
    components: {
      AppBarPage,
      AboutPage,
      FAQPage,
    },
    computed: {
      ...mapState(['pageName']),
      appBarTitle() {
        return this.$tr('aboutTitle');
      },
      currentPage() {
        return pageNameComponentMap[this.pageName] || null;
      },
    },
    $trs: { aboutTitle: 'About' },
  };

</script>
