c
      subroutine close_hsa(lu)
      close(lu)
      return
      end

      
c-------------------------------------------------
      subroutine drop(lu,iwx,iflag,iyrs,imns,idys,line,sfcp)
c
c     decodes tempdrop message into spline format
c     -------------------------------------------------
c
      character*1 clat,clon
      character*2 header(12)
      character*30 blank
      character*70 line
      character*80 dropl(200)
      character*200 remark
      dimension prs(12)
      logical plev(12),knots,skpwind
      integer iostat
c 
      common /dropdata/idropl,dropl
c
      data header /'99','00','92','85','70','50','40','30',
     *             '25','20','15','10'/
      data prs /1070.,1000.,925.,850.,700.,500.,400.,300.,
     *          250.,200.,150.,100./
      data plev /12*.false./
      data blank /'                             '/
c
      idropl = 0
      ihhmm = 9999
      lvl=0
      sfcp = 9999.
      splat = -999.
      splon = -999.
c
c     ------------------------------------------------
c     if iflag=1 then we are already at the XXAA line
c     ------------------------------------------------
c
c     read the line with the mission number
c     -------------------------------------
 10   if (iflag.ne.1) then
         read(12,'(a)',end=99)
         if(line(1:30).eq.blank)goto 10
         endif
c
c     read the first data line
c     ------------------------
 40   if (iflag.ne.1) then
         read(12,'(a)',end=99)line
         if(line(1:30).eq.blank)goto 40
         endif
c
c
c     read the value of the day
c     check if the winds are in knots or m/s
c     --------------------------------------
      read (line(7:8),'(i2)',err=1000) iday
      if (iday.gt.50) then
         iday=iday-50
         knots = .true.
         else
         knots = .false.
         endif
c
c     check for month, year flips
c     ---------------------------
      yy = iyrs
      mm = imns
      if (iday.lt.idys) then
         mm = imns+1
         if (mm.eq.13) then
            mm = 1
            yy = iyrs + 1.
            if (yy.eq.100.) yy = 00.
            endif
         endif
c
      yymmdd = yy * 10000. + float(mm) * 100. + float(iday)
      
c
c     read the value of the hour
c     --------------------------
      read (line(9:10),'(i2)',err=1000) ihour
      igmt = ihour * 100.
c
c     set the value of the highest mandatory wind level reporting
c     -----------------------------------------------------------
      if(line(11:11).eq.'/')then
        maxlvl=1
      elseif(line(11:11).eq.'0')then
        maxlvl=2
      elseif(line(11:11).eq.'9')then
        maxlvl=3
      elseif(line(11:11).eq.'8')then
        maxlvl=4
      elseif(line(11:11).eq.'7')then
        maxlvl=5
      elseif(line(11:11).eq.'5')then
        maxlvl=6
      elseif(line(11:11).eq.'4')then
        maxlvl=7
      elseif(line(11:11).eq.'3')then
        maxlvl=8
      elseif(line(11:11).eq.'2')then
        maxlvl=10
      elseif(line(11:11).eq.'1')then
        maxlvl=12
      endif
c
c     read the latitude
c     -----------------
      read (line(15:17),'(f3.1)',err=1000) alat
c
c     read the quadrant,longitude
c     ---------------------------
      read (line(19:23),'(i1,f4.1)',err=1000) nquad,alon
c
c     Assign negative sign to east or south (HSA convention)
c     ------------------------------------------------------
      if (nquad.eq.1 .or. nquad.eq.3) alon = -alon
      if (nquad.eq.5 .or. nquad.eq.3) alat = -alat
c
c     go to column 31 to read the surface group
c     -----------------------------------------
      itag=31
c
c
c     Go on to next mandatory level
c     --------------------------------------------
200   do 205 l = 1,12
         plev(l)=.false.
205      continue
c
c     count the number of the mandatory level
c     ---------------------------------------
      lvl=lvl+1
c
c     check to see if 925 level is missing
c     ------------------------------------
      if (lvl.eq.3 .and. line(itag:itag+1).eq.'85') lvl=lvl+1
c
c     return point for trop and max wind levels
c     -----------------------------------------
210   press = -99.
      temp = -99.
      rh = -99.
      geopot = -99.
      wdir = -99.
      wspd = -99.
      skpwind = .false.
c
      if(line(itag:itag+1).eq.header(lvl))then
        plev(lvl)=.true.
        press=prs(lvl)
        call geo (line,itag,plev,geopot,sfcp)
        itag=itag+6
        call tagtst(itag,line)
        pressx = press
        if (press.eq.1070. .and. sfcp.le.1070.) pressx = sfcp
        call temdew (line,itag,pressx,temp,rh)
        if(lvl.le.maxlvl)then
          itag=itag+6
          call tagtst(itag,line)

