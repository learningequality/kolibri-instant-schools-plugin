import client from 'kolibri.client';
import urls from 'kolibri.urls';
import { PageNames } from '../../constants';

export function showSelectProfilePage(store, params) {
  const { phone, password, facility } = params;
  return client({
      url: `${urls['kolibri:kolibri_instant_schools_plugin:phoneaccountprofile_list']()}?password=${password}&phone=${phone}`,
      method: 'GET',
      data: {
        password,
        phone,
      },
    })
    .then(response => {
      if (response.status !== 200) {
        // Handle error on login page
        return Promise.reject(response);
      }
      // On success, go to new page
      store.dispatch(
        'resetAndSetPageName',
        {
          pageName: PageNames.SELECT_PROFILE,
        },
        { root: true }
      );
      return store.commit('SET_STATE', {
        facility,
        phone,
        password,
        profiles: response.entity,
      });
    });
}

export function createProfile(store, profileName) {
  const { phone, password } = store.state;
  return client({
    url: urls['kolibri:kolibri_instant_schools_plugin:phoneaccountprofile_list'](),
    method: 'POST',
    data: {
      full_name: profileName,
      password,
      phone,
    },
  }).then(response => {
    if (response.status !== 201) {
      return Promise.reject(response);
    }
    return store.commit('ADD_PROFILE', {
      full_name: profileName,
      username: response.entity,
      isNew: true,
    });
  });
}
