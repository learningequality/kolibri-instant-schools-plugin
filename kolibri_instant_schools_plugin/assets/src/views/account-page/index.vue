<template>

  <div class="content">

    <h1>{{ $tr('profile') }}</h1>

    <section>
      <h2>{{ $tr('points') }}</h2>
      <points-icon class="points-icon" :active="true"/>
      <span class="points-num">{{ $formatNumber(totalPoints) }}</span>
    </section>

    <section>
      <h2>{{ $tr('role') }}</h2>
      {{ role }}
    </section>

    <section v-if="userHasPermissions">
      <h2>{{ $tr('devicePermissions') }}</h2>
      <p>
        <permissions-icon :permissionType="permissionType" class="permissions-icon"/>
        {{ permissionTypeText }}
      </p>
      <p>
        {{ $tr('youCan') }}
        <ul class="permissions-list">
          <li v-for="(value, key) in getUserPermissions" v-if="value" :key="key">
            {{ getPermissionString(key) }}
          </li>
        </ul>
      </p>
    </section>

    <form @submit.prevent="submitEdits">
      <ui-alert
        v-if="profileNameSuccess"
        type="success"
        :dismissible="false"
      >
        {{ $tr('profileNameSuccess') }}
      </ui-alert>
      <ui-alert
        v-if="profileNameError"
        type="error"
        :dismissible="false"
      >
        {{ profileNameErrorMessage || $tr('genericError') }}
      </ui-alert>

      <k-textbox
        ref="name"
        v-if="canEditName"
        type="text"
        autocomplete="name"
        :autofocus="false"
        :label="$tr('name')"
        :disabled="profileNameBusy"
        :maxlength="120"
        :invalid="!nameIsValid"
        :invalidText="$tr('required')"
        v-model="name"
      />
      <template v-else>
        <h2>{{ $tr('name') }}</h2>
        <p>{{ name }}</p>
      </template>

      <k-button
        type="submit"
        :text="$tr('saveChanges')"
        :primary="true"
        :disabled="profileNameBusy"
        class="no-ml"
      />
    </form>

    <h1>{{ $tr('account ') }}</h1>

    <ui-alert
      v-if="accountPasswordSuccess"
      type="success"
      :dismissible="false"
    >
      {{ $tr('accountPasswordSuccess') }}
    </ui-alert>

    <k-button
      v-if="canEditPassword"
      :text="$tr('changePassword')"
      :priamry="false"
      :raised="true"
      @click="showAccountPasswordModal(true)"
      class="no-ml"
    />

    <change-password-modal v-if="passwordModalIsOpen" />

  </div>

</template>


