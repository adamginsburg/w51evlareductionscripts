import os
from plotms_cli import plotms_cli as plotms
from clean import clean
from plotcal import plotcal
from imstat import imstat 
from viewer import viewer
from taskinit import *
mytb = casac.table()

    # Define the output name for the averaged data:
    #avg_data = "%s_spw%i_AVG.ms" % (field.replace(" ",""), spwn)

cleanboxes = [
    'box [[19:23:48.66885, +014.33.36.6619], [19:23:45.55100, +014.34.21.2514]] coord=J2000',
    'box [[19:23:43.14591, +014.30.19.2731], [19:23:40.98965, +014.30.59.0485]] coord=J2000',
    'box [[19:23:40.46514, +014.31.00.7410], [19:23:39.35778, +014.31.15.5504]] coord=J2000',
    'box [[19:23:44.13661, +014.30.20.9651], [19:23:43.52475, +014.30.37.0448]] coord=J2000',
    'box [[19:23:46.40916, +014.29.41.1877], [19:23:42.47571, +014.29.56.4237]] coord=J2000',
    'box [[19:23:43.20414, +014.29.54.7309], [19:23:41.39762, +014.30.20.1197]] coord=J2000',
    'box [[19:23:44.48635, +014.30.44.6607], [19:23:42.44664, +014.31.10.8964]] coord=J2000',
    ]

clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]

## # Use the SPLIT task to average the data in velocity.
## 
## # ... first removing any previous version
## os.system("rm -rf "+avg_data)
## 
## split(vis=vis,
##       outputvis=avg_data,
##       datacolumn='corrected', # was 'data'...
##       #timebin='10s',
##       width=width,
##       field=field,
##       spw=str(spwn))

