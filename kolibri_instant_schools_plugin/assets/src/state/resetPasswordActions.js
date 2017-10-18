// send phone number and get response
import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';

export function requestResetToken(store, { phoneNumber }) {
  return httpClient({
    path: urls['kolibri:user:passwordresettoken_list'](),
    method: 'POST',
    entity: {
      phone: phoneNumber,
    },
  });
}

export function getTokenStatus(store, { token, phoneNumber }) {
  return Promise.resolve();
}

export function updatePassword(store, { password }) {
  return Promise.resolve();
}
