// Configure the import map in config/importmap.rb. Read more: https://github.com/rails/importmap-rails
import "@hotwired/turbo-rails"
import "controllers"

// Configure CSRF token for AJAX requests
document.addEventListener('turbo:load', () => {
  const token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
  if (token) {
    // Set up CSRF token for all forms
    document.querySelectorAll('form').forEach(form => {
      if (!form.querySelector('input[name="authenticity_token"]')) {
        const input = document.createElement('input')
        input.type = 'hidden'
        input.name = 'authenticity_token'
        input.value = token
        form.appendChild(input)
      }
    })

    // Set up CSRF token for all AJAX requests
    document.addEventListener('turbo:before-fetch-request', (event) => {
      const fetchOptions = event.detail.fetchOptions
      fetchOptions.headers['X-CSRF-Token'] = token
    })
  }
}) 