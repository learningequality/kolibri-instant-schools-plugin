<template>
  <CoreMenuOption
    :label="$tr('about')"
    :link="url"
  >
    <mat-svg
      slot="icon"
      name="info_outline"
      category="action"
      :class="{ 'rtl-icon': isRtl }"
    />
  </CoreMenuOption>
</template>


<script>

  import { NavComponentSections } from 'kolibri.coreVue.vuex.constants';
  import CoreMenuOption from 'kolibri.coreVue.components.CoreMenuOption';
  import navComponents from 'kolibri.utils.navComponents';
  import urls from 'kolibri.urls';

  const component = {
    name: 'AboutSideNavEntry',
    components: {
      CoreMenuOption,
    },
    $trs: {
      about: 'About',
    },
    computed: {
      url() {
        return urls['kolibri:about:about']();
      },
    },
    priority: 10,
    section: NavComponentSections.ACCOUNT,
  };

  navComponents.register(component);

  export default component;

</script>
