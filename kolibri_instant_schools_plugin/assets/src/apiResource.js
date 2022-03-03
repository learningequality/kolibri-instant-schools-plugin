import { Resource } from 'kolibri.lib.apiResource';

export const SignUpResource = new Resource({
  name: 'signup',
});

export const PhoneNumberSignUpResource = new Resource({
  name: 'phonesignup',
  namespace: 'kolibri_instant_schools_plugin',
});

export const FacilityUserProfileResource = new Resource({
  name: 'facilityuserprofile',
  namespace: 'kolibri_instant_schools_plugin',
});
