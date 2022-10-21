
Kolibri Instant Schools Plugin
=================================

How can I install this plugin for development or local testing?
------------------------------

1. Ensure you have (Kolibri)[https://github.com/learningequality/kolibri] setup for local development. **Note that all commands below are to be done in the Kolibri repo unless specified otherwise.** Also, be sure you're checking out the correct version branch. The latest version of Kolibri supported by the plugin is the `release-v0.15.x` branch.
2. `git clone` this `kolibri_instant_schools_plugin` repository and then `cd` back into where you setup your Kolibri for development.
3. See the **Env Vars** section below and set the required variables.
4. Run `pip install -e ../relative/path/to/kolibri_instant_schools_plugin`
5. Run `kolibri manage migrate`
6. Run `kolibri plugin enable kolibri_instant_schools_plugin` and `kolibri plugin disable kolibri.plugins.user_auth kolibri.plugins.default_theme`.
7. As an alternative to item 6 above, we may instead use plugins files and update our package.json scripts __TEMPORARILY__ in our local Kolibri. Do not commit these changes to Kolibri.

Make your `build_tools/build_plugins.txt` read as follows and remember that this is __TEMPORARY__ and should not be committed to Kolibri:

```
kolibri.core
kolibri.plugins.device_management
kolibri.plugins.facility_management
kolibri.plugins.learn
kolibri.plugins.document_pdf_render
kolibri.plugins.html5_app_renderer
kolibri.plugins.media_player
kolibri.plugins.setup_wizard
kolibri.plugins.coach
kolibri_exercise_perseus_plugin
kolibri_instant_schools_plugin
kolibri.plugins.style_guide
kolibri.plugins.document_epub_render
kolibri.plugins.default_theme
```

8. Running the devserver. You may wish to run the server so that you can do frontend development. I suggest the following changes to make this easier for you:

In the `package.json` file in Kolibri, update all of the script entries that define a settings module to point to the `kolibri_instant_schools_plugin.instant_schools_settings` rather than the `kolibri.deployment.default.*.**` settings. Doing this will allow you to easily spin up the development server with hot reloading and you can run `yarn run devserver` or `yarn run devserver-hot` to start the full development server.

If you only need to work on Django backend and have the `DJANGO_SETTINGS_MODULE` env variable set, then you can run `yarn build` and `kolibri start --foreground`.

If things aren't working, double and triple check that the user plugin is disabled and the instant_schools plugin is enabled in `kolibri_settings.json` which is located in your `KOLIBRI_HOME` folder.

9. (Optional) - Copy the `kolibri_instant_schools_plugin/assets/src/views/about/views/about` to `$(KOLIBRI_HOME)/content/databases`. Note that the about folders are indeed nested and that is not a typo. 

Env Vars
--------

The following environment variables are *required*:

- `SMS_MESSAGE_TEMPLATE` - A string prepared for Python's `string.format()` with one variable `{url}` within the string somewhere. That will be where the URL the user clicks to reset their password will be inserted into the message template.
- `TWILIO_SID` & `TWILIO_AUTH_TOKEN` - These will allow us to send password reset tokens. You can find these in your Twilio account.
- `POST_USER_URL` - This is the base URL to where user information will be securely POSTed to partners.

The following environment variables are *optional*:

- `INSTANT_SCHOOLS_APP_NAME` - This allows partners to have their instances of the platform branded with a name of their choice.


How can I install this plugin, but not for development?
------------------------------

Note that this may be incomplete. Typically, a plugin like this will be used within a released build of Kolibri so the following does not follow our expected typical use case.

1. Inside your Kolibri virtual environment:

    `pip install kolibri_instant_schools_plugin`

2. Activate the plugin:

    `kolibri plugin kolibri_instant_schools_plugin enable`

3. Restart Kolibri.

