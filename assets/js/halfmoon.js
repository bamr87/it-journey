    // https://raw.githubusercontent.com/halfmoonui/halfmoon/master/js/halfmoon.js
    let darkModeOn = false;
      
    const createStorage = (name, value) => {
      localStorage.setItem(name, value);
    }
      
    const readStorage = name => {
      return localStorage.getItem(name);
    }
      
    const deleteStorage = name => {
      localStorage.removeItem(name);
    }
     
    const toggleDarkMode = (e) => {
      if (document.body.classList.contains("dark-mode")) {
        document.body.classList.remove("dark-mode");
        darkModeOn = false;
        createStorage("my_preferredMode", "light-mode");
      } else {
        document.body.classList.add("dark-mode");
        darkModeOn = true;
        createStorage("my_preferredMode", "dark-mode");
      }
    }
      
    document.getElementById("darkMode").addEventListener("click", toggleDarkMode)
      
    document.addEventListener("DOMContentLoaded", () => {
      if (readStorage("my_preferredMode")) {
        if (readStorage("my_preferredMode") == "dark-mode") {
          darkModeOn = true;
        } else {
          darkModeOn = false;
        }
      } else {
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
          darkModeOn = true;
        } else {
          if (document.body.classList.contains("dark-mode")) {
            darkModeOn = true;
          } else {
            darkModeOn = false;
          }
        }
      }

      if (darkModeOn) {
        if (!document.body.classList.contains("dark-mode")) {
          document.body.classList.add("dark-mode");
        }
        document.getElementById("darkMode").checked = true
      } else {
        if (document.body.classList.contains("dark-mode")) {
          document.body.classList.remove("dark-mode");
        }
      }
    })
