import sys
import dns.resolver


def main():
    '''
    DEFAULT VALUES
    '''
    hostname = 'www.wikipedia.org'
    mode = 'A'
    server = None
    argv = sys.argv

    for i in range(1,len(argv)):
        arg = argv[i]
        if arg == 'AAAA' or arg == 'A':
            mode = arg
        elif arg.startswith('@'):
            server = arg[1:]
        else:
            hostname = arg
    
    print(hostname)
    print(server)
    print(mode)
    handle_query(hostname,server,mode)




def handle_query(hostname,server,mode='A'):
    my_resolver = dns.resolver.Resolver()
    if server != None:
        nameservers = list()
        nameservers.append(server)
        my_resolver.nameservers = nameservers

    answers = my_resolver.query(qname=hostname,rdtype=mode)
    for answer in answers:
        print(answer)
    #print(answers)

main()
