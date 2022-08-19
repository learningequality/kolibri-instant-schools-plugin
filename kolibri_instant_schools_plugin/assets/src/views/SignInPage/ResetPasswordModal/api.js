import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';

export function createResetToken({ phoneNumber }) {
  const url = urls['kolibri:kolibri_instant_schools_plugin:passwordresettoken_list']();
  return httpClient({
    url,
    data: {
      phone: phoneNumber,
    },
  }).then(response => {
    if (response.status.code !== 201) {
      return Promise.reject(response);
    }
    return response;
  });
}
