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
  import throttle from 'lodash/throttle';

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
        height: 300,
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
      window.addEventListener('resize', this.throttleResizeIframe);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.throttleResizeIframe);
    },
    methods: {
      resizeIframe() {
        this.height = this.$refs.iframe.contentWindow.document.body.scrollHeight;
      },
      throttleResizeIframe: throttle(function() {
        this.resizeIframe();
      }, 100),
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

</style>
