document.addEventListener('DOMContentLoaded', function() {
  const header = document.querySelector('header') || document.querySelector('.header');
  if (header) {
    const headerHeight = header.offsetHeight;
    document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
    
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
      navMenu.style.top = headerHeight + 'px';
    }
  }
  
  window.addEventListener('resize', function() {
    if (header) {
      const headerHeight = header.offsetHeight;
      document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
      
      const navMenu = document.querySelector('.nav-menu');
      if (navMenu) {
        navMenu.style.top = headerHeight + 'px';
      }
    }
  });
  
  const dropdownItems = document.querySelectorAll('.nav-item.dropdown');
  const isMobile = () => window.matchMedia('(max-width: 768px)').matches;
  
  function ensureVisible(element) {
    if (isMobile()) {
      const navMenu = document.querySelector('.nav-menu');
      if (!navMenu) return;
      
      const elementRect = element.getBoundingClientRect();
      const navMenuRect = navMenu.getBoundingClientRect();
      
      if (elementRect.bottom > navMenuRect.bottom) {
        const scrollOffset = elementRect.bottom - navMenuRect.bottom + 10;
        navMenu.scrollTo({
          top: navMenu.scrollTop + scrollOffset,
          behavior: 'smooth'
        });
      }
    }
  }
  
  function preventDefaultLink(e) {
    // Tik mobiliame režime blokuojame nuorodos veikimą
    if (isMobile()) {
      e.preventDefault();
      
      const item = e.currentTarget.closest('.nav-item.dropdown');
      if (!item) return;
      
      const dropdown = item.querySelector('.product-dropdown');
      if (!dropdown) return;
      
      if (!dropdown.classList.contains('animating')) {
        dropdown.classList.add('animating');
        
        // Toggle active state
        if (item.classList.contains('active')) {
          item.classList.remove('active');
          dropdown.classList.remove('show');
        } else {
          // Close other dropdowns first
          dropdownItems.forEach(otherItem => {
            if (otherItem !== item) {
              otherItem.classList.remove('active');
              const otherDropdown = otherItem.querySelector('.product-dropdown');
              if (otherDropdown) {
                otherDropdown.classList.remove('show');
              }
            }
          });
          
          // Open this dropdown
          item.classList.add('active');
          dropdown.classList.add('show');
          
          setTimeout(function() {
            ensureVisible(dropdown);
          }, 50);
        }
        
        setTimeout(() => dropdown.classList.remove('animating'), 500);
      }
    }
    // Desktop režime nekeičiame numatytojo nuorodos veikimo
  }
  
  dropdownItems.forEach(function(item) {
    const link = item.querySelector('.nav-item-link');
    const dropdown = item.querySelector('.product-dropdown');
    
    if (!link || !dropdown) return;
    
    // Pridedame click eventą tik mobiliam režimui
    link.addEventListener('click', preventDefaultLink);
    
    // Remove any existing dropdown-toggle buttons for clean implementation
    const toggleButton = item.querySelector('.dropdown-toggle');
    if (toggleButton) {
      toggleButton.remove();
    }
    
    if (!isMobile()) {
      // Keep hover functionality for desktop
      item.addEventListener('mouseenter', function() {
        dropdown.style.display = 'block';
        dropdown.classList.add('show');
      });
      
      item.addEventListener('mouseleave', function() {
        setTimeout(function() {
          if (!item.matches(':hover') && !dropdown.matches(':hover')) {
            dropdown.classList.remove('show');
            dropdown.style.display = '';
          }
        }, 150);
      });
      
      dropdown.addEventListener('mouseenter', function() {
        dropdown.style.display = 'block';
        dropdown.classList.add('show');
      });
      
      dropdown.addEventListener('mouseleave', function() {
        setTimeout(function() {
          if (!item.matches(':hover') && !dropdown.matches(':hover')) {
            dropdown.classList.remove('show');
            dropdown.style.display = '';
          }
        }, 150);
      });
    }
  });
  
  function handleMobileView() {
    const isMobileView = window.matchMedia('(max-width: 768px)').matches;
    const dropdowns = document.querySelectorAll('.product-dropdown');
    const dropdownParents = document.querySelectorAll('.nav-item.dropdown');
    const navMenu = document.querySelector('.nav-menu');
    
    dropdowns.forEach(dropdown => {
      dropdown.classList.remove('show');
    });
    
    dropdownParents.forEach(parent => {
      parent.classList.remove('active');
    });
    
    if (navMenu && isMobileView) {
      navMenu.scrollTop = 0;
    }
  }
  
  handleMobileView();
  window.addEventListener('resize', handleMobileView);
  
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', function(e) {
      e.preventDefault();
      menuToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
    
    menuToggle.addEventListener('touchstart', function(e) {
      e.preventDefault();
      menuToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
    
    document.addEventListener('click', function(e) {
      if (!navMenu.contains(e.target) && !menuToggle.contains(e.target) && navMenu.classList.contains('active')) {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  }
});