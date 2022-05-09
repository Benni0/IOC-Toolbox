import dns.resolver

blacklists = {
    "XBL_SPAMHOUSE": ".xbl.spamhaus.org.",
    "ZEN_SPAMHOUSE": ".zen.spamhaus.org.",
    "ABUSE.CH_ZEUS": ".ipbl.zeustracker.abuse.ch.",
    "BARRACUDA_CENTRAL": ".b.barracudacentral.org.",
    "MCAFEE_RBL": ".cidr.bl.mcafee.com.",
    "SORBS": ".dnsbl.sorbs.net.",
    "SPAMCOP": ".bl.spamcop.net."
}

def get_listings(ip):
    listings = []
    
    for list in blacklists:
        dns_query = ".".join(reversed(ip.split('.'))) + blacklists[list]
        try:
            answer = dns.resolver.query(dns_query, 'A')
            if answer:
                listings.append(list)
        except dns.resolver.NXDOMAIN:
            pass
        except Exception as e:
            print(f"Unable to lookup {dns_query}, Error: {e}")
            
    return listings