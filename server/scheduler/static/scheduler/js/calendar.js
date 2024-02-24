document.addEventListener('DOMContentLoaded', function () {
  const monthYearText = document.getElementById('month-year');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const daysContainer = document.querySelector('.days');
  
  let currentDate = new Date();
  let currentMonth = currentDate.getMonth();
  let currentYear = currentDate.getFullYear();
  let selectedDate = null; // Variable to store the selected date
  
  function generateCalendar(month, year) {
    daysContainer.innerHTML = '';
    const daysInMonth = new Date(year, month + 1, 0).getDate();
  
    monthYearText.textContent = `${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}`;
  
    for (let i = 1; i <= daysInMonth; i++) {
      const dayElement = document.createElement('div');
      dayElement.classList.add('day');
      dayElement.textContent = i;
      dayElement.addEventListener('click', function () {
        highlightDate(dayElement);
      });
      daysContainer.appendChild(dayElement);
    }
  }
  
  generateCalendar(currentMonth, currentYear);
  
  prevBtn.addEventListener('click', function () {
    currentMonth--;
    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    }
    generateCalendar(currentMonth, currentYear);
  });
  
  nextBtn.addEventListener('click', function () {
    currentMonth++;
    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }
    generateCalendar(currentMonth, currentYear);
  });
  
  function highlightDate(dayElement) {
    const selectedDay = dayElement.textContent;
    const selectedMonth = currentMonth; // Keep zero-based indexing for consistency
    const selectedYear = currentYear;
    const dateString = `${selectedYear}-${selectedMonth < 9 ? '0' + (selectedMonth + 1) : selectedMonth + 1}-${selectedDay < 10 ? '0' + selectedDay : selectedDay}`;
    
    // Store the selected date in the variable
    selectedDate = dateString;
    
    // Redirect user to another page
    window.location.href = '/schedule/step-02/?date=' + encodeURIComponent(selectedDate);
  }
});
