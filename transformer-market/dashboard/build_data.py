import json, os, sys
out = sys.argv[1]
def w(name, rows):
    with open(os.path.join(out, name), 'w') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(name, len(rows))

U = {
 'woodmac_op': 'https://www.woodmac.com/news/opinion/transformer-troubles-manufacturing-and-policy-constraints-hit-us-transformer-supply/',
 'woodmac_eo': 'https://www.woodmac.com/press-releases/us-executive-order-banning-chinese-bulk-power-equipment-set-to-worsen-critical-transformer-shortage/',
 'powermag': 'https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/',
 'ppi': 'https://labordatahub.com/producer-prices/power-distribution-and-specialty-transformer-manufacturing',
 'eei': 'https://www.eei.org/en/news/news/all/2026-grid-record',
 'spg': 'https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/surging-energy-demand-puts-us-utility-capex-forecast-near-1-3t-in-2026-30',
 'gab': 'https://gabelli.com/research/utilities-u-s-outlook/',
 'siemens_lpt': 'https://www.investing.com/news/stock-market-news/siemens-energy-targets-us-transformer-production-in-2027-can-further-expand-factory-4113341',
}

def fig(id, group, label, value, unit=None, prefix=None, qualifier=None, note=None, prior=None, prior_label=None, asof=None, confidence='S', url=None):
    return dict(id=id, group=group, label=label, value=value, unit=unit, prefix=prefix, qualifier=qualifier, note=note, prior=prior, prior_label=prior_label, asof=asof, confidence=confidence, source_url=url)

figures = [
 fig('report_window','meta','Week of Oct 5–11, 2026 · first run, sets the baseline',None,asof='2026-10-11',confidence='P',url=None),
 fig('lpt_lead','headline','Large power transformer lead time',128,'weeks',note='Average in Wood Mackenzie’s Q2 2025 survey. 2026 trackers show 120–160+ weeks.',asof='2025-Q2',url=U['woodmac_op']),
 fig('gsu_lead','headline','Generator step-up lead time',144,'weeks',note='Longest of any class. Some 2026 trackers put it above 160 weeks.',asof='2025-Q2',url=U['woodmac_op']),
 fig('deficit_power','headline','Power transformer supply gap, 2026',15,'%',note='Share of US demand that supply can’t meet, per Wood Mackenzie.',prior=30,prior_label='2025',asof='2026',url=U['woodmac_eo']),
 fig('ppi_yoy','headline','Transformer prices, last 12 months',8.7,'%',prefix='+',note='BLS index WPU117409, Jul 2026. Up 91.4% since Jan 2020.',asof='2026-07',url=U['ppi']),
 fig('capex_2026','headline','Investor-owned utility capex, 2026',239,'B',prefix='$',note='EEI projection. $1.4T planned over 2026–30, up from $1.1T.',asof='2026',confidence='P',url=U['eei']),
 fig('lpt_import','headline','Large power transformers imported',80,'%',qualifier='>',note='Domestic plants cover about 20% of US demand, per Siemens Energy.',asof='2025',confidence='P',url=U['siemens_lpt']),

 fig('eei_2026','capex_annual','EEI',239,'B',prefix='$',note='Investor-owned electric companies, 2026 projection.',asof='2026',confidence='P',url=U['eei']),
 fig('sp_2026','capex_annual','S&P Global',227.8,'B',prefix='$',note='S&P utility peer group, 2026.',asof='2026',url=U['gab']),
 fig('rra_2026','capex_annual','RRA (S&P)',259.1,'B',prefix='$',note='46 tracked companies incl. gas utilities, 2026.',asof='2026-04',url=U['spg']),
 fig('eei_prior','capex_5yr','EEI, prior plan',1.1,'T',prefix='$',note='Late-2025 projection for 2025–29.',asof='2025',url=U['eei']),
 fig('rra_5yr','capex_5yr','RRA, 2026–30',1.295,'T',prefix='$',note='Record, April 2026 forecast.',asof='2026-04',url=U['spg']),
 fig('eei_5yr','capex_5yr','EEI, 2026–30',1.4,'T',prefix='$',note='Current EEI projection.',asof='2026',confidence='P',url=U['eei']),

 fig('gev_electrification','backlog','GE Vernova Electrification backlog',41,'B',prefix='$',qualifier='~',note='Q2 2026, includes Prolec GE. About $800M of US transformer orders in the quarter.',asof='2026-06-30',confidence='P',url='https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000147/gevpressrelease2q26.htm'),
 fig('siemens_grid','backlog','Siemens Energy Grid Technologies backlog',51,'B',prefix='€',note='Record, Aug 2026. Orders up 28%, led by large power transformers.',asof='2026-08',confidence='W',url='https://mgrid.org/2026/08/09/siemens-energys-grid-order-backlog-hits-a-record-51-billion-euros-on-transformer-demand/'),
 fig('hdh_backlog','backlog','HD Hyundai Electric backlog',8.5,'B',prefix='$',note='End of June 2026. Largest share of the US ultra-high-voltage market.',asof='2026-06-30',url='https://finance.biggo.com/news/78314cef-6521-4054-b7fb-58f76f7fde04'),
 fig('eaton_b2b','backlog','Eaton Electrical Americas book-to-bill',1.3,'x',note='Q2 2026. Segment backlog up 33% year over year.',asof='2026-06-30',confidence='P',url='https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000027/etn06302026exhibit99.htm'),
 fig('hammond_backlog','backlog','Hammond Power Solutions backlog, year over year',96.9,'%',prefix='+',note='Q2 2026. Down 6.9% from Q1 as shipments outran new orders.',asof='2026-06-30',confidence='P',url='https://tedmag.com/hammond-power-solutions-reports-2q-2026-results/'),
 fig('quanta_backlog','backlog','Quanta Services backlog',53.4,'B',prefix='$',note='Q2 2026 record. Owns PTT and Niagara Power Transformer.',asof='2026-06-30',confidence='P',url='https://www.prnewswire.com/news-releases/quanta-services-reports-second-quarter-2026-results-302838646.html'),

 fig('korea_exports','trade','Korean UHV transformer exports, 2025',1.3,'B',prefix='$',note='Record. About $738M went to the US.',asof='2025',url='https://transformer-magazine.com/news/korean-transformer-exports-hit-1-3-b/'),
 fig('korea_share','trade','Korean makers’ share of the US market',25,'%',qualifier='~',note='HD Hyundai alone held 25.7% of US ultra-high-voltage sales in 2025.',asof='2025',url='https://transformer-magazine.com/news/korean-transformer-exports-hit-1-3-b/'),
 fig('china_exports','trade','Chinese transformer exports, 2025',9.3,'B',prefix='$',qualifier='~',note='Record ¥64.6B. US-bound shipments up 182% in Jan–Feb 2026 (newsletter source).',asof='2025',confidence='W',url='https://crossdockinsights.com/p/transformer-crisis-is-threatening-america'),
 fig('mexico_imports','trade','US transformer imports from Mexico, 2023',2.3,'B',prefix='$',note='Largest source by value, about 20% of HS 8504 imports.',asof='2023',url='https://www.indexbox.io/blog/us-electrical-transformer-imports-2023/'),
 fig('eo_exposure','trade','Imports exposed to EO 14420',22,'B',prefix='$',qualifier='>',note='Bulk-power equipment imported since 2025, nearly all from China. Hardest hit: 100 MVA and up.',asof='2026-09',url=U['woodmac_eo']),

 fig('copper_px','inputs','Copper, COMEX',6.66,'/lb',prefix='$',note='Oct 9, 2026, near the record set on Sep 9.',prior=6.89,prior_label='record',asof='2026-10-09',confidence='W',url='https://metalcharts.org/copper-price'),
 fig('goes_add','inputs','Cleveland-Cliffs electrical steel (GOES) output added',25,'%',qualifier='up to',note='$200M expansion plus a $75M DOE award at Butler Works, PA. Cliffs is the only US maker.',asof='2026-10-04',confidence='P',url='https://www.businesswire.com/news/home/20261004168131/en/Cleveland-Cliffs-to-Host-U.S.-Secretary-of-Energy-Chris-Wright-and-Other-Government-Officials-at-Butler-Works-to-Showcase-GOES-Expansion-Project'),
 fig('goes_price','inputs','GOES price change, 2020–24',100,'%',prefix='+',note='Prices doubled. Cliffs widths top out near 920mm, narrower than many large-transformer cores need.',asof='2024',url='https://www.breakthroughjournal.org/p/america-makes-the-wrong-steel-for'),
 fig('price_since_2019','inputs','Power transformer unit prices vs 2019',77,'%',prefix='+',note='Wood Mackenzie, via POWER magazine.',asof='2025',url=U['powermag']),

 fig('prolec_half','valuation','GE Vernova paid for half of Prolec GE',5254,'M',prefix='$',note='Closed Feb 2, 2026.',asof='2026-02-02',confidence='P',url='https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000148/gev-20260630.htm'),
 fig('vtc_sale','valuation','Virginia Transformer sale talk',6,'B',prefix='$',qualifier='>',note='Bloomberg, early 2025. No deal confirmed since.',asof='2025',url='https://news.bloomberglaw.com/mergers-and-acquisitions/virginia-transformer-is-said-to-consider-6-billion-sale-1'),
 fig('maclean','valuation','Blackstone buying MacLean Power Systems',4,'B',prefix='$',qualifier='~',note='Reported Nov 2025. MacLean is now buying Delta Star.',asof='2025-11',url='https://www.bloomberg.com/news/articles/2025-11-26/blackstone-nears-4-billion-deal-for-maclean-power-systems'),
 fig('forgent_ipo','valuation','Forgent IPO price',27,'/share',prefix='$',note='Feb 5, 2026, NYSE: FPS.',asof='2026-02-05',url='https://www.renaissancecapital.com/IPO-Center/News/116759/Electrical-equipment-maker-Forgent-Power-Solutions-prices-US-IPO-at-$27-mid'),
 fig('forgent_follow','valuation','Forgent follow-on price',47,'/share',prefix='$',note='Follow-on sold by Neos-controlled holders and the company.',asof='2026',url='https://www.oppenheimer.com/hmgroup/2026/notable-transactions/joint-bookrunner-on-forgent-power-solutions-inc-billion-follow-on-offering'),
]
w('figures.json', figures)

