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
          :label="$tr('fullName')"
          v-model="fullName"
          :invalid="!fullNameIsValid"
          :invalidText="fullNameInvalidText"
          :maxlength="120"
          :disabled="disabled"
          @blur="fullNameIsBlurred=true"
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
        fullName: '',
        fullNameIsBlurred: false,
        formIsSubmitted: false,
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
      fullNameShouldValidate() {
        return this.fullName !== '' || this.fullNameIsBlurred || this.formIsSubmitted;
      },
      fullNameIsValid() {
        if (this.fullNameShouldValidate) {
          return this.fullName !== '' && !this.profileAlreadyExists(this.fullName);
        }
        return true;
      },
      fullNameInvalidText() {
        if (this.profileAlreadyExists(this.fullName)) {
          return this.$tr('profileAlreadyExists');
        }
        return this.$tr('required');
      },
    },
    methods: {
      submit() {
        this.formIsSubmitted = true;
        if (this.fullNameIsValid) {
          return this.$emit('submit', this.fullName);
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
          return function findMatch(fullName) {
            return Boolean(state.pageState.profiles.find(profile => profile.full_name === fullName));
          };
        },
      },
    },
    $trs: {
      cancel: 'Cancel',
      fullName: 'Full name',
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
