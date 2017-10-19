<template>

  <div>
    <iframe
      width="100%"
      frameborder
      :src="aboutSrc"
    >
    </iframe>

    <router-link :to="faqRoute">
      <k-button
        :text="$tr('viewFaq')"
        :primary="false"
        :raised="true"
      />
    </router-link>

    <br>

    <a :href="learnRoute">
      <k-button
        :text="$tr('startLearning')"
        :primary="true"
        :raised="true"
      />
    </a>

  </div>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';
  import { PageNames } from '../../constants';

  export default {
    name: 'aboutPage',

    $trs: {
      viewFaq: 'View FAQ',
      startLearning: 'Start learning',
    },

    components: {
      kButton,
    },

    computed: {
      faqRoute() {
        return { name: PageNames.FAQ };
      },
      learnRoute() {
        return '/learn';
      },
      aboutSrc() {
        return '/content/databases/about/about.html';
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

</style>
