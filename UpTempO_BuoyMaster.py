#!/usr/bin/python
import os
import sys
import time


def getBuoys():

    opf=open('UPTEMPO/UpTempO_Catalog.txt','r')
    data=opf.read()
    opf.close()
    data=data.split('\n')  #[0:-1]
    data=[d for d in data if d]

    reporting={}
    dead={}
    newdead={}
    buoyorder=[]
    for d in data:
        sd=d.split(',')
        buoyorder.append(sd[0])
        if len(sd) == 5:  # still reporting
            if sd[4].split(':')[1] == 'NEWDEAD': newdead[sd[0]]=sd[1:]
            else: reporting[sd[0]]=sd[1:]
        else:
            dead[sd[0]]=sd[1:]

    return reporting,dead,buoyorder,newdead

#==========================================

def BMvarDefs():

    vardefs={'pdepths':'Ocean Pressure Sensor Depths',
             'tdepths':'Temperature Sensor Depths',
             'sdepths':'Salinity Sensor Depths',
             'P1_ind':'Index of first Ocean Pressure value',
             'T1_ind':'Index of first Temperature value',
             'ED1_ind':'Index of first Estimated Depth Value (Marlin-Yug)',
             'bp_ind':'Index of Barometric Pressure',
             'vbatt_ind':'Index of battery voltage',
             'ta_ind':'Index of Atmospheric Temperature',
             'sub_ind':'Index of submergence',
             'cpdepths':'CTD Sensor Depths',
             'ctdepths':'CTD Temperature Depths',
             'csdepths':'CTD Salinity Depths',
             'CTDP1_ind':'Index of first CTD Pressure',
             'CTDT1_ind':'Index of first CTD Temperature',
             'CTDS1_ind':'Index of first CTD Salinity'}