c         check if sfc wind group is missing
c         ----------------------------------
          if (lvl.eq.1) then
              if(line(itag:itag+1) .eq. '00' .and.
     *                  line(itag+6:itag+7).ne.'00') then
                skpwind = .true.
              else
                call wind (line,itag,wdir,wspd,*99)
                call dstouv (wdir,wspd,alat,alon,knots)
                skpwind = .false.
             endif
          else
              if (line(itag:itag+1) .eq. '00' .and.
     *           line(itag+6:itag+7).ne.'00') then
                skpwind = .true.
              else
                call wind (line,itag,wdir,wspd,*99)
                call dstouv (wdir,wspd,alat,alon,knots)
                skpwind = .false.
              endif
          endif
        endif
c        
        if (temp .ne. -99. .or. rh .ne. -99. .or. geopot .ne. -99.
     1        .or. wdir .ne. -99. .or. wspd .ne. -99.) call out
     2        (lu,iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3         wspd,1)
        if (.not. skpwind) then
           itag=itag+6
           call tagtst(itag,line)
        endif
        goto 200
c
c
c     decode tropopause
c     -----------------
      elseif (line(itag:itag+1) .eq. '88') then
        if(line(itag+2:itag+4).eq.'999')then
          itag=itag+6
          call tagtst(itag,line)
          goto 210
        endif
        geopot = -99.
        read (line(itag+2:itag+4),'(f3.0)',err=1000) press
        itag=itag+6
        call tagtst(itag,line)
        pressx = press
        call temdew (line,itag,pressx,temp,rh)
        itag=itag+6
        call tagtst(itag,line)
        call wind (line,itag,wdir,wspd,*99)
        call dstouv (wdir,wspd,alat,alon,knots)
        if (temp .ne. -99. .or. rh .ne. -99. .or. 
     1     wdir .ne. -99. .or. wspd .ne. -99.) call out (lu,
     2     iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3     wspd,7)
        itag = itag+6
        call tagtst(itag,line)
        goto 210
c
c     decode max wind level
c     ---------------------
      elseif (line(itag:itag+1) .eq. '77' .or.
     1  line(itag:itag+1) .eq. '66') then
        if(line(itag+2:itag+4).ne.'999')then
          read (line(itag+2:itag+4),'(f3.0)',err=1000) press
          itag=itag+6
          call tagtst(itag,line)
          call wind (line,itag,wdir,wspd,*99)
          call dstouv (wdir,wspd,alat,alon,knots)
          if (temp .ne. -99. .or. rh .ne. -99. .or. geopot .ne. -99.
     1          .or. wdir .ne. -99. .or. wspd .ne. -99.) call out (lu,
     2          iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3          wspd,6)
        endif
c
      endif
c
c
c     end of part A decoding.  Now look for significant level data.
c     -------------------------------------------------------------

 60   read(12,'(a)',end=99)line
      
c
c     check if the line has data or duplicates part B
c     decode splash location.
c     -----------------------------------------------
      if(line(1:30).eq.blank) goto 60
      if(line(1:5).eq.'31313') goto 60
      if(line(1:5).eq.'51515') goto 60
      if(line(1:5).eq.'61616') goto 60
      if(line(1:5).eq.'62626') then
         remark = ' '
         itag = 1
         ix = 0
62       ix = ix+1
         if (line(itag:itag).eq.'=') goto 63
         remark(ix:ix) = line(itag:itag)
         itag = itag+1
         if (itag.eq.66) then
            read(12,'(a)',end=99) line
            itag=1
            if (line(1:4).eq.'XXBB') goto 63
            endif
         goto 62
c
63       do 65 i=1,ix
            if (remark(i:i+3).eq.'SPL ') then
               read(remark(i+4:i+14),'(2i2,a1,i3,i2,a1)')
     *         ilat1,ilat2,clat,ilon1,ilon2,clon
               splat = float(ilat1)+float(ilat2)/100.
               if (clat.eq.'S') splat = -splat
               splon = float(ilon1)+float(ilon2)/100.
               if (clon.eq.'E') splon = -splon
               endif
65          continue
c
         do 66 i=1,ix
            if (remark(i:i+7).eq.'DLM WND ') then
               itagr = 9
               call wind (remark(i:i+20),itagr,wdir,wspd,*99)
               call dstouv (wdir,wspd,alat,alon,knots)
               read(remark(i+14:i+19),'(2i3)',err=1000) ip1,ip2
               if (ip1.lt.ip2) ip1 = ip1+1000
               geopot = float(ip1+ip2)/2.0
               press = 1099.
               temp = -99.
               rh = -99.
               if (wdir .ne. -99. .or. wspd .ne. -99.) call out (lu,
     2          iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3          wspd,8)

               endif
