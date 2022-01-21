<template>
  <KPageContainer>
    <KRouterLink
      ref="backButton"
      appearance="raised-button"
      :text="$tr('back')"
      :to="aboutRoute"
    />

    <iframe
      ref="iframe"
      width="100%"
      frameborder="0"
      :src="faqSrc"
      :height="height"
      @load="resizeIframe"
    >
    </iframe>

    <KButton
      :text="$tr('toTop')"
      :primary="true"
      :raised="true"
      class="to-top-button"
      :class="{ 'to-top-button-visible': btnIsVisible }"
      @click="goToTop"
    />
  </KPageContainer>
</template>


<script>

  import throttle from 'lodash/throttle';
  import { PageNames } from '../../../constants';

  export default {
    name: 'FAQPage',
    $trs: {
      back: 'Back to about',
      toTop: 'Back to top',
    },
    data() {
      return {
        height: 5000,
        btnIsVisible: false,
      };
    },
    computed: {
      aboutRoute() {
        return { name: PageNames.ABOUT };
      },
      faqSrc() {
        return '/content/databases/about/faq.html';
      },
    },
    mounted() {
      this.resizeIframe();
      window.addEventListener('resize', this.throttleResizeIframe);
      document
        .querySelector('.main-wrapper')
        .addEventListener('scroll', this.throttleUpdateBtnVisibility);
      // scroll to top
      document.querySelector('.main-wrapper').scrollTop = 0;
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.throttleResizeIframe);
      document
        .querySelector('.main-wrapper')
        .removeEventListener('scroll', this.throttleUpdateBtnVisibility);
    },
    methods: {
      updateBtnVisibility() {
        this.btnIsVisible = document.querySelector('.main-wrapper').scrollTop > 500;
      },
      throttleUpdateBtnVisibility: throttle(function() {
        this.updateBtnVisibility();
      }, 100),
      goToTop() {
        this.$refs.backButton.$el.scrollIntoView(false);
      },
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

  .faq-page {
    padding-bottom: 32px;
  }

  .to-top-button {
    position: fixed;
    right: 32px;
    bottom: 32px;
    display: none;
  }

  .to-top-button-visible {
    display: block;
  }

</style>
