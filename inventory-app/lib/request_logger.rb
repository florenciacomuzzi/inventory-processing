module InventoryApp
  class RequestLogger
    def initialize(app)
      @app = app
      Rails.logger.info "RequestLogger middleware initialized"
    end

    def call(env)
      Rails.logger.info "RequestLogger middleware called"
      request = Rack::Request.new(env)
      
      # Log request details
      Rails.logger.info "=== Request Details ==="
      Rails.logger.info "Method: #{request.request_method}"
      Rails.logger.info "Path: #{request.path}"
      Rails.logger.info "Query: #{request.query_string}" unless request.query_string.empty?
      Rails.logger.info "Headers: #{request.env.select { |k,v| k.start_with?('HTTP_') }}"
      
      # Log request body if present
      if request.body.size > 0
        request.body.rewind
        body = request.body.read
        request.body.rewind
        Rails.logger.info "Body: #{body}"
      else
        Rails.logger.info "No request body present"
      end
      
      Rails.logger.info "====================="

      # Call the next middleware
      @app.call(env)
    rescue => e
      Rails.logger.error "Error in RequestLogger: #{e.message}"
      Rails.logger.error e.backtrace.join("\n")
      raise e
    end
  end
end 