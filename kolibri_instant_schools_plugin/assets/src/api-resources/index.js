const kolibri = require('kolibri');
const Resource = require('kolibri/core/assets/src/api-resource.js').Resource;

class PhoneNumberSignUpResource extends Resource {
  static resourceName() {
    return 'kolibri:user:phonesignup';
  }
}

module.exports = {PhoneNumberSignUpResource};
