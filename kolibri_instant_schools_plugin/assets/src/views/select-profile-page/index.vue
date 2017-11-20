<template>

  <div>
    <ui-toolbar
      type="colored"
      textColor="white"
    >
      <template slot="icon">
        <ui-icon-button
          icon="arrow_back"
          type="secondary"
          color="white"
          @click="showSignIn"
        />
      </template>
      <div>
        <ui-icon class="app-bar-icon">
          <logo />
        </ui-icon>
        <span class="brand">{{ $tr('instantSchoolsBrand') }}</span>
      </div>
    </ui-toolbar>

    <div class="container">
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
          :primary="false"
          @click="openModal"
          :disabled="disableForms"
        />
      </div>

      <new-profile-modal
        v-if="showNewProfileModal"
        @submit="addProfileToAccount"
        @close="closeModal"
        :disabled="disableForms"
        :showError="newProfileFailed"
      />
    </div>
  </div>

</template>


<script>

  import { kolibriLogin } from 'kolibri.coreVue.vuex.actions';
  import kButton from 'kolibri.coreVue.components.kButton';
  import newProfileModal from './new-profile-modal';
  import profilesList from './profiles-list';
  import { createProfile } from '../../state/profileActions';
  import { showSignIn } from '../../state/actions';
  import UiToolbar from 'keen-ui/src/UiToolbar';
  import UiIcon from 'keen-ui/src/UiIcon';
  import UiIconButton from 'keen-ui/src/UiIconButton';
  import logo from 'kolibri.coreVue.components.logo';

  export default {
    name: 'selectProfilePage',
    components: {
      kButton,
      logo,
      newProfileModal,
      profilesList,
      UiToolbar,
      UiIcon,
      UiIconButton,
    },
    data() {
      return {
        disableForms: false,
        newProfileFailed: false,
        showNewProfileModal: false,
      };
    },
    methods: {
      signInWithProfile({ username, isNew }) {
        this.disableForms = true;
        this.kolibriLogin({
          facility: this.facility,
          password: this.password,
          username,
        })
          .then(() => {
            if (isNew) {
              window.location = '/about';
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
    vuex: {
      getters: {
        profiles: ({ pageState }) => pageState.profiles,
        facility: ({ pageState }) => pageState.facility,
        password: ({ pageState }) => pageState.password,
      },
      actions: {
        createProfile,
        kolibriLogin,
        showSignIn,
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


<style lang="stylus" scoped>

  $iphone-5-width = 320px
  $vertical-page-margin = 50px

  .ui-icon
    background-color: transparent
    color: white

  #logo
    // 1.63 * font height
    height: $logo-size
    display: inline-block
    margin-left: $logo-margin

  .app-bar-icon
    font-size: 40px
    margin-left: 4px
    margin-right: 8px

  .brand
    color: white

  // adapted from sign-up-page .signup-form
  .container
    margin-top: $vertical-page-margin
    margin-left: auto
    margin-right: auto
    width: ($iphone-5-width - 10)px
    padding-left: 8px
    padding-right: 8px

  .buttons button
    margin-left: 0

  .profiles
    margin: 16px 0

</style>