lead = [
 dict(id='gsu',cls='Generator step-up (GSU)',low_wks=144,typical_wks=144,high_wks=160,extreme_wks=None,note='Wood Mackenzie Q2 2025 average 144 weeks; 2026 trackers report more than 160.',confidence='S',source_url=U['woodmac_op']),
 dict(id='lpt',cls='Large power (>100 MVA)',low_wks=110,typical_wks=128,high_wks=160,extreme_wks=208,note='128-week average (Wood Mackenzie). Some extra-high-voltage quotes run four to five years.',confidence='S',source_url='https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/'),
 dict(id='mid',cls='Mid power (30–100 MVA)',low_wks=60,typical_wks=None,high_wks=90,extreme_wks=None,note='2026 procurement guide range.',confidence='W',source_url='https://distroforge.com/blog/transformer-procurement-2026/'),
 dict(id='pad',cls='Pad-mount distribution',low_wks=30,typical_wks=None,high_wks=60,extreme_wks=None,note='About 30 weeks in one index, 40–60 in another. Three-phase pad-mount shortage expected to worsen.',confidence='W',source_url='https://usevawn.com/resources/electrical-equipment-lead-times/'),
 dict(id='dist',cls='Standard distribution',low_wks=26,typical_wks=None,high_wks=50,extreme_wks=None,note='Expected to ease toward 26–38 weeks by Q4 2026 as new plants ramp.',confidence='W',source_url='https://distroforge.com/blog/transformer-procurement-2026/'),
]
w('leadtimes.json', lead)

deficit = [
 dict(year=2025,label='2025',power_pct=30,kind='Estimate',note='Wood Mackenzie Q2 2025 survey.',confidence='S',source_url=U['powermag']),
 dict(year=2026,label='2026',power_pct=15,kind='Estimate',note='Wood Mackenzie, Sep 2026.',confidence='S',source_url=U['woodmac_eo']),
 dict(year=2030,label='2030',power_pct=5,kind='Projection',note='Secondary report of Wood Mackenzie modelling.',confidence='W',source_url='https://distroforge.com/blog/transformer-procurement-2026/'),
]
w('deficit.json', deficit)

ppi = [
 dict(series='WPU117409',name='Power and distribution transformers',month='2026-07',index_value=381.783,yoy_pct=8.7,since_jan2020_pct=91.4,confidence='S',source_url=U['ppi']),
 dict(series='PCU335311',name='Transformer manufacturing (NAICS 335311)',month='2026-03',index_value=455.9,yoy_pct=4.27,since_jan2020_pct=None,confidence='S',source_url='https://tradingeconomics.com/united-states/producer-price-index-by-industry-electric-power-and-specialty-transformer-manufacturing-fed-data.html'),
]
w('ppi.json', ppi)

