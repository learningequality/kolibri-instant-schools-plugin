import theme from './styles/theme.styl';
import keenVars from './styles/keen.scss';
import sideNav from './views/side-nav';
import appBar from 'kolibri.coreVue.components.appBar';

// overwrite username getter in appBar to show full_name
appBar.vuex.getters.username = state => state.core.session.full_name;

export default {
  styles: {
    theme,
    keenVars,
  },
  coreVue: {
    components: {
      sideNav,
    },
  },
};
