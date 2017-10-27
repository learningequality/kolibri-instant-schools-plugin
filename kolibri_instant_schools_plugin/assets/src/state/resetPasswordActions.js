import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';
import { PageNames } from '../constants';

export function showPasswordResetPage(store, params) {
  store.dispatch('SET_PAGE_NAME', PageNames.RESET_PASSWORD);
  store.dispatch('SET_PAGE_STATE', {
    token: params.token,
    phone: params.phone,
  });
  store.dispatch('CORE_SET_PAGE_LOADING', false);
}

export function createResetToken(store, { phoneNumber }) {
  return httpClient({
    path: urls['kolibri:user:passwordresettoken_list'](),
    method: 'POST',
    entity: {
      phone: phoneNumber,
    },
  }).then(response => {
    if (response.status.code !== 201) {
      return Promise.reject(response);
    }
    return response;
  });
}

export function getTokenStatus(store, { token, phoneNumber }) {
  return httpClient({
    path: `${urls['kolibri:user:passwordresettoken_list']()}${token}/?phone=${phoneNumber}`,
    method: 'GET',
  }).then(response => {
    if (response.status.code !== 200) {
      return Promise.reject(response);
    }
    return response;
  });
}

export function updatePassword(store, { password, token, phone }) {
  return httpClient({
    path: urls['kolibri:user:passwordchange_list'](),
    method: 'POST',
    entity: {
      password: encodeURIComponent(password),
      token,
      phone,
    },
  }).then(response => {
    if (response.status.code !== 200) {
      return Promise.reject(response);
    }
    return response;
  });
}