def cap(id, company, short, owner, state, country, lane, segment, inv, note, jobs, announced, oy, ol, status, conf, url):
    return dict(id=id, company=company, short=short, owner=owner, state=state, country=country, lane=lane, segment=segment, investment_usd_m=inv, capacity_note=note, jobs=jobs, announced=announced, online_year=oy, online_label=ol, status=status, confidence=conf, source_url=url)
E='765 kV / EHV'; P='Power transformers'; D='Distribution & MV'; K='Components & steel'; S_='Solid-state'
capacity = [
 cap('hitachi_gallman','Hitachi Energy','Hitachi · Gallman MS','Hitachi','MS','US',P,'10–160 MVA, up to 230 kV',528,'More than doubles Hitachi’s US small and mid power output',700,'2026-09-15',2029,'2029','Announced','P','https://www.hitachienergy.com/news-and-events/press-releases/2026/09/hitachi-deepens-commitment-to-u-s-manufacturing-with-528-million-mississippi-transformer-factory'),
 cap('hitachi_southboston','Hitachi Energy','Hitachi · South Boston VA','Hitachi','VA','US',P,'Large power transformers',457,'Billed as the largest US large-transformer plant',None,'2025-09',2028,'2028','Under construction','S','https://www.utilitydive.com/news/hitachi-unveils-1b-grid-manufacturing-investment-including-virginia-trans/759219/'),
 cap('hitachi_varennes','Hitachi Energy','Hitachi · Varennes QC','Hitachi','QC','CA',P,'Large power transformers',195,'Nearly triples site output; new test bay',500,'2025-10',2027.9,'End of 2027','Under construction','S','https://www.theglobeandmail.com/business/article-hitachi-plans-270-million-expansion-of-quebec-power-transformer'),
 cap('hitachi_alamo','Hitachi Energy','Hitachi · Alamo TN','Hitachi','TN','US',K,'Bushings',106,'Bushings plant for Hitachi’s own transformers',None,'2025-08',None,'Not disclosed','Under construction','S','https://www.latitudemedia.com/news/hitachi-energy-invests-106-million-to-build-out-the-u-s-transformer-supply-chain/'),
 cap('prolec_goldsboro','Prolec GE','Prolec GE · Goldsboro NC','GE Vernova','NC','US',P,'Power transformers',140,'220 → 420 units a year',330,'2025-05',2027.9,'End of 2027','Under construction','S','https://www.goldsborodailynews.com/2026/03/18/prolec-ge-waukesha-breaks-ground-on-140m-expansion/'),
 cap('prolec_shreveport','Prolec GE','Prolec GE · Shreveport LA','GE Vernova','LA','US',D,'Small power and distribution',34,'Third line, about 1,500 more units a year',None,'2024',2025,'2025','Operating','S','https://bossierpress.com/prolec-ge-completes-34-million-expansion-of-shreveport-facility-boosting-energy-transition-efforts-and-local-economy/'),
 cap('prolec_monterrey','Prolec GE','Prolec GE · Monterrey MX','GE Vernova','MX','MX',P,'Power transformers',85,'Doubles Prolec’s Mexico output',None,'2024',2025.5,'Mid-2025 (unconfirmed)','Unconfirmed','S','https://transformer-magazine.com/news/prolec-ge-invests-85-m-in-transformer-manufacturing-capacity/'),
 cap('siemens_charlotte','Siemens Energy','Siemens Energy · Charlotte NC','Siemens Energy','NC','US',P,'Large power transformers',150,'24 → 57 large units a year',559,'2024-07',2027,'2027 (slipped from 2026)','Under construction','S',U['siemens_lpt']),
 cap('hdh_montgomery','HD Hyundai Electric','HD Hyundai · Montgomery AL','HD Hyundai','AL','US',E,'Extra-high voltage up to 765 kV',200,'Adds 50% to EHV output plus 765 kV testing',None,'2026-03',2027.25,'Apr 2027','Under construction','S','https://en.sedaily.com/finance/2026/03/08/hd-hyundai-electric-breaks-ground-on-us-plant-expansion'),
 cap('hyosung_memphis','Hyosung HICO','Hyosung · Memphis TN','Hyosung Heavy Industries','TN','US',E,'765 kV and ultra-high voltage',157,'130 → 250+ units a year',None,'2025-11',2027.5,'2027–28','Under construction','S','https://evertiq.com/news/2026-09-18-hyosung-secures-287-million-us-orders-for-uhv-transformers'),
 cap('mitsubishi_memphis','Mitsubishi Electric Power Products','Mitsubishi · Memphis TN','Mitsubishi Electric','TN','US',E,'Shell-type, 161–765 kV, up to 1,500 MVA',200,'Built the first US-made 765 kV unit in 25 years',275,'2023',2025,'Operating','Operating','S','https://transformer-magazine.com/news/3122-first-765-kv-transformer-manufactured-in-u-s-in-25-years-power/'),
 cap('vtc_muscleshoals','Virginia Transformer','Virginia Transformer · Muscle Shoals AL','Private','AL','US',P,'2–500 MVA',None,'600k sq ft greenfield, seventh NA plant',1100,'2026-05-19',2028.05,'Jan 2028','Announced','P','https://governor.alabama.gov/newsroom/2026/05/governor-ivey-announces-virginia-transformer-plant-will-bring-1100-jobs-to-northwest-alabama/'),
 cap('vtc_rincon','Virginia Transformer','Virginia Transformer · Rincon GA','Private','GA','US',P,'Power transformers',40,'About 70% more output',400,'2025-11-20',2026.5,'2026–27','Under construction','P','https://gov.georgia.gov/press-releases/2025-11-20/gov-kemp-virginia-transformer-create-400-jobs-effingham-expansion'),
 cap('ptt_raeford','Pennsylvania Transformer Technology','PTT (Quanta) · Raeford NC','Quanta Services','NC','US',P,'5–750 MVA, up to 765 kV',102.5,'300k sq ft more across two buildings',217,'2025-12',None,'Not disclosed','Announced','S','https://transformer-technology.com/ptt-expands-manufacturing-in-raeford-nc-with-102-million-investment-transformer-technology-news/'),
 cap('niagara','Niagara Power Transformer','Niagara (Quanta) · Cheektowaga NY','Quanta Services','NY','US',P,'Power transformers',71,'90 → 140 units a year',None,'2026-09-02',None,'Not disclosed','Announced','S','https://www.ien.com/operations/news/22973547/centuryold-transformer-maker-plans-71m-expansion-in-new-york'),
 cap('howard_ellisville','Howard Industries','Howard · Ellisville MS','Private','MS','US',P,'Medium power',100,'230k sq ft more',100,'2026-04-02',None,'Not disclosed','Announced','P','https://www.howardcomputers.com/INFO/news/2026/04/02/howard-industries-announces-100-million-expansion-of-medium-power-transformer-plant-in-ellisville-mississippi.cfm'),
 cap('delta_lynchburg','Delta Star','Delta Star · Lynchburg VA','Private (to MacLean)','VA','US',P,'Power transformers and mobile substations',35,'Expansion; company being sold to MacLean',300,'2025-04',None,'Not disclosed','Under construction','S','https://cardinalnews.org/2026/09/01/lynchburg-based-delta-star-to-be-acquired-at-time-of-unprecedented-demand-for-transformers/'),
 cap('weg_tula','WEG','WEG · Atotonilco de Tula MX','WEG','MX','MX',P,'Power transformers up to 550 kV',156,'Part of a plan for 50% more capacity (2023)',None,'2023',None,'Not disclosed','Unconfirmed','S','https://transformer-technology.com/weg-s-a-unleashes-245-million-investment-to-supercharge-transformer-production-across-americas/'),
 cap('eaton_jonesville','Eaton','Eaton · Jonesville SC','Eaton','SC','US',D,'Three-phase distribution',340,'Converts an existing site',700,'2025-09',2027,'2027','Under construction','S','https://www.utilitydive.com/news/eaton-transformer-production-shortage-investment/739932/'),
 cap('ermco_az','ERMCO','ERMCO · Maricopa County AZ','Arkansas Electric Cooperatives','AZ','US',D,'Three-phase distribution',None,'566k sq ft, first plant west of the Mississippi',None,'2026-01',2027,'2027','Under construction','S','https://www.powermag.com/ermco-expands-transformer-manufacturing-west-with-new-arizona-facility/'),
 cap('central_moloney_fl','Central Moloney','Central Moloney · Panama City Beach FL','Private','FL','US',D,'Distribution',None,'Second plant in leased space',250,'2025',None,'Not confirmed','Unconfirmed','S','https://www.arkansasbusiness.com/article/2-arkansas-owned-transformer-makers-expanding-due-to-peak-demand/'),
 cap('jst_wytheville','JST Power Equipment','JST · Wytheville VA','Private','VA','US',D,'Pad-mount',None,'About 150 units in 2026, 1,000 a year from 2027',None,'2025-03',2026.38,'Opened May 2026','Operating','S','https://finance.yahoo.com/sectors/energy/articles/jst-power-equipment-opens-virginia-170000743.html'),
 cap('giga_houston','Giga Energy','Giga Energy · Houston TX','Private (venture)','TX','US',D,'Medium-voltage pad-mount',None,'Targets 1,000–3,000+ units a year (release conflicts)',100,'2025-12-16',2026.1,'Q1 2026 (planned)','Unconfirmed','P','https://www.prnewswire.com/news-releases/giga-energy-announces-new-houston-manufacturing-facility-to-expand-us-transformer-production-to-power-ai-infrastructure-302643008.html'),
 cap('vantran_waco','Forgent (VanTran / MGM)','VanTran/MGM · Waco TX','Forgent Power Solutions','TX','US',D,'Custom liquid-filled',None,'430k sq ft plant',700,'2025-05-22',2025.4,'May 2025','Operating','S','https://solarbuildermag.com/operations-maintenance/vantran-mgm-transformers-open-new-manufacturing-facility-in-texas/'),
 cap('hammond_mx','Hammond Power Solutions','Hammond · Mexico','Hammond Power Solutions','MX','MX',D,'Dry-type',None,'Began shipping Q1 2026',None,'2024',2026.1,'Q1 2026','Operating','P','https://tedmag.com/hammond-power-solutions-reports-2q-2026-results/'),
 cap('cliffs_weirton','Cleveland-Cliffs','Cleveland-Cliffs · Weirton WV','Cleveland-Cliffs','WV','US',D,'Distribution',150,'Planned plant that would use Cliffs steel',None,'2024',None,'Not disclosed','Unconfirmed','S','https://www.utilitydive.com/news/cleveland-cliffs-confirms-150-million-electric-transformer-weirton-plant/723363/'),
 cap('cliffs_butler','Cleveland-Cliffs','Cleveland-Cliffs · Butler PA','Cleveland-Cliffs','PA','US',K,'Grain-oriented electrical steel (GOES)',275,'Up to 25% more GOES; includes $75M DOE award',None,'2026-10-04',None,'Not disclosed','Announced','P','https://www.businesswire.com/news/home/20261004168131/en/Cleveland-Cliffs-to-Host-U.S.-Secretary-of-Energy-Chris-Wright-and-Other-Government-Officials-at-Butler-Works-to-Showcase-GOES-Expansion-Project'),
 cap('worthington_burlington','Worthington Steel','Worthington · Burlington ON','Worthington Steel','ON','CA',K,'Electrical steel and transformer cores',None,'New core-making facility',None,'2026',None,'Not disclosed','Announced','P','https://www.sec.gov/Archives/edgar/data/0001968487/000119312526352313/d163827dars.pdf'),
 cap('heron_ca','Heron Power','Heron Power · California','Private (venture)','CA','US',S_,'Solid-state transformers',100,'Targets 40 GW a year',None,'2026-02-18',2027.75,'2H 2027','Announced','S','https://www.canarymedia.com/articles/climatetech-finance/heron-power-raises-140m-electrical-transformers'),
]
w('capacity.json', capacity)

