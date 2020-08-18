from namebase_exchange.exchange import *

def update_namebase_dns(api_key: str, secret_key: str, domain: str, sialink : str):
    exchange = Exchange(api_key, secret_key)
    dns_settings = exchange.get_dns_settings(domain)
    dns_records = dns_settings['records']
    ns_set = False
    # verify a nameserver is already specified
    for record in dns_records:
        if record['type'] == 'NS' and record['value'] != '':
            ns_set = True

    if ns_set == False:
        # if there is no nameserver add one
        # name server ip address from blog: https://www.namebase.io/blog/setting-dns-records/
        exchange.update_dns_settings(domain=domain,
                                     record_type='NS',
                                     host='ns1',
                                     value='44.231.6.183')
    # chop off the sia://
    sialink = sialink[6:]
    exchange.update_dns_settings(domain=domain,
                                 record_type='TXT',
                                 host='@',
                                 value=sialink, ttl=0)