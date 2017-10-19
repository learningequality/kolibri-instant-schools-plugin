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
        height: null,
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
      window.addEventListener('resize', this.resizeIframe);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.resizeIframe);
    },
    methods: {
      goToTop() {
        this.$refs.backButton.$el.scrollIntoView();
      },
      resizeIframe() {
        this.height = this.$refs.iframe.contentWindow.document.body.scrollHeight;
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

</style>
