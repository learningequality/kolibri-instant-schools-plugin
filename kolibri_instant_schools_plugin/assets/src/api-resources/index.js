import { Resource } from 'kolibri.lib.apiResource';

class PhoneNumberSignUpResource extends Resource {
  static resourceName() {
    return 'kolibri:user:phonesignup';
  }
}
const phoneNumberSignUpResource = new PhoneNumberSignUpResource();

class FacilityUserProfileResource extends Resource {
  static resourceName() {
    return 'kolibri:user:facilityuserprofile';
  }
}
const facilityUserProfileResource = new FacilityUserProfileResource();

export {
  phoneNumberSignUpResource as PhoneNumberSignUpResource,
  facilityUserProfileResource as FacilityUserProfileResource,
};