def deal(id,date,date_label,acq,tgt,typ,val,val_note,status,seg,read,tw,conf,url):
    return dict(id=id,date=date,date_label=date_label,acquirer=acq,target=tgt,type=typ,value_usd_m=val,value_note=val_note,status=status,segment=seg,read_through=read,this_week='Yes' if tw else 'No',confidence=conf,source_url=url)
deals = [
 deal('ips_belyea','2026-10-07','Oct 7, 2026','Integrated Power Services','Belyea Company (high-voltage business)','Acquisition',None,'Undisclosed','Closed','Aftermarket','Refurbishment and rental are being rolled up',True,'S','https://pulse2.com/integrated-power-services-acquires-belyea-company/'),
 deal('marsons_cleanhill','2026-10-06','Oct 6, 2026','Marsons + Cleanhill Partners','US and Canada joint venture','Joint venture',None,'Undisclosed','Board-approved','New entrant','Indian supply moves toward the space China is losing',True,'S','https://www.tndindia.com/marsons-teams-up-with-cleanhill-partners-plans-jv-to-manufacture-transformers-for-north-american-market/'),
 deal('schneider_ptc','2026-10-05','Oct 5, 2026','Schneider Electric','PTC','Acquisition',22600,'$22.6B','Signed','Other','Shows how much electrical majors can spend (software, not transformers)',True,'S','https://www.axios.com/2026/10/05/schneider-electric-ptc'),
 deal('maclean_delta','2026-09-03','Sep 3, 2026','MacLean Power Systems (Blackstone, Centerbridge)','Delta Star','Acquisition',None,'Undisclosed','Signed, closing Q4 2026','Power','Private equity platform adds power transformers and mobile substations',False,'S','https://virginiabusiness.com/maclean-power-systems-acquire-delta-star/'),
 deal('tjc_sunbelt','2026-07-20','Jul 20, 2026','TJC','Sunbelt Solomon','Acquisition',None,'Undisclosed','Signed, close unconfirmed','Aftermarket','Private equity pays for remanufacturing and lifecycle services',False,'S','https://www.cahill.com/news/firm-news/2026-07-24-cahill-private-credit-group-represents-financing-sources-in-tjc-acquisition-of-sunbelt-solomon'),
 deal('hammond_aeg','2026-07-15','Jul 2026','Hammond Power Solutions','AEG Power Solutions','Acquisition',None,'Undisclosed','Closed','Other','Dry-type maker adds power electronics',False,'P','https://tedmag.com/hammond-power-solutions-reports-2q-2026-results/'),
 deal('hitachi_canduct','2026-06-15','Jun 2026','Hitachi Energy','Canduct Group','Acquisition',None,'Undisclosed','Signed, closing Q3 2026','Components','Incumbents are buying scarce components',False,'P','https://www.hitachienergy.com/news-and-events/press-releases/2026/06/hitachi-energy-bolsters-the-regional-transformer-market-with-strategic-investment-in-north-america'),
 deal('heron_b','2026-02-18','Feb 18, 2026','a16z, Breakthrough Energy Ventures','Heron Power','Series B',140,'$140M','Closed','Solid-state','Venture money for solid-state transformers',False,'S','https://www.canarymedia.com/articles/climatetech-finance/heron-power-raises-140m-electrical-transformers'),
 deal('forgent_ipo','2026-02-05','Feb 5, 2026','Public markets','Forgent Power Solutions','IPO',1500,'$1.5–1.7B raised','Closed','Distribution','Investors reward data-center electrical makers; follow-on priced at $47 vs $27 IPO',False,'S','https://www.renaissancecapital.com/IPO-Center/News/116759/Electrical-equipment-maker-Forgent-Power-Solutions-prices-US-IPO-at-$27-mid'),
 deal('gev_prolec','2026-02-02','Feb 2, 2026','GE Vernova','Prolec GE (Xignux’s 50%)','Acquisition',5254,'$5.25B','Closed','Power','Implies about $10.5B for the whole company',False,'P','https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000148/gev-20260630.htm'),
 deal('blackstone_maclean','2025-11-26','Nov 2025','Blackstone','MacLean Power Systems','Acquisition',4000,'~$4B (reported)','Reported','Components','The platform now buying Delta Star',False,'S','https://www.bloomberg.com/news/articles/2025-11-26/blackstone-nears-4-billion-deal-for-maclean-power-systems'),
 deal('amperesand_a','2025-11-15','Nov 2025','Walden Catalyst, Temasek','Amperesand','Series A',80,'$80M','Closed','Solid-state','Solid-state transformers for data centers',False,'S','https://techcrunch.com/2026/02/20/why-investors-are-going-gaga-over-solid-state-transformers/'),
 deal('eaton_resilient','2025-08-15','Aug 2025','Eaton','Resilient Power Systems','Acquisition',None,'Undisclosed','Closed','Solid-state','Incumbent buys solid-state know-how',False,'S','https://www.tdworld.com/utility-business/news/55311261/eaton-corporation-eaton-acquires-resilient-power-systems-to-expand-solid-state-transformer-technology'),
 deal('vtc_sale','2025-01-15','Early 2025','Sale process','Virginia Transformer','Sale exploration',6000,'>$6B (reported)','No deal confirmed','Power','Largest private NA power-transformer maker tested the market',False,'S','https://news.bloomberglaw.com/mergers-and-acquisitions/virginia-transformer-is-said-to-consider-6-billion-sale-1'),
 deal('quanta_ptt','2024-01-15','2023–24','Quanta Services','Pennsylvania Transformer Technology','Acquisition',300,'~$300M','Closed','Power','Contractor integrates into transformer supply; later added Niagara',False,'S','https://transformer-magazine.com/news/quanta-buys-pennsylvania-transformer-manufacturer-for-300-m/'),
 deal('ermco_spire','2022-12-15','Dec 2022','ERMCO','Spire Power Solutions','Acquisition',None,'Undisclosed','Closed','Distribution','Co-op-owned maker adds dry-type and liquid brands',False,'S','https://www.lincolninternational.com/transactions/mill-point-capital-has-sold-spire-power-solutions-to-ermco/'),
]
w('deals.json', deals)

