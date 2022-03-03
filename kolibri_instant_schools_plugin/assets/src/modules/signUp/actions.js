import CatchErrors from 'kolibri.utils.CatchErrors';
import { ERROR_CONSTANTS } from 'kolibri.coreVue.vuex.constants';
import { PhoneNumberSignUpResource } from '../../apiResource';
import urls from 'kolibri.urls';

export function signUpNewUser(store, signUpCreds) {
  store.commit('RESET_STATE');
  store.dispatch('SET_SIGN_UP_BUSY', true);
  PhoneNumberSignUpResource.saveModel({ data: signUpCreds })
    .then(() => {
      // TODO: Better solution?

      window.location = urls['kolibri:kolibri_instant_schools_plugin:instant_schools_about']();
    })
    .catch(error => {
      const errors = CatchErrors(error, [
        ERROR_CONSTANTS.USERNAME_ALREADY_EXISTS,
        ERROR_CONSTANTS.INVALID,
      ]);
      if (errors) {
        // We have recognized errors, set them on the errors state
        store.commit('SET_SIGN_UP_ERRORS', errors);
      } else {
        // No errors we recognize, flag there are unrecognized errors
        store.dispatch('handleApiError', error, { root: true });
      }
      store.commit('SET_SIGN_UP_BUSY', false);
    });
}
