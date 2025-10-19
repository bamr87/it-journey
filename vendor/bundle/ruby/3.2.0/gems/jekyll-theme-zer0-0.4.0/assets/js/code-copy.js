document.addEventListener('DOMContentLoaded', function () {
  document
    .querySelectorAll('pre.highlight')
    .forEach(function (pre) {
      var button = document.createElement('button');
      var copyText = 'Copy';
      button.className = 'copy';
      button.type = 'button';
      button.ariaLabel = 'Copy code to clipboard';
      button.innerText = copyText;
      button.tabIndex = 1; // Add this line to make the button focusable with the keyboard
      button.addEventListener('click', function () {
        var code = pre.querySelector('code').innerText
          .split('\n')
          .filter(line => !line.trim().startsWith('#'))
          .join('\n')
          .trim();
        navigator.clipboard.writeText(code);
        button.innerText = 'Copied';
        setTimeout(function () {
          button.innerText = copyText;
        }, 4000);
      });
      pre.appendChild(button);
      pre.classList.add('has-copy-button'); // Add a class to the pre element
    });
});