def pol(id,date,date_label,instrument,kind,status,rate,applies,effect,until,conf,url):
    return dict(id=id,date=date,date_label=date_label,instrument=instrument,kind=kind,status=status,rate_label=rate,applies_to=applies,effect=effect,until=until,confidence=conf,source_url=url)
policy = [
 pol('s232_cores','2025-08-18','Aug 2025','Section 232 steel derivatives: cores and laminations','Tariff','In force','50%','Imported GOES cores and laminations','Raises costs for US builders that import cores.',None,'W','https://x.com/tengyanAI/status/2064320611409911949'),
 pol('scotus_ieepa','2026-02-20','Feb 20, 2026','IEEPA tariffs struck down','Tariff','Struck down','None (refunds under way)','All IEEPA duties','Supreme Court ruled IEEPA does not allow tariffs. CBP is processing refunds.',None,'S','https://www.aoshearman.com/en/insights/scotus-rejects-ieepa-tariffs-refund-opportunities-and-uncertainty-emerge'),
 pol('sec122','2026-02-24','Feb 24, 2026','Section 122 global tariff','Tariff','Expired','10%','Most imports','Temporary surcharge. Trade court ruled it invalid; stayed on appeal.','Jul 24, 2026','S','https://www.skadden.com/insights/publications/2026/05/us-trade-court-strikes-down-section-122-tariffs'),
 pol('s232_restructure','2026-04-06','Apr 6, 2026','Section 232 metals restructure (Proclamation 11021)','Tariff','In force','25%','Transformers (HTS 8504) as steel derivatives, on full customs value','Goods that are almost all metal pay 50%; goods with little metal are excluded.',None,'S','https://www.whitecase.com/insight-alert/united-states-modifies-steel-aluminum-and-copper-section-232-tariffs'),
 pol('s232_copper','2026-04-06','Apr 6, 2026','Section 232 copper','Tariff','In force','50% / 25%','Semi-finished copper / copper-intensive derivatives','Refined copper tariff phases in: 15% in 2027, 30% in 2028.',None,'S','https://www.freightfigures.com/articles/section-232-copper-tariff-tiered-rates-april-2026'),
 pol('dpa','2026-04-20','Apr 20, 2026','Defense Production Act determination','Support','In force',None,'Transformers, grid equipment, electrical core steel','Lets DOE buy and finance new domestic capacity.',None,'P','https://www.govinfo.gov/content/pkg/FR-2026-04-23/pdf/2026-08011.pdf'),
 pol('s232_grid_tier','2026-06-08','Jun 2026','Section 232 temporary grid-equipment tier','Tariff','In force, scope disputed','15%','Large transformers: HTS 8504.23.00 (liquid, above 10 MVA) and 8504.34.00 under the narrow reading','Distribution transformers and switchgear likely stay at 25%.','Dec 31, 2027','W','https://distroforge.com/blog/section-232-tariff-grid-equipment-procurement-impact/'),
 pol('usmca','2026-07-01','Jul 1, 2026','USMCA joint review','Trade deal','Not renewed',None,'Mexico- and Canada-built supply','Agreement stays in force but now faces a review every year.',None,'S','https://www.whitecase.com/insight-alert/usmca-2026-joint-review-united-states-declines-extend-agreement-triggering-annual'),
 pol('doe_eff','2026-07-15','Jul 15, 2026','DOE distribution-transformer efficiency review','Standard','Under review',None,'The 2024 rule, compliance due 2029','Could change the mix of amorphous and GOES cores or push back compliance.',None,'S','https://www.energy.gov/cmei/articles/doe-issues-request-information-rfi-energy-conservation-standards-distribution'),
 pol('sec301','2026-07-24','Jul 24, 2026','Section 301 forced-labor tariffs','Tariff','In force','10–12.5%','60 economies; Mexico 10% (non-USMCA goods), Korea topped up to 12.5% with MFN','Replaced Section 122 with no time limit and stacks on other duties.',None,'S','https://www.honigman.com/alert-3462'),
 pol('eo14420','2026-08-26','Aug 26, 2026','EO 14420 on foreign bulk-power equipment','Ban','In force, rules pending',None,'Power and instrument transformers, inverters, batteries and breakers from 24 countries, mainly China','Applies to deals after Aug 26. Some law firms cite it as EO 14421.',None,'S','https://www.crowell.com/en/insights/client-alerts/power-play-new-executive-order-targets-electrical-grid-equipment'),
 pol('doe_rfi','2026-10-09','Oct 9, 2026','DOE comment period on EO 14420 closes','Ban','Closed',None,'Docket DOE-HQ-2026-1123','First step toward the implementing rules.',None,'S','https://www.hklaw.com/en/insights/publications/2026/09/doe-seeks-public-comment-on-bulk-power-system-executive-order'),
 pol('doe_rules','2026-12-24','~Dec 24, 2026','DOE implementing rules due','Ban','Pending',None,'Covered equipment and buyers','Will settle whether data-center substations count, and may set pre-qualified vendor lists.',None,'S','https://www.mcguirewoods.com/client-resources/alerts/2026/9/doe-issues-request-for-information-on-securing-u-s-bulk-power-system-under-executive-order-14421/'),
 pol('tier_expiry','2027-12-31','Dec 31, 2027','Temporary grid-equipment tier ends','Tariff','Scheduled','15% → 25%','Large transformer HTS lines','Import duty on large units rises unless extended.',None,'S','https://www.ghy.com/trade-compliance/us-adjusts-section-232-tariffs-on-aluminum-steel-and-copper-full-customs-value-now-applies/'),
]
w('policy.json', policy)

