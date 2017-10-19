<template>

  <div>
    <iframe
      ref="iframe"
      width="100%"
      frameborder="0"
      :src="aboutSrc"
      :height="height"
      @load="resizeIframe"
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
    data() {
      return {
        height: null,
      };
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
    mounted() {
      this.resizeIframe();
      window.addEventListener('resize', this.resizeIframe);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.resizeIframe);
    },
    methods: {
      resizeIframe() {
        this.height = this.$refs.iframe.contentWindow.document.body.scrollHeight;
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

</style>
