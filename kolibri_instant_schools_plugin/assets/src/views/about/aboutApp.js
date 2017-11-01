import { showAbout, showFaq } from './state/actions';

import KolibriModule from 'kolibri_module';
import { PageNames } from './constants';
import RootVue from './views';
import Vue from 'kolibri.lib.vue';
import router from 'kolibri.coreVue.router';
import store from './state/store';
import { getCurrentSession } from 'kolibri.coreVue.vuex.actions';

class AboutModule extends KolibriModule {
  ready() {
    getCurrentSession(store).then(() => {
      const routes = [
        {
          name: PageNames.ABOUT,
          path: '/',
          handler: () => {
            showAbout(store);
          },
        },
        {
          name: PageNames.FAQ,
          path: '/faq',
          handler: () => {
            showFaq(store);
          },
        },
        {
          path: '*',
          redirect: '/',
        },
      ];

      this.rootvue = new Vue({
        el: 'rootvue',
        name: 'AboutRoot',
        render: createElement => createElement(RootVue),
        router: router.init(routes),
      });
    });
  }
}

export default new AboutModule();