def m(company, owner, ownership, segments, plants, move, conf):
    return dict(company=company, owner=owner, ownership=ownership, segments=segments, na_plants=plants, latest_move=move, confidence=conf)
mfr = [
 m('Hitachi Energy','Hitachi (TSE: 6501)','Public','Power, large power, bushings','South Boston VA; Crystal Springs MS; Varennes QC; Alamo TN','$528M Gallman MS plant (Sep 15, 2026); buying Canduct','P'),
 m('Prolec GE','GE Vernova (NYSE: GEV)','Public','Power, distribution','Seven sites incl. Goldsboro NC, Shreveport LA, Waukesha WI, Monterrey MX','Now fully owned by GE Vernova; Goldsboro doubling','P'),
 m('Siemens Energy','Siemens Energy (ETR: ENR)','Public','Large power','Charlotte NC (under construction)','Charlotte start slipped to 2027','S'),
 m('HD Hyundai Electric','HD Hyundai (KRX: 267260)','Public','765 kV / EHV','Montgomery AL','$200M second plant, due Apr 2027','S'),
 m('Hyosung HICO','Hyosung Heavy Industries (KRX)','Public','765 kV / EHV','Memphis TN','$287M of US data-center orders (Sep 2026)','S'),
 m('Mitsubishi Electric Power Products','Mitsubishi Electric','Public','Shell-type EHV','Memphis TN','Operating; first US-built 765 kV unit in 25 years','S'),
 m('Virginia Transformer','Private (Roanoke VA)','Private','Power 2–500 MVA, distribution','Six NA plants incl. Rincon GA; Muscle Shoals AL coming','Muscle Shoals greenfield (May 2026); sale talk above $6B','S'),
 m('Pennsylvania Transformer Technology','Quanta Services (NYSE: PWR)','Public','Power 5–750 MVA, up to 765 kV','Canonsburg PA; Raeford NC','$102.5M Raeford expansion','S'),
 m('Niagara Power Transformer','Quanta Services (NYSE: PWR)','Public','Power','Cheektowaga NY','$71M expansion, 90 → 140 units a year (Sep 2026)','S'),
 m('Delta Star','MacLean Power Systems (Blackstone, Centerbridge), pending','PE','Power, mobile substations','Lynchburg VA; San Carlos CA; Saint-Jean-sur-Richelieu QC','Sale to MacLean signed Sep 2026','S'),
 m('Howard Industries','Private (Laurel MS)','Private','Distribution, medium power','Laurel and Ellisville MS','$100M medium-power expansion (Apr 2026)','P'),
 m('WEG','WEG (B3: WEGE3)','Public','Power up to 550 kV, distribution','Washington MO; Atotonilco de Tula MX','$165M NA generator expansion (Sep 2026)','S'),
 m('Eaton','Eaton (NYSE: ETN)','Public','Three-phase, distribution, solid-state','Waukesha WI; Nacogdoches TX; Jonesville SC (2027)','$340M Jonesville plant','P'),
 m('ERMCO','Arkansas Electric Cooperatives','Co-op','Distribution, dry-type','Tennessee, Arkansas, plus Spire plants in GA, TN, TX, MX','Arizona three-phase plant for 2027','S'),
 m('Central Moloney','Private (Pine Bluff AR)','Private','Distribution','Pine Bluff AR; Panama City Beach FL','Second plant, up to 250 jobs','S'),
 m('Forgent Power Solutions','NYSE: FPS (Neos Partners controls)','Public','Data-center distribution, switchboards','MGM (Vernon CA); VanTran (Waco TX)','IPO Feb 2026 at $27; follow-on at $47','S'),
 m('JST Power Equipment','Private','Private','Pad-mount','Wytheville VA','Opened May 2026; 1,000 units a year from 2027','S'),
 m('Giga Energy','Private (venture-backed)','Private','Medium-voltage pad-mount','Houston TX; Long Beach CA','Houston plant planned to start Q1 2026','P'),
 m('Hammond Power Solutions','TSX: HPS.A','Public','Dry-type','Canada, US, Mexico','Bought AEG Power Solutions (Jul 2026)','P'),
 m('Cleveland-Cliffs','NYSE: CLF','Public','GOES steel; planned distribution plant','Butler PA; Weirton WV (planned)','Up to 25% more GOES at Butler (Oct 2026)','P'),
 m('Sunbelt Solomon','TJC, pending (from Trilantic)','PE','New and remanufactured distribution','Sharon PA; Elba AL','TJC deal signed Jul 2026','S'),
 m('Integrated Power Services','Private equity-backed','PE','Aftermarket, refurbished high voltage','Greenville SC; Easton PA (Belyea)','Bought Belyea’s high-voltage business (Oct 7, 2026)','S'),
 m('Heron Power','Venture (a16z, Breakthrough Energy)','Private','Solid-state','California (planned)','$140M Series B (Feb 2026)','S'),
 m('DG Matrix','Venture (Engine; ABB and MHI)','Private','Solid-state','Raleigh NC','$60M Series A','S'),
 m('Marsons + Cleanhill','Marsons (India) and Cleanhill Partners (NY)','JV','11–345 kV, GSUs up to 200 MVA (imported)','US company (planned)','Joint venture approved Oct 6, 2026','S'),
 m('LS Electric','LS Electric (KRX)','Public','Ultra-high voltage (built in Korea)','Switchboard plants in Bastrop TX and Cedar City UT','$123M UHV order for western US projects','S'),
]
w('manufacturers.json', mfr)

