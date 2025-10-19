document.addEventListener('DOMContentLoaded', function () {
    const folders = document.querySelectorAll('.folder');

    folders.forEach(folder => {
      folder.addEventListener('click', function () {
        const nextElement = this.nextElementSibling;
        if (nextElement.classList.contains('nested-list-group')) {
          nextElement.classList.toggle('show');
        }
      });
    });
  });