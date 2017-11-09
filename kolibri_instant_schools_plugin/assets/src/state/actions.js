import { PageNames } from '../constants';
import * as coreActions from 'kolibri.coreVue.vuex.actions';
import { isUserLoggedIn } from 'kolibri.coreVue.vuex.getters';
import router from 'kolibri.coreVue.router';
import { FacilityResource } from 'kolibri.resources';
import { createTranslator } from 'kolibri.utils.i18n';
import { PhoneNumberSignUpResource, FacilityUserProfileResource } from '../api-resources';

const name = 'userPageTitles';

const messages = {
  userAccountPageTitle: 'User Account',
  userSignInPageTitle: 'User Sign In',
  userSignUpPageTitle: 'User Sign Up',
};

const translator = createTranslator(name, messages);

function redirectToHome() {
  window.location = '/';
}

function showRoot(store) {
  const userSignedIn = isUserLoggedIn(store.state);
  if (userSignedIn) {
    router.getInstance().replace({
      name: PageNames.ACCOUNT,
    });
    return;
  }
  router.getInstance().replace({
    name: PageNames.SIGN_IN,
  });
}

function showAccount(store) {
  const userSignedIn = isUserLoggedIn(store.state);
  if (!userSignedIn) {
    router.getInstance().replace({
      name: PageNames.SIGN_IN,
    });
    return;
  }
  store.dispatch('SET_PAGE_NAME', PageNames.ACCOUNT);
  store.dispatch('CORE_SET_PAGE_LOADING', false);
  store.dispatch('CORE_SET_ERROR', null);
  store.dispatch('CORE_SET_TITLE', translator.$tr('userAccountPageTitle'));
  const pageState = {
    nameBusy: false,
    nameSuccess: false,
    nameError: false,
    nameErrorMessage: '',
    passwordError: false,
    passwordBusy: false,
    passwordSuccess: false,
    passwordErrorMessage: '',
    showPasswordModal: false,
  };
  store.dispatch('SET_PAGE_STATE', pageState);
}

function _errorMessageHandler(apiError) {
  if (apiError.status.code === 400) {
    return Object.values(apiError.entity)[0][0];
  } else if (apiError.status.code === 403) {
    return apiError.entity[0];
  }
  return '';
}

function changeName(store, newName) {
  return FacilityUserProfileResource.getModel(store.state.core.session.user_id)
    .save({ full_name: newName })
    .then(
      () => {
        coreActions.getCurrentSession(store, true);
        store.dispatch('SET_NAME_SUCCESS', true);
        store.dispatch('SET_NAME_ERROR', false, '');
        store.dispatch('SET_NAME_BUSY', false);
      },
      error => {
        store.dispatch('SET_NAME_SUCCESS', false);
        store.dispatch('SET_NAME_ERROR', true, _errorMessageHandler(error));
        store.dispatch('SET_NAME_BUSY', false);
      }
    );
}

function changePassword(store, newPassword) {
  return FacilityUserProfileResource.getModel(store.state.core.session.user_id)
    .save({ password: newPassword })
    .then(
      () => {
        coreActions.getCurrentSession(store, true);
        store.dispatch('SET_PASSWORD_SUCCESS', true);
        store.dispatch('SET_PASSWORD_ERROR', false, '');
        store.dispatch('SET_PASSWORD_BUSY', false);
      },
      error => {
        store.dispatch('SET_PASSWORD_SUCCESS', false);
        store.dispatch('SET_PASSWORD_ERROR', true, _errorMessageHandler(error));
        store.dispatch('SET_PASSWORD_BUSY', false);
      }
    );
}

function resetNameState(store) {
  store.dispatch('SET_NAME_SUCCESS', false);
  store.dispatch('SET_NAME_ERROR', false, '');
  store.dispatch('SET_NAME_BUSY', false);
}

function _resetPasswordState(store) {
  store.dispatch('SET_PASSWORD_SUCCESS', false);
  store.dispatch('SET_PASSWORD_ERROR', false, '');
  store.dispatch('SET_PASSWORD_BUSY', false);
}

function showPasswordModal(store, show) {
  if (show) {
    _resetPasswordState(store);
  }
  store.dispatch('SHOW_PASSWORD_MODAL', show);
}

function showSignIn(store) {
  const userSignedIn = isUserLoggedIn(store.state);
  if (userSignedIn) {
    router.getInstance().replace({
      name: PageNames.ACCOUNT,
    });
    return;
  }
  store.dispatch('SET_PAGE_NAME', PageNames.SIGN_IN);
  store.dispatch('SET_PAGE_STATE', {});
  store.dispatch('CORE_SET_PAGE_LOADING', false);
  store.dispatch('CORE_SET_ERROR', null);
  store.dispatch('CORE_SET_LOGIN_ERROR', '');
  store.dispatch('CORE_SET_TITLE', translator.$tr('userSignInPageTitle'));
}

function resetSignUpState(store) {
  const pageState = {
    busy: false,
    errorCode: null,
    errorMessage: '',
  };

  store.dispatch('SET_PAGE_STATE', pageState);
}

function showSignUp(store) {
  const userSignedIn = isUserLoggedIn(store.state);
  if (userSignedIn) {
    router.getInstance().replace({
      name: PageNames.ACCOUNT,
    });
    return Promise.resolve();
  }
  const FacilityCollection = FacilityResource.getCollection().fetch();

  return FacilityCollection.then(facilities => {
    store.dispatch('CORE_SET_FACILITIES', facilities);
    store.dispatch('SET_PAGE_NAME', PageNames.SIGN_UP);
    store.dispatch('CORE_SET_PAGE_LOADING', false);
    store.dispatch('CORE_SET_ERROR', null);
    store.dispatch('CORE_SET_TITLE', translator.$tr('userSignUpPageTitle'));
    resetSignUpState(store);
  }).catch(error => coreActions.handleApiError(store, error));
}

function signUp(store, signUpCreds) {
  const signUpModel = PhoneNumberSignUpResource.createModel(signUpCreds);
  const signUpPromise = signUpModel.save(signUpCreds);

  resetSignUpState(store);
  store.dispatch('SET_SIGN_UP_BUSY', true);

  signUpPromise
    .then(() => {
      store.dispatch('SET_SIGN_UP_ERROR', null, '');
      // TODO: Better solution?
      window.location = '/about';
    })
    .catch(error => {
      function _errorMessageHandler(apiError) {
        if (apiError.status.code === 400 || apiError.status.code === 200) {
          return apiError.entity[0];
        }
        return '';
      }

      store.dispatch('SET_SIGN_UP_ERROR', error.status.code, _errorMessageHandler(error));
      store.dispatch('SET_SIGN_UP_BUSY', false);
    });
}

export {
  showRoot,
  showSignIn,
  showSignUp,
  signUp,
  resetSignUpState,
  showAccount,
  resetNameState,
  changeName,
  changePassword,
  showPasswordModal,
};