<script>

  import { changeName, resetNameState, showAccountPasswordModal } from '../../state/actions';
  import {
    facilityConfig,
    isSuperuser,
    isAdmin,
    isCoach,
    isLearner,
    totalPoints,
    getUserRole,
    getUserPermissions,
    userHasPermissions,
  } from 'kolibri.coreVue.vuex.getters';
  import responsiveWindow from 'kolibri.coreVue.mixins.responsiveWindow';
  import { validateUsername } from 'kolibri.utils.validators';
  import { fetchPoints } from 'kolibri.coreVue.vuex.actions';
  import kButton from 'kolibri.coreVue.components.kButton';
  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import pointsIcon from 'kolibri.coreVue.components.pointsIcon';
  import permissionsIcon from 'kolibri.coreVue.components.permissionsIcon';
  import uiAlert from 'keen-ui/src/UiAlert';
  import { PermissionTypes, UserKinds } from 'kolibri.coreVue.vuex.constants';
  import changePasswordModal from './change-password-modal';

  export default {
    name: 'accountPage',
    $trs: {
      genericError: 'Something went wrong',
      profileNameSuccess: 'Profile name updated!',
      name: 'Profile name',
      saveChanges: 'Save changes',
      isLearner: 'Learner',
      isCoach: 'Coach',
      isAdmin: 'Admin',
      isSuperuser: 'Superuser permissions ',
      manageContent: 'Manage content',
      points: 'Points',
      role: 'Role',
      devicePermissions: 'Device permissions',
      required: 'This field is required',
      limitedPermissions: 'Limited permissions',
      youCan: 'You can',
      profile: 'Profile',
      changePassword: 'Change password',
      accountPasswordSuccess: 'Password changed',
      account: 'Account',
    },
    components: {
      kButton,
      kTextbox,
      uiAlert,
      pointsIcon,
      permissionsIcon,
      changePasswordModal,
    },
    mixins: [responsiveWindow],
    data() {
      return {
        name: this.fullName,
        formSubmitted: false,
      };
    },
    computed: {
      role() {
        if (this.getUserRole === UserKinds.ADMIN) {
          return this.$tr('isAdmin');
        } else if (this.getUserRole === UserKinds.COACH) {
          return this.$tr('isCoach');
        } else if (this.getUserRole === UserKinds.LEARNER) {
          return this.$tr('isLearner');
        }
        return '';
      },
      permissionType() {
        if (this.isSuperuser) {
          return PermissionTypes.SUPERUSER;
        } else if (this.userHasPermissions) {
          return PermissionTypes.LIMITED_PERMISSIONS;
        }
        return null;
      },
      permissionTypeText() {
        if (this.permissionType === PermissionTypes.SUPERUSER) {
          return this.$tr('isSuperuser');
        } else if (this.permissionType === PermissionTypes.LIMITED_PERMISSIONS) {
          return this.$tr('limitedPermissions');
        }
        return '';
      },
      canEditName() {
        return this.userIsAdmin || this.facilityConfig.learnerCanEditName;
      },
      canEditPassword() {
        return this.userIsAdmin || this.facilityConfig.learnerCanEditPassword;
      },
      // i.e. not a coach or a learner
      userIsAdmin() {
        return !this.isCoach && !this.isLearner;
      },
      nameIsValid() {
        return this.name !== '';
      },
    },
    created() {
      this.fetchPoints();
    },
    methods: {
      submitEdits() {
        this.formSubmitted = true;
        if (this.name === this.fullName) {
          return;
        }
        this.resetNameState();
        if (!this.nameIsValid) {
          return this.$refs.name.focus();
        }
        this.changeName(this.name);
      },
      getPermissionString(permission) {
        if (permission === 'can_manage_content') {
          return this.$tr('manageContent');
        }
        return permission;
      },
    },
    vuex: {
      getters: {
        facilityConfig,
        isSuperuser,
        isAdmin,
        isCoach,
        isLearner,
        totalPoints,
        fullName: state => state.core.session.full_name,
        getUserRole,
        getUserPermissions,
        userHasPermissions,
        profileNameBusy: state => state.pageState.profileNameBusy,
        profileNameError: state => state.pageState.profileNameError,
        profileNameErrorMessage: state => state.pageState.profileNameErrorMessage,
        profileNameSuccess: state => state.pageState.profileNameSuccess,
        accountPasswordSuccess: state => state.pageState.accountPasswordSuccess,
        passwordModalIsOpen: state => state.pageState.showAccountPasswordModal,
      },
      actions: {
        changeName,
        resetNameState,
        fetchPoints,
        showAccountPasswordModal,
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'

  // taken from docs, assumes 1rem = 16px
  $vertical-page-margin = 50px
  $iphone-width = 320

  .content
    padding-top: $vertical-page-margin
    margin-left: auto
    margin-right: auto
    width: ($iphone-width - 20)px

  .no-ml
    margin-left: 0

  .points-icon, .points-num
    display: inline-block

  .points-icon
    width: 2em
    height: 2em

  .points-num
    color: $core-status-correct
    font-size: 3em
    font-weight: bold
    margin-left: 16px

  section
    margin-bottom: 36px

  .permissions-list
    padding-left: 37px

  .permissions-icon
    padding-right: 8px

</style>
