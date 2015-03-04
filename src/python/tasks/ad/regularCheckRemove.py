import ldap, ldif
from ldap.controls import SimplePagedResultsControl
import sys
import ldap.modlist as modlist
import getpass
import datetime
from datetime import date, timedelta



past_n_days = sys.argv[1]
ad_login = sys.argv[2]
secret = sys.argv[3]
yesterday = date.today() - timedelta(int(past_n_days))
daysBeforeTimestamp =  yesterday.strftime("%Y%m%d") +"000000.0Z"
current_time = datetime.datetime.now()
log = open("/var/log/ad_leave_log","a")

#ad_login = raw_input("AD login name:")
#secret = getpass.getpass()
#title = raw_input("query title:")
#displayName = raw_input("query name:")
displayName = "xSP"


def getSingleUserFromName():
    AD_DOMAIN = 'TREND'
    AD_HOST = 'ldap://10.28.1.212:3268'
    AD_PORT = 3268
    AD_BASE = 'DC=tw,DC=trendnet,DC=org'
    #AD_FILTER = '(&(objectClass=user)(userAccountControl=514)(samaccountname='+user_name+'*)(whenChanged>=20140101000000.0Z))'
    AD_FILTER = '(&(objectClass=user)(userAccountControl=514)(whenChanged>='+daysBeforeTimestamp+'))'
#    print AD_FILTER
  #  AD_FILTER = '(&(objectClass=user)(title='+title+'*))'
#AD_FILTER = "(&(objectClass=group)(CN=*"+displayName+"*))"

# LDAP connection
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
        ldap_connection = ldap.initialize(AD_HOST)
        ldap_connection.set_option(ldap.OPT_REFERRALS,0)
        ldap_connection.simple_bind_s(ad_login, secret)
        r =  ldap_connection.search(AD_BASE,ldap.SCOPE_SUBTREE,AD_FILTER)
        Type,users = ldap_connection.result(r,200)
        cnt = 0
        for user in users:
#    ldif_writer=ldif.LDIFWriter(open("/tmp/yes","a"))
#    ldif_writer.unparse("",user[1])
            # print user[1]
            toPrint = "\t"+user[1]['name'][0] + " "+ user[1]['whenChanged'][0] +" " 
            if user[1].has_key('title') :
                toPrint += user[1]['title'][0] + " "
         
            if user[1].has_key('manager') :
                toPrint += user[1]['manager'][0] + " "

            toPrint += " \n"
            log.write(toPrint)
            
    #print str(cnt)+" "+ user[0] 
#            if title == 'Director' :
#                print user[1]['name']
    #print user[1]['title'][0] + ", report to:'" + user[1]['manager'][0] + "',  "+user[1]['info'][0]
            cnt+= 1
    #if cnt >= 1 :
    #    break 

        return(cnt)

    except ldap.LDAPError, e:
      err_msg = str(current_time) + ' Error connecting to LDAP server: ' + str(e) + '\n'
      sys.stderr.write(err_msg)
      log.write(err_msg)
      sys.exit(1)

# Lookup usernames from LDAP via paged search
#paged_results_control = SimplePagedResultsControl(
#  ldap.LDAP_CONTROL_PAGE_OID, True, (PAGE_SIZE, ''))
#accounts = []
#pages = 0
#while True:


result = str(current_time)+" "+ str(getSingleUserFromName()) +"\n"


print result
log.write("========================================")
log.write(result)

