
Kolibri External Plugin Template
=================================


How can I install this plugin?
------------------------------

(NOTE - THIS MAY BE INCOMPLETE)

1. Inside your Kolibri virtual environment:

    `pip install kolibri_instant_schools_plugin`

2. Activate the plugin:

    `kolibri plugin kolibri_instant_schools_plugin enable`

3. Restart Kolibri.


How can I install this plugin for development?
------------------------------

1. Run `pip install -e <LOCAL-PATH-TO-REPO>`
2. Set a `DJANGO_SETTINGS_MODULE` environment variable set to `kolibri_instant_schools_plugin.instant_schools_settings`
3. If you have an existing DB, destroy it
4. Run `kolibri manage migrate --database=instant_schools`
5. Run `kolibri plugin kolibri_instant_schools_plugin enable` and `kolibri plugin kolibri.plugins.user disable`
6. Copy `kolibri_instant_schools_plugin/assets/src/views/about/views/about` to `~/.kolibri/content/databases/` (note nested 'about' folders!)
7. Run the devserver: `kolibri manage devserver --debug -- --webpack --lint`

If things aren't working, double and triple check that the user plugin is disabled and the instant_schools plugin is enabled in `kolibri_settings.json` because it often gets reset.


How to publish to PyPi?
------------------------------

1. Follow the instructions above to installing the plugin for development.

2. Update `setup.py` to a newer version.

3. In the terminal move to the root level of repo dir and run the following command to publish to PyPi:

    `make release`