def BuoyMaster(bid):


    bids={
          '123451234512345':{'notes':'UpTempO 2022 #0', # Mike\ Steele\ ONR\ SVPS_0001.pdf
                             'name':['2022','0'],       #  also, ONR_SVPS_DataFields_2022.pdf
                             'imeiabbv':'123451',       #  SVPS surface velocity program, TC cell and no ? droque
                             'wmo':'987654',
                             'deploymentDate':'',
                             'deploymentLon':'',
                             'deploymentLat':'',
                             'vessel':'SASSIE',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-SVPS-0001',
                             'tdepths':[0.0,2.5,5.0,7.5,10,15,20],     # SST 0.14, hull 0.44
                             'pdepths':[10,20,30],          # hull
                             'CTDtdepths':[10,20,30],
                             'CTDsdepths':[10,20],
                             'CTDpdepths':[10,20,30],
                             'HULLtdepths':[0.44],
                             'HULLsdepths':[0.44],
                             'vbatt_ind':1,
                             'sub_ind':1},

          '300534062892700':{'notes':'UpTempO 2022 #1', # Mike\ Steele\ ONR\ SVPS_0001.pdf
                             'name':['2022','1'],       #  also, ONR_SVPS_DataFields_2022.pdf
                             'imeiabbv':'892700',       #  SVPS surface velocity program, TC cell and no ? droque
                             'wmo':'4802632',
                             'deploymentDate':'',
                             'deploymentLon':'',
                             'deploymentLat':'',
                             'vessel':'SASSIE',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-SVPS-0001',
                             'tdepths':[0.14],
                             'HULLtdepths':[0.44],     # SST 0.14, hull 0.44
                             'HULLsdepths':[0.38],          # hull
                             'vbatt_ind':1,
                             'sub_ind':1},

          '300534062894700':{'notes':'UpTempO 2022 #2', # Mike\ Steele\ ONR\ SVP\ Salinity\ Ball\ 0003.pdf
                             'name':['2022','2'],       #  also, ONR_SVPS_DataFields_2022.pdf
                             'imeiabbv':'894700',
                             'wmo':'4802633',
                             'deploymentDate':'',
                             'deploymentLon':'',
                             'deploymentLat':'',
                             'vessel':'SASSIE',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-IB-SVPS-0003',
                             'tdepths':[0.14],
                             'HULLtdepths':[0.44],     # SST 0.14, hull 0.44
                             'HULLsdepths':[0.38],          # hull
                             'vbatt_ind':1,
                             'sub_ind':1},

          '300534062897730':{'notes':'UpTempO 2022 #3', # Mike\ Steele\ ONR\ SVP\ Salinity\ Ball\ 0004.pdf
                             'name':['2022','3'],       #  also, ONR_SVPS_DataFields_2022.pdf
                             'imeiabbv':'897730',
                             'wmo':'4802634',
                             'deploymentDate':'',
                             'deploymentLon':'',
                             'deploymentLat':'',
                             'vessel':'SASSIE',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-IB-SVPS-0004',
                             'tdepths':[0.14],
                             'HULLtdepths':[0.44],     # SST 0.14, hull 0.44
                             'HULLsdepths':[0.38],          # hull
                             'vbatt_ind':1,
                             'sub_ind':1},

          '300534062893700':{'notes':'UpTempO 2022 #4', # Mike\ Steele\ NASA\ SVP-S2_0001.pdf
                         'name':['2022','4'],           #  also Nasa_SVPS_XIM_DataFields_2022.pdf
                         'imeiabbv':'893700',
                         'wmo':'4802635',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-SVPS-XIM-0001',
                         'tdepths':[0.14],              # SST 0.14m
                         'CTDtdepths':[5],                 # 37IM 5m
                         'CTDsdepths':[5],                 # 37IM
                         'CTDpdepths':[5],                 # 37IM
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534062894730':{'notes':'UpTempO 2022 #5', # Mike\ Steele\ NASA\ SVP-S2_0002.pdf
                         'name':['2022','5'],           #  also Nasa_SVPS_XIM_DataFields_2022.pdf
                         'imeiabbv':'894730',
                         'wmo':'4802636',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-SVPS-XIM-0002',
                         'tdepths':[0.14],              # SST 0.14m
                         'CTDtdepths':[5],                 # 37IM 5m
                         'CTDsdepths':[5],                 # 37IM
                         'CTDpdepths':[5],                 # 37IM
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534062894740':{'notes':'UpTempO 2022 #6', # Mike\ Steele\ NASA\ SVP-S2_0003.pdf
                         'name':['2022','6'],           #  also Nasa_SVPS_XIM_DataFields_2022.pdf
                         'imeiabbv':'894740',
                         'wmo':'4802637',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-SVPS-XIM-0003',
                         'tdepths':[0.14],              # SST 0.14m
                         'CTDtdepths':[5],                 # 37IM 5m
                         'CTDsdepths':[5],                 # 37IM
                         'CTDpdepths':[5],                 # 37IM
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534062898720':{'notes':'UpTempO 2022 #7', # Mike\ Steele\ ONR\ SVP-S2.pdf
                         'name':['2022','7'],           #  also ONR_SVPS2_37IM_DataFields_2022.pdf
                         'imeiabbv':'898720',
                         'wmo':'4802638',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-SVPS2-37IM-0001',
                         'tdepths':[0.14],          # SST 0.14
                         'HULLtdepths':[0.44],      # hull 0.44
                         'CTDtdepths':[5],          # 37IM 5m
                         'HULLsdepths':[0.38],      # hull 0.38
                         'CTDsdepths':[5],          # 37IM
                         'CTDpdepths':[5],          # 37IM
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534063807110':{'notes':'UpTempO 2022 #8', # Mike\ Steele\ ONR\ SVP-S2_0002.pdf
                         'name':['2022','8'],           #  also ONR_SVPS2_37IM_DataFields_2022.pdf
                         'imeiabbv':'807110',
                         'wmo':'4802639',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-SVPS2-37IM-0002', # UW-SVPS2-0002 ?
                         'tdepths':[0.14],          # SST 0.14
                         'HULLtdepths':[0.44],      # hull 0.44
                         'CTDtdepths':[5],          # 37IM 5m
                         'HULLsdepths':[0.38],      # hull 0.38
                         'CTDsdepths':[5],          # 37IM
                         'CTDpdepths':[5],          # 37IM
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534063704980':{'notes':'UpTempO 2022 #9', # Uptempo_NASA_Sound9_0002.pdf
                         'name':['2022','9'],           #  also, Nasa_T-Chain_DataFields_2022.pdf
                         'imeiabbv':'704980',
                         'wmo':'4802640',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SASSIE',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-TC-S9-XT-XIM-0001',
                         'tdepths':[0.25,2.5,5.0,7.5,15,25,35,50],
                         'CTDtdepths':[10,20,30,40,60],
                         'CTDsdepths':[10,20,30,40,60],
                         'CTDpdepths':[10,20,30,40,60],
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534063803100':{'notes':'UpTempO 2022 #10', # Uptempo_NASA_Sound9_0002.pdf
                         'name':['2022','10'],           #  also, Nasa_T-Chain_DataFields_2022.pdf
                         'imeiabbv':'803100',
                         'wmo':'4802666',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SIZRS',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-TC-S9-XT-XIM-0002',
                         'tdepths':[0.25,2.5,5.0,7.5,15,25,35,50],
                         'CTDtdepths':[10,20,30,40,60],
                         'CTDsdepths':[10,20,30,40,60],
                         'CTDpdepths':[10,20,30,40,60],
                         'vbatt_ind':1,
                         'sub_ind':1},

          '300534062896730':{'notes':'UpTempO 2022 #11', # Uptempo_ONR_Sound9_Seabird.pdf
                         'name':['2022','11'],           #  also, ONR_T-Chain_DataFields_2022.pdf
                         'imeiabbv':'896730',
                         'wmo':'4802667',
                         'deploymentDate':'',
                         'deploymentLon':'',
                         'deploymentLat':'',
                         'vessel':'SIZRS',
                         'brand':'Pacific Gyre',
                         'pgname':'UW-TCS-37IM-S9XT-0001',
                         'tdepths':[0.25,2.5,5.0,7.5,15,25,35,50],
                         'HULLtdepths':[0.57],
                         'CTDtdepths':[10,20,30,40,60],
                         'HULLsdepths':[0.51],
                         'CTDsdepths':[10,20,30,40,60],
                         'CTDpdepths':[20,40,60],
                         'vbatt_ind':1,
                         'sub_ind':1},




           '300534062158460':{'notes':'UpTempO 2021 #5',
                             'name':['2021','5'],
                             'imeiabbv':'158460',
                             'wmo':'',
                             'deploymentDate':'11/02/2021',
                             'deploymentLon':-167.035249,
                             'deploymentLat':69.148342,
                             'vessel':'SIZRS',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-IB-SVPS-0001',
                             'tdepths':[0,0.28],  # changed from 0.22 2/2/2022
                             'sdepths':[0.28],
                             'vbatt_ind':1,
                             'sub_ind':1},

         '300534062158480':{'notes':'UpTempO 2021 #4',
                             'name':['2021','4'],
                             'imeiabbv':'158480',
                             'wmo':'',
                             'deploymentDate':'10/13/2021',
                             'deploymentLon':-156.980291,
                             'deploymentLat':72.966354,
                             'vessel':'SIZRS',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-IB-SVPS-0002',
                             'tdepths':[0,0.28],  # changed from 0.22 2/2/2022
                             'sdepths':[0.28],
                             'vbatt_ind':1,
                             'sub_ind':1},

        '300534060051570':{'notes':'UpTempO 2021 #3',
                             'name':['2021','3'],
                             'imeiabbv':'051570',
                             'wmo':'',
                             'deploymentDate':'9/29/2021',
                             'deploymentLon':-152.502925,
                             'deploymentLat':57.736547,
                             'vessel':'SIZRS',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-TC-1W-0015',
                             'pdepths':[25],
                             'tdepths':[0.0,2.5, 5, 7.5, 10, 15, 20, 25],
                             'bp_ind':1,
                             'sub_ind':1,
                             'vbatt_ind':1},

          '300534060251600':{'notes':'UpTempO 2021 #2',
                             'name':['2021','2'],
                             'imeiabbv':'251600',
                             'wmo':'',
                             'deploymentDate':'9/15/2021',
                             'deploymentLon':-150.008014,
                             'deploymentLat':72.036603,
                             'vessel':'SIZRS',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-TC-1W-0016',
                             'pdepths':[20.,40.,60.],
                             'tdepths':[2.5, 5., 7.5, 10., 15., 20., 25., 30., 35., 40., 50., 60.],
                             'bp_ind':1,
                             'sub_ind':1,
                             'vbatt_ind':1},

          '300534060649670':{'notes':'UpTempO 2021 #1',
                             'name':['2021','1'],
                             'imeiabbv':'649670',
                             'deploymentDate':'8/25/2021',
                             'deploymentLon':-150.035994,
                             'deploymentLat':72.052522,
                             'vessel':'SIZRS',
                             'brand':'Pacific Gyre',
                             'pgname':'UW-TC-S9C-0001',
                             'pdepths':[5.,10.,20.,25.],  # Called DepthPodx, changed from ddepths 2/1/2022
                             'CTDsdepths':[5.,10.,20.],   # sal readings at 5, 10, 20m
                             'tdepths':[0.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0],
                             'vbatt_ind':1,
                             'bp_ind':1,
                             'sub_ind':1},



        '300234061160500':{'notes':'UpTempO 2020 #1',
                             'name':['2020','1'],
                             'imeiabbv':'160500',
                             'vessel':'MIRAI',
                             'brand':'Marlin-Yug',
                             'pdepths':[20.,40.,60.],
                             'tdepths':[0.,1.,4.,6.5,9.,12.,14.5,17.,20.,25.,30.,35.,40.,45.,50.,55.,60.],
                             'P1_ind':6,
                             'ED1_ind':9,
                             'T1_ind':26,
                             'bp_ind':43,
                             'vbatt_ind':7,
                             'ta_ind':45,
                             'sub_ind':46},

          '300234067939910':{'notes':'UpTempO 2020 JW-1',
                             'name':['2020','JW-2'],
                             'imeiabbv':'9910',
                             'vessel':'WARM',
                             'brand':'Pacific Gyre',
                             'tdepths':[3.,12.],
                             'cpdepths':[10.],
                             'ctdepths':[10.],
                             'T1_ind':6,
                             'CTDT1_ind':11,
                             'CTDS1_ind':10,
                             'CTDP1_ind':9,
                             'vbatt_ind':8},

          '300234060320940':{'notes':'UpTempO 2019 #5',
                             'name':['2019','5'],
                             'brand':'Marlin-Yug',
                             'imeiabbv':'320940',
                             'vessel':'MOSAiC',
                             'pdepths':[20.,40.,60.],
                             'tdepths':[0.,2.5, 5., 7.5, 10., 15., 20., 25., 30., 35., 40., 50., 60.],
                             'P1_ind':6,
                             'ED1_ind':9,
                             'T1_ind':23,
                             'bp_ind':36,
                             'vbatt_ind':37,
                             'sub_ind':38},

          #----- Added in 2019 -------
        '300234060320930':{'inote':'NOT YET DEPLOYED (ETD = mid aug) --> NABOS cruise cancelled',
                           'notes':'UpTempO 2019 #4',
                           'name':['2019','4'],
                           'brand':'Marlin-Yug',
                           'imeiabbv':'320930',
                           'vessel':'MOSAiC',
                           'pdepths':[25],
                           'tdepths':[0.,2.5,5.0,7.5,10.,15.,20.,25.],
                           'ED1_ind':6,
                           'P1_ind':14,
                           'T1_ind':16,
                           'bp_ind':24,
                           'vbatt_ind':25,
                           'sub_ind':26},


	'300234068719480':{'inote':'Deployed 9/12/2019 via SIZRS by Mike',
                           'notes':'UpTempO 2019 #3',
                           'name':['2019','3'],
                           'brand':'Pacific Gyre',
                           'imeiabbv':'9480',
                           'vessel':'SIZRS',
                           'pdepths':[25.],
                           'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.],
                           'reportTilt':1,
                           'tiltdepths':[2.5,5.0,7.5,10.,15.,20.,25.],
                           'T1_ind':7,
                           'P1_ind':6,
                           'bp_ind':15,
                           'vbatt_ind':16,
                           'sub_ind':17,
                           'tilt1_ind':24},


	'300234068519450':{'inote':'DEPLOYED 8/13/2019 via SIZRS by Jamie Morison',
				'notes':'UpTempO 2019 #2',
				'name':['2019','2'],
				'brand':'Pacific Gyre',
				'imeiabbv':'9450',
                'wmo':'4801670',
                'deploymentDate':'8/14/2019',
                'deploymentLon':-149.817103,
                'deploymentLat':72.013322,
				'vessel':'SIZRS',
                'pgname':'UW-TC-1W-0014',
				'pdepths':[20.,40.,60.],
				'tdepths':[0.0,2.5,5.,7.5,10.,15.,20.,25.,30.,35.,40.,50.,60.],
				'T1_ind':9,
				'P1_ind':6,
				'bp_ind':22,
				'vbatt_ind':23,
				'sub_ind':24},

	'300234068514830':{'inote':'DEPLOYED via airdrop by Jamie Morison 7/10/2019',
				'notes':'UpTempO 2019 #1',
				'name':['2019','1'],
				'brand':'Pacific Gyre',
				'imeiabbv':'4830',
				'vessel':'SIZRS',
				'pdepths':[20.0],
				'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.],
				'T1_ind':9,
				'P1_ind':6,
				'bp_ind':22,
				'vbatt_ind':23,
				'sub_ind':24},

	'300234067936870':{'notes':'WARM 2019 W9',
                           'name':['2019','W-9'],
                           'brand':'Pacific Gyre',
                           'imeiabbv':'6870',
                           'vessel':'WARM',
                           'pdepths':10.,
                           'tdepths':[0.0,4.3,10.],
                           'T1_ind':7,
                           'P1_ind':6,
                           'vbatt_ind':10,
                           #****BIOSENSOR INFO****
                           'biosensors':['LI_192_0','LI_192_1','LI_192_2','LI_192_3','LI_192_4','LI_192_5','Cyclops_CHL'],
                           'biodepths':[0.0, 0.5, 1.0, 4.1, 6.4, 8.0, 4.7],
                           #----for "plot_warm" in webplots---
                           'lidepths':[0.0, 0.5, 1.0, 4.1, 6.4, 8.0]},

    '300234064735100':{'notes':'used to be UpTempO 2017 #6... was returned',
                           'name':['2018','2'],
			               'brand':'Pacific Gyre',
                           'imeiabbv':'5100',
                           'vessel':'SIZRS',
                           'pdepths':[20.,40.,60.],
                           'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.,30.,35.,40.,50.,60.],
                           'T1_ind':9,
                           'P1_ind':6,
                           'bp_ind':22,
                           'vbatt_ind':23,
                           'sub_ind':24},

    '300234063993850':{'notes':'Amundsen 2016 06',
                           'name':['2016','6'],
			               'brand':'Pacific Gyre',
                           'imeiabbv':'3850',
                           'wmo':'4801613',             # get this from L1 or L2.dat
                           'pgname':'UW-TC-37IM-0015',  # get this from api.pacificgyre.com
                           'vessel':'Amundsen',
                           'deploymentDate':'9/1/2016',
                           'deploymentLon':-139.02, # get this from L1 or L2.dat
                           'deploymentLat':70.44, # get this from L1 or L2.dat
                           'pdepths':[25.],
                           'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.],
                           'P1_ind':6,
                           'T1_ind':9,
                           'bp_ind':22,
                           'vbatt_ind':23,
                           'sub_ind':24},

    '300234063994900':{'notes':'Araon 2016 03',
                           'name':['2016','3'],
			               'brand':'Pacific Gyre',
                           'imeiabbv':'4900',
                           'wmo':'4801613',
                           'pgname':'UW-TC-1W-0005',
                           'vessel':'Araon',
                           'deploymentDate':'8/20/2016',
                           'deploymentLon':-161.00,
                           'deploymentLat':76.00,
                           'pdepths':[25.],
                           'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.],
                           'P1_ind':6,
                           'T1_ind':9,
                           'bp_ind':22,
                           'vbatt_ind':23,
                           'sub_ind':24},

##     '300234064735100':{'notes':'JWARM 2018 #1',
#                            'name':['2018','JW-1'],
# 			               'brand':'Pacific Gyre',
#                            'imeiabbv':'2490',
#                            'vessel':'ICEX',
#                            'pdepths':[20.,40.,60.],
#                            'tdepths':[0.0,2.5,5.0,7.5,10.,15.,20.,25.,30.,35.,40.,50.,60.],
#                            'T1_ind':9,
#                            'P1_ind':6,
#                            'bp_ind':22,
#                            'vbatt_ind':23,
#                            'sub_ind':24},

          }

    binf=bids[bid]
    if 'listening' not in binf: binf['listening']='1'


    return binf
