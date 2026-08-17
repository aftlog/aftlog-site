(function () {
  var input = document.getElementById('help-search');
  var btns = document.querySelectorAll('.pg-cat-btn');
  var cards = document.querySelectorAll('#help-grid .pg-blog-card');
  var curCat = 'all';
  function apply() {
    var q = (input.value || '').toLowerCase();
    cards.forEach(function (c) {
      var ok = true;
      if (curCat !== 'all' && c.dataset.cat !== curCat) ok = false;
      if (ok && q) {
        var text = (c.textContent || '').toLowerCase();
        if (text.indexOf(q) === -1) ok = false;
      }
      c.style.display = ok ? '' : 'none';
    });
  }
  if (input) input.addEventListener('input', apply);
  if (btns) btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      curCat = b.dataset.cat;
      apply();
    });
  });
})();
