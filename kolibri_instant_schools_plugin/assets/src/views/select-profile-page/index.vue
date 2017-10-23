<template>

  <div>
    <h1>{{ $tr('selectProfilePageHeader') }}</h1>

    <div class="profiles">
      <profiles-list
        :profiles="profiles"
        @selectprofile="signInWithProfile"
      />
    </div>

    <div class="buttons">
      <k-button
        :text="$tr('newProfileButton')"
        :ariaLabel="$tr('newProfileButton')"
        :primary="true"
        @click="showNewProfileModal=true"
      />
    </div>

    <new-profile-modal
      v-if="showNewProfileModal"
      @submit="addProfileToPhoneAccount"
      @close="showNewProfileModal=false"
    />
  </div>

</template>


<script>

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
        showNewProfileModal: false,
      };
    },
    methods: {
      signInWithProfile({ username }) {
        console.log('signing in as ', username);
      },
    },
    vuex: {
      getters: {
        profiles: ({ pageState }) => pageState.profiles,
      },
      actions: {
        addProfileToPhoneAccount(profileName) {
          console.log('yoyo', profileName);
        },
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
