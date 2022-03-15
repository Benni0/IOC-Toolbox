import dns.resolver

def get_master(domain):
    try:
        answers = dns.resolver.query(domain, 'SOA')
        if len(answers) > 0:
            return answers[0].mname
        else:
            return None
    except:
        return None