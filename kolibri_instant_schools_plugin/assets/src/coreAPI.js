import theme from './styles/theme.styl';
import keenVars from './styles/keen.scss';
import sideNav from './views/side-nav';

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