66          continue
c
         if (line(1:4).ne.'XXBB') goto 60
         endif
c
c     check significant level data
c     ----------------------------
 75   if(line(1:4).eq.'XXBB')then
        itag=31
c
c     added check for case of no sigt/h data -- jlf 1/98
c     --------------------------------------------------
        call tagtst(itag,line)
        if(line(itag:itag+4).eq.'21212' .or.
     1     line(itag:itag+4).eq.'31313') goto 75
c
        ihead=-11
 70     ihead=ihead+11
        if(ihead.gt.99)ihead=11
        read(line(itag:itag+1),'(i2)',err=75)jhead
        if(jhead.eq.ihead)then
          if(line(itag+2:itag+4).eq.'///') then
             itag=itag+6
             call tagtst(itag,line)
             itag=itag+6          
             goto 71
             endif
          read(line(itag+2:itag+4),'(i3)',err=1000)iprs
          if(iprs.lt.100)iprs=iprs+1000.
          press=iprs
          itag=itag+6
          call tagtst(itag,line)
          call temdew (line,itag,press,temp,rh)
          geopot = -99.
          wdir = -99.
          wspd = -99.
          if (temp .ne. -99. .or. rh .ne. -99. .or. geopot .ne. -99.
     1          .or. wdir .ne. -99. .or. wspd .ne. -99.) call out (lu,
     2          iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3          wspd,2)
          itag=itag+6
 71       call tagtst(itag,line)
c
          if(line(itag:itag+4).eq.'21212' .or.
     1       line(itag:itag+4).eq.'31313')goto 75
          goto 70
        endif
c
c     decode signficant wind levels--added surface decode--SEF 12/17/99
c     -----------------------------------------------------------------
      elseif(line(itag:itag+4).eq.'21212')then
        itag=itag+6
        ihead=-11
 30     ihead=ihead+11
        if(ihead.gt.99)ihead=11
        read(line(itag:itag+1),'(i2)',err=75)jhead
        if(jhead.eq.ihead)then
          if(line(itag+2:itag+4).eq.'///') then
             itag=itag+6
             call tagtst(itag,line)
             itag=itag+6
             goto 31
          endif
          read(line(itag+2:itag+4),'(i3)',err=1000)iprs
          if(iprs.lt.100)iprs=iprs+1000.
          press=iprs
          itag=itag+6
          call tagtst(itag,line)
          call wind (line,itag,wdir,wspd,*99)
          call dstouv (wdir,wspd,alat,alon,knots)
          temp=-99.
          rh=-99.
          geopot=-99.
          if (temp .ne. -99. .or. rh .ne. -99. .or. geopot .ne. -99.
     1          .or. wdir .ne. -99. .or. wspd .ne. -99.) call out (lu,
     2          iwx,yymmdd,igmt,alat,alon,press,temp,rh,geopot,wdir,
     3          wspd,2)
          itag=itag+6
          call tagtst(itag,line)
 31       goto 30
        endif
        goto 75
c
      elseif(line(itag:itag+4).eq.'31313')then
        read (line(itag+13:itag+16),'(i4)',err=1000) ihhmm
        itag = itag+19
        call tagtst(itag,line)
        goto 75
c
c     decode extrapolated levels in additional data groups
c     ----------------------------------------------------
      elseif(line(itag:itag+4).eq.'51515')then
        itag = itag+6
        call tagtst(itag,line)
500     if (line(itag:itag+4).eq.'10190') then
          itag = itag+6
          call tagtst(itag,line)
          do 505 l = 1,12
            plev(l)=.false.
505         continue
          press = -99.
          temp = -99.
          rh = -99.
          geopot = -99.
          wdir = -99.
          wspd = -99.
c
          do 510 l = 1,12
            if(line(itag:itag+1).eq.header(l))then
               plev(l)=.true.
               press=prs(l)
               call geo (line,itag,plev,geopot,sfcp)
               if (geopot .ne. -99.) call out(lu,iwx,yymmdd,igmt,
     *         alat,alon,press,temp,rh,geopot,wdir,wspd,3)
               endif
510         continue
          itag = itag+6
          call tagtst(itag,line)
          goto 500
c
c       added loop to re-check for extrapolated levels if doubtful
c       temperature or height groups first appear--SEF 12/17/99
c       ----------------------------------------------------------
	elseif(line(itag:itag+3) .eq. '1016') then
	  itag = itag + 12
	  call tagtst (itag,line)
	  goto 500
        endif
