class ApplicationController < ActionController::Base
  # Only allow modern browsers supporting webp images, web push, badges, import maps, CSS nesting, and CSS :has.
  allow_browser versions: :modern

  # Enable CSRF protection
  protect_from_forgery with: :exception

  # Add CSRF token to all responses
  after_action :set_csrf_cookie

  private

  def set_csrf_cookie
    cookies['XSRF-TOKEN'] = form_authenticity_token if protect_against_forgery?
  end
end 