def t(id, order, kind, stance, heading, body):
    return dict(id=id, order=order, kind=kind, stance=stance, heading=heading, body=body)
take = [
 t('headline',0,'headline','Neutral','Headline','Demand and policy still favor US transformer makers. But most new incumbent capacity lands in 2027–29, so segment, timing and steel supply now decide who wins.'),
 t('imp_policy',1,'implication','Tailwind','Policy is pushing China out, and India is stepping in','EO 14420 targets the Chinese units data centers used to get around lead times. If DOE’s December rules cover data-center substations, that demand moves to domestic and allied makers. The Marsons–Cleanhill venture shows Indian suppliers moving in. Plan prices against Indian, Korean and Mexican competition.'),
 t('imp_aftermarket',2,'implication','Opportunity','The aftermarket is the quickest way in','IPS–Belyea, TJC–Sunbelt Solomon and MacLean–Delta Star all bought refurbishment, rental, mobile substations or lifecycle services within three months. These businesses deliver in months instead of years, need far less capital, and skip most of the utility approval cycle. A repair and rewind shop builds the same skills and customers.'),
 t('imp_steel',3,'implication','Risk','Core steel is the gating input','Cleveland-Cliffs adding up to 25% is welcome, but it is still the only US GOES maker, its widths are too narrow for many large cores, and imported cores pay Section 232 duties. Copper is near a record. Lock in core supply before you lock in a site.'),
 t('imp_timing',4,'implication','Risk','Timing is the biggest risk','Eaton, ERMCO, HD Hyundai, Siemens Energy and Prolec GE land in 2027, Virginia Transformer and Hitachi South Boston in 2028, Hitachi Mississippi in 2029. The power-transformer gap fell from 30% to 15% in a year, and price growth has cooled to single digits. A plant announced in 2027 ships into that wave.'),
 t('imp_gaps',5,'implication','Opportunity','Gaps most likely to last','Three-phase pad-mount units for data centers and industry, where Wood Mackenzie expects the shortage to worsen. Generator step-up units, with the longest lead times and a gas-turbine boom behind them. Refurbishment, rental and test-bay capacity. Skip 765 kV: it needs too much capital and expertise for a newcomer.'),
 t('imp_exits',6,'implication','Tailwind','Exit prices are high','Prolec GE was valued near $10.5B, Virginia Transformer reportedly tested a sale above $6B, and Forgent rose from a $27 IPO to a $47 follow-on. A build-to-sell plan over four to six years works if you win qualified utility or data-center customers before 2028. Buying a small maker is faster but expensive.'),
 t('bottom_line',7,'bottom_line','Neutral','Bottom line','The bull case holds for 2026–28, helped by policy and a utility capex base of $239B in 2026. It now depends on picking the right segment (pad-mount, medium voltage, GSU, aftermarket), arriving before 2028, and securing core steel.'),
 t('cav_sources',8,'caveat','Neutral','How the numbers were gathered','Figures come from web search summaries of the linked pages; the research environment could not open pages directly. Several lead-time and price figures come from vendor blogs, tagged W. Check primary sources before committing capital.'),
 t('cav_conflicts',9,'caveat','Neutral','Where sources disagree','Law firms cite the August order as EO 14420 or EO 14421. Sources also disagree on which transformers get the temporary 15% Section 232 rate; both readings are shown.'),
 t('cav_gaps',10,'caveat','Neutral','What is missing','No clean 2026 import series for HS 8504 yet, and several plant start dates are undisclosed.'),
]
w('takeaways.json', take)

def ev(id, window, date, date_label, title, detail, category, sig, impl, src_label, url):
    return dict(id=id, window=window, date=date, date_label=date_label, title=title, detail=detail, category=category, significance=sig, implication=impl, source_label=src_label, source_url=url)
