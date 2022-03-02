<template>

  <CoreBase
    :navBarNeeded="true"
    :appBarTitle="appBarTitle"
  >
    <component
      :is="currentPage"
    />
  </CoreBase>

</template>


<script>

  import { mapState } from 'vuex';
  import CoreBase from 'kolibri.coreVue.components.CoreBase';
  import { PageNames } from '../../constants';
  import AboutPage from './AboutPage';
  import FAQPage from './FAQPage';

  const pageNameComponentMap = {
    [PageNames.ABOUT]: AboutPage,
    [PageNames.FAQ]: FAQPage,
  };

  export default {
    $trs: { aboutTitle: 'About' },
    name: 'About',
    components: {
      CoreBase,
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
  };

</script>
