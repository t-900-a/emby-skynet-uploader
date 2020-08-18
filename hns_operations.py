from namebase_exchange.exchange import *

def update_namebase_dns(api_key: str, secret_key: str, domain: str, sialink : str) -> bool:
    updated_records = []
    # chop off the sia://
    sialink = sialink[6:]
    exchange = Exchange(api_key, secret_key)
    dns_settings = exchange.get_dns_settings(domain)
    dns_records = dns_settings['records']
    ns_set = False
    txt_set = False
    for record in dns_records:
        # verify a nameserver is already specified
        if record['type'] == 'NS' and record['value'] != '':
            ns_set = True
        # modify the existing TXT record if there is one
        if record['type'] == 'TXT':
            txt_set = True
            record['host'] = ''
            record['value'] = sialink
        updated_records.append(record)

    if ns_set == False:
        # if there is no nameserver add one
        # name server ip address from blog: https://www.namebase.io/blog/setting-dns-records/
        updated_records.append({'type':'NS','host':'ns1','value':'44.231.6.183','ttl':0})
    if txt_set == False:
        updated_records.append({'type':'TXT','host':'',
                                'value':'AAApJJPnci_CzFnddB076HGu1_C64T6bfoiQqvsiVB5XeQ','ttl':0})

    dns_update_success = exchange.update_dns_settings(domain=domain,
                                 records=updated_records)
    try:
        dns_update_success = dns_update_success['success']
    except Exception as e:
        print(dns_update_success)
        raise e
    if dns_update_success == False:
        print('Namebase DNS record update failed')
    else:
        print('Namebase DNS record update successful')

    return dns_update_success