TW='This week'; L6='Last six weeks'
events = [
 ev('ips_belyea',TW,'2026-10-07','Oct 7','IPS buys Belyea’s high-voltage business','Refurbished 69–230 kV transformers, breakers and switchgear, plus portable-substation rental, based in Easton PA. Terms undisclosed.','Deals','High','Third aftermarket or rental deal in three months. Investors pay for anything that can deliver in under two years.','pulse2','https://pulse2.com/integrated-power-services-acquires-belyea-company/'),
 ev('doe_rfi_close',TW,'2026-10-09','Oct 9','DOE comments on the grid-equipment order close','Docket DOE-HQ-2026-1123 under EO 14420. Implementing rules are due around Dec 24.','Policy','High','The rules decide whether data-center substations count, which sets who can sell large units.','Holland & Knight','https://www.hklaw.com/en/insights/publications/2026/09/doe-seeks-public-comment-on-bulk-power-system-executive-order'),
 ev('marsons_cleanhill',TW,'2026-10-06','Oct 6','Marsons and Cleanhill form a US–Canada venture','Indian maker of 11–345 kV units and GSUs up to 200 MVA teams with a New York private-equity firm. Imports first, local manufacturing later. Marsons stock rose up to 16%.','New entrants','Medium','First visible Indian move after the order on Chinese equipment.','T&D India','https://www.tndindia.com/marsons-teams-up-with-cleanhill-partners-plans-jv-to-manufacture-transformers-for-north-american-market/'),
 ev('cliffs_goes',TW,'2026-10-06','Oct 6','Cleveland-Cliffs shows its GOES expansion','$200M plus a $75M DOE award adds up to 25% more grain-oriented electrical steel at Butler Works. Energy Secretary Wright visited.','Inputs','Medium','Real but small relief on the scarcest input. No completion date given.','Business Wire','https://www.businesswire.com/news/home/20261004168131/en/Cleveland-Cliffs-to-Host-U.S.-Secretary-of-Energy-Chris-Wright-and-Other-Government-Officials-at-Butler-Works-to-Showcase-GOES-Expansion-Project'),
 ev('schneider_ptc',TW,'2026-10-05','Oct 5','Schneider Electric agrees to buy PTC for $22.6B','All-cash software deal, not transformers.','Deals','Low','Shows how much cash electrical-equipment majors can deploy.','Axios','https://www.axios.com/2026/10/05/schneider-electric-ptc'),
 ev('copper',TW,'2026-10-09','Oct 9','Copper holds near its record','About $6.66/lb on COMEX, close to the $6.89 high of Sep 9.','Inputs','Low','Winding costs stay high.','MetalCharts','https://metalcharts.org/copper-price'),
 ev('voltamp',TW,'2026-10-07','Oct 7','Voltamp starts its new plant in India','Commercial production began at the Vadodara power-transformer plant.','New entrants','Low','More Indian capacity that could ship to North America.','TradeBrains','https://tradebrains.in/indian-markets/voltamp-transformers-in-focus-after-commencing-commercial-production-at-new-200-cr-vadodara-plant-12637961'),
 ev('weg_gen',L6,'2026-09-28','Sep 28','WEG adds $165M of generator capacity in North America','Generators, not transformers; Mexico first phase in Q2 2027.','Capacity','Low','',"Economic News Brasil",'https://economicnewsbrasil.com.br/2026/09/28/producao-geradores-weg-2030/'),
 ev('hitachi_gallman',L6,'2026-09-15','Sep 15','Hitachi Energy plans a $528M Mississippi plant','10–160 MVA units up to 230 kV, production in 2029, more than 700 jobs.','Capacity','High','',"Hitachi Energy",'https://www.hitachienergy.com/news-and-events/press-releases/2026/09/hitachi-deepens-commitment-to-u-s-manufacturing-with-528-million-mississippi-transformer-factory'),
 ev('hyosung_orders',L6,'2026-09-15','Sep 15','Hyosung wins $287M of US orders','765 kV and 345 kV units for two US tech companies’ data centers.','Demand','Medium','',"Evertiq",'https://evertiq.com/news/2026-09-18-hyosung-secures-287-million-us-orders-for-uhv-transformers'),
 ev('doe_rfi_pub',L6,'2026-09-09','Sep 9','DOE asks for comments on the grid-equipment order','Request for information published in the Federal Register.','Policy','Medium','',"Federal Register",'https://www.federalregister.gov/documents/2026/09/09/2026-18370/securing-the-united-states-bulk-power-system'),
 ev('maclean_delta',L6,'2026-09-03','Sep 3','MacLean Power Systems to buy Delta Star','Blackstone- and Centerbridge-backed platform adds power transformers and mobile substations. Closing Q4 2026.','Deals','High','',"Virginia Business",'https://virginiabusiness.com/maclean-power-systems-acquire-delta-star/'),
 ev('niagara',L6,'2026-09-02','Sep 2','Niagara Power Transformer expands','$71M to go from 90 to 140 units a year (owned by Quanta).','Capacity','Medium','',"IEN",'https://www.ien.com/operations/news/22973547/centuryold-transformer-maker-plans-71m-expansion-in-new-york'),
 ev('eo14420',L6,'2026-08-26','Aug 26','Executive order on foreign grid equipment','National emergency covering transformers, inverters, batteries and breakers from 24 countries, mainly China.','Policy','High','',"Crowell",'https://www.crowell.com/en/insights/client-alerts/power-play-new-executive-order-targets-electrical-grid-equipment'),
]
w('events.json', events)

def wl(id, sort_date, when, item, why):
    return dict(id=id, sort_date=sort_date, when=when, item=item, why=why)
watch = [
 wl('ppi','2026-10-15','Oct 15','BLS producer prices for September','Shows whether transformer price growth keeps cooling.'),
 wl('asia_q3','2026-10-25','Late Oct','Q3 results: Hitachi, HD Hyundai, Hyosung, LS Electric','US order intake and backlog.'),
 wl('gev_q3','2026-10-28','Oct 28','GE Vernova Q3 (some calendars say Oct 22)','Electrification orders and how fast Prolec is ramping.'),
 wl('us_q3','2026-11-05','Late Oct – Nov','Eaton, Quanta, Hubbell, Hammond Q3; Siemens Energy full year','Book-to-bill and comments on pricing.'),
 wl('closings','2026-12-15','Q4 2026','Delta Star, Sunbelt Solomon and Hitachi–Canduct closings','Confirms the deals and may reveal prices.'),
 wl('doe_rules','2026-12-24','~Dec 24','DOE rules under EO 14420','Whether data-center substations count; any pre-qualified vendor list.'),
 wl('open','2027-01-15','Open','DOE efficiency decision; Marsons–Cleanhill final agreement; Virginia Transformer sale; ERCOT 765 kV approvals; USMCA review','Each could move demand, competition or exit values.'),
 wl('tier','2027-12-31','Dec 31, 2027','Temporary 15% Section 232 tier expires','Duty on imported large units rises unless extended.'),
]
w('watchlist.json', watch)
