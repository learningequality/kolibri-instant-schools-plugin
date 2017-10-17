
Kolibri External Plugin Template
=================================


How can I install this plugin?
------------------------------

1. Inside your Kolibri virtual environment:

    `pip install kolibri_instant_schools_plugin`

2. Activate the plugin:

    `kolibri plugin kolibri_instant_schools_plugin enable`

3. Restart Kolibri.

How can I install this plugin for development?
------------------------------

1. Download this repo.

2. Open terminal in your Kolibri repo.

3. run the following commands:

    ```
    pip install -e <LOCAL-PATH-TO-REPO>
    kolibri plugin kolibri_instant_schools_plugin enable
    kolibri plugin kolibri.plugins.user disable
    ```



How to publish to PyPi?
------------------------------

1. Follow the instructions above to installing the plugin for development.

2. Update `setup.py` to a newer version.

3. In the terminal move to the root level of repo dir and run the following command to publish to PyPi:

    `make release`