c
      elseif(line(1:4).eq.'NNNN')then
        call dropout(lu,ihhmm,splat,splon)
        return
c
      elseif(line(1:5).eq.'Sonde')then
        call dropout(lu,ihhmm,splat,splon)
        return

      elseif(line(1:4) .eq. 'XXCC') then
        call dropout(lu,ihhmm,splat,splon)
        return

      elseif(line(1:4) .eq. 'XXDD') then
        call dropout(lu,ihhmm,splat,splon)
        return
      endif
c

 99   call dropout(lu,ihhmm,splat,splon)
      
1000  return
      end
c
c
c
      subroutine uvcomp (dir,spd)
c 
c     this subroutine changes dir to u, and spd to v, where dir is
c     given in meteorological degrees.  The original values of dir
c     and spd are destroyed.
c
      degrad = atan(1.0) / 45.
      dirdg = 270.0 - dir
      if (dirdg .lt. 0.0) dirdg = dirdg + 360.
      dirrd = dirdg * degrad
      dir = spd * cos(dirrd)
      spd = spd * sin(dirrd)
      return
      end
c
c
c
      subroutine uvcomp2(dir,spd,u,v)
      degrad=atan(1.)/45.
      dirdg=270.-dir
      if(dirdg.lt.0.)then
        dirdg=dirdg+360.
      endif
      dirrd=dirdg*degrad
      u=spd*cos(dirrd)
      v=spd*sin(dirrd)
      return
      end
c
c
c
      subroutine temdew (line,lptr,press,temp,rh)
      character*70 line
c
c     extract the temperature
c
      temp = -99.
      rh = -99.
c
      if (line(lptr:lptr+2) .ne. '///') then
        read (line(lptr:lptr+2),'(f3.1)') atemp
        read (line(lptr+2:lptr+2),'(i1)') ifrac
        if (mod(ifrac,2) .eq. 0) then
          temp = atemp
        else
          temp = -atemp
        endif
      endif
c
c     extract the dewpoint depression
c
      if (line(lptr+3:lptr+4) .ne. '//') then
        read (line(lptr+3:lptr+4),'(i2)') idd
        if (idd .gt. 50) then
          dd = float (idd - 50)
        else
          dd = float (idd) / 10.
        endif
        dewpt = temp - dd
        call relhum (press,temp,dewpt,rh)
      endif
      return
      end
c
c
c
      subroutine relhum (press,temp,dewpt,rh)
      parameter (tkelvn = 273.16)
      parameter (em = 9.4051)
      parameter (e = 2353.)
c
c     compute the relative humidity using the vapor pressure vprs
c     and the saturation vapor pressure svprs
c
      vprs = 10**(em - e / (dewpt + tkelvn))
      svprs = 10**(em - e / (temp + tkelvn))
      fmixr = vprs / (press - vprs)
      smixr = svprs / (press - svprs)
      rh = 100. * fmixr / smixr
      if(rh.gt.100.)rh=100.
      return
      end
c
c
c
      subroutine geo (line,lptr,plev,geopot,sfcp)
      character*70 line
      logical plev
      dimension plev(12)
c
c     extract the geopential height (modifications by JLF 11/92)
c
      if (line(lptr+2:lptr+4) .ne. '///') then
        read (line(lptr+2:lptr+4),'(f3.0)') geopot 
c
        if (plev(1)) then                          ! Surface
          if (geopot .lt. 100.) geopot = geopot + 1000.
          sfcp = geopot
          endif
c
        if (plev(2)) then                          ! 1000 mb
          if (geopot .ge. 500.) geopot = -(geopot-500.)
          endif
c
        if (plev(3)) then
          if (sfcp.le.925..and.geopot.ge.500.) geopot=-(geopot-500.)
          endif
c
        if (plev(4)) then
          geopot = geopot+1000.
          if (sfcp.le.950..and.geopot.gt.1500.) geopot=geopot-1000.
          endif
c
        if (plev(5)) then                          ! 700 mb
          add = 2000.
          if (geopot .lt. 500.) add = 3000.
          if (sfcp.lt.960.) add = 2000.    
          geopot = geopot + add
          endif
c
        if (plev(6) .or. plev(7)) then             ! 500, 400 mb
          geopot = geopot * 10.
          endif
c
        if (plev(8) .or. plev(9) .or. plev(10)     ! >= 300 mb
     *      .or. plev(11) .or. plev(12)) then
          geopot = geopot * 10.
          if (geopot.lt.8500.) geopot = geopot + 10000.
          endif
