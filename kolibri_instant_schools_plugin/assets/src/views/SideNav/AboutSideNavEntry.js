import { UserKinds, NavComponentSections } from 'kolibri.coreVue.vuex.constants';
import registerNavItem from 'kolibri.utils.registerNavItem';
import urls from 'kolibri.urls';
import { createTranslator } from 'kolibri.utils.i18n';

const translator = createTranslator('AboutSideNavEntry', {
  about: 'About',
});

registerNavItem({
  get url() {
    return urls['kolibri:kolibri_instant_schools_plugin:instant_schools_about']();
  },
  get label() {
    return translator.$tr('about');
  },
  icon: 'info',
  role: UserKinds.LEARNER,
  section: NavComponentSections.ACCOUNT,
});
