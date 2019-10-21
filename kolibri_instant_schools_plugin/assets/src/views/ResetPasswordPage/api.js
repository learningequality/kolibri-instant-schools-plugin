import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';

export function getTokenStatus({ token, phoneNumber }) {
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

export function updatePassword({ password, token, phone }) {
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
