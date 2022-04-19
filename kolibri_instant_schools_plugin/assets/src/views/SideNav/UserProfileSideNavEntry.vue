<template>

  <CoreMenuOption
    :label="$tr('account')"
    :link="url"
  >
    <mat-svg
      slot="icon"
      name="account_circle"
      category="action"
    />
  </CoreMenuOption>

</template>


<script>

  import { UserKinds, NavComponentSections } from 'kolibri.coreVue.vuex.constants';
  import CoreMenuOption from 'kolibri.coreVue.components.CoreMenuOption';
  import navComponents from 'kolibri.utils.navComponents';
  import urls from 'kolibri.urls';

  const component = {
    name: 'UserProfileSideNavEntry',
    components: {
      CoreMenuOption,
    },
    $trs: {
      account: 'Account',
    },
    computed: {
      url() {
        return urls['kolibri:kolibri.plugins.userProfile:userProfile']();
      },
    },
    role: UserKinds.LEARNER,
    priority: 10,
    section: NavComponentSections.ACCOUNT,
  };

  navComponents.register(component);

  export default component;

</script>
