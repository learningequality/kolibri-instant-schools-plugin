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
      ref="iframe"
      width="100%"
      frameborder="0"
      :src="faqSrc"
      :height="height"
      @load="resizeIframe"
    >
    </iframe>

    <br>

    <k-button
      :text="$tr('toTop')"
      :primary="true"
      :raised="true"
      @click="goToTop"
      class="to-top-button"
      :class="{ 'to-top-button-visible': btnIsVisible }"
    />

  </div>

</template>


<script>

  import kButton from 'kolibri.coreVue.components.kButton';
  import { PageNames } from '../../constants';
  import throttle from 'lodash/throttle';

  export default {
    name: 'faqPage',
    $trs: {
      back: 'Back to about',
      toTop: 'Back to top',
    },
    components: {
      kButton,
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
        .querySelector('.content-container')
        .addEventListener('scroll', this.throttleUpdateBtnVisibility);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.throttleResizeIframe);
      document
        .querySelector('.content-container')
        .removeEventListener('scroll', this.throttleUpdateBtnVisibility);
    },
    methods: {
      updateBtnVisibility() {
        this.btnIsVisible = document.querySelector('.content-container').scrollTop > 500;
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


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  .to-top-button
    position: fixed
    right: 32px
    bottom: 32px
    display: none

  .to-top-button-visible
    display: block

</style>
