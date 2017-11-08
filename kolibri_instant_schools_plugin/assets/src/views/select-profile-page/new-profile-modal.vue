<template>

  <core-modal
    :title="$tr('newProfileModalTitle')"
    @cancel="closeModal"
  >
    <div class="contents">
      <ui-alert
        v-if="showError"
        type="error"
        :dismissible="false"
      >
        {{ $tr('problemCreatingProfile') }}
      </ui-alert>

      <form @submit.prevent="submit">
        <k-textbox
          :autofocus="true"
          :label="$tr('profileName')"
          v-model="profileName"
          :invalid="!profileNameIsValid"
          :invalidText="profileNameInvalidText"
          :maxlength="120"
          :disabled="disabled"
          @blur="profileNameIsBlurred=true"
        />

        <div class="buttons">
          <k-button
            :text="$tr('cancel')"
            :primary="false"
            @click="closeModal"
            :disabled="disabled"
          />
          <k-button
            :text="$tr('save')"
            type="submit"
            :primary="true"
            :disabled="disabled"
          />
        </div>
      </form>
    </div>
  </core-modal>

</template>


<script>

  import coreModal from 'kolibri.coreVue.components.coreModal';
  import kTextbox from 'kolibri.coreVue.components.kTextbox';
  import kButton from 'kolibri.coreVue.components.kButton';
  import uiAlert from 'keen-ui/src/UiAlert';

  export default {
    name: 'newProfileModal',
    components: {
      coreModal,
      kButton,
      kTextbox,
      uiAlert,
    },
    data() {
      return {
        formIsSubmitted: false,
        profileName: '',
        profileNameIsBlurred: false,
      };
    },
    props: {
      disabled: {
        type: Boolean,
        required: true,
      },
      showError: {
        type: Boolean,
        default: false,
      },
    },
    computed: {
      profileNameShouldValidate() {
        return this.profileName !== '' || this.profileNameIsBlurred || this.formIsSubmitted;
      },
      profileNameIsValid() {
        if (this.profileNameShouldValidate) {
          return this.profileName !== '' && !this.profileAlreadyExists(this.profileName);
        }
        return true;
      },
      profileNameInvalidText() {
        if (this.profileAlreadyExists(this.profileName)) {
          return this.$tr('profileAlreadyExists');
        }
        return this.$tr('required');
      },
    },
    methods: {
      submit() {
        this.formIsSubmitted = true;
        if (this.profileNameIsValid) {
          return this.$emit('submit', this.profileName);
        }
      },
      closeModal() {
        // Guard against closing during request until 'X' button can be removed from modal
        if (!this.disabled) {
          this.$emit('close');
        }
      },
    },
    vuex: {
      getters: {
        profileAlreadyExists(state) {
          return function findMatch(profileName) {
            return Boolean(state.pageState.profiles.find(profile => profile.full_name === profileName));
          };
        },
      },
    },
    $trs: {
      cancel: 'Cancel',
      profileName: 'Profile name',
      newProfileModalTitle: 'New profile',
      problemCreatingProfile: 'There was a problem creating this profile',
      profileAlreadyExists: 'This profile already exists',
      required: 'Required',
      save: 'Save',
    },
  };

</script>


<style lang="stylus" scoped>

  .buttons
    text-align: right

  button[type='submit']
    margin-right: 0

</style>
