<template>

  <KPageContainer>
    <iframe
      ref="iframe"
      width="100%"
      frameborder="0"
      :src="aboutSrc"
      :height="height"
      @load="resizeIframe"
    >
    </iframe>

    <KButtonGroup class="center">
      <KRouterLink
        appearance="raised-button"
        :text="$tr('viewFaq')"
        :to="faqRoute"
      />

      <KExternalLink
        appearance="raised-button"
        :href="learnRoute"
        :text="$tr('startLearning')"
        :primary="true"
        :raised="true"
      />
    </KButtonGroup>
  </KPageContainer>

</template>


<script>

  import throttle from 'lodash/throttle';
  import { PageNames } from '../../../constants';
  import urls from 'kolibri.urls';

  export default {
    name: 'AboutPage',
    $trs: {
      viewFaq: 'More information',
      startLearning: 'Start learning',
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
        return urls['kolibri:kolibri.plugins.learn:learn']();
      },
      aboutSrc() {
        return '/content/databases/about/about.html';
      },
    },
    mounted() {
      this.resizeIframe();
      window.addEventListener('resize', this.throttleResizeIframe);
      // scroll to top
      document.querySelector('.main-wrapper').scrollTop = 0;
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


<style lang="scss" scoped>

  @import '~kolibri-design-system/lib/styles/definitions';

  .center {
    // Makes children elements which are inline-block centered
    display: block;
    text-align: center;
  }

</style>
