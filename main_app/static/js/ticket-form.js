const dateTimeInput = document.getElementById('id_date')

const fp = flatpickr(dateTimeInput, {
  minDate: 'today',
  enableTime: true,
  time_24hr: true,
  dateFormat: 'Y-m-d H:i',
  defaultDate: new Date(new Date().setMonth(new Date().getMonth() + 1))
})

dateTimeInput.addEventListener('click', () => {
  fp.open()
})