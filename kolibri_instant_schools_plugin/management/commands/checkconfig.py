import glob
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from .utils.pynginxconfig import NginxConfig

from kolibri_instant_schools_plugin.smpp.utils import send_message
from kolibri_instant_schools_plugin.smpp.config import CONF_PATH as SMPP_CONF_PATH

import logging as logger

logging = logger.getLogger("kolibri")
logging.propagate = False


NUM = "75801457470"


class Command(BaseCommand):
    help = "Check that the system nginx config seems correctly configured"

    requires_system_checks = False

    def handle(self, *args, **options):

        if not self.check_static_editable_files():
            return

        if not self.check_smpp_config_and_connection():
            return

        log_statuses = [self.check_nginx_config(path) for path in glob.glob("/etc/nginx/sites-enabled/*")]
        if not any(log_statuses):
            logging.error("No valid nginx config files found; aborting!")
            return


    def check_nginx_config(self, path):

        logging.info("Checking config file: {path}".format(path=path))

        nc = self.nc = NginxConfig()
        nc.loadf(path)

        # get upstream backend server block
        upstream = nc.get_value(nc.get([("upstream", "kolibri")]))
        if not upstream:
            logging.warning("Not a valid kolibri nginx log (no upstream kolibri block specified); skipping.")
            return False

        # check the upstream host, and warn if not what expected
        upstream_host = nc.get_value(nc.get(["server"], upstream))
        if upstream_host != "127.0.0.1:8080":
            logging.warning("The upstream kolibri server value should probably be set to 127.0.0.1:8080 (currently it is {host}).".format(host=upstream_host))

        # load the server block from the config file
        server = self.server = nc.get_value(nc.get([("server",)]))
        if not server:
            logging.error("Could not find 'server' block in nginx config.")
            return False

        # check what port nginx is listening on
        listen_port = nc.get_value(nc.get(["listen"], server))
        if listen_port != "80":
            logging.warning("The nginx 'listen' port should probably be set to port 80 (currently it is {port}).".format(port=listen_port))

        # check that the log config is correct
        log_format_raw = nc.get_value(nc.get(["log_format"]))
        log_format = "".join(log_format_raw).replace("\'", "").strip()
        if not log_format_raw:
            logging.error("Could not find 'log_format' setting in nginx config.")
            return False
        if not log_format.startswith("visitorid "):
            logging.error("Must use 'visitorid' log format.")
            return False
        if not log_format.endswith('"$uid_set" "$uid_got"'):
            logging.error("""Must include the following fields at the end of the 'visitorid' log format:  "$uid_set" "$uid_got" """)
            return False
        access_log = (nc.get_value(nc.get(["access_log"], server)) or "").strip()
        if not access_log.endswith(" visitorid"):
            logging.error("In nginx server block, access_log must specify 'visitorid' log format.")
            return False
        if not access_log.endswith('kolibri.log visitorid'):
            logging.error("In nginx server block, access_log must point to a file named 'kolibri.log'.")
            return False

        # check that the location blocks are correct
        if not self.check_nginx_location_block("content") or not self.check_nginx_location_block("static"):
            return False

        # check that the HTTP version for proxying is set up correctly
        proxy_http_version = nc.get_value(nc.get(["proxy_http_version"], server))
        if proxy_http_version != "1.1":
            logging.error("You must include the following line in the server block in your in your nginx config:\n\t proxy_http_version 1.1;")
            return False

        # check that the userid nginx cookie settings are turned on
        for name, value in [("userid", "on"), ("userid_name", "visitor"), ("userid_path", "/"), ("userid_expires", "max")]:
            if not self.check_nginx_server_block_value(name, value):
                return False

        logging.info("No blocking issues found with nginx config! Check for any warnings above.")
        return True

    def check_nginx_location_block(self, foldername):
        url_path = "/" + foldername
        disk_path_expected = os.path.join(settings.KOLIBRI_HOME, foldername)
        disk_path_actual = self.nc.get_value(self.nc.get(["alias"], self.nc.get_value(self.nc.get([("server",), ("location", url_path)]) or [])))
        if not disk_path_actual:
            logging.error("Could not find 'location /content' block containing an alias value, in server block in nginx config.")
            return False
        if not os.path.isdir(disk_path_actual):
            logging.error("The path pointed to by the 'location /{foldername}' block is not a directory: {path}".format(path=disk_path_actual, foldername=foldername))
            return False
        if os.name != 'nt':
            if os.stat(disk_path_actual).st_uid == 0:
                logging.error("The path pointed to by the 'location /{foldername}' block is owned by root, please run: sudo chown <yourusername> {path}".format(path=disk_path_actual, foldername=foldername))
                return False
            if not os.access(disk_path_actual, os.W_OK):
                logging.error("The path pointed to by the 'location /{foldername}' block is not writeable by the current user: {path}".format(path=disk_path_actual, foldername=foldername))
                return False
        if disk_path_actual != disk_path_expected:
            logging.error("The path pointed to by the 'location /{foldername}' block seems to be incorrect (observed: {actual}, expected: {expected}".format(actual=disk_path_actual, expected=disk_path_expected, foldername=foldername))
            return False
        return True

    def check_nginx_server_block_value(self, name, value):
        if self.nc.get_value(self.nc.get([name], self.server)) != value:
            logging.error("Expected in nginx server block:   {name}  {value};".format(name=name, value=value))
            return False
        return True

    def check_smpp_config_and_connection(self):

        logging.info("Attempting to send an SMS using the SMPP config.")

        try:
            send_message("+" + "".join([str(int(i) + 1) for i in reversed(NUM)]), "This is a test!")
        except Exception as e:
            logging.error("Unable to send SMS, please check settings in {path}\n\t\tError: {error})".format(path=SMPP_CONF_PATH, error=str(e)))
            return False

        self.stdout.write("SMS sent successfully!")
        return True

    def check_static_editable_files(self):
        logging.info("Checking for the existence of user-editable static files.")
        good = True
        about_dir = os.path.join(settings.KOLIBRI_HOME, "content", "databases", "about")
        for name in ["tos.txt", "faq.html", "about.html"]:
            path = os.path.join(about_dir, name)
            if not os.path.isfile(path):
                logging.error("Missing file at {path} -- please copy this file in from the provided templates (see docs) and edit as desired.".format(path=path))
                good = False
        return good