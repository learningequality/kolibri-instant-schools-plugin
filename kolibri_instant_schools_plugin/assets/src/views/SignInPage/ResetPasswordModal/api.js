import { httpClient } from 'kolibri.client';
import urls from 'kolibri.urls';

export function createResetToken({ phoneNumber }) {
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
