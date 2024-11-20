import { UserKinds, NavComponentSections } from 'kolibri.coreVue.vuex.constants';
import registerNavItem from 'kolibri.utils.registerNavItem';
import urls from 'kolibri.urls';
import { createTranslator } from 'kolibri.utils.i18n';

const translator = createTranslator('LoginSideNavEntry', {
  signIn: 'Sign in',
});

registerNavItem({
  get url() {
    return urls['kolibri:kolibri_instant_schools_plugin:instant_schools_auth']();
  },
  get label() {
    return translator.$tr('signIn');
  },
  icon: 'login',
  role: UserKinds.ANONYMOUS,
  section: NavComponentSections.ACCOUNT,
});
