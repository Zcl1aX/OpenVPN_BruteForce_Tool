# OpenVPN_BruteForce_Tool


#Help:


    -c, --config       [Config]       OpenVPN config file
    -u, --user         [Username]     Username to guess passwords against
    -p, --passw        [Password]     Password to try with username
    -t, --thread       [Thread]       Count of threads
    


#Example:  


    python3 ovpn_brute.py -c /opt/ovpn.conf -u /opt/username.txt -p /opt/passwordlist.txt -t 20
