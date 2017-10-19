<template>

  <div>

    <router-link :to="aboutRoute">
      <k-button
        :text="$tr('back')"
        :primary="false"
        :raised="true"
        ref="backButton"
      />
    </router-link>

    <iframe
      width="100%"
      frameborder
      :src="faqSrc"
    >
    </iframe>

    <br>

    <k-button
      :text="$tr('toTop')"
      :primary="true"
      :raised="true"
      @click="goToTop"
    />

  </div>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';
  import { PageNames } from '../../constants';

  export default {
    name: 'faqPage',

    $trs: {
      back: 'Back to about',
      toTop: 'Back to top',
    },

    components: {
      kButton,
    },

    computed: {
      aboutRoute() {
        return { name: PageNames.ABOUT };
      },
      faqSrc() {
        return '/content/databases/about/faq.html';
      },
    },

    methods: {
      goToTop() {
        this.$refs.backButton.$el.scrollIntoView();
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

</style>
