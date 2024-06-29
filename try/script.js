function toggleMenu(element) {
    var menuBar = document.getElementById('menuBar');
    var links = menuBar.getElementsByTagName('a');
    
    if (element.classList.contains('active')) return; // Don't remove active if already active
    var activeLink = menuBar.querySelector('a.active');
    if (activeLink) activeLink.classList.remove('active');
    element.classList.add('active');
  }
  