c
      endif
      return
      end
c
c
c
      subroutine wind (line,lptr,wdir,wspd,*)
      character*70 line
c
c     extract the wind direction and speed
c
      if (line(lptr:lptr+4) .ne. '/////') then
        read (line(lptr:lptr+1),'(f2.0)') wdir
        read (line(lptr+2:lptr+4),'(f3.0)') wspd
      else
        wdir = -99.
        wspd = -99.
      endif
      return
      end
c
c
c
      subroutine dstouv (wdir,wspd,alat,alon,knots)
      logical knots
      real alat,alon,wdir,wspd
c
c     convert wind direction and speed to u, v (in m/s)
c
      if (wdir .ne. -99.) then
        wdir = wdir * 10.
        if(wspd.ge.500.0)then
          wspd=wspd-500.
          wdir=wdir+5
        endif
        if (knots) wspd = 0.514444 * wspd
        call uvcomp (wdir,wspd)
      endif
      return
      end
c
c
c
      subroutine tagtst(itag,line)
      character*70 line
c
c     check if the end of the line has been reached and the next line should 
c     be read
c  
c      if(itag.gt.47)then
        if(itag.lt.66)then
          do i=itag,itag+5
            if(line(i:i).ne.' ')return
          end do
        endif
        read(12,'(70a)',end=99)line
        itag=1
c     endif
 99   return
      end
c
c
c
      subroutine recco(lu,iyrs,imns,idys,line)
      character*1 quad
      character*30 blank
      character*70 line
      logical knots
      data blank /'                             '/
c
c
c     Read the day
c     ------------
      read(line(13:14),'(i2)') iday
      if(line(13:13).eq.' ') read (line(14:15),'(i2)') iday
      if (iday.gt.50) then
         iday=iday-50
         knots = .true.
         else
         knots = .false.
         endif
c
c     check for month, year flips
c     ---------------------------
      yy = iyrs
      mm = imns
      if (idys.gt.27.and.iday.eq.1) then
         mm = imns+1
         if (mm.eq.13) then
            mm = 1
            yy = iyrs + 1.
            if (yy.eq.100.) yy = 00.
            endif
         endif
c
      yymmdd = yy * 10000. + float(mm) * 100. + float(iday)
c
c
c     read the next line
c
 20   read(12,'(a)',end=99)line
c
c     check if the line has information
c
      if(line(1:30).eq.blank)goto 20
c
c     define the data type
c
      if(index(line,'AF').ne.0)iwx=6
      if(index(line,'NOAA').ne.0)iwx=3
c
c     read the data line
c
 10   read(12,'(a)',end=99)line
c
c     if line is NNNN return
c
      if(index(line,'NNNN').ne.0)return
c
c     check if the line has data
c
      if(line(1:30).eq.blank)goto 10
c
c     recco's begin with 97779 or 95559
c
      if (line(1:5) .eq. '97779'.or. line(1:5).eq.'95559') then
        read (line(7:8),'(i2)') ihour
        read (line(9:10),'(i2)') min
        quad = line(14:14)
        read (line(15:17),'(f3.1)') alat
        read (line(19:21),'(f3.1)') alon
        if (quad .eq. '1' .and. line(19:19) .ne. '9')alon = alon + 100.
        read (line(31:32),'(f2.0)') wdir
        read (line(33:35),'(f3.0)') wspd
        if(wspd.ge.500.0)then
          wspd=wspd-500.
          wdir=wdir+0.5
        endif
        call rtmdew (line,temp,dewpt,*99)
        call rpress (line,press,geopot)
        call relhum (press,temp,dewpt,rh)
        call rdstuv (wdir,wspd,alat,alon)
        igmt = float(ihour) * 100. + min
        call out (lu,iwx,yymmdd,igmt,alat,alon,press,
     1            temp,rh,geopot,wdir,wspd,4)
        go to 10
      endif
 99   return
      end
c
c
c
      subroutine rtmdew (line,temp,dwpt,*)
      character*70 line,line2
c
c     extract the temperature from the RECCO
c
      read (line(37:38),'(f2.0)',err=99) atemp
      if (atemp .lt. 50.) then
        temp = atemp
      else
        atemp = atemp - 50.
        temp = -atemp
        endif
c
c     if the dewpoint is missing, it may be in plain text on line 2
c
      if (line(39:40) .eq. '//') then
        read (12,'(a)',end=99) line2
        if (line2(1:3) .eq. 'DEW') then
          read (line2(11:15),'(f5.1)') dewpt
        else
          dewpt = 0.0
          endif
        dwpt = dewpt
        go to 20
        endif
