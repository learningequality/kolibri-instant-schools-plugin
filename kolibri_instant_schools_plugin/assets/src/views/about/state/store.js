import Vuex from 'kolibri.lib.vuex';
import * as coreStore from 'kolibri.coreVue.vuex.store';

const initialState = {
  pageName: undefined,
  pageState: {},
};

const mutations = {
  SET_PAGE_NAME(state, name) {
    state.pageName = name;
  },
  SET_PAGE_STATE(state, pageState) {
    state.pageState = pageState;
  },
};

Object.assign(initialState, coreStore.initialState);
Object.assign(mutations, coreStore.mutations);

export default new Vuex.Store({
  state: initialState,
  mutations,
});
