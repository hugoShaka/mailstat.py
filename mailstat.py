#!/usr/bin/python3
import sys, os, re, csv
import logging
import optparse
from os import environ, remove

# initialize script
logging.basicConfig(format='%(levelname).1s: %(module)s:%(lineno)d: '
                           '%(message)s')
log = logging.getLogger(__name__)

def scanfolder(folder,score):
    if score==1:
        log.info('Scanning directory %s as SPAM', folder)
    else:
        log.info('Scanning directory %s as HAM', folder)
    results=[]
    for root, dirs, files in os.walk(folder): #On parcours le dossier courant
        for file in files:
            results.append((scanmail(folder+'/'+file),score))
    return results

def scanmail(file):
    mail=open(file,'r', encoding='utf-8', errors='ignore')
    match=re.search(r"X-Spam-Score: (?P<spamlevel>[0-9].[0-9]+)",mail.read())
    if match != None:
        return float(match.group('spamlevel'))
    else :
        return 0

def readconf(file):
    repos=open(file,'r')
    toScan=[]
    for line in repos:
        toScan.append((line.split(',')[0],int(line.split(',')[1])))
    return toScan


def exportdata(results,scandest):
    csvfile=open(scandest, 'w')
    resultwriter=csv.writer(csvfile, dialect='excel')
    for line in results:
        resultwriter.writerow(line)


def main():
    usage = '%prog [-c CONFIG FILE] [-o OUTPUT FILE]'
    parser = optparse.OptionParser(usage, version='%prog 0.1')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
        help='turn verbose more one')
    parser.add_option('-q', '--quiet', action='store_false', dest='verbose',
        default=False, help='be quiet')
    parser.add_option('-c', '--config',
        help='Specify a file where folders to scan are listed, SPAM=1, HAM=0.\n e.g. :\n /path/to/my/mailbox/spam,1 \n /path/to/my/mailbox/ham,0')
    parser.add_option('-o', '--output',
        help='Specify a file where results are exported, default = ./mailstat.csv')

    options, args = parser.parse_args()

    if options.verbose or environ.get('PYCLEAN_DEBUG') == '1':
        log.setLevel(logging.DEBUG)
        log.debug('argv: %s', sys.argv)
        log.debug('options: %s', options)
        log.debug('args: %s', args)
    else:
        log.setLevel(logging.WARNING)

#    d = destroyer()
#    d.next()  # initialize coroutine

    if not options.config and not args:
        parser.print_usage()
        exit(1)

    if options.config:
        log.info('Loading config file : %s', options.config)
        toScan=readconf(options.config)

    if not options.config:
        log.info('Loading default config file : %s', '/etc/mailstat.conf')
        toScan=readconf('/etc/mailstat.conf')

    log.info('Starting to scan folders')
    results=[]
    for repo in toScan:
        results+=scanfolder(repo[0],repo[1])

    if options.output:
        scandest=options.output
    else:
        scandest='mailstat.csv'
    log.info('Scan finished, exporting the results to %s',scandest)
    exportdata(results,scandest)

    log.info('Task finished')
    exit(0)

if __name__ == '__main__':
    main()

