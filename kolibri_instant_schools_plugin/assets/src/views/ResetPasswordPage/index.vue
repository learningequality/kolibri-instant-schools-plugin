<template>

  <ImmersivePage
    :appBarTitle="title"
    :route="backRoute"
  >
    <ResetPasswordPageStatus
      v-if="showStatus"
      :status="status"
      @close="goToHomePage"
    />
    <NewPasswordForm
      v-else
      :disable="disableForms"
      @submit="submitNewPassword"
    />
  </ImmersivePage>

</template>


<script>

  import { mapState } from 'vuex';
  import ImmersivePage from 'kolibri.coreVue.components.ImmersivePage';
  import { PageNames, ResetPasswordStates as STATES } from '../../constants';
  import { getTokenStatus, updatePassword } from './api';
  import NewPasswordForm from './NewPasswordForm';
  import ResetPasswordPageStatus from './ResetPasswordPageStatus';

  export default {
    name: 'ResetPasswordPage',
    components: {
      ImmersivePage,
      NewPasswordForm,
      ResetPasswordPageStatus,
    },
    props: {
      title: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        status: STATES.CHECKING_TOKEN,
        disableForms: false,
      };
    },
    computed: {
      ...mapState('signIn', ['token', 'phone']),
      showStatus() {
        return this.status !== STATES.ENTER_PASSWORD;
      },
      backRoute() {
        return { name: PageNames.SIGN_IN };
      },
    },
    mounted() {
      getTokenStatus({
        token: this.token,
        phoneNumber: this.phone,
      })
        .then(() => {
          this.status = STATES.ENTER_PASSWORD;
        })
        .catch(response => {
          if (response.status.code === 400) {
            this.status = STATES.LINK_EXPIRED;
          } else {
            this.status = STATES.OTHER_ERROR;
          }
        });
    },
    methods: {
      submitNewPassword(newPw) {
        this.disableForms = true;
        return updatePassword({
          password: newPw,
          token: this.token,
          phone: this.phone,
        })
          .then(() => {
            this.status = STATES.PASSWORD_CHANGED;
          })
          .catch(() => {
            this.status = STATES.OTHER_ERROR;
          })
          .then(() => {
            this.disableForms = false;
          });
      },
      goToHomePage() {
        this.$router.replace({ name: PageNames.SIGN_IN });
      },
    },
  };

</script>


<style lang="scss" scoped></style>
