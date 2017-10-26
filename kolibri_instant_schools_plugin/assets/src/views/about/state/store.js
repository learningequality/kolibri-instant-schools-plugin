import Vuex from 'kolibri.lib.vuex';
import * as coreStore from 'kolibri.coreVue.vuex.store';

const initialState = {
  pageName: undefined,
};

const mutations = {
  SET_PAGE_NAME(state, name) {
    state.pageName = name;
  },
};

Object.assign(initialState, coreStore.initialState);
Object.assign(mutations, coreStore.mutations);

export default new Vuex.Store({
  state: initialState,
  mutations,
});