c
c     otherwise, get the dewpoint from the main line
      read (line(39:40),'(f2.0)',err=99) dewpt
      if (dewpt .lt. 50.) then
        dwpt = dewpt
      else
        dewpt = dewpt - 50.
        dwpt = -dewpt
        endif
20    continue
      return
99    return 1
      end
c
c
c
      subroutine rpress (line,press,geopot)
      character*70 line
      integer prsind
      dimension sprs(7)
      data sprs /200.,850.,700.,500.,400.,300.,250./
c
c     extract the pressure and geopotential from the RECCO message
c
      read (line(44:44),'(i1)') prsind
      if (prsind .eq. 0) then
        read (line(45:47),'(f3.0)') geopot
        if (geopot .lt. 800.) geopot = geopot + 1000.
        press = 1070.
      elseif (prsind .eq. 9) then
        geopot = -99.
        read (line(25:27),'(f3.0)') tralt
        pralt = tralt * 10.
        press = 1013.25 * (1. - (pralt / 44331.)) ** (1. / 0.190263)
      elseif (prsind .ge. 1 .and. prsind .le. 7) then
        press = sprs(prsind)
        read (line(45:47),'(f3.0)') geopot
        if (prsind .gt. 3 .and. prsind .lt. 7) then
          geopot = geopot * 10.
        elseif (prsind .eq. 2) then
          if (geopot .lt. 800.) geopot = geopot + 1000.
        elseif (prsind .eq. 1 .or. prsind .eq. 7) then
          geopot = geopot * 10.
          if (geopot .lt. 800.) geopot = geopot + 1000.
        elseif (prsind.eq.3)then
          geopot=geopot+3000.
        endif
      else if (prsind .eq. 8) then
        read (line(25:27),'(f3.0)') tralt   ! true alt in decameters
        read (line(45:47),'(f3.0)') dvalue  ! d-value in decameters
        if (dvalue .gt. 500.) dvalue = -(dvalue - 500.)
        pralt = tralt * 10. - dvalue * 10.
        press = 1013.25 * (1. - (pralt / 44331.))
     1    ** (1. / 0.190263)
        geopot = pralt
        if (geopot .lt. 0.) geopot = geopot + 500.
      else
        press = 0.
        geopot = 0.
        endif
      return
      end
c
c
c
      subroutine rdstuv (wdir,wspd,alat,alon)
      real alat,alon,wdir,wspd
c
c     convert wind direction and speed to u, v for RECCOs
c
      wdir = wdir * 10.
      wspd = 0.514444 * wspd
      call uvcomp (wdir,wspd)
      return
      end
c
c
c
      subroutine vortex(lu,iyrs,imns,idys,line)
      character*4 itime1,itime2
      character*30 blank
      character*70 line
      logical knots
      dimension a(10,8)
      data blank /'                             '/
c
c
      i=0
      iwx=7
c
c
c     Read the day
c     ------------
      read(line(13:14),'(i2)') iday
      if(line(13:13).eq.' ') read (line(14:15),'(i2)') iday
      if (iday.gt.50) then
         iday=iday-50
         knots = .true.
         else
         knots = .false.
         endif
c
c     check for month, year flips
c     ---------------------------
      yy = iyrs
      mm = imns
      if (idys.gt.27.and.iday.eq.1) then
         mm = imns+1
         if (mm.eq.13) then
            mm = 1
            yy = iyrs + 1.
            if (yy.eq.100.) yy = 00.
            endif
         endif
c
      yymmdd = yy * 10000. + float(mm) * 100. + float(iday)
c
c
c
c     read the line with the mission number
c
 10   read(12,'(a)',end=99)line
c
c     check if the line has information
c
      if(line(1:30).eq.blank)goto 10
c
c     read the line 'SUPPLEMENTARY VORTEX DATA MESSAGE'
c
 20   read(12,'(a)',end=99)line
c
c     check if the line has the information
c
      if(line(1:30).eq.blank)goto 20
c
c     read the data line
c
3330  read(12,'(a)',end=99)line
c
c     check if line is data, remarks, or has no information at all
c
      if(index(line,'MF').ne.0.or.index(line,'REM').ne.0.or.
     1   line(1:30).eq.blank)goto 3330
c
c     if the line with the observation times has been read, write data
c
      if(index(line,'OB').ne.0)goto 90
c
c     count the number of the data point
c
      i=i+1
c
c     check for end of message
c
      if(index(line,'NNNN').ne.0)return
c
c     read the latitude
c
      read(line(3:5),'(i3)')ilat
c
c     read the longitude
c
      read(line(8:11),'(i4)')ilon
