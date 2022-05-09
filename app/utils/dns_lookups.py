import dns.resolver

def get_master(domain):
    try:
        answers = dns.resolver.query(domain, 'SOA')        
        if len(answers) > 0:
            return str(answers[0].mname)
        else:
            return None
    except dns.resolver.NXDOMAIN:
        return "NXDOMAIN"
    except Exception as e:
        return None
    
def get_ptr(ip):
    try:
        reverse_lookup = ".".join(reversed(ip.split('.'))) +'.in-addr.arpa.'
        answers = dns.resolver.query(reverse_lookup, 'PTR')
        if len(answers) > 0:
            return str(answers[0])
        return None
    except Exception as e:
        print(e)
        return None
    
def get_a_record(domain):
    try:
        answers = dns.resolver.query(domain, 'A')
        if len(answers) > 0:
            return [str(record) for record in answers]
        else:
            return None
    except Exception as e:
        print(f"Unable to lookup {domain}, Error: {e}")
        return None