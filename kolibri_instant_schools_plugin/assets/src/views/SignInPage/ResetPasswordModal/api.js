import client from 'kolibri.client'
import urls from 'kolibri.urls';

export function createResetToken({ phoneNumber, phonePrefix }) {
  return client({
    url: urls['kolibri:kolibri_instant_schools_plugin:passwordresettoken_list'](),
    method: 'POST',
    data: {
      phone: phoneNumber,
      prefix: phonePrefix,
    },
  }).then(response => {
    if (response.status.code !== 201) {
      return Promise.reject(response);
    }
    return response;
  });
}
