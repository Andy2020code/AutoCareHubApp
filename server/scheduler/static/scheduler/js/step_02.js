document.addEventListener('DOMContentLoaded', function () {
    // Function to parse the URL query string and retrieve the value of the 'date' parameter
    function getParameterByName(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }

    // Get the value of the 'date' parameter from the URL
    var dateParam = getParameterByName('date');

    // Display the extracted date on the page
    var lastSavedDateElement = document.getElementById('last-saved-date');
    if (dateParam) {
        var dateObj = new Date(dateParam);
        var options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        var formattedDate = dateObj.toLocaleDateString('en-US', options);
        //lastSavedDateElement.textContent = 'Last saved date: ' + formattedDate;
        // Set the value of the text input to the formatted date
        document.getElementById('id_date').value = formattedDate;
    } else {
        lastSavedDateElement.textContent = 'No date available';
    }
});










//expand and collapse the content function
document.addEventListener('DOMContentLoaded', function () {
    const titles = document.querySelectorAll('.collapsible .title');
    titles.forEach(title => {
      title.addEventListener('click', function () {
        const content = this.nextElementSibling;
        const arrow = this.querySelector('.arrow');
        if (content.style.display === 'block') {
          content.style.display = 'none';
          arrow.style.transform = 'rotate(0deg)';
        } else {
          content.style.display = 'block';
          arrow.style.transform = 'rotate(90deg)';
        }
      });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const titles = document.querySelectorAll('.collapsible_02 .title_02');
    titles.forEach(title => {
      title.addEventListener('click', function () {
        const content = this.nextElementSibling;
        const arrow = this.querySelector('.arrow_02');
        if (content.style.display === 'block') {
          content.style.display = 'none';
          arrow.style.transform = 'rotate(0deg)';
        } else {
          content.style.display = 'block';
          arrow.style.transform = 'rotate(90deg)';
        }
      });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const titles = document.querySelectorAll('.collapsible_03 .title_03');
    titles.forEach(title => {
      title.addEventListener('click', function () {
        const content = this.nextElementSibling;
        const arrow = this.querySelector('.arrow_03');
        if (content.style.display === 'block') {
          content.style.display = 'none';
          arrow.style.transform = 'rotate(0deg)';
        } else {
          content.style.display = 'block';
          arrow.style.transform = 'rotate(90deg)';
        }
      });
    });
});
  