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

    <div class="center">
      <KRouterLink
        appearance="raised-button"
        :text="$tr('viewFaq')"
        :to="faqRoute"
      />

      <a :href="learnRoute">
        <KButton
          :text="$tr('startLearning')"
          :primary="true"
          :raised="true"
        />
      </a>
    </div>
  </KPageContainer>
</template>


<script>

  import throttle from 'lodash/throttle';
  import { PageNames } from '../../../constants';

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
        return '/learn';
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
    text-align: center;
  }

</style>
