/* Predictive Planner (DEEPSEEK STEP 8.10) — JS engine mirroring the app.
   Inputs: engine hours + avg hours/month + last-service hours per item. */
(function () {
  var DEFAULTS = [
    { id:'oil', label:'Engine oil', ih:100, im:0, kw:'oil' },
    { id:'gear', label:'Gear lube / lower-unit oil', ih:100, im:0, kw:'gear' },
    { id:'impeller', label:'Water pump impeller', ih:200, im:0, kw:'impeller' },
    { id:'plugs', label:'Spark plugs', ih:200, im:0, kw:'plug' },
    { id:'battery', label:'Battery check', ih:0, im:12, kw:'battery' },
    { id:'trailer', label:'Trailer service', ih:0, im:12, kw:'trailer' },
    { id:'winterization', label:'Winterization', ih:0, im:12, kw:'winter' }
  ];
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem('aftlog_pred_snap')||'{}'); } catch(e){}
  function sev(hours, item){
    if(!item.lastLogged) return 'yellow';
    if(item.ih>0){ var hr = (item.lastServiceHours + item.ih) - hours; if(hr<=0) return 'red'; return hr <= item.ih*0.25 ? 'yellow' : 'green'; }
    var next = item.lastServiceDate ? new Date(item.lastServiceDate).getTime() + item.im*30.4*86400000 : 0;
    return next && Date.now()>next ? 'red' : 'yellow';
  }
  function reason(hours, avg, item){
    if(!item.lastLogged) return 'No service logged yet — schedule this before it becomes overdue.';
    if(item.ih>0){ var nextDue=item.lastServiceHours+item.ih; var hr=nextDue-hours;
      return hr<=0 ? ('Due now: last serviced at '+item.lastServiceHours+' h; interval '+item.ih+' h (due at '+nextDue+' h).')
                   : ('Last serviced at '+item.lastServiceHours+' h; '+item.ih+' h interval; about '+Math.round(hr)+' h remain (due near '+nextDue+' h).'); }
    var last=new Date(item.lastServiceDate); var next=new Date(last.getTime()+item.im*30.4*86400000);
    return Date.now()>next ? ('Due now: last done '+last.toISOString().slice(0,10)+', interval '+item.im+' months.')
      : ('Last done '+last.toISOString().slice(0,10)+'; '+item.im+' months; next ~'+next.toISOString().slice(0,10)+'.');
  }
  function paint(){
    var hours = +document.getElementById('pp-hours').value || 0;
    var avg = +document.getElementById('pp-avg').value || 20;
    var box = document.getElementById('pp-list'); box.innerHTML='';
    DEFAULTS.forEach(function(d){
      var st = saved[d.id]||{};
      var item = { lastServiceHours: st.lastServiceHours==null?null:+st.lastServiceHours, lastServiceDate: st.lastServiceDate||null, lastLogged: !!st.lastServiceHours||!!st.lastServiceDate, ih:d.ih, im:d.im };
      var se = sev(hours, item); var color = se==='red'?'#FF6B6B':se==='yellow'?'#F5B041':'#2ECC71'; var sevL = se.toUpperCase();
      var card=document.createElement('div'); card.className='pp-item';
      card.style.borderLeft='4px solid '+color;
      var hrLine=d.ih>0 ? (Math.round((item.lastServiceHours+(d.ih||0)-hours))+' h to go') : '';
      card.innerHTML = '<div class="pp-row"><div class="pp-left"><strong>'+d.label+'</strong><br><input class="pp-h fin" data-id="'+d.id+'" placeholder="last service hours" value="'+ (item.lastServiceHours==null?'':item.lastServiceHours)+'"><input class="pp-d fin" data-id="'+d.id+'" placeholder="last date (YYYY-MM-DD)" value="'+ (item.lastServiceDate||'') +'"></div><div class="pp-sev" style="color:'+color+'">'+sevL+'</div></div><div class="pp-reason">'+reason(hours,avg,item)+'</div>';
      box.appendChild(card);
    });
    // bind inputs
    box.querySelectorAll('.pp-h').forEach(function(inp){ inp.addEventListener('input', function(){ saved[inp.dataset.id]=saved[inp.dataset.id]||{}; saved[inp.dataset.id].lastServiceHours=inp.value; save(); paint(); }); });
    box.querySelectorAll('.pp-d').forEach(function(inp){ inp.addEventListener('input', function(){ saved[inp.dataset.id]=saved[inp.dataset.id]||{}; saved[inp.dataset.id].lastServiceDate=inp.value; save(); paint(); }); });
    // header
    document.getElementById('pp-head').textContent = 'Engine '+Math.round(hours)+' h  ·  avg '+Math.round(avg)+' h/month';
  }
  function save(){ try{ localStorage.setItem('aftlog_pred_snap', JSON.stringify(saved)); }catch(e){} }
  window.ppExport=function(){ window.print(); };
  window.ppDownload=function(){
    var hours=+document.getElementById('pp-hours').value||0; var avg=+document.getElementById('pp-avg').value||20;
    var t='PREDICTIVE PLANNER - AFTLOG\nEngine hours: '+Math.round(hours)+'  avg '+Math.round(avg)+' h/month\n\n';
    DEFAULTS.forEach(function(d){ var st=saved[d.id]||{}; var item={lastServiceHours:st.lastServiceHours==null?null:+st.lastServiceHours,lastServiceDate:st.lastServiceDate||null,lastLogged:!!st.lastServiceHours||!!st.lastServiceDate,ih:d.ih,im:d.im}; t+='- '+d.label+' ['+sev(hours,item).toUpperCase()+']\n  '+reason(hours,avg,item)+'\n'; });
    var b=new Blob([t],{type:'text/plain'}); var a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='aftlog-predictive-planner.txt'; a.click();
  };
  document.addEventListener('DOMContentLoaded', function(){ var h=document.getElementById('pp-hours'); var a=document.getElementById('pp-avg'); if(h) h.addEventListener('input', paint); if(a) a.addEventListener('input', paint); paint(); });
})();
