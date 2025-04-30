namespace :db do
  namespace :mongoid do
    desc "Create indexes for all models"
    task create_indexes: :environment do
      Rails.logger.info "Creating indexes for all models..."
      Mongoid::Tasks::Database.create_indexes
      Rails.logger.info "Indexes created successfully!"
    end
  end
end 