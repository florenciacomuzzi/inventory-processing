class InventoryUnit
  include Mongoid::Document
  include Mongoid::Timestamps
  field :batch_id, type: String
  field :upc, type: String
  field :price, type: BigDecimal
  field :quantity, type: Integer
  field :department_id, type: String
  field :internal_id, type: String
  field :name, type: String
  field :properties, type: Object
  field :tags, type: Array
  
  embeds_one :batch_stats, class_name: 'BatchStats'
  
  index({ upc: 1 }, { unique: true, background: true })
  
  # Create index when model is loaded
  def self.create_indexes!
    collection.indexes.create_one({ upc: 1 }, unique: true, background: true)
  end
  
  # Call create_indexes! when model is loaded
  create_indexes!
end