c
c     save the value of the latitude
c
      alat=ilat/10.
c
c     save the value of the longitude
c
      alon=ilon/10.
c
c     read the pressure level
c
      read(line(14:14),'(i1)',err=190)ihgt
c
c     save the value of the pressure
c
      if(ihgt.eq.5)press=400.
      if(ihgt.eq.4)press=500.
      if(ihgt.eq.3)press=700.
      if(ihgt.eq.2)press=850.
      if(ihgt.eq.1)press=1000.
      if(ihgt.eq.0)press=1070.
c
c     read the value of the geopotential
c
 190  read(line(15:17),'(i3)',err=191)ihgt
c
c     save the value of the geopotential
c
      geopot=ihgt
c
c     adjust the value of the geopotential
c
      if(press.eq.1070..and.geopot.lt.100)geopot=geopot+1000.
      if(press.eq.850.0)geopot=geopot+1000.
      if(press.eq.700.0)geopot=geopot+3000.
      if(press.eq.500.0)geopot=geopot+5000.
      if(press.eq.400.0)geopot=geopot+7000.
c
c     read the value of the temperature
c
 191  read(line(20:21),'(f2.0)',err=192)temp
c
c     correct the value of the temperature
c
      if(temp.ge.50.0)temp=50.0-temp
c
c     read the value of the dewpoint
c
 192  read(line(22:23),'(f2.0)',err=193)dewpt
c
c     correct the value of the dewpoint
c
      if(dewpt.ge.50.0)dewpt=50.0-dewpt
c
c     read the value of the wind direction
c
 193  read(line(25:26),'(i2)',err=194)iwdir
c
c     save the value of the wind direction
c
      wdir=iwdir
c
c     read the value of the wind speed
c
      read(line(27:29),'(i3)',err=194)iwspd
c
c     save the value of the wind speed
c
      wspd=iwspd
c
c     calculate the relative humidity
c
      call relhum (press,temp,dewpt,rh)
c
c     calculate the u and v components of the wind
c
      call rdstuv (wdir,wspd,alat,alon)
c
c     save values until time has been calculated
c
      a(i,1)=alat
      a(i,2)=alon
      a(i,3)=press
      a(i,4)=temp
      a(i,5)=rh
      a(i,6)=geopot
      a(i,7)=wdir
      a(i,8)=wspd
c
c     reinitialize values of the variables
c
 194  press=-99.
      temp=-99.
      rh=-99.
      geopot=-99.
      wdir=-99.
      wspd=-99.
c
c     continue loop
c
      goto 3330
c
c     read time of the first observation
c
 90   if(index(line,'SFC').ne.0)goto 3330
      idx1=index(line,'AT')
      if(idxchk.ne.2)then
        read(line(idx1+3:idx1+6),'(a)')itime1
        read(itime1(1:2),'(i2)')ihour1
        read(itime1(3:4),'(i2)')imin1
        jtime1=ihour1*60+imin1
      else
        read(line(idx1+3:idx1+6),'(a)')itime2
        read(itime2(1:2),'(i2)')ihour2
        read(itime2(3:4),'(i2)')imin2
        jtime2=ihour2*60+imin2
      endif
c
c     read time of the second observation
c
      if(idxchk.ne.2)then
        idx2=index(line(idx1+1:70),'AT')+idx1
        if(idx2.eq.0)then
          read(12,'(a)',end=99)line
          idxchk=2
          goto 90
        endif
        read(line(idx2+3:idx2+6),'(a)')itime2
        read(itime2(1:2),'(i2)')ihour2
        read(itime2(3:4),'(i2)')imin2
        jtime2=ihour2*60+imin2
      endif
      idxchk=1
c
c     calculate the times and write out the data
c
      do j=1,i
        itime=j*(jtime2-jtime1)/i+jtime1
        itime=itime/60*100+mod(itime,60)
        alat=a(j,1)
        alon=a(j,2)
        press=a(j,3)
        temp=a(j,4)
        rh=a(j,5)
        geopot=a(j,6)
        wdir=a(j,7)
        wspd=a(j,8)
        call out (lu,iwx,yymmdd,itime,alat,alon,press,temp,rh,geopot,
     1            wdir,wspd,5)
      end do
      i=0
      goto 3330
99    continue
      stop
      end
c
c
c
      subroutine out (lu,iwx,yymmdd,igmt,alat,alon,press,
     1                temp,rh,geopot,wdir,wspd,msgtype)
      character*4 tail
      character*80 dropl(200)
      real alat,alon,wdir,wspd
