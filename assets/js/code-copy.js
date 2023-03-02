// Copy code to clipboard

document
    .querySelectorAll('pre.highlight')
    .forEach(function (pre) {
      var button = document.createElement('button');
      var copyText = 'Copy';
      button.className = 'copy';
      button.type = 'button';
      button.ariaLabel = 'Copy code to clipboard';
      button.innerText = copyText;
      button.addEventListener('click', function () {
        var code = pre.querySelector('code').innerText.trim();
        navigator.clipboard.writeText(code);
        button.innerText = 'Copied';
        setTimeout(function () {
          button.innerText = copyText;
        }, 4000);
      });
      pre.appendChild(button);
    });