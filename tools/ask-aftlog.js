/* Ask AftLog — grounded offline chat engine (DEEPSEEK STEP 8.9).
   Mirrors the app's AskGrounding: intent classify -> local answer. */
(function () {
  var convo = [];
  function $(id){ return document.getElementById(id); }
  function addMsg(role, text, chips){
    convo.push({ role: role, text: text });
    var box = $('ask-log');
    if(!box) return;
    var d = document.createElement('div');
    d.className = 'ask-msg ask-' + role;
    d.textContent = (role === 'user' ? 'You: ' : 'AftLog: ') + text;
    box.appendChild(d);
    if (chips && chips.length) {
      var c = document.createElement('div'); c.className = 'ask-chips';
      chips.forEach(function (s) {
        var b = document.createElement('button'); b.className='ask-chip'; b.textContent = s;
        b.onclick = function () { ask(s); };
        c.appendChild(b);
      });
      box.appendChild(c);
    }
    box.scrollTop = box.scrollHeight;
    try { localStorage.setItem('aftlog_ask_convo', JSON.stringify(convo)); } catch (e) {}
  }
  function ground(q){
    var l = q.toLowerCase();
    if (l.indexOf('overheat') >= 0 || l.indexOf('tell-tale') >= 0 || l.indexOf('temp') >= 0)
      return { text: 'Likely overheating: impeller first, then thermostat, blocked inlet. Stop if it beeps continuously — run the full check for causes.', chips: ['What are all the causes?', 'When is it serious?', 'Winterization steps'], grounded: true };
    if ((l.indexOf('won') >= 0 && l.indexOf('start') >= 0) || l.indexOf('no start') >= 0 || l.indexOf('crank') >= 0)
      return { text: 'No start: kill switch / lanyard on? Battery 12.6V+? Fuel bulb hard? Spark at the plugs? Start simple, work outward.', chips: ['Is it the battery?', 'Check the fuel', 'Why no spark?'], grounded: true };
    if (l.indexOf('battery') >= 0 || l.indexOf('dies') >= 0)
      return { text: 'Battery dying: 1) age (4-5 yr = replace), 2) parasitic draw, 3) charging system at speed.', chips: ['Is it the alternator?', 'How do I test a draw?', 'Battery size'], grounded: true };
    if (l.indexOf('winter') >= 0)
      return { text: 'Winterize before first hard frost: stabilize fuel, fog the engine, drain water systems, change lower-unit oil, remove the battery to a maintainer, then cover.', chips: ['Winterization checklist', 'Spring prep', 'Fuel storage'], grounded: true };
    if (l.indexOf('log fuel') >= 0 || l.indexOf('fuel fill') >= 0)
      return { text: 'To log a fuel fill: Log tab → Fuel → Add Fill → enter litres/gallons + price (add the odometer reading). AftLog learns your real range over time.', chips: ['How do I log a trip?', 'Fuel logging help'], grounded: true };
    if (l.indexOf('prop slip') >= 0)
      return { text: 'Prop slip compares actual speed to theoretical speed from RPM and pitch. 10-20% is normal; more usually means a spun hub, damaged prop, or wrong pitch.', chips: ['Open the calculators', 'Why is slip high?'], grounded: true };
    if (l.indexOf('interval') >= 0 || l.indexOf('planner') >= 0 || l.indexOf(' due') >= 0)
      return { text: 'Smart Planner turns intervals and usage into one schedule: oil every 100 hr, impeller every 200 hr or 2-3 seasons; complete a task and it reschedules the next.', chips: ['What is due?', 'Boat Health Score'], grounded: true };
    if (l.indexOf('launch') >= 0)
      return { text: 'Launch: drain plug in, straps off, winch unhooked, lights connected, bow rope ready, crew seated and lines clear.', chips: ['Ramp mode', 'Retrieve checklist'], grounded: true };
    return null;
  }
  window.ask = function (typed) {
    typed = (typed || '').trim(); if (!typed) return;
    var inp = $('ask-input'); if (inp) inp.value = '';
    addMsg('user', typed);
    var g = ground(typed);
    if (g) { addMsg('assistant', g.text); }
    else { addMsg('assistant', 'That needs the online AI assistant. This tool answers grounded questions offline — troubleshooting, checklists, winterization, calculators, and planner rules. Try one of those.'); }
  };
  window.askExport = function () {
    var t = 'Ask AftLog\n';
    convo.forEach(function (m) { t += (m.role === 'user' ? 'You: ' : 'AftLog: ') + m.text + '\n'; });
    var blob = new Blob([t], { type: 'text/plain' }); var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'aftlog-ask-aftlog.txt'; a.click();
  };
  window.askPhoto = function (inp) {
    if (inp.files && inp.files[0]) {
      var p = document.querySelector('.ask-photo'); if (p) p.style.display = 'block';
    }
  };
  document.addEventListener('DOMContentLoaded', function () {
    var s = []; try { s = JSON.parse(localStorage.getItem('aftlog_ask_convo') || '[]'); } catch (e) {}
    s.forEach(function (m) { addMsg(m.role, m.text); });
  });
})();