c
      common /output/nrecs
      common /dropdata/idropl,dropl

      tail='0000'
      if (msgtype.eq.1) tail = 'MANL'     ! DROP/Mandatory
      if (msgtype.eq.2) tail = 'SIGL'     ! DROP/Significant
      if (msgtype.eq.3) tail = 'ADDL'     ! DROP/Additional (51515)
      if (msgtype.eq.4) tail = 'RECO'     ! RECCO
      if (msgtype.eq.5) tail = 'SUPV'     ! SUPPL VTX
      if (msgtype.eq.6) tail = 'MWND'     ! DROP/Max wind
      if (msgtype.eq.7) tail = 'TROP'     ! DROP/Tropopause
      if (msgtype.eq.8) tail = 'DLMW'     ! DROP/DLM wind
      nrecs = nrecs+1
c
c     Write it to the output file.
c     If DROP, save line until we get exact time later
c     ------------------------------------------------

      if (msgtype.le.3 .or. msgtype.eq.6 .or. msgtype.eq.7 .or.
     1   msgtype.eq.8) then
         idropl = idropl+1
         write(dropl(idropl),510) iwx,yymmdd,igmt,alat,alon,press,
     1               temp,rh,geopot,wdir,wspd,tail
         else
         write (lu,510) iwx,yymmdd,igmt,alat,alon,press,temp,rh,
     1           geopot,wdir,wspd,tail
         endif
c
      return
510   format (i2,1x,f7.0,1x,i4,1x,2(f7.3,1x),3(f6.1,1x),
     1  f7.1,2(f6.1,1x),a4)
      end
c
c
c
      subroutine dropout(lu,itime,splat,splon)
      character*80 dropl(200),dropx,dropsh
      dimension press(200)
      logical sort
c
      common /dropdata/idropl,dropl
c
      sort = .true.
      do 100 i = 1,idropl
c
         read(dropl(i)(33:38),*) press(i)
         if (splat.ne.-999.) write(dropl(i)(17:31),'(f7.3,1x,f7.3)')
     *                       splat,splon
c
         if (itime.ge.2400) goto 100
c
         read(dropl(i)(12:15),'(i4)') nhr
         if (nhr.eq.0 .and. itime.gt.2300) then
            read(dropl(i)(8:9),*) iday
            iday = iday-1
            if (iday.eq.0) then
               read(dropl(i)(6:7),*) mth
               iday = 31
               mth = mth-1
               if (mth.eq.2) iday = 28
               if (mth.eq.4 .or. mth.eq.6 .or. mth.eq.9 .or.
     *             mth.eq.11) iday = 30
               if (mth.eq.0) then
                  mth =12
                  read(dropl(i)(4:5),*) iyr
                  iyr = iyr-1
                  write(dropl(i)(4:5),'(i2.2)') iyr
                  endif
               write(dropl(i)(6:7),'(i2.2)') mth
               endif
            write(dropl(i)(8:9),'(i2.2)') iday
            endif
c
         write(dropl(i)(12:15),'(i4)') itime
100      continue
c
c     sort by pressure
c     ----------------
      if (.not.sort) goto 300
      do 200 i=1,idropl-1
         do 210 j=i+1,idropl
            if (press(i).lt.press(j)) then
               dropx = dropl(j)
               pressx = press(j)
               do 220 k=j,i+1,-1
                  dropl(k) = dropl(k-1)
                  press(k) = press(k-1)
220               continue
               dropl(i) = dropx
               press(i) = pressx
               endif
210         continue
200      continue   
c
      u1 = -99.
      u2 = -99.
      v1 = -99.
      v2 = -99.
      bad = -99.
      psh = 8520.
      dropsh = dropl(1)
300   do 310 i=1,idropl
         read(dropl(i)(33:38),*) pr
         if (pr.eq.200.) then
            read(dropl(i)(62:66),*) u1
            read(dropl(i)(69:73),*) v1
            endif
         if (pr.eq.850.) then
            read(dropl(i)(62:66),*) u2
            read(dropl(i)(69:73),*) v2
            endif
         write(lu,'(a)') dropl(i)
310      continue
c
      if (u1.ne.-99. .and. u2.ne.-99. 
     *   .and. v1.ne.-99. .and. v2.ne.-99.) then
         ushear = u1-u2
         vshear = v1-v2
         write(dropsh(33:38),'(f6.1)') psh
         write(dropsh(40:60),'(f6.1,1x,f6.1,1x,f7.1)') bad,bad,bad
         write(dropsh(61:73),'(f6.1,1x,f6.1)') ushear,vshear
         dropsh(75:78) = 'WSHR'
         write(lu,'(a)') dropsh
         endif       
c
      return
      end
