<template>
  <div>
    <div class="container">
      <h1>{{ $tr('selectProfilePageHeader') }}</h1>

      <div class="profiles">
        <ProfilesList
          :profiles="profiles"
          :disabled="disableForms"
          @selectprofile="signInWithProfile"
        />
      </div>

      <div class="buttons">
        <KButton
          :text="$tr('newProfileButton')"
          :primary="false"
          :disabled="disableForms"
          @click="openModal"
        />
      </div>

      <NewProfileModal
        v-if="showNewProfileModal"
        :disabled="disableForms"
        :showError="newProfileFailed"
        @submit="addProfileToAccount"
        @close="closeModal"
      />
    </div>
  </div>
</template>


<script>

  import urls from 'kolibri.urls';
  import { mapActions, mapState } from 'vuex';
  import NewProfileModal from './NewProfileModal';
  import ProfilesList from './ProfilesList';

  export default {
    name: 'SelectProfilePage',
    components: {
      NewProfileModal,
      ProfilesList,
    },
    data() {
      return {
        disableForms: false,
        newProfileFailed: false,
        showNewProfileModal: false,
      };
    },
    computed: {
      ...mapState('signIn', ['facility', 'password', 'profiles']),
    },
    methods: {
      ...mapActions(['kolibriLogin']),
      ...mapActions('signIn', ['createProfile']),
      signInWithProfile({ username, isNew }) {
        this.disableForms = true;
        this.kolibriLogin({
          facility: this.facility,
          password: this.password,
          username,
        })
          .then(() => {
            if (isNew) {
              window.location = urls['kolibri:about:about']();
            }
          })
          .catch(() => {
            this.disableForms = false;
          });
      },
      addProfileToAccount(profileName) {
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
    $trs: {
      instantSchoolsBrand: 'Instant Schools',
      logIn: 'Sign in',
      newProfileButton: 'New profile',
      selectProfilePageHeader: 'Select profile',
    },
  };

</script>


<style lang="scss" scoped>

  $iphone-5-width: 320px;
  $vertical-page-margin: 50px;

  .ui-icon {
    color: white;
    background-color: transparent;
  }
  // #logo {
  //   display: inline-block;
  //   // 1.63 * font height
  //   height: $logo-size;
  //   margin-left: $logo-margin;
  // }
  .app-bar-icon {
    height: 36px;
    margin-right: 8px;
    vertical-align: middle;
  }

  .brand {
    color: white;
  }

  // adapted from sign-up-page .signup-form
  .container {
    width: ($iphone-5-width - 10) px;
    padding-right: 8px;
    padding-left: 8px;
    margin-top: $vertical-page-margin;
    margin-right: auto;
    margin-left: auto;
  }

  .buttons button {
    margin-left: 0;
  }

  .profiles {
    margin: 16px 0;
  }

</style>
