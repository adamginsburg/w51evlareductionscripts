rawvis='13A-064.sb18020284.eb19181492.56353.71736577546.ms'
vis = '3c48_Ku_spw1.ms'
flux_calibrator = '0137+331=3C48'
refant='ea03'
split(vis=rawvis, outputvis=vis, field=flux_calibrator, datacolumn='data', spw='1')
setjy(vis=vis, field=flux_calibrator, scalebychan=True, modimage='3c48_C.im', usescratch=False)
gencal(vis=vis,caltable='calKu_spw1.gaincurve',caltype='gc')
gaincal(vis=vis,caltable='calKu_spw1.G0',field=flux_calibrator, spw='',
    gaintable=['calKu_spw1.gaincurve'],
    gaintype='G',refant=refant, calmode='p',solint='int',minsnr=3,gaincurve=False)
plotcal(caltable='calKu_spw1.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_spw1_phasecal_phase.png')
gaincal(vis=vis,caltable='calKu_spw1.K0',
    gaintable=['calKu_spw1.gaincurve','calKu_spw1.G0'],
    field=flux_calibrator,spw='',gaintype='K',gaincurve=False,
    refant=refant,combine='scan',solint='inf',minsnr=3)
plotcal(caltable='calKu_spw1.G0',xaxis='time',yaxis='phase', figfile='plots/3c48_spw1_ampcal_phase.png')
plotcal(caltable='calKu_spw1.G0',xaxis='time',yaxis='amp', figfile='plots/3c48_spw1_ampcal_amp.png')
bandpass(vis=vis,caltable='calKu_spw1.B0',
    gaintable=['calKu_spw1.gaincurve', 'calKu_spw1.G0','calKu_spw1.K0'],
    field=flux_calibrator,refant=refant,solnorm=False,
    bandtype='B', combine='scan', solint='inf', gaincurve=False)
plotcal(caltable='calKu_spw1.B0',xaxis='freq',yaxis='amp', figfile='plots/3c48_spw1_bandcal_amp.png')
plotcal(caltable='calKu_spw1.B0',xaxis='freq',yaxis='phase', figfile='plots/3c48_spw1_bandcal_phase.png')
gaincal(vis=vis,caltable='calKu_spw1.G1int',
    gaintable=['calKu_spw1.gaincurve',
              'calKu_spw1.K0','calKu_spw1.B0'],
    field=flux_calibrator,refant=refant,solnorm=F,
    spw='', solint='int',gaintype='G',calmode='p',gaincurve=False,)
plotcal(caltable='calKu_spw1.G1int',xaxis='time',yaxis='phase', figfile='plots/3c48_spw1_G1cal_phase.png')
plotcal(caltable='calKu_spw1.G1int',xaxis='time',yaxis='amp', figfile='plots/3c48_spw1_G1cal_amp.png')

gaincal(vis=vis, caltable='calKu_spw1.G2', 
        gaintable=['calKu_spw1.gaincurve',
                   'calKu_spw1.K0','calKu_spw1.B0','calKu_spw1.G1int'], 
        gainfield=['',flux_calibrator,flux_calibrator,flux_calibrator], 
        interp=['','nearest','nearest','nearest'], 
        field=flux_calibrator,refant=refant,solnorm=F,
        spw='',
        solint='inf',combine='scan',gaintype='G',calmode='a',gaincurve=False)
gaincal(vis=vis, caltable='calKu_spw1.G3', 
        gaintable=['calKu_spw1.gaincurve',
                   'calKu_spw1.K0','calKu_spw1.B0','calKu_spw1.G1int'], 
        gainfield=['',flux_calibrator,flux_calibrator,flux_calibrator], 
        interp=['','nearest','nearest','nearest'], 
        field=flux_calibrator,refant=refant,solnorm=F,
        spw='',
        solint='inf',combine='scan',gaintype='G',calmode='a',gaincurve=False)

plotcal(caltable='calKu_spw1.G2',xaxis='time',yaxis='phase', figfile='plots/3c48_spw1_G2cal_phase.png')
plotcal(caltable='calKu_spw1.G2',xaxis='time',yaxis='amp', figfile='plots/3c48_spw1_G2cal_amp.png')
plotcal(caltable='calKu_spw1.G3',xaxis='time',yaxis='phase', figfile='plots/3c48_spw1_G3cal_phase.png')
plotcal(caltable='calKu_spw1.G3',xaxis='time',yaxis='amp', figfile='plots/3c48_spw1_G3cal_amp.png')

clean(vis=vis, imagename='3c48_Ku_spw1_junk', imsize=1024)

applycal(vis=vis, field=flux_calibrator, 
        gaintable=['calKu_spw1.gaincurve','calKu_spw1.G0','calKu_spw1.K0','calKu_spw1.B0','calKu_spw1.G1int','calKu_spw1.G2'],
        interp=['','nearest','nearest','nearest','nearest','nearest'],
        parang=False, calwt=False, gaincurve=False)

clean(vis=vis, imagename='3c48_Ku_spw1', imsize=1024)

