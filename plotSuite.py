#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2/7/2022

@author: suzanne
"""
import os, glob, re, sys
import matplotlib.pyplot as plt  # ver 3.5
import matplotlib as mpl  # ver 3.5
import matplotlib.colors as colors
import numpy as np
import datetime as dt
import pandas as pd
import cartopy.crs as ccrs
import ProcessFields as pfields
from satelliteBase import BeaufortSatelliteMap
import matlab.engine
import UpTempO_BuoyMaster as BM

def plotSuite(args):

    today = dt.datetime.now()
    args.strdate = "%d%.2d%.2d" % (today.year,today.month,today.day)

    extent=[int(item.strip()) for item in args.mapDomain.split(',')]

    if os.path.exists(f'{args.base_dir}/Ship_track.xlsx'):
        os.remove(f'{args.base_dir}/Ship_track.xlsx')  # I get an error if I try to overwrite. :(
    os.system(f'/usr/local/bin/lftp sftp://sassie@ftp.polarscience.org/ --password 2Icy2Fresh! -e "cd /FTP/; get -e Ship_track.xlsx -o {args.base_dir}/Ship_track.xlsx; bye"')
    dfship = pd.read_excel(f'{args.base_dir}/Ship_track.xlsx',header=None)
    args.shipLon = dfship.iloc[-1][4]
    args.shipLat = dfship.iloc[-1][3]
    print(f'ship location: {args.shipLat:.2f}N, {-1*args.shipLon:.2f}W')

    ax0,fig0,figstr0 = BeaufortSatelliteMap(args,today,surface='SST')
    ax1,fig1,figstr1 = BeaufortSatelliteMap(args,today,surface='SSS')

    ax10,fig10, figstr10 = BeaufortSatelliteMap(args,today,surface='SST',zoom=True)
    ax11,fig11, figstr11 = BeaufortSatelliteMap(args,today,surface='SSS',zoom=True)

    cmap = plt.cm.turbo
    normsst = colors.BoundaryNorm(np.arange(-2,6,0.5),cmap.N)
    normsss = colors.BoundaryNorm(np.arange(22,31,0.25),cmap.N)

    newline = '\n'
    degree = '\u00B0'

    # filexlsx = f'{args.base_dir}/InsituData_{today.year}{today.month:02}{today.day:02}T{today.hour:02}:{today.minute:02}:{today.second:02}.xlsx'
    # print('filexlsx',filexlsx)
    # with pd.ExcelWriter(filexlsx) as writer:

    outHeaders = {'Date':'Date','Lat':'Lat','Lon':'Lon',
       'DateTimeStr':'Date',
       'CTD-S2':'Salinity',
       'S1':'Salinity',
       'Salinity-0':'Salinity',
       'Salinity':'Salinity',
       'Ts':'Temperature',
       'T1':'Temperature',
       'WaterTemp-0':'Temperature'}
    columnsWrite = ['Date','Lat','Lon']

    if bool(args.buoyIDS):
        # get buoy data
        bids = [item.strip() for item in args.buoyIDS.split(',')]
        buoyTpts=[]
        buoyTptsZ=[]
        buoySpts=[]
        buoySptsZ=[]
        for ii,bid in enumerate(bids):
            print(ii,bid)
            print()
            # if bid=='300534060649670':  # THIS PARA SHOULD BE REMOVED DURING EXPERIMENT, WHEN STRDATE = TODAY
            #     df = pfields.getPGbuoy(args,bid,'pscapluw','20210929')
            # elif bid=='300534062158480':
            #     df = pfields.getPGbuoy(args,bid,'pscapluw','20211013')
            df = pfields.getPGbuoy(args,bid,'pscapluw')
            print('length of df',len(df))
            print('line 98 in plotS',df.head())
            binf = BM.BuoyMaster(bid)
            # if len(df)==0:
            #     print(df.head())
            #     exit(-1)
            if len(df)>0:

                # try:
                (tcol,) = [col for col in df.columns if col.startswith('T') or col.startswith('CTD-T')]
                print('line 107 plotSuite',tcol)
                buoyTlabel = f"{binf['name'][0]}-{int(binf['name'][1]):02d}: {df[tcol].iloc[-1]:.1f}{degree}C, {df['Lon'].iloc[-1]:.2f}W, {df['Lat'].iloc[-1]:.2f}N"
                buoyTpts.append(ax0.scatter(df['Lon'],df['Lat'], 2*df['index'], c=df[tcol],
                            cmap=cmap, norm=normsst, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoyTlabel))
                if args.smallDomain is not None:
                    buoyTptsZ.append(ax10.scatter(df['Lon'],df['Lat'], 2*df['index'], c=df[tcol],
                                cmap=cmap, norm=normsst, transform=ccrs.PlateCarree(),  #cmap=sstcmap, norm=sstnorm,
                                edgecolor='face', label=buoyTlabel))
                columnsWrite.append(tcol)

                (scol,) = [col for col in df.columns if col.startswith('S') or col.startswith('CTD-S')]
                print('line 119 plotSuite',scol)
                buoySlabel = f"{binf['name'][0]}-{int(binf['name'][1]):02d}: {df[scol].iloc[-1]:.1f} psu, {df['Lon'].iloc[-1]:.2f}W, {df['Lat'].iloc[-1]:.2f}N"
                buoySpts.append(ax1.scatter(df['Lon'], df['Lat'], 2*df['index'], c=df[scol],
                            cmap=cmap, norm=normsss, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoySlabel))
                if args.smallDomain is not None:
                    buoySptsZ.append(ax11.scatter(df['Lon'], df['Lat'], 2*df['index'], c=df[scol],
                                cmap=cmap, norm=normsss, transform=ccrs.PlateCarree(),
                                edgecolor='face', label=buoySlabel))
                columnsWrite.append(scol)

            else:

                df['Ts'] = np.nan
                buoyTlabel = f"{binf['name'][0]}-{int(binf['name'][1]):02d}: no temperature data"
                buoyTpts.append(ax1.scatter(df['Lon'], df['Lat'], df['Ts'], c=df['Ts'],  # <- dummy vars
                            cmap=cmap, norm=normsst, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoyTlabel))
                buoyTptsZ.append(ax11.scatter(df['Lon'], df['Lat'], df['Ts'], c=df['Ts'],
                            cmap=cmap, norm=normsst, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoyTlabel))
                columnsWrite.append('Ts')

                df['S1'] = np.nan
                buoySlabel = f"{binf['name'][0]}-{int(binf['name'][1]):02d}: no salinity data"
                buoySpts.append(ax1.scatter(df['Lon'], df['Lat'], df['S1'], c=df['S1'],  # <- dummy vars
                            cmap=cmap, norm=normsss, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoySlabel))
                buoySptsZ.append(ax11.scatter(df['Lon'], df['Lat'], df['S1'], c=df['S1'],
                            cmap=cmap, norm=normsss, transform=ccrs.PlateCarree(),
                            edgecolor='face', label=buoySlabel))
                columnsWrite.append('S1')

            print('line 134 in plotSuite',bid,columnsWrite)

            # # reorder to descending dates for writing to ouput
            # if len(df)>0:
            #     df.sort_values(by='Date',ascending=False,inplace=True)
            #     df = df.reset_index(drop=True)
            #     print(df.head())

            dfNew = df[columnsWrite]
            print('line 142',dfNew.columns)
            dfNew.rename(columns=outHeaders,inplace=True)
            print(dfNew.head())
            print('line 141',dfNew.columns)
            # sheetname = f'UTO_{binf["name"][0]}-{int(binf["name"][1]):02d}'
            # print('sheetname',sheetname)
            # dfWrite.to_excel(writer, sheet_name=sheetname)
            utoFile = f'{args.base_dir}/UTO_{binf["name"][0]}-{int(binf["name"][1]):02d}.xlsx'
            if os.path.exists(utoFile):
                dfPrev = pd.read_excel(utoFile)
                dfPrev = pd.concat([dfPrev,dfNew],axis=0,ignore_index=True)
                dfPrev.drop_duplicates(inplace=True)
                dfPrev.to_excel(utoFile,index=False)
            else:
                dfNew.to_excel(utoFile,index=False)

        # legends for temps
        legend10 = ax0.legend(handles=buoyTpts,bbox_to_anchor=(1.1,1),loc=2,borderaxespad=0.,fontsize=9,title='HydroBuoy Data')
        print('line 174',buoyTpts)
        frame10 = legend10.get_frame()
        frame10.set_facecolor('lightgray')
        frame10.set_edgecolor('black')
        leg = ax0.get_legend()
        for ii in range(len(bids)):
            leg.legendHandles[ii].set_color('k')

        legend110 = ax10.legend(handles=buoyTptsZ,bbox_to_anchor=(1.1,1),loc=2,borderaxespad=0.,fontsize=9,title='HydroBuoy Data')
        frame10 = legend110.get_frame()
        frame10.set_facecolor('lightgray')
        frame10.set_edgecolor('black')
        leg = ax10.get_legend()
        for ii in range(len(bids)):
            leg.legendHandles[ii].set_color('k')

        # legends for sali
        # if 'Salinity' in dfNew.columns:
        print('line 172',len(bids))
        legend11 = ax1.legend(handles=buoySpts,bbox_to_anchor=(1.1,1),loc=2,borderaxespad=0.,fontsize=9,title='HydroBuoy Data')
        frame11 = legend11.get_frame()
        frame11.set_facecolor('lightgray')
        frame11.set_edgecolor('black')
        leg = ax1.get_legend()
        for ii in range(len(bids)):
            print(ii)
            leg.legendHandles[ii].set_color('k')

        legend111 = ax11.legend(handles=buoySptsZ,bbox_to_anchor=(1.1,1),loc=2,borderaxespad=0.,fontsize=9,title='HydroBuoy Data')
        frame11 = legend111.get_frame()
        frame11.set_facecolor('lightgray')
        frame11.set_edgecolor('black')
        leg = ax11.get_legend()
        for ii in range(len(bids)):
            leg.legendHandles[ii].set_color('k')

        # plt.show()
        # exit(-1)

    if bool(args.swiftIDS):
        print('line 195 plotS, in swiftIDS')
        # get swift data
        eng = matlab.engine.start_matlab()
        eng.addpath(f'{args.base_dir}/swift_telemetry')
        # IDs = ['12','16','17']  # '09', ,'13','15'  # matlab format with the semi colons
        IDs = [item for item in args.swiftIDS.split(',')]  # '09', ,'13','15'  # matlab format with the semi colons
        print('swift ids',IDs)
        # exit(-1)
        # WHEN data are current, use the next two lines
        # starttime = starttimeObj.strftime('%Y-%m-%dT%H:%M:%S')
        # endtime = today.strftime('%Y-%m-%dT%H:%M:%S')

        # startswift = today - dt.timedelta(hours=int(args.hourstoPlot))
        startswift = dt.datetime(2018,9,1)
        starttime = f'{startswift.year}-{startswift.month:02d}-{startswift.day:02d}T00:00:00'
        endtime = '' #f'{today.year}-{today.month:02d}-{today.day:02d}T23:59:59'
        print('SWIFT times',starttime,endtime)
        # exit(-1)
        # can do eng.cd(r'../swift_telemetry') if you need to.

        swiftTpts=[]
        swiftTptsZ=[]
        swiftSpts=[]
        swiftSptsZ=[]
        for ID in IDs:
            print('in getSWIFT, line 564,',starttime,endtime)
            print()

            dfSwift = pfields.getSWIFT(args, ID, starttime, endtime, eng)
            print(dfSwift.head())
            print('line 215 in plotSuite')
            print(dfSwift.columns)
            dfSwift.reset_index(inplace=True)  # used for plotting
            print(dfSwift.tail())
            columnsWrite = ['DateTimeStr','Lat','Lon','WaterTemp-0','Salinity-0']
            # fig5,ax5 = plt.subplots(1,1)
            # ax5.scatter(dfSwift['Lon'],dfSwift['Lat'],20,dfSwift['WaterTemp-0'],cmap=sstcmap)
            # ax5.scatter(dfSwift['Lon'].iloc[-1],dfSwift['Lat'].iloc[-1],150,dfSwift['WaterTemp-0'].iloc[-1],cmap=sstcmap)
            # print(dfSwift.tail(30))
            # plt.show()
            # exit(-1)
            # reqCols=['Lon','Lat]
            # if dfSwfit[]  IF STATEMENT LOOKING FOR NON-NANS IN lon/lat/data
            if not dfSwift['Lon'].isnull().all():
                Tcols = [col for col in dfSwift.columns if col.startswith('WaterTemp')]
                Scols = [col for col in dfSwift.columns if col.startswith('Salinity')]
                Dcols = [col for col in dfSwift.columns if col.startswith('CTdepth')]
                for tcol,dcol in zip(Tcols,Dcols):
                    if not dfSwift[tcol].isnull().all():
                        swiftTlabel=f"#{ID}: {dfSwift[tcol].iloc[-1]:.1f}{degree}C at {dfSwift[dcol].iloc[-1]:.2f}m, {dfSwift['Lon'].iloc[-1]:.2f}W, {dfSwift['Lat'].iloc[-1]:.2f}N"
                        swiftTpts.append(ax0.scatter(dfSwift['Lon'], dfSwift['Lat'], 2*dfSwift['index'], dfSwift[tcol],
                                   cmap=cmap, norm=normsst, marker='s', edgecolor='face',transform=ccrs.PlateCarree(), label=swiftTlabel))
                        if args.smallDomain is not None:
                            swiftTptsZ.append(ax10.scatter(dfSwift['Lon'], dfSwift['Lat'], 2*dfSwift['index'], dfSwift[tcol],
                                       cmap=cmap, norm=normsst, marker='s', edgecolor='face',transform=ccrs.PlateCarree(), label=swiftTlabel))

                    else:
                        swiftTlabel=f"SWIFT {ID} No SST data."

                for scol,dcol in zip(Scols,Dcols):
                    if not dfSwift[scol].isnull().all():
                        swiftSlabel=f"#{ID}: {dfSwift[scol].iloc[-1]:.2f} at {dfSwift[dcol].iloc[-1]:.2f}m, {dfSwift['Lon'].iloc[-1]:.2f}W, {dfSwift['Lat'].iloc[-1]:.2f}N"
                        swiftSpts.append(ax1.scatter(dfSwift['Lon'], dfSwift['Lat'],2*dfSwift['index'],dfSwift[scol],
                                   cmap=cmap, norm=normsss, marker='s', edgecolor='face',transform=ccrs.PlateCarree(), label=swiftSlabel))
                        if args.smallDomain is not None:
                            swiftSptsZ.append(ax11.scatter(dfSwift['Lon'], dfSwift['Lat'],2*dfSwift['index'],dfSwift[scol],
                                       cmap=cmap, norm=normsss, marker='s', edgecolor='face',transform=ccrs.PlateCarree(), label=swiftSlabel))
                    else:
                        swiftSlabel=f"SWIFT {ID} No SSS data."
            else:
                swiftTlabel=f"SWIFT {ID} No lon/lat."
                swiftSlabel=f"SWIFT {ID} No lon/lat."

            # reorder to descending dates for writing to ouput
            # dfSwift.sort_values(by='DateObj',ascending=False,inplace=True)
            # dfSwift = dfSwift.reset_index(drop=True)
            # dfSwift.drop(columns=(['index','DateObj']),axis=1, inplace=True)
            dfswiftNew = dfSwift[columnsWrite]
            dfswiftNew.rename(columns=outHeaders,inplace=True)
            print('dfswiftNew')
            print(dfswiftNew.head())
            # sheetname = f'Swift{ID}'
            # dfSwiftWrite.to_excel(writer, sheet_name=sheetname)
            swiftFile = f'{args.base_dir}/Swift{ID}.xlsx'
            if os.path.exists(swiftFile):
                dfswiftPrev = pd.read_excel(swiftFile)
                dfswiftPrev = pd.concat([dfswiftPrev,dfswiftNew],axis=0,ignore_index=True)
                dfswiftPrev.drop_duplicates(inplace=True)
                dfswiftPrev.to_excel(swiftFile,index=False)
            else:
                dfswiftNew.to_excel(swiftFile,index=False)

        legend20 = ax0.legend(handles=swiftTpts,bbox_to_anchor=(1.1, 0.8), loc=2, borderaxespad=0.,fontsize=9,title='Swift Data' )
        frame20 = legend20.get_frame()
        frame20.set_facecolor('lightblue')
        frame20.set_edgecolor('black')
        leg = ax0.get_legend()
        for ii in range(len(IDs)):
            leg.legendHandles[ii].set_color('k')

        legend120 = ax10.legend(handles=swiftTpts,bbox_to_anchor=(1.1, 0.8), loc=2, borderaxespad=0.,fontsize=9,title='Swift Data' )
        frame20 = legend120.get_frame()
        frame20.set_facecolor('lightblue')
        frame20.set_edgecolor('black')
        leg = ax10.get_legend()
        for ii in range(len(IDs)):
            leg.legendHandles[ii].set_color('k')

        legend21 = ax1.legend(handles=swiftSpts,bbox_to_anchor=(1.1, 0.8), loc=2, borderaxespad=0.,fontsize=9,title='Swift Data' )
        frame21 = legend21.get_frame()
        frame21.set_facecolor('lightblue')
        frame21.set_edgecolor('black')
        leg = ax1.get_legend()
        for ii in range(len(IDs)):
            leg.legendHandles[ii].set_color('k')

        legend121 = ax11.legend(handles=swiftSpts,bbox_to_anchor=(1.1, 0.8), loc=2, borderaxespad=0.,fontsize=9,title='Swift Data' )
        frame21 = legend121.get_frame()
        frame21.set_facecolor('lightblue')
        frame21.set_edgecolor('black')
        leg = ax11.get_legend()
        for ii in range(len(IDs)):
            leg.legendHandles[ii].set_color('k')

    if bool(args.buoyIDS):
        ax0.add_artist(legend10) # UTO legend: need to add legends back, as by default only last legend is shown
        ax10.add_artist(legend110)
    if bool(args.swiftIDS):
        ax0.add_artist(legend20) # swift legend
        ax10.add_artist(legend120)
    fig0.savefig(figstr0)
    fig10.savefig(figstr10)


    if bool(args.buoyIDS):
        ax1.add_artist(legend11) # UTO legend
        ax11.add_artist(legend111)
    if bool(args.swiftIDS):
        ax1.add_artist(legend21) # swift legend
        ax11.add_artist(legend121)
    fig1.savefig(figstr1)
    fig11.savefig(figstr11)
    print(figstr0)
    print(figstr10)
    print(figstr1)
    print(figstr11)
    os.system(f'/usr/local/bin/lftp sftp://sassie@ftp.polarscience.org/ --password 2Icy2Fresh! -e "cd /FTP/insitu/images/; put {figstr0};put {figstr10};put {figstr1};put {figstr11}; bye"')

    # writer.close()
    os.system(f'/usr/local/bin/lftp sftp://sassie@ftp.polarscience.org/ --password 2Icy2Fresh! -e "cd /FTP/insitu/data/; mput *.xlsx; bye"')
    # os.system(f'mv {args.base_dir}/*.xlsx {args.base_dir}/excel_files/')
        # plt.show(block=False)
        # plt.pause(0.001)
        # input('Press enter to close figures.')
        # plt.close('all')
        # exit(-1)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,  fromfile_prefix_chars='@')
    parser.add_argument('--base_dir', type=str, default=os.getcwd(), help='root directory')
    # parser.add_argument('--minLon', type=int, help='minimum Longitude for plot domain')  # cant seem to pass list of ints...
    # parser.add_argument('--maxLon', type=int, help='maximum Longitude for plot domain')
    # parser.add_argument('--minLat', type=int, help='minimum Latitude for plot domain')
    # parser.add_argument('--maxLat', type=int, help='maximum Latitude for plot domain')
    # parser.add_argument('--strdate', type=str, default='None', help='date for which to get data, in yyyymmdd format')
    parser.add_argument('--mapDomain', type=str, help='list of lons/lats: W, E, S, N')
    # parser.add_argument('--shipLocation', type=str, help='lon, lat of Ship')
    parser.add_argument('--smallDomain', type=int, help='+/- m from shipLocation')

    # parser.add_argument('--strdateSSS',type=str,default='None',help='date for which to get , in yyyymmdd format')
    # parser.add_argument('--satelliteICE',type=str,default='g02202', help='Ice Concentration source: \n'
    #                                                       '\t g02202 \n'
    #                                                       '\t nsidc-0081')
    # parser.add_argument('--satelliteSSS',type=str,default='JPL-L3', help='Sea Surface Salinity source: \n'
    #                                                       '\t JPL-L3 \n'
    #                                                       '\t RSS-L3 \n'
    #                                                       '\t JPL-L2B-NRT \n'
    #                                                       '\t JPL-L2B-del \n'  <- we're using this one. Not sure if it's actually 'delayed'
    #                                                       '\t these have not all been tested')
    parser.add_argument('--buoyIDS', type=str, help='list of 15-digit UpTempO buoy IDs. Options: \n'
                                                   '\t 300534060649670 (2021-01) \n'
                                                   '\t 300534062158480 (2021-04)')
    parser.add_argument('--swiftIDS', type=str, help='list of 2-digit Swift buoy IDs. Options: \n'
                                                   '\t 09 \n'
                                                   '\t 13 \n'
                                                   '\t 15')
    parser.add_argument('--hourstoPlot', type=int, help='plot data this number of hours leading up to latest')

    args, unknown = parser.parse_known_args()
    print(args)
    # IDs = [item for item in args.swiftIDS.split(',')]  # '09', ,'13','15'  # matlab format with the semi colons
    # print('swift ids',IDs)
    # exit(-1)
    plotSuite(args)
