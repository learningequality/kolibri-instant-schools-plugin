import * as actions from './actions';

export default {
  namespaced: true,
  state: {
    hasMultipleFacilities: null,
    facility: {},
    phone: null,
    password: null,
    profiles: [],
    token: null,
  },
  mutations: {
    SET_STATE(state, payload) {
      Object.assign(state, payload);
    },
    RESET_STATE(state) {
      state.hasMultipleFacilities = null;
    },
    ADD_PROFILE(state, newProfile) {
      if (state.profiles) {
        state.profiles.push(newProfile);
      }
    },
  },
  actions,
};
