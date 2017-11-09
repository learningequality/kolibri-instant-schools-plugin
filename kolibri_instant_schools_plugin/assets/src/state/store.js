import Vuex from 'kolibri.lib.vuex';
import * as coreStore from 'kolibri.coreVue.vuex.store';

/**
 ** pageState schemas
 **/

const initialState = {
  pageName: undefined,
  pageState: {},
  facility: undefined,
};

const mutations = {
  SET_PAGE_NAME(state, name) {
    state.pageName = name;
  },
  SET_PAGE_STATE(state, pageState) {
    state.pageState = pageState;
  },
  // Account Page Mutations
  SET_NAME_BUSY(state, isBusy) {
    state.pageState.nameBusy = isBusy;
  },
  SET_NAME_SUCCESS(state, isSuccessful) {
    state.pageState.nameSuccess = isSuccessful;
  },
  SET_NAME_ERROR(state, isError, errorMessage) {
    state.pageState.nameError = isError;
    state.pageState.nameErrorMessage = errorMessage;
  },
  SET_PASSWORD_BUSY(state, isBusy) {
    state.pageState.passwordBusy = isBusy;
  },
  SET_PASSWORD_SUCCESS(state, isSuccessful) {
    state.pageState.passwordSuccess = isSuccessful;
  },
  SET_PASSWORD_ERROR(state, isError, errorMessage) {
    state.pageState.passwordError = isError;
    state.pageState.passwordErrorMessage = errorMessage;
  },
  SHOW_PASSWORD_MODAL(state, show) {
    state.pageState.showPasswordModal = show;
  },
  // Sign Up Page Mutations
  SET_SIGN_UP_BUSY(state, isBusy) {
    state.pageState.busy = isBusy;
  },
  SET_SIGN_UP_ERROR(state, errorCode, errorMessage) {
    state.pageState.errorCode = errorCode;
    state.pageState.errorMessage = errorMessage;
  },
  ADD_PROFILE(state, newProfile) {
    if (state.pageState.profiles) {
      state.pageState.profiles.push(newProfile);
    }
  },
};

// assigns core state and mutations
Object.assign(initialState, coreStore.initialState);
Object.assign(mutations, coreStore.mutations);

const store = new Vuex.Store({
  state: initialState,
  mutations,
});

export { store as default };
