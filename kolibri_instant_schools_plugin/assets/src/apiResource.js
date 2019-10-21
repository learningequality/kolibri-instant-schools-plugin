import { Resource } from 'kolibri.lib.apiResource';

export const SignUpResource = new Resource({
  name: 'signup',
});

export const PhoneNumberSignUpResource = new Resource({
  name: 'phonesignup',
  namespace: 'user',
});

export const FacilityUserProfileResource = new Resource({
  name: 'facilityuserprofile',
  namespace: 'user',
});
