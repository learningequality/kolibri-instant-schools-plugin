import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';

export function requestResetToken(store, { phoneNumber }) {
  return httpClient({
    path: urls['kolibri:user:passwordresettoken_list'](),
    method: 'POST',
    entity: {
      phone: phoneNumber,
    },
  }).then(response => {
    const { code } = response.status;
    if (code === 400 || code === 500) {
      return Promise.reject(response);
    }
    return response;
  });
}

export function getTokenStatus(store, { token, phoneNumber }) {
  return Promise.resolve();
}

export function updatePassword(store, { password }) {
  return Promise.resolve();
}
