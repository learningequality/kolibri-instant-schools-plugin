import router from 'kolibri.coreVue.router';
import RootVue from './views/UserIndex';
import routes from './routes';
import pluginModule from './modules/pluginModule';
import KolibriApp from 'kolibri_app';

class InstantSchoolsAuthModule extends KolibriApp {
  get stateSetters() {
    return [() => this.store.dispatch('setFacilitiesAndConfig')];
  }
  get routes() {
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

export default new InstantSchoolsAuthModule();
