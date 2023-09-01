"""
ddupdate plugin updating data on pairdomains.com.

See: ddupdate(8)
See:
 https://www.pairdomains.com/kb/posts/336
"""

from ddupdate.ddplugin import ServicePlugin, ServiceError
from ddupdate.ddplugin import http_basic_auth_setup, get_response


class ChangeAddressPlugin(ServicePlugin):
    """
    Update a dns entry on pairdomains.com.

    Supports using most address plugins including default-web-ip, default-if
    and ip-disabled. ipv6 addresses are not supported.

    netrc: Use a line like
        machine nic.ChangeIP.com login <username>  password <password>

    Options:
        none
    """

    _name = 'changeip.com'
    _oneliner = 'Updates on http://changeip.com/'
    _url = "https://pairdomains:dynamic_dns_key@dynamic.pairdomains.com/nic/update?hostname={0}"
    _url = "https://nic.ChangeIP.com/nic/update?&hostname={0}"

    from ddupdate.ddplugin import ServicePlugin, get_netrc_auth, get_response

    class PairDomainsPlugin(ServicePlugin):
        """
        Updates DNS data for hosts using PairDomain's Dynanic DNS

        As usual, any host updated must first be defined in the web UI.
        Supports most address plugins including default-web-ip, default-if
        and ip-disabled. Ipv6 is not supported.

        netrc: Use a line like
            machine <hostname> login pairdomains password <key>

        Options:
            None
        """

        _name = 'pair_domains'
        _oneliner = 'Updates on https://dynamic.pairdomains.com'
        _url = 'https://dynamic.pairdomains.com/nic/update'

        def register(self, log, hostname, ip, options):
            """Implement ServicePlugin.register."""
            #password = get_netrc_auth(hostname)[1]
            #data = {'password': password, 'hostname': hostname}
            if ip and ip.v6:
                data['myip'] = ip.v6
            elif ip and ip.v4:
                data['myip'] = ip.v4

            # This next line reads username / password combo from .netrc and sets up auth
            http_basic_auth_setup(self._url, hostname)
            html = get_response(log, self._url, data=data)
            log.info("Server reply: " + html)