def selfcal(vis, spwn=6, doplots=True, INTERACTIVE=False, reclean=True, field='W51 Ku',
        outdir_template="spw%i_selfcal_iter/", statsbox='170,50,229,97', ant1list=['ea14','ea05'],
        ant2list=['ea16','ea07'], avgchannel_wide='128', avgchannel_narrow='8',
        cleanboxes=cleanboxes, refant='ea27', solint='30s', niter=2,
        multiscale=[0,5,10,15,25,50], imsize=512, robust=0.0 ):
    """
    Docstring incomplete
    """

    spw = int(spwn)
    outdir = outdir_template % spwn
    try:
        os.mkdir(outdir)
    except OSError:
        pass

    # you're supposed to pass in avg_data as input
    avg_data = vis

    mytb.open(vis+"/ANTENNA")
    antnames = mytb.getcol("NAME")

    # plot each antenna's ampl vs time for flagging purposes
    for ant2 in ant2list:
        for ant in ant1list:
            plotms(vis=vis, spw=str(spwn), xaxis='time', yaxis='amp', avgchannel=avgchannel_wide,
                    avgscan=F, coloraxis='baseline', iteraxis='', xselfscale=T,
                    yselfscale=T,
                    antenna=ant+"&"+ant2,
                    title='Amp vs Time before averaging for spw %i ant %s-%s' % (spwn,ant,ant2),
                    plotfile=outdir+'ampvstime_spw%i_ant%s-%s.png' % (spwn,ant,ant2),
                    field=field,
                    overwrite=True,
                    )

            plotms(vis=vis, spw=str(spwn), xaxis='freq', yaxis='phase', avgtime='1e8',
                    avgscan=T, coloraxis='corr', iteraxis='baseline', xselfscale=T,
                    yselfscale=T,
                    antenna=ant+"&"+ant2,
                    title='Phase vs Freq with time averaging for spw %i ant %s-%s' % (spwn,ant,ant2),
                    plotfile=outdir+'phasevsfreq_spw%i_ant%s-%s.png' % (spwn,ant,ant2),
                    field=field,
                    overwrite=True,
                    )

            plotms(vis=vis, spw=str(spwn), xaxis='amp', yaxis='phase', avgtime='1e8',
                    avgscan=T, coloraxis='corr', iteraxis='baseline', xselfscale=T,
                    yselfscale=T,
                    antenna=ant+"&"+ant2,
                    title='Phase vs Amp with time averaging for spw %i ant %s-%s' % (spwn,ant,ant2),
                    plotfile=outdir+'phasevsamp_spw%i_ant%s-%s.png' % (spwn,ant,ant2),
                    field=field,
                    overwrite=True,
                    )

    # imagename = "noaverage_spw%i" % spwn
    # os.system("rm -rf "+imagename+".image")
    # os.system("rm -rf "+imagename+".model")
    # os.system("rm -rf "+imagename+".flux")
    # os.system("rm -rf "+imagename+".psf")
    # os.system("rm -rf "+imagename+".residual")
    # clean(vis=vis, field=field, imagename=imagename, mode='mfs', 
    #         weighting='briggs', robust=robust, niter=500, imsize=512)
    # viewer(imagename+".image",
    #         outfile=outdir+imagename+".image.png",
    #         outformat='png',
    #         gui=False)
    # exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


    #width = 10 # for TW Hydra
    # width = 4 # for NGC 3256


    # (0) Using your split-off, calibrated data, plot the "model" in this MS using
    # plotms.  It should be unit-valued for all data.  If not, run delmod to get
    # rid of any model that might still be lurking in the header, and/or clearcal
    # to set to 1 any MODEL data.
    plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp',
            avgchannel=avgchannel_wide, xdatacolumn='model', ydatacolumn='model', avgscan=F,
            coloraxis='baseline', iteraxis='', xselfscale=T, yselfscale=T,
            title='Model Amp vs Time after split for spw %i.  Should be all 1s' % spwn,
            plotfile=outdir+'ampvstime_model_shouldbe1.png', field=field,
            overwrite=True,)
    delmod(vis=avg_data)

    plotms(vis=avg_data, spw='0', xaxis='phase', yaxis='amp',
            avgchannel=avgchannel_wide, xdatacolumn='data', ydatacolumn='data', avgscan=F,
            coloraxis='baseline', iteraxis='', xselfscale=T, yselfscale=T,
            title='Corrected Phase vs Amp after split',
            plotfile=outdir+'ampvsphase_corrected_avg_spw%i.png' % spwn, field=field,
            overwrite=True,)

    # (0.5) Run clean non-interactively with some set number of iterations, and be
    # sure to keep the image around for comparison later.  Run delmod to get rid of
    # the model it saved to the MS header.
    #if reclean:
    #    imagename="average_spw%i_shallowclean" % spwn

    #    for suffix in clean_output_suffixes:
    #        os.system("rm -rf "+imagename+suffix)

    #    clean(vis=avg_data, field=field, imagename=imagename, mode='mfs', 
    #            weighting='briggs', robust=robust, niter=100, imsize=512)
    #    viewer(imagename+".image",
    #            outfile=outdir+imagename+".image.png",
    #            outformat='png',
    #            gui=False)
    #    exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
    #    delmod(avg_data,scr=True)


    # (1) Clean a single SPW *interactively*, boxing the brightest regions and not
    # cleaning very deeply (maybe 100 iterations).  Keep this model in the header
    # -- it's what you'll use for the first round of self-calibration.
    if reclean:
        imagename="average_spw%i_shallowclean_masked" % spwn

        for suffix in clean_output_suffixes:
            os.system("rm -rf "+imagename+suffix)

        clean(vis=avg_data, field=field, imagename=imagename, mode='mfs', 
                psfmode='hogbom',multiscale=multiscale,
                weighting='briggs', robust=robust, niter=100, imsize=imsize,
                mask=cleanboxes,
                nterms=2,
                usescratch=True)
        viewer(imagename+".image.tt0",
                outfile=outdir+imagename+".image.tt0.png",
                outformat='png',
                gui=False)
        exportfits(imagename=imagename+".image.tt0", fitsimage=imagename+".fits", overwrite=True)

    imrms = [imstat(imagename+".image.tt0",box=statsbox)['rms']]

    # FAILS!!!!
    #plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp',
    #        avgchannel='128', xdatacolumn='model', ydatacolumn='model', avgscan=F,
    #        coloraxis='baseline', iteraxis='', xselfscale=T, yselfscale=T,
    #        title='Model Amp vs Time after shallow clean for spw %i.' % spwn,
    #        plotfile=outdir+'ampvstime_model_shallowclean_spw%i.png' % spwn, field=field,
    #        overwrite=True,)


    for calnum in xrange(niter):

        # for Ku D W51 Ku spw 2
        if reclean:

            first_image = 'spw%i_C_C_firstim_selfcal%i' % (spwn,calnum)

            for suffix in clean_output_suffixes:
                os.system("rm -rf "+first_image+suffix)

            clean(vis=avg_data,imagename=first_image,field=field, mode='mfs', 
                    psfmode='hogbom',multiscale=multiscale,
                    weighting='briggs', robust=robust, niter=100, imsize=imsize,
                    mask=cleanboxes,
                    nterms=2,
                    usescratch=True)
            exportfits(imagename=first_image+".image.tt0", fitsimage=first_image+".fits", overwrite=True)

        viewer(first_image+".image.tt0",
                outfile=outdir+first_image+".image.tt0.png",
                outformat='png',
                gui=False)

        # this fails?
        #plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp',
        #    avgchannel='128', xdatacolumn='model', ydatacolumn='model', avgscan=F,
        #    coloraxis='baseline', iteraxis='', xselfscale=T, yselfscale=T,
        #    title='Model Amp vs Time after shallow clean for spw %i iter %i.' % (spwn,calnum),
        #    plotfile=outdir+'ampvstime_model_shallowclean_spw%i_iter%i.png' % (spwn,calnum), field=field,
        #    overwrite=True,)

        # DONE avg/split ing

        caltable = 'selfcal%i_%s_spw%i.gcal' % (calnum,field.replace(" ",""),spwn)
        if reclean:
            os.system('rm -rf '+caltable)
            gaincal(vis=avg_data,
                    field='',
                    caltable=caltable,
                    spw='',
                    # gaintype = 'T' could reduce failed fit errors by averaging pols...
                    gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
                    solint=solint,
                    refant=refant,
                    calmode='p',
                    combine='scan',
                    minblperant=4)

        #
        # Watch out for failed solutions noted in the terminal during this
        # solution. If you see a large fraction (really more than 1 or 2) of
        # your antennas failing to converge in many time intervals then you
        # may need to lengthen the solution interval.
        #

        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
        # INSPECT THE CALIBRATION
        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

        #
        # After you have run the gaincal, you want to inspect the
        # solution. Use PLOTCAL to look at the solution (here broken into
        # panels by SPW with individual antennas mapped to colors). Look at
        # the overall magnitude of the correction to get an idea of how
        # important the selfcal is and at how quickly it changes with time to
        # get an idea of how stable the instrument and atmosphere were.
        #

        if doplots:

            for ant2 in ant2list:
                for ant in ant1list:
                    # (4) Have a look at the gain solutions by antenna.  Which antennas
                    # have the largest phase corrections?  Before applying the
                    # calibration, use plotms to display the corrected phase vs. amp
                    # for these antennas, to compare with *after* the correction is
                    # applied.
                    plotcal(caltable=caltable,
                            xaxis='time', yaxis='phase',
                            showgui=False,
                            antenna=ant+'&'+ant2,
                            figfile=outdir+'selfcal%i_spw%i_phasevstime_ant%s-%s.png' % (calnum,spwn,ant,ant2),
                            iteration='')#, subplot = 221)
                    #plotcal(caltable=caltable, xaxis='amp', yaxis='phase',
                    #        showgui=False,
                    #        antenna=ant,
                    #        figfile=outdir+'selfcal%i_spw%i_phasevsamp_ant%s.png' % (calnum,spwn,ant),
                    #        iteration='')#, subplot = 221)
                    if calnum == 0:
                        datacol='data'
                    else:
                        datacol='corrected'
                    plotms(vis=avg_data, xaxis='time', yaxis='phase',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phasetime.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=avg_data, xaxis='time', yaxis='amp',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_amptime.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=avg_data, xaxis='phase', yaxis='amp',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phaseamp.png' % (calnum,spwn,ant,ant2),)

            plotcal(caltable=caltable,
                    xaxis='time', yaxis='phase',
                    plotrange=[0,0,-180,180],
                    showgui=INTERACTIVE,
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phasevstime.png' % (calnum,spwn),
                    iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            plotcal(caltable=caltable,
                    xaxis='antenna', yaxis='phase',
                    showgui=INTERACTIVE,
                    figfile=outdir+'selfcal%i_spw%i_phasevsantenna.png' % (calnum,spwn),
                    iteration='')

            plotcal(caltable=caltable,
                    xaxis='time', yaxis='amp',
                    plotrange=[0,0,0.5,1.5],
                    showgui=INTERACTIVE,
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvstime.png' % (calnum,spwn),
                    iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            #plotcal(caltable=caltable,
            #        xaxis='phase', yaxis='amp',
            #        plotrange=[-50,50,0.5,1.5],
            #        showgui=INTERACTIVE,
            #        figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase.png' % (calnum,spwn),
            #        iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            # THERE WILL BE WEIRD "LUSTRE" ERRORS GENERATED BY THE FILE SYSTEM. DO
            # NOT FREAK OUT. These are just a feature of our fast file
            # system. Plotcal will still work.

            # It can be useful useful to plot the X-Y solutions (i.e., differences
            # between polarizations) as an indicator of the noise in the
            # solutions.

            plotcal(caltable=caltable,
                    xaxis='time', 
                    yaxis='phase',
                    plotrange=[0,0,-25, 25], 
                    poln = '/',
                    showgui=INTERACTIVE,
                    iteration='spw,antenna' if INTERACTIVE else '', 
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_poldiff.png' % (calnum,spwn),
                    subplot = 221 if INTERACTIVE else 111)

            plotms(vis=avg_data,
                    xaxis='uvdist',
                    yaxis='amp',
                    xdatacolumn='corrected',
                    ydatacolumn='corrected',
                    avgtime='1e8s',
                    avgchannel=avgchannel_narrow,
                    coloraxis='baseline',
                    overwrite=True,
                    title='Iteration %i for spw %i' % (calnum,spw),
                    plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_uvdistamp.png' % (calnum,spwn),
                    )

            #plotms(vis=avg_data,
            #        xaxis='phase',
            #        yaxis='amp',
            #        xdatacolumn='corrected',
            #        ydatacolumn='corrected',
            #        avgtime='60s',
            #        avgchannel=avgchannel_narrow,
            #        coloraxis='corr',
            #        overwrite=True,
            #        title='Iteration %i for spw %i' % (calnum,spw),
            #        plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phaseamp.png' % (calnum,spwn),
            #        )

            plotms(vis=avg_data,
                    xaxis='time',
                    yaxis='amp',
                    xdatacolumn='corrected',
                    ydatacolumn='corrected',
                    avgtime='10s',
                    avgchannel=avgchannel_narrow,
                    coloraxis='baseline',
                    overwrite=True,
                    title='Iteration %i for spw %i' % (calnum,spw),
                    plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_amptime.png' % (calnum,spwn),
                    )


        # The rms noise is about 4 to 8 deg, depending on antenna, but the
        # phase changes are considerably larger.  This indicates that the
        # application of this solution will improve the image.

        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
        # APPLY THE CALIBRATION
        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

        #
        # If you are satisfied with your solution, you can now apply it to the
        # data to generate a new corrected data column, which you can then
        # image. Be sure to save the previous flags before you do so because
        # applycal will flag data without good solutions. The commented
        # command after the applycal will roll back to the saved solution in
        # case you get in trouble.
        #

        # flagmanager(vis=avg_data,
        #             mode='save',
        #             versionname='before_selfcal_apply')
        # 2013-03-04 19:53:37     SEVERE  agentflagger:: (file /opt/casa/stable-2013-02/gcwrap/tools/flagging/agentflagger_cmpt.cc, line 37)      Exception Reported: Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG
        # *** Error *** Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG

        if reclean:
            applycal(vis=avg_data,
                     gaintable=caltable,
                     interp='linear',
                     flagbackup=True) # was False when flagmanager was used

        # (6) Plot corrected phase vs. amp for the antennas you picked out in (4),
        # to check that in fact the corrections have been applied as expected.
        for ant2 in ant2list:
            for ant in ant1list:
                plotms(vis=avg_data, xaxis='time', yaxis='phase',
                        xdatacolumn='corrected', ydatacolumn='corrected',
                        avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                        antenna=ant+'&'+ant2,
                        overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                        plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phasetime_applied.png' % (calnum,spwn,ant,ant2),)
                plotms(vis=avg_data, xaxis='time', yaxis='amp',
                        xdatacolumn='corrected', ydatacolumn='corrected',
                        avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                        antenna=ant+'&'+ant2,
                        overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                        plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_amptime_applied.png' % (calnum,spwn,ant,ant2),)
                plotms(vis=avg_data, xaxis='phase', yaxis='amp',
                        xdatacolumn='corrected', ydatacolumn='corrected',
                        avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                        antenna=ant+'&'+ant2,
                        overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                        plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phaseamp_applied.png' % (calnum,spwn,ant,ant2),)
                plotms(vis=vis, spw='0', xaxis='freq', yaxis='phase', avgtime='1e8',
                        avgscan=T, coloraxis='corr', iteraxis='baseline', xselfscale=T,
                        yselfscale=T,
                        antenna=ant+'&'+ant2,
                        title='Phase vs Freq with time averaging for spw %i ant %s-%s iter %i' % (spwn,ant,ant2,calnum),
                        plotfile=outdir+'phasevsfreq_spw%i_ant%s-%s_selfcal%i.png' % (spwn,ant,ant2,calnum),
                        field=field,
                        overwrite=True,
                        )
        

        # Use this command to roll back to the previous flags in the event of
        # an unfortunate applycal.

        #flagmanager(vis=avg_data,
        #            mode='restore',
        #            versionname='before_selfcal_apply')


        if reclean:
            selfcal_image = 'spw%i_C_C_selfcal%i' % (spwn,calnum)
            for suffix in clean_output_suffixes:
                os.system("rm -rf "+selfcal_image+suffix)
            clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs',
                    psfmode='hogbom',multiscale=multiscale,
                    weighting='briggs', robust=robust, niter=1000, imsize=imsize,
                    nterms=2,
                    mask=cleanboxes,
                    usescratch=True)
            exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

            plotms(vis=avg_data, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
                    ydatacolumn='corrected-model',
                    avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                    yselfscale=T,
                    title='Residual vs. Baseline after CSCLEAN iter %i' % calnum,
                    plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline.png' % (calnum,spwn),
                    field=field,
                    overwrite=True,
                    )
                
            plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
                    ydatacolumn='corrected-model', 
                    coloraxis='baseline', iteraxis='', xselfscale=T,
                    yselfscale=T,
                    title='Residual vs. Time after CSCLEAN iter %i' % (calnum),
                    plotfile=outdir+'post_selfcal%i_spw%i_residVStime.png' % (calnum,spwn),
                    field=field,
                    overwrite=True,
                    )

            plotms(vis=avg_data, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
                    ydatacolumn='corrected-model', 
                    avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                    yselfscale=T,
                    title='Residual vs. UVDIST after CSCLEAN iter %i' % (calnum) ,
                    plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist.png' % (calnum,spwn),
                    field=field,
                    overwrite=True,
                    )

        imrms.append(imstat(selfcal_image+".image.tt0",box=statsbox)['rms'])

        viewer(selfcal_image+".image.tt0",
                outfile=outdir+selfcal_image+".image.tt0.png",
                outformat='png',
                gui=False)

        print "FINISHED ITERATION %i" % calnum

    print "FINISHED ITERATING!!! YAY!"

    # final phase + gain cal:
    # http://casaguides.nrao.edu/index.php?title=Calibrating_a_VLA_5_GHz_continuum_survey#One_Last_Iteration:_Amplitude_.26_Phase_Self_Calibration
    aptable = 'selfcal_ap_%s_spw%i.gcal' % (field.replace(" ",""),spwn)
    gaincal(vis=avg_data, field='', caltable=aptable, gaintable=caltable, spw='',
            solint='inf', refant=refant, calmode='ap', combine='', minblperant=4)

    plotcal(caltable=aptable,
            xaxis='phase', yaxis='amp',
            plotrange=[-50,50,0.5,1.5],
            showgui=INTERACTIVE,
            figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase_final.png' % (calnum,spwn),
            iteration='spw' if INTERACTIVE else '')#, subplot = 221)

    applycal(vis=avg_data,
             gaintable=[aptable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    selfcal_image = 'spw%i_C_C_selfcal%i_final' % (spwn,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', mask=cleanboxes,
            weighting='briggs', robust=robust, niter=10000, imsize=imsize,
            nterms=2,
            usescratch=True)
    exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

    plotms(vis=avg_data, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model',
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Baseline after CSCLEAN iter %i' % calnum,
            plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )
        
    plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
            ydatacolumn='corrected-model', 
            coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Time after CSCLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVStime.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    plotms(vis=avg_data, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model', 
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. UVDIST after CSCLEAN iter %i' % (calnum) ,
            plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    selfcal_image = 'spw%i_C_C_selfcal%i_final_multiscale' % (spwn,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', imagermode='csclean',# mask=cleanboxes,
            multiscale=multiscale, psfmode='hogbom',
            nterms=2,
            weighting='briggs', robust=robust, niter=10000, imsize=imsize,
            usescratch=True)
    exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

    plotms(vis=avg_data, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model',
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Baseline after multiscale CLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline_multiscale.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )
        
    plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
            ydatacolumn='corrected-model', 
            coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Time after multiscale CLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVStime_multiscale.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    plotms(vis=avg_data, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model', 
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. UVDIST after multiscale CLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist_multiscale.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    return imrms


def apply_selfcal(rawvis, field, spwn_source, spwn_target, calnum=0):

    noavg_data = '%s_spw%i_split.ms' % (field.replace(" ",""),spwn_target)
    aptable = 'selfcal_ap_%s_spw%i.gcal' % (field.replace(" ",""),spwn_source)
    caltable = 'selfcal%i_%s_spw%i.gcal' % (calnum,field.replace(" ",""),spwn_source)

    os.system('rm -rf '+noavg_data)
    split(vis=vis,
          outputvis=noavg_data,
          datacolumn='corrected', # was 'data'...
          spw=str(spwn_target))
    applycal(vis=noavg_data,
             gaintable=[aptable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    selfcal_image = 'spw%i_C_C_selfcal%i_final_cube' % (spwn_target,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=noavg_data,imagename=selfcal_image,field=field, mode='frequency',# mask=cleanboxes,
            multiscale=[0,5,10,25], psfmode='hogbom',
            weighting='briggs', robust=robust, niter=10000, imsize=512)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

