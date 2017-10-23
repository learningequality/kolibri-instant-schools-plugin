<template>

  <core-modal
    :title="$tr('newProfileModalTitle')"
    @cancel="closeModal"
  >
    <div class="contents">
      <k-textbox
        :label="$tr('fullName')"
        v-model="fullName"
        :invalid="!fullNameIsInvalid"
        :invalidText="$tr('required')"
        maxlength="120"
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
          @click="submit"
          :disabled="disabled"
        />
      </div>
    </div>


  </core-modal>

</template>


<script>

  import coreModal from 'kolibri.coreVue.components.coreModal';
  import kTextbox from 'kolibri.coreVue.components.kTextbox';

  export default {
    name: 'newProfileModal',
    components: {
      coreModal,
      kTextbox,
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
    },
    computed: {
      fullNameShouldValidate() {
        return this.fullNameIsBlurred || this.formIsSubmitted;
      },
      fullNameIsValid() {
        if (this.fullNameShouldValidate) {
          return this.fullName !== '' && !this.profileAlreadyExists(this.fullName);
        }
        return true;
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
