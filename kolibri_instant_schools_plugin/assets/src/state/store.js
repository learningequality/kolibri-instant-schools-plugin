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
  SET_PROFILE_NAME_BUSY(state, isBusy) {
    state.pageState.profileNameBusy = isBusy;
  },
  SET_PROFILE_NAME_SUCCESS(state, isSuccessful) {
    state.pageState.profileNameSuccess = isSuccessful;
  },
  SET_PROFILE_NAME_ERROR(state, isError, errorMessage) {
    state.pageState.profileNameError = isError;
    state.pageState.profileNameErrorMessage = errorMessage;
  },
  SET_ACCOUNT_PASSWORD_BUSY(state, isBusy) {
    state.pageState.accountPasswordBusy = isBusy;
  },
  SET_ACCOUNT_PASSWORD_SUCCESS(state, isSuccessful) {
    state.pageState.accountPasswordSuccess = isSuccessful;
  },
  SET_ACCOUNT_PASSWORD_ERROR(state, isError, errorMessage) {
    state.pageState.accountPasswordError = isError;
    state.pageState.accountPasswordErrorMessage = errorMessage;
  },
  SHOW_ACCOUNT_PASSWORD_MODAL(state, show) {
    state.pageState.showAccountPasswordModal = show;
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
