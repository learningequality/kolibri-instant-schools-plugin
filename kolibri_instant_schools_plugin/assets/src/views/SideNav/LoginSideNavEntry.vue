<template>

  <CoreMenuOption
    icon="login"
    :label="$tr('signIn')"
    :link="url"
  >
    <mat-svg
      slot="icon"
      name="exit_to_app"
      category="action"
      :class="{ 'rtl-icon': isRtl }"
    />
  </CoreMenuOption>

</template>


<script>

  import { UserKinds, NavComponentSections } from 'kolibri.coreVue.vuex.constants';
  import CoreMenuOption from 'kolibri.coreVue.components.CoreMenuOption';
  import navComponents from 'kolibri.utils.navComponents';
  import urls from 'kolibri.urls';

  const component = {
    name: 'LoginSideNavEntry',
    components: {
      CoreMenuOption,
    },
    $trs: {
      signIn: 'Sign in',
    },
    computed: {
      url() {
        return urls['kolibri:kolibri_instant_schools_plugin:instant_schools_auth']();
      },
    },
    role: UserKinds.ANONYMOUS,
    priority: 10,
    section: NavComponentSections.ACCOUNT,
  };

  navComponents.register(component);

  export default component;

</script>
