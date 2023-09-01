"""
ddupdate plugin updating data on pairdomains.com.

See: ddupdate(8)
See:
 https://www.pairdomains.com/kb/posts/336
"""

from ddupdate.ddplugin import ServicePlugin, ServiceError
from ddupdate.ddplugin import http_basic_auth_setup, get_response



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
    _url = 'https://dynamic.pairdomains.com/nic/update?hostname={0}'

    def register(self, log, hostname, ip, options):
        """Implement ServicePlugin.register()."""
        url = self._url.format(hostname)
        api_host = urlparse(url).hostname
        username, password = get_netrc_auth(api_host)
        user_pw = ('%s:%s' % (username, password))
        credentials = base64.b64encode(user_pw.encode('ascii'))
        auth_header = ('Authorization', 'Basic ' + credentials.decode("ascii"))
        url = self._url.format(hostname)
        if ip and ip.v4:
            url += "&ip=" + ip.v4
        if ip and ip.v6:
            url += "&ip6=" + ip.v6
        html = get_response(log, url, header=auth_header)
        key = html.split()[0]
        if key not in ['OK', 'good', 'nochg']:
            raise ServiceError("Bad server reply: " + html)
        log.info("Server reply: " + html)
