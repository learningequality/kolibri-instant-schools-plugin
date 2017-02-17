<template>

  <div :style="pageHeight" class="signup-page">

    <form class="signup-form" :style="wideWidth" ref="form" @submit.prevent="signUp">
      <h1 class="signup-title">{{ $tr('createAccount') }}</h1>

      <ui-textbox
        :placeholder="$tr('enterName')"
        :label="$tr('name')"
        :aria-label="$tr('name')"
        v-model="name"
        autocomplete="name"
        autofocus
        required
        id="name"
        type="text" />

      <ui-textbox
        :placeholder="$tr('enterUsername')"
        :label="$tr('username')"
        :aria-label="$tr('username')"
        v-model="username"
        autocomplete="username"
        required
        id="username"
        type="text" />

      <ui-textbox
        id="password"
        type="password"
        :placeholder="$tr('enterPassword')"
        :aria-label="$tr('password')"
        :label="$tr('password')"
        v-model="password"
        autocomplete="new-password"
        required />

      <ui-textbox
        id="confirmed-password"
        type="password"
        :placeholder="$tr('confirmPassword')"
        :aria-label="$tr('confirmPassword')"
        :label="$tr('confirmPassword')"
        v-model="confirmed_password"
        autocomplete="new-password"
        required />

      <icon-button id="submit" :primary="true" text="Finish" type="submit" />

      <p v-if="signUpError" class="signup-error">{{ $tr('signUpError') }}</p>

      <!-- Need terms of service thing -->
    </form>

  </div>

</template>


<script>

  const actions = require('../../actions');
  const responsiveWindow = require('kolibri.coreVue.mixins.responsiveWindow');

  module.exports = {
    name: 'Sign-Up-Page',
    $trNameSpace: 'signUpPage',
    $trs: {
      createAccount: 'Create an Account',
      name: 'Name',
      enterName: 'Enter Name',
      username: 'Username',
      enterUsername: 'Enter Username',
      password: 'Password',
      enterPassword: 'Enter Password',
      confirmPassword: 'Confirm Password',
      signUpError: 'That username already exists. Try a different username.',
    },
    components: {
      'icon-button': require('kolibri.coreVue.components.iconButton'),
      'ui-textbox': require('keen-ui/src/UiTextbox'),
    },
    computed: {
      wideWidth() {
        const width = 0.25 * this.windowSize.width;
        return {
          width: `${width}px`,
        };
      },
      pageHeight() {
        const height = this.windowSize.height;
        return {
          height: `${height}px`,
        };
      },
    },
    data: () => ({
      name: '',
      username: '',
      password: '',
      confirmed_password: '',
    }),
    methods: {
      signUp() {
        this.signUpAction({
          full_name: this.name,
          username: this.username,
          password: this.password,
        });
      },
    },
    vuex: {
      getters: {
        signUpError: state => state.core.signUpError === 400,
      },
      actions: {
        signUpAction: actions.signUp,
      },
    },
    mixins: [responsiveWindow],
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  .signup-page
    position: relative
    width: 100%

  .signup-title
    text-align: center


  .signup-form
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%)

  #submit
    width: 100%

  .signup-error
    color: red

</style>
