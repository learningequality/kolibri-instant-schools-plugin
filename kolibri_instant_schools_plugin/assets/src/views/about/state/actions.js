import { PageNames } from '../constants';
import { createTranslator } from 'kolibri.utils.i18n';

const translator = createTranslator('aboutPageTitles', {
  aboutPageTitle: 'About',
  faqPageTitle: 'FAQ',
});

function showAbout(store) {
  store.dispatch('SET_PAGE_NAME', PageNames.ABOUT);
  store.dispatch('CORE_SET_TITLE', translator.$tr('aboutPageTitle'));
  store.dispatch('CORE_SET_ERROR', null);
}

function showFaq(store) {
  store.dispatch('SET_PAGE_NAME', PageNames.FAQ);
  store.dispatch('CORE_SET_TITLE', translator.$tr('faqPageTitle'));
  store.dispatch('CORE_SET_ERROR', null);
}

export { showAbout, showFaq };
