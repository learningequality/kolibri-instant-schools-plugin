<template>

  <div>
    <h1>{{ $tr('selectProfilePageHeader') }}</h1>

    <div class="profiles">
      <profiles-list
        :profiles="profiles"
        @selectprofile="signInWithProfile"
        :disabled="disableForms"
      />
    </div>

    <div class="buttons">
      <k-button
        :text="$tr('newProfileButton')"
        :ariaLabel="$tr('newProfileButton')"
        :primary="true"
        @click="showNewProfileModal=true"
        :disabled="disableForms"
      />
    </div>

    <new-profile-modal
      v-if="showNewProfileModal"
      @submit="addProfileToPhoneAccount"
      @close="showNewProfileModal=false"
      :disabled="disableForms"
    />
  </div>

</template>


<script>

  import { kolibriLogin } from 'kolibri.coreVue.vuex.actions';
  import kButton from 'kolibri.coreVue.components.kButton';
  import newProfileModal from './new-profile-modal';
  import profilesList from './profiles-list';

  export default {
    name: 'selectProfilePage',
    components: {
      kButton,
      newProfileModal,
      profilesList,
    },
    data() {
      return {
        disableForms: false,
        showNewProfileModal: false,
      };
    },
    methods: {
      signInWithProfile({ username }) {
        this.disableForms = true;
        this.kolibriLogin({
          facility: this.facility,
          password: this.password,
          username,
        }).catch(() => {
          this.disableForms = false;
        });
      },
    },
    vuex: {
      getters: {
        profiles: ({ pageState }) => pageState.profiles,
        facility: ({ pageState }) => pageState.facility,
        password: ({ pageState }) => pageState.password,
      },
      actions: {
        addProfileToPhoneAccount(store, profileName) {
          this.disableForms = true;
          store.dispatch('ADD_PROFILE', {
            username: 'jb',
            full_name: 'jonathan',
          });
          this.showNewProfileModal = false;
          this.disableForms = false;
        },
        kolibriLogin,
      },
    },
    $trs: {
      newProfileButton: 'New profile',
      selectProfilePageHeader: 'Who is learning today?',
    },
  };

</script>


<style lang="stylus" scoped>

  .buttons button
    margin-left: 0

  .profiles
    margin: 1em 0

</style>
