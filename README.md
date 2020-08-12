
Kolibri Instant Schools Plugin
=================================

How can I install this plugin for development?
------------------------------

1. Ensure you have (Kolibri)[https://github.com/learningequality/kolibri] setup for local development. Note that all commands below are to be done in the Kolibri repo unless specified otherwise. Also, be sure you're checking out the correct version branch. As of August 2020, this would be `release-v0.12.x`.
2. `git clone` this `kolibri_instant_schools_plugin` repository.
3. Set and export the following local variables for use in your development environment: `KOLIBRI_HOME` - this ought to be a new path that was not previously used as a `KOLIBRI_HOME`. Also set `DJANGO_SETTINGS_MODULE` to `kolibri_instant_schools_plugin.instant_schools_settings`.
4. Run `pip install -e ../relative/path/to/kolibri_instant_schools_plugin`
5. Run `kolibri manage migrate --database=instant_schools`
6. Run `kolibri plugin kolibri_instant_schools_plugin enable` and `kolibri plugin kolibri.plugins.user disable`. If you find that you're having issues, see the next item.
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

8. Running the devserver. In the `package.json` file in Kolibri, update all of the script entries that define a settings module to point to the `kolibri_instant_schools_plugin.instant_schools_settings` rather than the `kolibri.deployment.default.*.**` settings. Doing this will allow you to easily spin up the development server with hot reloading.

If things aren't working, double and triple check that the user plugin is disabled and the instant_schools plugin is enabled in `kolibri_settings.json` which is located in your `KOLIBRI_HOME` folder.


How do I test SMPP locally?
----------------------------

1. From the root of the `kolibri_instant_schools_plugin` project, `cd kolibri_instant_schools_plugin/smpp/SMPPSim` 
2. Now, unzip the file: `unzip SMPPSim.zip` which should create a new folder `SMPPSim` 
3. Now, `cd SMPPSim` and you can run `sudo sh startsmppsim.sh` from that folder anytime to test SMPP.

This will start a server that will be used for the SMPP testing. You can see output of SMPP activity logged in the console where this is run.


How can I install this plugin, but not for development?
------------------------------

Note that this may be incomplete. Typically, a plugin like this will be used within a released build of Kolibri so the following does not follow our expected typical use case.

1. Inside your Kolibri virtual environment:

    `pip install kolibri_instant_schools_plugin`

2. Activate the plugin:

    `kolibri plugin kolibri_instant_schools_plugin enable`

3. Restart Kolibri.


How to publish to PyPi?
------------------------------

1. Follow the instructions above to installing the plugin for development.

2. Update `setup.py` to a newer version.

3. In the terminal move to the root level of repo dir and run the following command to publish to PyPi:

    `make release`

