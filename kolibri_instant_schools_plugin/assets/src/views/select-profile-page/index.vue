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
        @click="openModal"
        :disabled="disableForms"
      />
    </div>

    <new-profile-modal
      v-if="showNewProfileModal"
      @submit="addProfileToPhoneAccount"
      @close="closeModal"
      :disabled="disableForms"
      :showError="newProfileFailed"
    />
  </div>

</template>


<script>

  import { kolibriLogin } from 'kolibri.coreVue.vuex.actions';
  import kButton from 'kolibri.coreVue.components.kButton';
  import newProfileModal from './new-profile-modal';
  import profilesList from './profiles-list';
  import { createProfile } from '../../state/profileActions';

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
        newProfileFailed: false,
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
      addProfileToPhoneAccount(profileName) {
        this.disableForms = true;
        this.createProfile(profileName)
          .then(() => {
            this.showNewProfileModal = false;
            // Wait for profile list to update before scrolling down
            return this.$nextTick().then(() => {
              this.scrollToBottom();
            });
          })
          .catch(() => {
            this.newProfileFailed = true;
          })
          .then(() => {
            this.disableForms = false;
          });
      },
      scrollToBottom() {
        const container = document.querySelector('.content-container');
        container.scrollTop = container.scrollHeight;
      },
      openModal() {
        this.showNewProfileModal = true;
        this.newProfileFailed = false;
      },
      closeModal() {
        this.showNewProfileModal = false;
        this.newProfileFailed = false;
      },
    },
    vuex: {
      getters: {
        profiles: ({ pageState }) => pageState.profiles,
        facility: ({ pageState }) => pageState.facility,
        password: ({ pageState }) => pageState.password,
      },
      actions: {
        createProfile,
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
