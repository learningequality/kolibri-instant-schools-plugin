import router from 'kolibri.coreVue.router';
import store from 'kolibri.coreVue.vuex.store';
import RootVue from './views/about';
import pluginModule from './modules/pluginModule';
import { PageNames } from './constants';
import KolibriApp from 'kolibri_app';

class AboutModule extends KolibriApp {
  get routes() {
    const routes = [
      {
        name: PageNames.ABOUT,
        path: '/',
        handler: () => {
          store.dispatch('resetAndSetPageName', {
            pageName: PageNames.ABOUT,
          });
        },
      },
      {
        name: PageNames.FAQ,
        path: '/faq',
        handler: () => {
          store.dispatch('resetAndSetPageName', {
            pageName: PageNames.FAQ,
          });
        },
      },
    ];
    return routes;
  }
  get RootVue() {
    return RootVue;
  }
  get pluginModule() {
    return pluginModule;
  }
  ready() {
    return super.ready().then(() => {
      router.afterEach((toRoute, fromRoute) => {
        this.store.dispatch('resetModuleState', { toRoute, fromRoute });
      });
    });
  }
}

export default new AboutModule();
