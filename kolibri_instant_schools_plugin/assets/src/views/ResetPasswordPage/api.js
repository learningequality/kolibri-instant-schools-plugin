import client from 'kolibri.client';
import urls from 'kolibri.urls';

export function getTokenStatus({ token, phoneNumber }) {
  return client({
    url: `${urls['kolibri:kolibri_instant_schools_plugin:passwordresettoken_list']()}${token}/?phone=${phoneNumber}`,
    method: 'GET',
  }).then(response => {
    if (response.status !== 200) {
      return Promise.reject(response);
    }
    return response;
  });
}

export function updatePassword({ password, token, phone }) {
  return client({
    url: urls['kolibri:kolibri_instant_schools_plugin:passwordchange_list'](),
    method: 'POST',
    data: {
      password: encodeURIComponent(password),
      token,
      phone,
    },
  }).then(response => {
    if (response.status !== 200) {
      return Promise.reject(response);
    }
    return response;
  });
}
