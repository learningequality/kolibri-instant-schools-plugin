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
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.throttleResizeIframe);
    },
    methods: {
      goToTop() {
        this.$refs.backButton.$el.scrollIntoView();
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

</style>
