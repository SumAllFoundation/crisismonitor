
def hashtags_to_json(data,name):
    #Save JSON Object and return the dictionary
    #hDict = to_json(hashtags,'hashtags2')
    import re
    import urllib2
    import json
    dataDict={}
    temp={}
    a=data
    a.index = a.index.format()
    temp = a.to_dict()
    for k,v in temp.iteritems():
         dataDict[k] = {'ts' : v}
    # #Articles
    # link1 = 'http://www.cnn.com/2013/06/11/world/europe/turkey-protests'
    # link2 = 'http://www.guardian.co.uk/commentisfree/2013/jun/18/turkey-standing-man'
    # link3 = 'http://www.nytimes.com/2013/06/16/world/europe/protesters-in-turkey.html?smid=tw-share&_r=0'
    # link4 = 'http://www.bbc.co.uk/news/world-europe-22925619'
    # link5 = 'http://www.guardian.co.uk/world/2013/jun/22/turkey-protests-erdogan-brazil-unrest-taksim'
    # link6 = 'http://edition.cnn.com/2013/06/24/world/europe/turkey-gokcek-hashtag/index.html?hpt=hp_t3'
    # #Append
    for k,v in dataDict.iteritems():
        if k in u'stoplyingcnn':
            dataDict[u'stoplyingcnn']['english'] = 'Stop Lying CNN!'
            dataDict[u'stoplyingcnn']['side'] = 'Govt'
        if re.compile(r'\bcevapver\b').search(k):
            dataDict[u'cevapver']['english'] = 'Answer!'
            dataDict[u'cevapver']['side'] = 'Pro'
            print k, ' amended'
        if k in u'türkiyebaşbakanınınyanında':
            dataDict[u'türkiyebaşbakanınınyanında']['english'] = 'Turkey stands behind the Prime Minister'
            dataDict[u'türkiyebaşbakanınınyanında']['side'] = 'Govt'
            print k, ' amended'
        if k in u'weareerdoğan':
            dataDict[u'weareerdoğan']['english'] = 'We are Erdogan'
            dataDict[u'weareerdoğan']['side'] = 'Govt'
            print k, ' amended'
        if k in u'wearegezi':
            dataDict[u'wearegezi']['english'] = 'We are Gezi'
            dataDict[u'wearegezi']['side'] = 'Pro'
        if re.compile(r'\bdirenankara\b').search(k):
            dataDict[u'direnankara']['english'] = 'Resist Ankara'
            dataDict[u'direnankara']['side'] = 'Pro'
            print k, ' amended'
        if k in u'direnhayattv':
            dataDict[u'direnhayattv']['english'] = 'Resist Hayat TV'
            dataDict[u'direnhayattv']['side'] = 'Pro'
            print k, ' amended'
        if k in u'direntürkçe':
            dataDict[u'direntürkçe']['english'] = 'Resist Turkish'
            dataDict[u'direntürkçe']['side'] = 'Pro'
            print k, ' amended'
        if k in u'direngezi':
            dataDict[u'direngezi']['english'] = 'Resist Gezi'
            dataDict[u'direngezi']['side'] = 'Pro'
            #dataDict[u'direngezi']['side'] = [link1,link3]
            print k, ' amended'
        if k in u'bugüngünlerdenankara':
            dataDict[u'bugüngünlerdenankara']['english'] = 'Today is Ankara'
            dataDict[u'bugüngünlerdenankara']['side'] = 'Govt'
            #dataDict[u'bugüngünlerdenankara']['article'] = [link4]
            print k, ' amended'
        if re.compile(r'\bdirengeziseninleyiz\b').search(k):
            dataDict[r'direngeziseninleyiz']['english'] = 'Resist Gezi, we are with you'
            dataDict[r'direngeziseninleyiz']['side'] = 'Pro'
            #dataDict[r'direngeziseninleyiz']['article'] = [link1]
            print k, ' amended'
        if k in u'provokatörünlüleriboykotediyoruz':
            dataDict[u'provokatörünlüleriboykotediyoruz']['english'] = 'Boycotting the provocateurs'
            dataDict[u'provokatörünlüleriboykotediyoruz']['side'] = 'Govt'
            print k, ' amended'
        if k in u'provokatörbaşbakanistemiyoruz':
            dataDict[u'provokatörbaşbakanistemiyoruz']['english'] = 'We dont want a provocateur Prime Minister'
            dataDict[u'provokatörbaşbakanistemiyoruz']['side'] = 'Pro'
            print k, ' amended'
        if k in u'türkiyeseninledikdureğilme':
            dataDict[u'türkiyeseninledikdureğilme']['english'] = 'Turkey is with you, dont compromise. '
            dataDict[u'türkiyeseninledikdureğilme']['side'] = 'Govt'
            print k, ' amended'
        if k in u'direngeziparkı':
            dataDict[u'direngeziparkı']['english'] = 'Resist Gezi Park'
            dataDict[u'direngeziparkı']['side'] = 'Pro'
            print k, ' amended'
        if re.compile(r'\bdirengeziparki\b').search(k):
            dataDict[u'direngeziparki']['english'] = 'Resist Gezi Park'
            dataDict[u'direngeziparki']['side'] = 'Pro'
            print k, ' amended'
        if k in u'occupyturkey':
            dataDict[u'occupyturkey']['english'] = 'Occupy Turkey'
            dataDict[u'occupyturkey']['side'] = 'Pro'
            print k, ' amended'
        if k in u'occupygezi':
            dataDict[u'occupygezi']['english'] = 'Occupy Gezi'
            dataDict[u'occupygezi']['side'] = 'Pro'
            print k, ' amended'
        if k in u'turkey':
            dataDict[k]['english'] = 'Turkey'
            dataDict[k]['side'] = 'Neutral'
            print k, ' amended'
        if k in u'türkiyesokakta':
            dataDict[u'türkiyesokakta']['english'] = 'Turkey took the streets'
            dataDict[u'türkiyesokakta']['side'] = 'Pro'
            #dataDict[u'türkiyesokakta']['article'] = [link3]
            print k, ' amended'
        if k in u'1milyonyarintaksime':
            dataDict[u'1milyonyarintaksime']['english'] = '1 million to Taksim!'
            dataDict[u'1milyonyarintaksime']['side'] = 'Pro'
            print k, ' amended'
        if k in u'doktorumadokunma':
            dataDict[u'doktorumadokunma']['english'] = 'Dont touch my doctor'
            dataDict[u'doktorumadokunma']['side'] = 'Pro'
        if k in u'SenÖde':
            dataDict[u'SenÖde']['english'] = 'You Pay!'
            dataDict[u'SenÖde']['side'] = 'Govt'
        if k in u'RedHackTarafındanHacklendik':
            dataDict[u'RedHackTarafındanHacklendik']['english'] = 'Hacked by RedHack'
            dataDict[u'RedHackTarafındanHacklendik']['side'] = 'Pro'
        if k in u'direnmüftü':
            dataDict[u'direnmüftü']['english'] = 'Resist Preacher!'
            dataDict[u'direnmüftü']['side'] = 'Pro'
        if k in u'duranadam':
            dataDict[u'duranadam']['english'] = 'Standing Man'
            dataDict[u'duranadam']['side'] = 'Pro'
            #dataDict['duranadam']['article'] = [link2]
        if k in u'BugünMilyonlarKAZLIÇEŞMEDE':
            dataDict[u'BugünMilyonlarKAZLIÇEŞMEDE']['english'] = '1 Million to Kazlicesme'
            dataDict[u'BugünMilyonlarKAZLIÇEŞMEDE']['side'] = 'Govt'
            #dataDict[u'BugünMilyonlarKAZLIÇEŞMEDE']['article']=[link4]
        if k in u'direnmersin':
            dataDict[u'direnmersin']['english'] = 'Resist Mersin!'
            dataDict[u'direnmersin']['side'] = 'Pro'
        if k in u'gündemiakgençlikbelirler':
            dataDict[u'gündemiakgençlikbelirler']['english'] = 'AKP Youth Movement determines the Agenda'
            dataDict[u'gündemiakgençlikbelirler']['side'] = 'Govt'
        if k in u'bingöldekitecavüzesessizkalma':
            dataDict[u'bingöldekitecavüzesessizkalma']['english'] = 'Dont forget the rape in Bingol'
            dataDict[u'bingöldekitecavüzesessizkalma']['side'] = 'Pro'
        if k in u'çapulculartaksime':
            dataDict[u'çapulculartaksime']['english']='All Looters to Taksim!'
            dataDict[u'çapulculartaksime']['side']='Pro'
            #dataDict[u'çapulculartaksime']['article'] = [link5]
        if k in u'provokatörmelihgökçek':
            dataDict[u'provokatörmelihgökçek']['english'] = 'Provocateur Mayor Melih Gokcek'
            dataDict[u'provokatörmelihgökçek']['side'] = 'Pro'
            #dataDict[u'provokatörmelihgökçek']['article'] = link6
        if k in u'kiralıkkatilahmetşahbaz':
            dataDict[u'kiralıkkatilahmetşahbaz']['english'] = 'Assasin Ahmet Sahbaz'
            dataDict[u'kiralıkkatilahmetşahbaz']['side'] = 'Pro'
        if k in u'bbctürkiyeyikariştirmahaberleridoğruver':
            dataDict[u'bbctürkiyeyikariştirmahaberleridoğruver']['english']='BBC, dont meddle, be balanced!'
            dataDict[u'bbctürkiyeyikariştirmahaberleridoğruver']['side'] = 'Govt'
        if k in u'redhack':
            dataDict[u'redhack']['english'] = 'RedHack'
            dataDict[u'redhack']['side'] = 'Pro'
        if k in u'dirençözüm':
            dataDict[u'dirençözüm']['english'] = 'Resist, resolution!'
            dataDict[u'dirençözüm']['side'] = 'Pro'
        if k in u'direnlice':
            dataDict[u'direnlice']['english'] = 'Resist, Lice!'
            dataDict[u'direnlice']['side'] = 'Pro'
        if k in u'dindargençliktakipleşiyor':
            dataDict[u'dindargençliktakipleşiyor']['english'] = 'Religious Youth following each other'
            dataDict[u'dindargençliktakipleşiyor']['side'] = 'Govt'        
        if k in u'direnmısır':
            dataDict[u'direnmısır']['english'] = 'Resist Egypt'
            dataDict[u'direnmısır']['side']  = 'Govt'
        if k in u'sivaskatliamınıunutmaunutturma':
            dataDict[u'sivaskatliamınıunutmaunutturma']['english'] = 'Dont forget Sivas massacre'
            dataDict[u'sivaskatliamınıunutmaunutturma']['side'] = 'Pro'
        if k in u'wearewithmorsi':
            dataDict[u'wearewithmorsi']['english'] = 'We are with Morsi'
            dataDict [u'wearewithmorsi']['side'] = 'Govt'
        if k in u'unutmadimaklımda':
            dataDict[u'unutmadimaklımda']['english'] = 'Dont forget Madimak'
            dataDict[u'unutmadimaklımda']['side'] = 'Pro'
        if k in u'aliismailkorkmaz':
            dataDict[u'aliismailkorkmaz']['english'] = 'Ali Ismail Korkmaz'
            dataDict[u'aliismailkorkmaz']['side'] = 'Govt'

    #Save
    f = open('%s.json'  % (name),'w')
    f.write(json.dumps(dataDict))
    f.close()
    return(dataDict)