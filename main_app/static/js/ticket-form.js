const dateTimeInput = document.getElementById('id_date')

const fp = flatpickr(dateTimeInput, {
  minDate: 'today',
  enableTime: true,
  dateFormat: "Y-m-d h:iK",
})

dateTimeInput.addEventListener('click', () => {
  fp.open()
})