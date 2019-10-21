<template>
  <div>
    <h1>{{ header }}</h1>
    <p class="explanation">
      {{ explanation }}
    </p>
    <div v-if="showButton" class="buttons">
      <KButton
        :text="$tr('homeButton')"
        :primary="true"
        @click="$emit('close')"
      />
    </div>
  </div>
</template>


<script>

  import KButton from 'kolibri.coreVue.components.KButton';
  import { ResetPasswordStates as STATES } from '../../constants';

  export default {
    name: 'ResetPasswordPageStatus',
    components: {
      KButton,
    },
    props: {
      status: {
        type: String,
        required: true,
      },
    },
    computed: {
      header() {
        switch (this.status) {
          case STATES.CHECKING_TOKEN:
            return this.$tr('validatingToken');
          case STATES.PASSWORD_CHANGED:
            return this.$tr('passwordChanged');
          case STATES.LINK_EXPIRED:
            return this.$tr('linkExpired');
          case STATES.OTHER_ERROR:
            return this.$tr('serverError');
          default:
            return '';
        }
      },
      explanation() {
        switch (this.status) {
          case STATES.CHECKING_TOKEN:
            return this.$tr('confirmingLink');
          case STATES.PASSWORD_CHANGED:
            return this.$tr('passwordSuccessfullyChanged');
          case STATES.LINK_EXPIRED:
            return this.$tr('needToRequestNewToken');
          case STATES.OTHER_ERROR:
            return this.$tr('thereWasAProblem');
          default:
            return '';
        }
      },
      showButton() {
        return this.status !== STATES.CHECKING_TOKEN;
      },
    },
    $trs: {
      confirmingLink: 'Confirming the validity of the password reset link…',
      homeButton: 'Home',
      linkExpired: 'Link has expired',
      passwordChanged: 'Password changed',
      passwordSuccessfullyChanged: 'Your password was successfully changed',
      needToRequestNewToken:
        'If you need to reset your password, please request again from the home page.',
      serverError: 'Error making request',
      thereWasAProblem: 'There was a problem with your request. Please try again.',
      validatingToken: 'Validating token',
    },
  };

</script>


<style lang="scss" scoped>

  .explanation {
    margin: 1em 0;
  }

  .buttons button {
    margin-left: 0;
  }

</style>
