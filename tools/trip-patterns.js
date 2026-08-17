/* Trip Pattern Engine (DEEPSEEK STEP 8.11) — JS mirror of the app.
   Trips stored in localStorage, entered as date/distance/hours/fuel. */
(function () {
  var trips = [];
  try { trips = JSON.parse(localStorage.getItem('aftlog_trips') || '[]'); } catch (e) {}
  function seasonOf(m){ return (m>=3&&m<=5)?'spring':(m>=6&&m<=8)?'summer':(m>=9&&m<=11)?'fall':'winter'; }
  function compute(){
    if(!trips.length) return null;
    var totalD=0,totalH=0,totalF=0,short=0,med=0,long=0,count=0;
    var season={spring:0,summer:0,fall:0,winter:0};
    var speeds=[],lengths=[];
    trips.forEach(function(t){
      var d=+t.d||0,h=+t.h||0,f=+t.f||0;
      totalD+=d; totalH+=h; totalF+=f; count++;
      season[seasonOf(+t.d.slice(0,2)==0?new Date(t.d).getMonth()+1:+t.d.slice(0,2))]++;
      if(h>0) speeds.push(d/h);
      lengths.push(d);
      if(d<15)short++; else if(d<=50)med++; else long++;
    });
    var avgD = count? totalD/count:0, avgS = speeds.length? speeds.reduce(function(a,b){return a+b;},0)/speeds.length:0, avgF = totalH? totalF/totalH:0;
    var type = (short>=med&&short>=long)?'Short hop':(med>=short&&med>=long)?'Medium trip':'Long trip';
    var se={}; Object.keys(season).forEach(function(k){ se[k]= count? season[k]/count:0; });
    // trends
    var now=new Date(); function hoursIn(from,to){ var s=0; trips.forEach(function(t){ var dt=new Date(t.d); if(dt>=from&&dt<to) s+=+t.h||0; }); return s; }
    var last30=hoursIn(new Date(now-30*86400000),now); var prior90=hoursIn(new Date(now-120*86400000),new Date(now-30*86400000));
    var hoursTrend = ((last30/30)/((prior90/90)||1))>1.25?'up':(((last30/30)/((prior90/90)||1))<0.75?'down':'stable');
    var cut=new Date(now-45*86400000); var rh=0,rf=0; trips.forEach(function(t){ if(new Date(t.d)>cut){ rh+=+t.h||0; rf+=+t.f||0; } });
    var recentBurn = rh? rf/rh : avgF; var fuelTrend = recentBurn<avgF*0.97?'improving':recentBurn>avgF*1.03?'declining':'stable';
    // outliers
    var sorted=lengths.slice().sort(function(a,b){return a-b;}); var med=sorted.length%2? sorted[Math.floor(sorted.length/2)] : (sorted[sorted.length/2-1]+sorted[sorted.length/2])/2;
    var scored=trips.map(function(t){ return {dev:Math.abs((+t.d||0)-med), t:t}; }).sort(function(a,b){return b.dev-a.dev;}).slice(0,3);
    var outliers=[];
    scored.forEach(function(s){ if(s.dev>=2) outliers.push({date:s.t.d, distance:+s.t.d||0}); });
    return { totalTrips:count, totalDistance:totalD, totalHours:totalH, avgTripLength:avgD, avgSpeed:avgS, avgFuelBurn:avgF, seasonal:se, commonTripType:type, fuelTrend:fuelTrend, hoursTrend:hoursTrend, outliers:outliers };
  }
  function paint(){
    var p=compute();
    var box=document.getElementById('tp-results');
    if(!p || !p.totalTrips){ box.innerHTML='<p class="pg-muted">Add at least one trip to see patterns.</p>'; return; }
    var sev=[['Trips',p.totalTrips],['Distance',Math.round(p.totalDistance)+' km'],['Hours',p.totalHours.toFixed(1)],['Avg trip',Math.round(p.avgTripLength)+' km'],['Avg speed',p.avgSpeed.toFixed(0)+' km/h'],['Fuel',p.avgFuelBurn.toFixed(1)+' L/hr']].map(function(x){return '<div class="tp-stat"><div>'+x[1]+'</div><span>'+x[0]+'</span></div>';}).join('');
    var h = '<div class="tp-stats">'+sev+'</div>';
    h += '<div class="tp-bar" id="tp-bar"></div>';
    h += '<div class="tp-trends"><span>Fuel: <b>'+p.fuelTrend+'</b></span><span>Hours: <b>'+p.hoursTrend+'</b></span><span>Common: <b>'+p.commonTripType+'</b></span></div>';
    if(p.outliers.length){ h += '<div class="tp-out"><strong>Most unusual trips</strong>' + p.outliers.map(function(o){ return '<div>'+o.date+' — '+Math.round(o.distance)+' km</div>'; }).join('') + '</div>'; }
    box.innerHTML = h;
    drawBar(p.seasonal);
  }
  function drawBar(se){
    var el=document.getElementById('tp-bar'); if(!el) return;
    var max=Math.max(se.spring,se.summer,se.fall,se.winter,0.0001);
    var labels=[['spring','Spring'],['summer','Summer'],['fall','Fall'],['winter','Winter']];
    el.innerHTML = '<div class="tp-bar-row">' + labels.map(function(l){ var v=se[l[0]]/max*100; return '<div class="tp-bar-col"><div class="tp-bar-bg"><div class="tp-bar-fill" style="height:'+v+'%"></div></div><span>'+l[1]+'</span><b>'+Math.round(se[l[0]]*100)+'%</b></div>'; }).join('') + '</div>';
  }
  function save(){ try{ localStorage.setItem('aftlog_trips', JSON.stringify(trips)); }catch(e){} }
  window.tpAdd=function(){
    var d=document.getElementById('tp-d').value, km=document.getElementById('tp-km').value, h=document.getElementById('tp-h').value, f=document.getElementById('tp-f').value;
    if(!d||!km) return;
    trips.push({d:d, km:km, h:h||'', f:f||''}); save(); paint();
  };
  window.tpReset=function(){ trips=[]; save(); paint(); };
  window.tpExport=function(){ var p=compute(); if(!p) return; var t='TRIP PATTERN - AFTLOG\nTrips: '+p.totalTrips+' Distance: '+Math.round(p.totalDistance)+'km Hours: '+p.totalHours.toFixed(1)+'\nAvg '+Math.round(p.avgTripLength)+'km  Speed '+p.avgSpeed.toFixed(0)+'  Fuel '+p.avgFuelBurn.toFixed(1)+'\nCommon '+p.commonTripType+'  Fuel-trend '+p.fuelTrend+'  Hours-trend '+p.hoursTrend+'\n'; var blob=new Blob([t],{type:'text/plain'}); var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='aftlog-trip-patterns.txt'; a.click(); };
  document.addEventListener('DOMContentLoaded', function(){ paint(); });
})();
